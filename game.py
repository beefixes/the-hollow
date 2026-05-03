"""
The Hollow - A Text-Based Horror Game
Final Project | Python Programming
"""

import json
import os
import time
import random

# ─── Game Data ────────────────────────────────────────────────────────────────

ROOMS = {
    "front_porch": {
        "name": "Front Porch",
        "description": (
            "You stand before an old farmhouse at the edge of a dead cornfield. "
            "The front door hangs open. A rusted lantern flickers near the entrance. "
            "Something inside the house groans — wood settling, you hope."
        ),
        "exits": {"inside": "foyer"},
        "items": ["rusty_key"],
        "event": None,
    },
    "foyer": {
        "name": "Foyer",
        "description": (
            "Wallpaper peels from the walls in long, curling strips. "
            "A grand staircase leads up into darkness. To your left is a hallway. "
            "To your right, a door with a brass handle. "
            "Muddy boot prints on the floor lead toward the hallway."
        ),
        "exits": {"upstairs": "upstairs_hall", "hallway": "hallway", "right": "locked_study", "outside": "front_porch"},
        "items": [],
        "event": "muddy_prints",
    },
    "hallway": {
        "name": "Dark Hallway",
        "description": (
            "The hallway stretches into shadow. Framed photographs line the walls — "
            "each one has had the faces scratched out. "
            "At the far end you can see a faint light under a door."
        ),
        "exits": {"back": "foyer", "forward": "kitchen"},
        "items": ["matches"],
        "event": "scratched_photos",
    },
    "kitchen": {
        "name": "Kitchen",
        "description": (
            "The kitchen smells of rot and iron. A pot sits on the stove, "
            "still warm. On the table is a torn journal page and a bread knife. "
            "A cellar door is cut into the floor."
        ),
        "exits": {"back": "hallway", "cellar": "cellar"},
        "items": ["journal_page", "bread_knife"],
        "event": "warm_pot",
    },
    "cellar": {
        "name": "Root Cellar",
        "description": (
            "Stone steps lead down into a damp cellar. Shelves of black, "
            "decomposed preserves line the walls. In the corner, a heavy iron door "
            "is bolted shut. Scratched into the wood floor: 'DON'T OPEN IT'."
        ),
        "exits": {"upstairs": "kitchen", "iron_door": "locked_room"},
        "items": ["iron_bolt"],
        "event": "scratching_sounds",
    },
    "locked_study": {
        "name": "The Study",
        "description": (
            "Bookshelves sag under the weight of water-damaged volumes. "
            "A desk sits in the center with papers scattered across it. "
            "Behind the desk, a safe is built into the wall."
        ),
        "exits": {"out": "foyer"},
        "items": ["safe_note"],
        "event": None,
        "locked": True,
        "key_required": "rusty_key",
    },
    "upstairs_hall": {
        "name": "Upstairs Hall",
        "description": (
            "The upstairs hall is narrow and low-ceilinged. "
            "Three doors line the hall. One at the end is sealed with wooden planks. "
            "The floorboards creak with every step."
        ),
        "exits": {"downstairs": "foyer", "bedroom": "master_bedroom", "childs_room": "childs_room"},
        "items": [],
        "event": "footsteps_below",
    },
    "master_bedroom": {
        "name": "Master Bedroom",
        "description": (
            "A four-poster bed dominates the room, its curtains torn and gray. "
            "Across the mirror above the dresser, in what looks like old lipstick: "
            "'HE'S STILL HERE'. A locket rests on the pillow."
        ),
        "exits": {"out": "upstairs_hall"},
        "items": ["locket"],
        "event": "mirror_writing",
    },
    "childs_room": {
        "name": "Child's Room",
        "description": (
            "Faded alphabet posters cling to the walls. A rocking horse "
            "sways gently in the corner — with no wind to move it. "
            "A small music box sits on the shelf."
        ),
        "exits": {"out": "upstairs_hall"},
        "items": ["music_box"],
        "event": "rocking_horse",
    },
    "locked_room": {
        "name": "The Room",
        "description": (
            "Beyond the iron door is a small stone room. "
            "In the center, a figure sits hunched in a chair, back to you. "
            "It is perfectly still. On the floor, a circle of salt surrounds the chair."
        ),
        "exits": {"out": "cellar"},
        "items": [],
        "event": "final_room",
        "locked": True,
        "key_required": "iron_bolt",
    },
}

ITEMS = {
    "rusty_key":   {"name": "Rusty Key",      "description": "An old skeleton key, heavily corroded. It might open something."},
    "matches":     {"name": "Box of Matches", "description": "Half a box of matches. Enough to light your way — briefly."},
    "journal_page":{"name": "Torn Journal Page", "description": (
        "The handwriting is frantic: 'It followed us back from the hollow. "
        "I locked it in the cellar. Do NOT let it out. "
        "Salt keeps it still. Fire kills it for good.'"
    )},
    "bread_knife": {"name": "Bread Knife",    "description": "A dull kitchen knife. Better than nothing."},
    "iron_bolt":   {"name": "Iron Bolt",      "description": "A heavy iron bolt, clearly from a door somewhere in this house."},
    "safe_note":   {"name": "Safe Note",      "description": "A slip of paper reads: 'The combination is the year this house was built — 1887.'"},
    "locket":      {"name": "Gold Locket",    "description": "Inside is a tiny photo of a family. On the back: 'The salt breaks the circle. Fire ends it.'"},
    "music_box":   {"name": "Music Box",      "description": "It plays three notes, then stops. Over and over. Three notes."},
}

EVENTS = {
    "muddy_prints": (
        "You crouch to examine the boot prints. They're fresh — "
        "the mud hasn't dried yet. They stop abruptly in the middle of the foyer."
    ),
    "scratched_photos": (
        "You lean in close to one of the photographs. The scratching is deep, "
        "almost violent — done with something sharp. In one frame, "
        "a small handprint remains untouched at the edge."
    ),
    "warm_pot": (
        "You lift the lid off the pot. Whatever was inside has been burned to nothing, "
        "but the pot itself is still warm to the touch. Someone was here recently."
    ),
    "scratching_sounds": (
        "You freeze. From behind the iron door comes a slow, rhythmic scratching — "
        "three scratches, then silence. Three scratches, then silence."
    ),
    "footsteps_below": (
        "The floorboards beneath you creak. From below — from the foyer — "
        "you hear the unmistakable sound of slow, deliberate footsteps. "
        "Then they stop."
    ),
    "mirror_writing": (
        "You stare at the mirror. For just a moment, in your own reflection, "
        "you see a second figure standing behind you. You spin — nothing is there."
    ),
    "rocking_horse": (
        "You take a step toward the rocking horse. It stops. "
        "You freeze. The room is completely silent. "
        "Then, very slowly, it begins to rock again."
    ),
    "final_room": None,  # Handled separately as the ending trigger
}

# ─── Player State ─────────────────────────────────────────────────────────────

def new_player(name):
    """Create and return a fresh player state dictionary."""
    return {
        "name": name,
        "current_room": "front_porch",
        "inventory": [],
        "visited": [],
        "sanity": 100,
        "alive": True,
        "ending": None,
    }

# ─── Display Helpers ──────────────────────────────────────────────────────────

def slow_print(text, delay=0.03):
    """Print text one character at a time for dramatic effect."""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def divider():
    print("\n" + "─" * 55 + "\n")

def show_title():
    """Print the game title screen."""
    os.system("cls" if os.name == "nt" else "clear")
    title = r"""
  _____ _            _   _       _ _
 |_   _| |__   ___  | | | | ___ | | | _____      __
   | | | '_ \ / _ \ | |_| |/ _ \| | |/ _ \ \ /\ / /
   | | | | | |  __/ |  _  | (_) | | | (_) \ V  V /
   |_| |_| |_|\___| |_| |_|\___/|_|_|\___/ \_/\_/

    """
    print(title)
    slow_print("  A text-based horror game. For those who dare enter.", 0.02)
    print()

# ─── Room & Movement ──────────────────────────────────────────────────────────

def describe_room(player):
    """Print the current room's description and available exits/items."""
    room_id = player["current_room"]
    room = ROOMS[room_id]

    divider()
    slow_print(f"[ {room['name'].upper()} ]", 0.04)
    print()
    slow_print(room["description"])
    print()

    # Show items present in the room
    if room["items"]:
        items_here = [ITEMS[i]["name"] for i in room["items"]]
        print(f"  You notice: {', '.join(items_here)}")

    # Show available exits
    exits = list(room["exits"].keys())
    print(f"  Exits: {', '.join(exits)}")

    # Show sanity
    print(f"\n  [Sanity: {player['sanity']}%]")

    # Fire event once per visit
    if room_id not in player["visited"] and room.get("event"):
        event_key = room["event"]
        if event_key != "final_room" and event_key in EVENTS:
            print()
            slow_print(f"  >> {EVENTS[event_key]}", 0.025)
            reduce_sanity(player, 8)

    if room_id not in player["visited"]:
        player["visited"].append(room_id)

def move(player, direction):
    """Attempt to move the player in the given direction."""
    room = ROOMS[player["current_room"]]
    exits = room["exits"]

    if direction not in exits:
        print("  You can't go that way.")
        return

    destination_id = exits[direction]
    destination = ROOMS[destination_id]

    # Check if destination is locked
    if destination.get("locked"):
        key_needed = destination.get("key_required")
        if key_needed not in player["inventory"]:
            item_name = ITEMS[key_needed]["name"] if key_needed in ITEMS else "something"
            print(f"  The way is blocked. You need: {item_name}.")
            return
        else:
            slow_print(f"  You use the {ITEMS[key_needed]['name']} to get through.")

    player["current_room"] = destination_id
    describe_room(player)

# ─── Inventory & Items ────────────────────────────────────────────────────────

def pick_up(player, item_name):
    """Pick up an item from the current room into the player's inventory."""
    room = ROOMS[player["current_room"]]
    # Find a matching item (fuzzy match on name)
    found = None
    for item_id in room["items"]:
        if item_name.lower() in ITEMS[item_id]["name"].lower() or item_name.lower() in item_id:
            found = item_id
            break

    if not found:
        print(f"  There's no '{item_name}' here to pick up.")
        return

    player["inventory"].append(found)
    room["items"].remove(found)
    slow_print(f"  You picked up: {ITEMS[found]['name']}.")

def show_inventory(player):
    """Display everything the player is carrying."""
    if not player["inventory"]:
        print("  You're not carrying anything.")
        return
    print("  You're carrying:")
    for item_id in player["inventory"]:
        print(f"    - {ITEMS[item_id]['name']}: {ITEMS[item_id]['description']}")

def examine_item(player, item_name):
    """Examine an item in inventory or in the current room."""
    all_available = player["inventory"] + ROOMS[player["current_room"]]["items"]
    for item_id in all_available:
        if item_name.lower() in ITEMS[item_id]["name"].lower() or item_name.lower() in item_id:
            slow_print(f"  {ITEMS[item_id]['description']}")
            return
    print(f"  You don't see any '{item_name}' to examine.")

# ─── Sanity System ────────────────────────────────────────────────────────────

def reduce_sanity(player, amount):
    """Lower the player's sanity and trigger effects at low levels."""
    player["sanity"] = max(0, player["sanity"] - amount)
    if player["sanity"] <= 30 and player["sanity"] > 0:
        visions = [
            "  The walls breathe.",
            "  You hear your name — but no one is here.",
            "  The shadows move when you look away.",
            "  Something is wrong with the light.",
        ]
        slow_print(random.choice(visions), 0.03)
    if player["sanity"] == 0:
        player["alive"] = False
        player["ending"] = "lost_mind"

# ─── Endings ──────────────────────────────────────────────────────────────────

def trigger_ending(player, choice):
    """Handle the final room encounter and determine the ending."""
    divider()
    has_journal = "journal_page" in player["inventory"] or "locket" in player["inventory"]
    has_matches = "matches" in player["inventory"]
    has_knife   = "bread_knife" in player["inventory"]

    slow_print("The figure in the chair does not move. The salt circle surrounds it completely.\n", 0.03)
    time.sleep(1)

    if choice == "1" and has_matches:
        # Good ending — fire
        slow_print("You strike a match. The flame catches the edge of the salt circle.", 0.03)
        time.sleep(0.8)
        slow_print("The figure convulses. A sound tears through the room — not a scream exactly.", 0.03)
        time.sleep(0.8)
        slow_print("Then silence. Then nothing. The house exhales.", 0.03)
        time.sleep(1)
        slow_print("\nYou walk out the front door as the first light of morning touches the cornfield.", 0.03)
        player["ending"] = "good"

    elif choice == "2":
        # Neutral ending — leave
        slow_print("You back away slowly. You leave the house. You drive until the farmhouse", 0.03)
        slow_print("is a dark smear in your rearview mirror.", 0.03)
        time.sleep(0.8)
        slow_print("\nBut sometimes, late at night, you hear three scratches on the wall.", 0.03)
        player["ending"] = "neutral"

    elif choice == "3" and has_knife:
        # Bad ending — break the circle
        slow_print("You drag the knife through the salt circle.", 0.03)
        time.sleep(0.8)
        slow_print("The figure turns.", 0.03)
        time.sleep(1.5)
        slow_print("\nThe last entry in the county record lists one more missing person.", 0.03)
        player["alive"] = False
        player["ending"] = "bad"

    else:
        # Default — flee
        slow_print("You back out of the room and run. You don't look back.", 0.03)
        player["ending"] = "neutral"

def show_ending(player):
    """Print the ending screen based on how the game concluded."""
    divider()
    endings = {
        "good":      ("YOU SURVIVED",   "The hollow is quiet now. The thing in the chair is gone.\nWell done."),
        "neutral":   ("YOU ESCAPED",    "You made it out. But you left something behind.\nOr something followed you."),
        "bad":       ("YOU ARE LOST",   "The Hollow claimed another. The house waits for the next visitor."),
        "lost_mind": ("YOUR MIND BROKE","The darkness took you before anything else could.\nSanity: 0%."),
    }
    title, text = endings.get(player["ending"], ("THE END", ""))
    slow_print(f"  ══ {title} ══", 0.05)
    print()
    slow_print(f"  {text}", 0.03)
    print()
    slow_print(f"  Rooms explored: {len(player['visited'])} / {len(ROOMS)}", 0.02)
    slow_print(f"  Final sanity:   {player['sanity']}%", 0.02)
    divider()

# ─── Save / Load ──────────────────────────────────────────────────────────────

SAVE_FILE = "save.json"

def save_game(player):
    """Write the current player state to a JSON file."""
    with open(SAVE_FILE, "w") as f:
        json.dump(player, f, indent=2)
    print("  Game saved.")

def load_game():
    """Load player state from a JSON file, or return None if not found."""
    if not os.path.exists(SAVE_FILE):
        return None
    with open(SAVE_FILE, "r") as f:
        return json.load(f)

# ─── Command Parser ───────────────────────────────────────────────────────────

def parse_command(player, raw):
    """Parse a text command and route it to the correct action."""
    command = raw.strip().lower()
    tokens  = command.split()

    if not tokens:
        return

    verb = tokens[0]
    args = " ".join(tokens[1:]) if len(tokens) > 1 else ""

    if verb in ("go", "move", "walk", "enter"):
        move(player, args)

    elif verb in ("n", "s", "e", "w", "up", "down",
                  "inside", "outside", "back", "forward",
                  "upstairs", "downstairs", "hallway", "right",
                  "cellar", "bedroom", "childs_room", "iron_door"):
        move(player, verb)

    elif verb in ("get", "pick", "grab", "take"):
        target = args.replace("up ", "").strip()
        pick_up(player, target)

    elif verb in ("inventory", "i", "bag", "items", "carrying"):
        show_inventory(player)

    elif verb in ("look", "l", "describe", "examine", "inspect", "read"):
        if args:
            examine_item(player, args)
        else:
            describe_room(player)

    elif verb in ("save",):
        save_game(player)

    elif verb in ("help", "h", "?"):
        show_help()

    elif verb in ("quit", "exit", "q"):
        confirm = input("  Quit the game? (y/n): ").strip().lower()
        if confirm == "y":
            player["alive"] = False
            player["ending"] = "quit"

    else:
        print(f"  Unknown command: '{command}'. Type 'help' for a list of commands.")

def show_help():
    """Print the command reference."""
    print("""
  Commands:
    go [direction]       Move in a direction (e.g., go inside, go upstairs)
    [direction]          Shortcut move (e.g., hallway, back, upstairs)
    get [item]           Pick up an item
    look / examine       Look around or examine an item (examine journal)
    inventory / i        Show what you're carrying
    save                 Save your progress
    help                 Show this menu
    quit                 Exit the game
    """)

# ─── Final Room Interaction ───────────────────────────────────────────────────

def handle_final_room(player):
    """Special interactive sequence for the game's climax."""
    slow_print("\nYou step into the room. The figure does not react.", 0.03)
    reduce_sanity(player, 20)
    time.sleep(1)
    slow_print("What do you do?\n", 0.03)

    has_matches = "matches" in player["inventory"]
    has_knife   = "bread_knife" in player["inventory"]

    print("  1. Use the matches — set the circle alight" + ("" if has_matches else " [no matches]"))
    print("  2. Leave the room and get out of the house")
    print("  3. Break the salt circle" + ("" if has_knife else " [need something sharp]"))
    print()

    choice = input("  Your choice (1/2/3): ").strip()
    trigger_ending(player, choice)

# ─── Main Game Loop ───────────────────────────────────────────────────────────

def game_loop(player):
    """Run the main game loop until the player is no longer alive."""
    describe_room(player)

    while player["alive"]:
        # Check for final room event
        if player["current_room"] == "locked_room" and "locked_room" not in player["visited"]:
            handle_final_room(player)
            break

        try:
            raw = input("\n  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if raw:
            parse_command(player, raw)

def main():
    """Entry point — handle new game vs. load, then start the loop."""
    show_title()

    # Offer to load a saved game
    saved = load_game()
    if saved:
        choice = input("  A saved game was found. Load it? (y/n): ").strip().lower()
        if choice == "y":
            player = saved
            slow_print(f"\n  Welcome back, {player['name']}. The house remembers you.", 0.03)
            game_loop(player)
            if player.get("ending") and player["ending"] != "quit":
                show_ending(player)
            return

    # New game
    print()
    name = input("  Enter your name, if you dare: ").strip()
    if not name:
        name = "Stranger"

    player = new_player(name)
    slow_print(f"\n  Very well, {name}. Try to stay sane.\n", 0.03)
    time.sleep(1)

    game_loop(player)

    if player.get("ending") and player["ending"] != "quit":
        show_ending(player)
        # Clear save file on game end
        if os.path.exists(SAVE_FILE):
            os.remove(SAVE_FILE)

if __name__ == "__main__":
    main()
