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


def update_priority(card_dict, deck, card_id, correct):
    """Adjust a card's priority and reinsert it into the review heap."""
    card = card_dict[card_id]
    card.setdefault("priority", 5)
    card.setdefault("streak", 0) 
    card.setdefault("wrong_streak", 0) #track consecutive wrong answers

    # Correct answers reduce priority, but never below 0.
    if correct:
        card["streak"] += 1
        card["wrong_streak"] = 0  # Reset the wrong streak on a correct answer.
        push = min(card["streak"], 3)
        card["priority"] += push
    else:
        # Wrong answers increase priority so the card is reviewed earlier.
        card["streak"] = 0  
        card["wrong_streak"] += 1  # Increment the wrong streak on a wrong answer.
        delay = max(0, 3 - card["wrong_streak"])  # Decrease delay with more consecutive wrong answers.

        if deck:
            soonest = deck[0][0] if deck else 0
            card["priority"] = soonest + delay  
        else:
            card["priority"] = delay

    heapq.heappush(deck, (card["priority"], card_id))


def run_session(card_dict, heap, filepath):
    """Run the interactive review loop until the user quits or the deck is finished."""
    print("Welcome to my flashcard app. Type 'quit' to exit.\n")

    if not heap:
        print("No cards to review. Exiting...")
        return

    while heap:
        priority, card_id = heapq.heappop(heap)
        card = card_dict[card_id]

        # Skip cards that are still scheduled for later review.
        if card["priority"] > 0:
            heapq.heappush(heap, (card["priority"], card_id))
            continue

        print(f"Question: {card['question']}")
        user_input = input("\nPress Enter to see the answer (or type 'quit' to exit): ").strip().lower()

        if user_input == "quit":
            heapq.heappush(heap, (card["priority"], card_id))
            print("saving and exiting...")
            save_deck(filepath, card_dict)
            break

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
    print("No more cards to review. Good job! Exiting...")


def main():
    # Determine the deck file path relative to this script, not the current working directory.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.abspath(os.path.join(script_dir, "..", "..", "flashcards_correct.JSON"))
    try:
        card_dict, heap = load_deck(filepath)
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Please make sure the file exists.")
        return
    except json.JSONDecodeError:
        print(f"Error: {filepath} is not a valid JSON file. Please check the file format.")
        return

    run_session(card_dict, heap, filepath)


if __name__ == "__main__":
    main()
