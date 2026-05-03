# The Hollow 🕯️
### A Text-Based Horror Game — Python Final Project

---

## Overview

**The Hollow** is a text-based horror adventure game written in Python. You play as a person who has entered an abandoned farmhouse and must uncover its dark secret — and escape with your mind (and life) intact.

The game features room exploration, a dynamic inventory system, a sanity mechanic, multiple endings, and save/load functionality via JSON.

---

## How to Run

**Requirements:** Python 3.8 or higher — no external libraries needed.

```bash
python game.py
```

---

## How to Play

Type commands to interact with the world. Examples:

| Command | What it does |
|---|---|
| `go inside` | Move in a direction |
| `hallway` | Shortcut movement |
| `get journal` | Pick up an item |
| `look` | Describe the current room |
| `examine knife` | Inspect an item in detail |
| `inventory` or `i` | Show what you're carrying |
| `save` | Save your progress to a file |
| `help` | Show all commands |
| `quit` | Exit the game |

---

## Game Features

- **9 explorable rooms** — each with unique descriptions and atmosphere
- **8 collectible items** — some required to progress, others lore-building
- **Sanity system** — disturbing events chip away at your mind. Reach 0% and you lose
- **Multiple endings** — 4 possible outcomes based on your choices and what you've collected
- **Save & Load** — progress is saved to `save.json` using Python's `json` module
- **Locked rooms** — certain paths require specific items to enter
- **Atmospheric events** — first-visit triggers that reveal the story

---

## Project Structure

```
the_hollow/
│
├── game.py        # All game logic (single-file project)
├── save.json      # Auto-generated when you save (not committed)
└── README.md      # This file
```

---

## Python Concepts Demonstrated

| Concept | Where Used |
|---|---|
| Functions | Every feature is its own function (`move`, `pick_up`, `describe_room`, etc.) |
| Dictionaries | `ROOMS`, `ITEMS`, `EVENTS`, `player` state |
| Lists | Inventory, visited rooms, room items |
| JSON file I/O | `save_game()` and `load_game()` |
| User input | Main game loop command parser |
| Conditionals | Movement locks, ending logic, sanity effects |
| String manipulation | Command parsing, fuzzy item matching |
| Randomness | `random.choice()` for sanity event messages |
| `os` module | Save file detection, screen clearing |
| `time` module | Dramatic pacing with `time.sleep()` |

---

## Endings

There are **4 possible endings** — your choices in the final room, combined with what you've collected, determine your fate. Explore thoroughly!

---

## Author

*Your Name Here*  
Python Programming — Final Project
