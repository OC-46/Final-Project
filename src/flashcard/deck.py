import json
import heapq


def load_deck(filepath):
    with open(filepath, "r") as f:
        cards = json.load(f)
    
    card_dict = {}
    heap = []

    for card in cards:
        card_dict[card["id"]] = card
        heapq.heappush(heap, (card["priority"], card["id"]))

    return card_dict, heap

def save_deck(filepath, card_dict):
    with open(filepath, "w") as f:
        json.dump(list(card_dict.values()), f, indent = 2)
        