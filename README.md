# Smart-Shuffle Music Streaming Engine

A sophisticated playlist sequencer designed for music streaming services. It features "Smart Shuffle" intelligence that prevents artist repetition and supports priority "Queue Next" requests.

## Key Features

- **Circular Playlist**: The playlist wraps around indefinitely from end to start.
- **Smart Spacing Rule**: Prevents songs from the same artist from playing too close together (controlled by a restriction factor `K`).
- **Priority Queueing**: Users can force a song to play next, bypassing the smart spacing algorithm.
- **True Undo (History)**: Supports navigating back through the actual play history, even if the shuffle order or queue changed.

## Data Structures Used

| Structure | Purpose |
| :--- | :--- |
| **Circular Doubly Linked List** | Main playlist backbone for seamless forward/backward traversal and wrap-around. |
| **Hash Map + Frequency Array** | Tracks artist "Cooldowns" efficiently in O(1). |
| **Deque (Sliding Window)** | Tracks the sequence of the last `K` artists to manage the cooldown window. |
| **Stack** | Stores the history of actually played Track IDs for reliable `PREV` functionality. |

## How to Run

Ensure you have Python 3 installed. Run the following command in your terminal:

```bash
python3 playlist_manager.py
```

The tool will start an interactive session with a `playlist > ` prompt.

## CLI Commands

| Command | Description |
| :--- | :--- |
| `ADD_SONG <id> <artist> <title>` | Appends a new song to the playlist. |
| `PLAY` | Plays the current song, updates history and cooldowns. |
| `NEXT` | Moves to the next valid song (skips restricted artists). |
| `PREV` | Returns to the previous song from the actual play history. |
| `ADD_NEXT <id>` | Injects an existing song into the "Priority Next" slot. |
| `SET_RESTRICTION_K <k>` | Sets the spacing restriction. |
| `HELP` | Displays a list of available commands. |
| `EXIT` | Closes the CLI tool. |

## Example Usage

```text
ADD_SONG S1 Adele Hello
ADD_SONG S2 Drake Hotline
ADD_SONG S3 Adele Skyfall
SET_RESTRICTION_K 2
PLAY
NEXT
```
