import heapq
import json
import os
import sys
import random

try:
    from .deck import load_deck, save_deck
except ImportError:
    # Allow running this module directly with `python src/flashcard/main.py`.
    src_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if src_root not in sys.path:
        sys.path.insert(0, src_root)
    from flashcard.deck import load_deck, save_deck


def update_priority(card_dict, heap, card_id, correct):
    """Adjust a card's priority and reinsert it into the review heap."""
    card = card_dict[card_id]
    card.setdefault("priority", 0)
    card.setdefault("streak", 0) 
    card.setdefault("wrong_streak", 0) #track consecutive wrong answers

    # Correct answers increase priority (delay) to show later.
    if correct:
        card["streak"] += 1
        card["wrong_streak"] = 0  # Reset the wrong streak on a correct answer.
        push = min(card["streak"], 3)
        card["priority"] += push
    else:
        # Wrong answers set priority based on consecutive mistakes: 3 cards later for first wrong, 2 for second, immediate for third+.
        card["streak"] = 0  
        card["wrong_streak"] += 1  # Increment the wrong streak on a wrong answer.
        if card["wrong_streak"] == 1:
            card["priority"] = 3
        elif card["wrong_streak"] == 2:
            card["priority"] = 2
        else:
            card["priority"] = 0

    heapq.heappush(heap, (card["priority"], card_id))


def run_session(card_dict, heap, filepath):
    """Run the interactive review loop continuously until the user quits."""
    print("Welcome to my flashcard app. Type 'quit' to exit.\n")

    completed = 0
    while True:
        if not heap:
            completed += 1
            if completed > 1:
                print(f"Whole deck completed {completed} times! Starting over...\n")
            else:
                print("Starting the deck...\n")
            card_dict, heap = load_deck(filepath)
            if not heap:
                print("No cards to review. Exiting...")
                return

        while heap:
            priority, card_id = heapq.heappop(heap)
            card = card_dict[card_id]

            # Skip cards that are still scheduled for later review.
            if card["priority"] > 0:
                card["priority"] -= 1
                heapq.heappush(heap, (card["priority"], card_id))
                continue

            print(f"Question: {card['question']}")
            user_input = input("\nPress Enter to see the answer (or type 'quit' to exit): ").strip().lower()

            if user_input == "quit":
                print("saving and exiting...")
                save_deck(filepath, card_dict)
                return

            print(f"\nAnswer: {card['answer']}")

            result = input("\nDid you get it right? (y/n): ").strip().lower()
            while result not in ("y", "n"):
                result = input("please enter y or n: ").strip().lower()

            got_right = (result == "y")
            if got_right:
                update_priority(card_dict, heap, card_id, True)
                print("good job!\n")
            else:
                update_priority(card_dict, heap, card_id, False)
                print("you'll get it next time!\n")

            print("-" * 40 + "\n")

        save_deck(filepath, card_dict)


def main():
    # Determine the deck file path relative to this script, not the current working directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = input("Enter the JSON file name: ").strip()
    filepath = os.path.abspath(os.path.join(script_dir, "..", "..", filename))
    try:
        card_dict, heap = load_deck(filepath)
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please make sure the file exists.")
        return
    except json.JSONDecodeError:
        print(f"Error: {filename} is not a valid JSON file. Please check the file format.")
        return

    run_session(card_dict, heap, filepath)


if __name__ == "__main__":
    main()
