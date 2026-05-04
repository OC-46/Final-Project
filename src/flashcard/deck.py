import json


def load_deck(filepath):
    """Load flashcards from JSON, validate cards, and return card dictionary."""
    with open(filepath, "r") as f:
        data = json.load(f)

    # Ensure the JSON root is a list
    if not isinstance(data, list):
        raise ValueError("JSON file must contain an array of cards at the root level.")

    card_dict = {}
    skipped = 0

    for card in data:
        # Validate that card is a dict and has required fields.
        if not isinstance(card, dict):
            print(f"Warning: Skipping non-dict card: {card}")
            skipped += 1
            continue

        if "id" not in card or "question" not in card or "answer" not in card:
            print(f"Warning: Skipping card with missing fields: {card}")
            skipped += 1
            continue

        # Skip duplicate IDs to avoid overwriting cards.
        if card["id"] in card_dict:
            print(f"Warning: duplicate id '{card['id']}' found, skipping.")
            skipped += 1
            continue

        # Ensure streak and wrong_streak fields exist; if missing, default to 0.
        card.setdefault("priority", 0)
        card.setdefault("streak", 0)
        card.setdefault("wrong_streak", 0)
        card_dict[card["id"]] = card

    if skipped > 0:
        print(f"Finished loading deck with {skipped} skipped cards due to missing or duplicate fields.")

    return card_dict


def save_deck(filepath, card_dict):
    """Write the current deck back to JSON with pretty formatting."""
    try:
        with open(filepath, "w") as f:
            json.dump(list(card_dict.values()), f, indent=2)
    except IOError as e:
        raise IOError(f"Failed to save deck to {filepath}: {e}")
