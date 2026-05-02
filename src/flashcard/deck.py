import json
import heapq


def load_deck(filepath):
    """Load flashcards from JSON, validate cards, and build a priority heap."""
    with open(filepath, "r") as f:
        cards = json.load(f)

    card_dict = {}
    heap = []
    skipped = 0

    for card in cards:
        # Validate required fields on each card.
        if "id" not in card or "question" not in card or "answer" not in card or "priority" not in card:
            print(f"Warning: Skipping card with missing fields: {card}")
            skipped += 1
            continue

        # Skip duplicate IDs to avoid overwriting cards.
        if card["id"] in card_dict:
            print(f"Warning: duplicate id '{card['id']}' found, skipping.")
            skipped += 1
            continue

        # Ensure numeric priority and streak fields exist; if missing, default to 0.
        card.setdefault("priority", 0)
        card.setdefault("streak", 0)
        card_dict[card["id"]] = card
        heapq.heappush(heap, (card["priority"], card["id"]))

    if skipped > 0:
        print(f"Finished loading deck with {skipped} skipped cards due to missing or duplicate fields.")

    return card_dict, heap


def save_deck(filepath, card_dict):
    """Write the current deck back to JSON with pretty formatting."""
    with open(filepath, "w") as f:
        json.dump(list(card_dict.values()), f, indent=2)
