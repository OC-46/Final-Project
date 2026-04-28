import random
from .deck import load_deck, save_deck


def run_session(card_dict, deck):
    print("Welcome to my flashcard app. Type 'quit' to exit.\n")

    while deck:
        card_id = deck.pop(0)
        card = card_dict[card_id]

        print(f"Question: {card['question']}")
        user_input = input("\nPress Enter to see the answer (or type 'quit' to exit): ").strip().lower()

        if user_input == "quit":
            print("Ending session")
            break

        print(f"\nAnswer: {card['answer']}")

        result = input("\nDid you get it right? (y/n): ").strip().lower()
        while result not in ("y", "n"):
            result = input("please enter y or n: ").strip().lower()

        if result == "y":
            print("good job!\n")
        else:
            print("you'll get it next time!\n")

        print("-"*40 + "\n")

    if not deck:
        print("you have completed the whole deck!")



def main():
    filepath = "../flashcards.JSON"
    card_dict, deck = load_deck(filepath)

    deck_list = [card_id for _, card_id in deck]
    
    run_session(card_dict, deck_list)


if __name__ == "__main__":
    main()
