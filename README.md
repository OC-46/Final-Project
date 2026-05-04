# Final Project: flashcard deck

## What this project does
This is a simple terminal based flashcard app that adapts review order based on how well you answer each card. It loads flashcards from a JSON file, asks the user questions, shows answers immediately, and adjusts the review schedule so cards you get wrong appear sooner based on consecutive wrong answers.

## How to install dependencies and run it
1. Make sure you have Python 3 installed.
2. No other outside libraries are used.

python3 --version
python3 -m pip install -r requirements.txt


3. Run the app from the repository root:

python3 src/flashcard/main.py

5. The app will prompt you to enter the JSON file name. The JSON files should be in the repository root; if not, the program will not run.

## Data structures and algorithms used
- dict (`card_dict`) in `src/flashcard/deck.py` stores flashcards keyed by `id` for fast lookup and updates.
- `collections.deque` in `src/flashcard/main.py` manages the review queue for ordered card presentation.
- `json` in `src/flashcard/deck.py` reads and writes the flashcard deck from disk.

### logic
- `src/flashcard/deck.py`
  - `load_deck(filepath)` loads cards from JSON, validates required fields, skips invalid or duplicate cards.
  - `save_deck(filepath, card_dict)` writes the updated deck back to JSON.
- `src/flashcard/main.py`
  - `build_queue(card_dict)` creates an initial deque of card IDs.
  - `schedule_card(queue, card_id, wrong_streak)` inserts a card back into the queue based on the number of consecutive wrong answers.
  - `run_session(card_dict, filepath)` runs the interactive question-and-answer loop.
  - `main()` prompts for the JSON file and starts the session.

## What is working
- Reading flashcards from a JSON file.
- Validating each card for required fields and skipping invalid cards.
- Using a deque-based queue to schedule review order based on consecutive wrong answers.
- Interacting with the user in the terminal to show questions and check responses.
- Tracking streaks and adjusting queue position based on whether the answer was correct or wrong.
- Saving changed streaks and wrong streaks back to the JSON file when exiting.

## What is not working or missing
- There is no graphical interface; it is terminal-only.
- The scheduling strategy is basic and may not follow a full spaced repetition algorithm.
- It does not currently support adding new cards through the app.

## ai

I used AI when I was looking to find edge cases that an AI could catch much easier than I could, as well as debugging the scheduling function to fine-tune and find the right queue positioning when you get cards right or wrong. I also used it to develop some of the JSON files to save time. 