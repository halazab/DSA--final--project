# Problem 12: The "Smart-Shuffle" Streaming Engine (Playlist Manager)

## Problem Description
You are engineering the playlist sequencer for a music streaming service. The system must manage a playlist of songs but with "Smart Shuffle" intelligence that prevents repetition and respects "Queue Next" requests.

### The System Rules
1.  **Playlist Structure**:
    *   Songs are nodes in a sequence.
    *   **Looping**: The playlist wraps around (End -> Start).
2.  **Navigation**:
    *   `PLAY`: Plays current song.
    *   `NEXT` / `PREV`: Moves cursor.
3.  **Smart Features**:
    *   **Spacing Rule**: If a song by Artist "X" is played, NO song by Artist "X" can play again for the next `K` songs (e.g., K=3). If the "Natural Next" song violates this, skip it and find the nearest valid one forward.
    *   **Priority Queueing**: Users can `ADD_NEXT(song)`, which injects the song *immediately after* the current one. This ignores the Spacing Rule (User intent overrides algorithm).
    *   **History**: Keep a global stack of *actually played* songs to support a true "Undo" even if the shuffle order changed.

## Must Use Data Structures
*   **Circular Doubly Linked List**: The primary playlist backbone.
*   **Hash Map + Frequency Array**: To track "Cooldowns" for artists efficiently.
*   **Stack**: Global history of played Track IDs for the `PREV` button to work reliably.
*   **Deque (Sliding Window)**: To track the sequence of last `K` artists played.

## Operations to Implement (CLI Commands)
*   `ADD_SONG <id> <artist> <title>`: Append to playlist.
*   `PLAY`: Play current song (Push to History, Update Artist Cooldown).
*   `NEXT`: Move to next *valid* song (Skipping restricted artists).
*   `PREV`: Restore state to previous song from History.
*   `ADD_NEXT <id>`: Priority insert.
*   `SET_RESTRICTION_K <k>`: Set artist spacing.

## Sample Execution

```text
> ADD_SONG S1 Adele Hello
> ADD_SONG S2 Drake Hotline
> ADD_SONG S3 Adele Skyfall
> ADD_SONG S4 Taylor Style
> SET_RESTRICTION_K 2

> PLAY
Playing: S1 (Adele). Cooldown: [Adele].

> NEXT
(Natural next is S2 Drake... Valid? Yes)
Playing: S2 (Drake). Cooldown: [Adele, Drake].

> NEXT
(Natural next is S3 Adele... Valid? NO! Recent Adele. Skipping S3...)
(Next is S4 Taylor... Valid? Yes)
Playing: S4 (Taylor). Cooldown: [Drake, Taylor]. (Adele expired)

> PREV
Playing: S2 (Drake) - Restored from History.
```