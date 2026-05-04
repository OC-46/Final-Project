# Final Project: flashcard deck

## What this project does
This is a simple terminal-based flashcard app that adapts review order based on how well you answer each card. It loads flashcards from a JSON file, asks the user questions, shows answers imediately, and updates card priorities so cards you get wrong appear sooner.

## How to install dependencies and run it
1. Make sure you have Python 3 installed.
2. not other outside libraires are used

bash
python3 --version
python3 -m pip install -r requirements.txt

3. Run the app from the repository root:

python3 src/flashcard/main.py


4. you can also run:

python3 -m src.flashcard.main

5. The app expects all json files to be in the repository, if not the program will not run

## Data structures and algorithms used
- dict (`card_dict`) in `src/flashcard/deck.py` stores flashcards keyed by `id` for fast lookup and updates.
- `heapq` priority queue (`heap`) in `src/flashcard/deck.py` keeps review order based on each card's `priority` value.
- `json` in `src/flashcard/deck.py` reads and writes the flashcard deck from disk.

### logic
- `src/flashcard/deck.py`
  - `load_deck(filepath)` loads cards from JSON, validates required fields, skips invalid or duplicate cards, and builds the starting heap.
  - `save_deck(filepath, card_dict)` writes the updated deck back to JSON.
- `src/flashcard/main.py`
  - `update_priority(card_dict, deck, card_id, correct)` adjusts a card's priority after review.
  - `run_session(card_dict, heap, filepath)` runs the interactive question-and-answer loop.
  - `main()` loads the deck and starts the session.

## What is working
- Reading flashcards from a JSON file.
- Validating each card for required fields and skipping invalid cards.
- Using a heap-based priority queue to schedule review order.
- Interacting with the user in the terminal to show questions and check responses.
- Updating card priorities based on whether the answer was correct or wrong.
- Saving changed priorities back to the JSON file when exiting.

## What is not working or missing
- There is no graphical interface; it is terminal-only.
- The scheduling strategy is basic and may not follow a full spaced repetition algorithm.
- It does not currently support adding new cards through the app.

## ai

I used ai when I was looking to find edge cases that an ai could catch much easier than I could, as well as debugging the updating priority function to findtune and find the right level of priority when you would get cards right or wrong. I also used it to develop some of the json files to save time. 