import collections
import json
import os
import sys
 
try:
    # Try relative import first (works when run as a module with `python -m flashcard.main`)
    from .deck import load_deck, save_deck
except ImportError:
    # Fallback- add src to path for direct script execution
    src_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if src_root not in sys.path:
        sys.path.insert(0, src_root)
    from flashcard.deck import load_deck, save_deck
 
 
def build_queue(card_dict):
    """Build an ordered deque of card IDs from the deck."""
    # Use a deque for insertion at both ends during rescheduling
    return collections.deque(card_dict.keys())
 
 
def reset_streaks(card_dict):
    """Clear wrong_streak on all cards (called between deck passes)."""
    # Reset so cards don't permanently stay near the front after a bad round
    for card in card_dict.values():
        card["wrong_streak"] = 0
 
 
def schedule_card(queue, card_id, wrong_streak):
    """
    Insert a card back into the queue at the right position.
      - Correct answer (wrong_streak == 0): append to the end (back of queue).
      - 1st wrong: insert 3 cards from the front.
      - 2nd wrong: insert 2 cards from the front.
      - 3rd+ wrong: insert at the front (show immediately next).
    """
    if wrong_streak == 0:
        # Correct: card goes to back so it won't show again for a while
        queue.append(card_id)
    elif wrong_streak == 1:
        # First wrong: show again soon (after ~3 more cards)
        insert_at = min(3, len(queue))
        queue.insert(insert_at, card_id)
    elif wrong_streak == 2:
        # Second wrong: show even sooner (after ~2 more cards)
        insert_at = min(2, len(queue))
        queue.insert(insert_at, card_id)
    else:
        # Third+ wrong: show immediately next to reinforce learning
        queue.appendleft(card_id)
 
 
def run_session(card_dict, filepath):
    """Run the interactive review loop continuously until the user quits."""
    print("Welcome to my flashcard app. Type 'quit' to exit.\n")
 
    # Ensure wrong_streak is initialized on every card
    # (in case JSON didn't include these fields)
    for card in card_dict.values():
        card.setdefault("streak", 0)
        card.setdefault("wrong_streak", 0)
 
    completed = 0
    queue = build_queue(card_dict)
 
    # Exit early if deck is completely empty
    if not queue:
        print("No cards to review. Exiting...")
        return
 
    try:
        while True:
            # Refill queue when all cards have been reviewed
            if not queue:
                completed += 1
                print(f"Deck completed! ({completed} pass(es) done). Starting over...\n")
                # Reset wrong_streaks so cards don't stay near front across passes
                reset_streaks(card_dict)
                # Create new queue with same cards in original order
                queue = build_queue(card_dict)
 
            card_id = queue.popleft()
            card = card_dict[card_id]
 
            print(f"Question: {card['question']}")
            user_input = input("\nPress Enter to see the answer (or type 'quit' to exit): ").strip().lower()
 
            # Allow user to exit gracefully without reviewing entire deck
            if user_input == "quit":
                print("Saving and exiting...")
                # Reset progress before saving so app starts fresh next time
                for c in card_dict.values():
                    c["streak"] = 0
                    c["wrong_streak"] = 0
                    c["priority"] = 0
                save_deck(filepath, card_dict)
                return
 
            print(f"\nAnswer: {card['answer']}")
 
            # Validate user input before processing
            result = input("\nDid you get it right? (y/n): ").strip().lower()
            while result not in ("y", "n"):
                result = input("Please enter y or n: ").strip().lower()
 
            if result == "y":
                # Card answered correctly: increment streak and reset wrong count
                card["streak"] += 1
                card["wrong_streak"] = 0
                # Send to back of queue so it won't appear again soon
                schedule_card(queue, card_id, wrong_streak=0)
                print("Good job!\n")
            else:
                # Card answered incorrectly: reset streak and increment wrong count
                card["streak"] = 0
                card["wrong_streak"] += 1
                # Bring card forward so user gets more chances to learn it
                schedule_card(queue, card_id, wrong_streak=card["wrong_streak"])
                print("You'll get it next time!\n")
 
            print("-" * 40 + "\n")
 
    except KeyboardInterrupt:
        # Gracefully handle Ctrl+C without crashing
        print("\nInterrupted. Saving progress...")
        try:
            # Reset progress before saving so app starts fresh next time
            for c in card_dict.values():
                c["streak"] = 0
                c["wrong_streak"] = 0
                c["priority"] = 0
            save_deck(filepath, card_dict)
        except Exception as e:
            # Warn user if save fails, but don't crash
            print(f"Warning: Failed to save progress: {e}")
 
 
def main():
    # Get directory where this script is located (src/flashcard/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = input("Enter the JSON file name: ").strip()
    # Navigate up two levels to repo root where JSON files are stored
    filepath = os.path.abspath(os.path.join(script_dir, "..", "..", filename))
    try:
        card_dict = load_deck(filepath)
    except FileNotFoundError:
        # File doesn't exist in the repo
        print(f"Error: {filename} not found. Please make sure the file exists.")
        return
    except json.JSONDecodeError:
        # File exists but JSON is malformed
        print(f"Error: {filename} is not a valid JSON file. Please check the file format.")
        return
    except ValueError as e:
        # JSON is valid but root isn't an array or other validation failed
        print(f"Error: {e}")
        return
    except IOError as e:
        # File I/O error during loading
        print(f"Error: {e}")
        return
 
    run_session(card_dict, filepath)
 
 
# Only run main() if this file is executed directly (not imported)
if __name__ == "__main__":
    main()