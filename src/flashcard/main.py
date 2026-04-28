import heapq
import json
import random
from .deck import load_deck, save_deck


def update_priority(card_dict, deck, card_id, correct):
    card = card_dict[card_id]
    if correct:
        card["priority"] = max(0, card["priority"] - 1)
    else:
        card["priority"] += 2

    heapq.heappush(deck, (card["priority"], card_id))
    


def run_session(card_dict, heap, filepath):
    print("Welcome to my flashcard app. Type 'quit' to exit.\n")

    if not heap:
        print("No cards to review. Exiting...")
        return

    while heap:
        priority, card_id = heapq.heappop(heap)
        card = card_dict[card_id]

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
        
        if user_input == "quit":
            print("Quitting mid-card — this card won't be marked right or wrong.")
            heapq.heappush(heap, (card["priority"], card_id))
            save_deck(filepath, card_dict)
            break

        print(f"\nAnswer: {card['answer']}")

        result = input("\nDid you get it right? (y/n): ").strip().lower()
        while result not in ("y", "n"):
            result = input("please enter y or n: ").strip().lower()


        if got_right := (result == "y"):
            update_priority(card_dict, heap, card_id, True)

        if got_right:
             print("good job!\n")
        else:
            print("you'll get it next time!\n")

        print("-"*40 + "\n")

    save_deck(filepath, card_dict)
    print("No more cards to review. Good job! Exiting...")



def main():
    filepath = "../flashcards.JSON"
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
