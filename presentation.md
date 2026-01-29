# Presentation: Smart-Shuffle Streaming Engine
**DSA Final Project - Problem 12**

---

## 1. The Challenge
Music Streaming services face a common problem: **Shuffle Repetition**.
- Standard random shuffle might play the same artist twice in a row.
- Users want control ("Play Next") without breaking the flow.
- "Undo" should reflect reality, not just the static list.

---

## 2. Our System Rules
1. **Circular Playlist**: Seamless looping.
2. **Spacing Rule (K)**: No artist can repeat within the next `K` songs.
3. **Priority Override**: `ADD_NEXT` bypasses algorithmic rules.
4. **History Stack**: True "Back" button functionality.

---

## 3. Data Structures Used (The "Why")

### A. Circular Doubly Linked List (CDLL)
- **Why?** To support infinite looping and efficient `NEXT/PREV` movement.
- **Complexity**: O(1) for insertion and pointer movement.

### B. Deque + Hash Map (Sliding Window)
- **Why?** To track artist cooldowns in O(1).
- **How?** Deque limits the window size to `K`. Hash map counts artist frequency in that window.

### C. Stack (History)
- **Why?** To remember the exact path taken by the user (even with shuffles and priority skips).
- **Complexity**: O(1) push/pop.

---

## 4. Key Algorithm: Smart Next
1. **Check Priority**: If the neighbor node has a `priority` flag (set by `ADD_NEXT`), play it immediately.
2. **Spacing Rule**: If not priority, check if the artist is in the `cooldown_map`.
3. **Skip if Invalid**: Move to the next node and repeat until a valid song is found.
4. **Fallback**: If the whole list is restricted (corner case), play the natural next.

---

## 5. Live Demonstration
*Commands to demonstrate:*
1. **Setup**: `ADD_SONG S1 Adele Hello`, `ADD_SONG S2 Drake Hotline`, `ADD_SONG S3 Adele Skyfall`, `ADD_SONG S4 Taylor Style`.
2. **Set Rule**: `SET_RESTRICTION_K 2`.
3. **Flow**:
   - `PLAY` (S1 Adele)
   - `NEXT` (Plays S2 Drake - Adele on cooldown)
   - `NEXT` (Natural is S3 Adele - **SKIPPED** - Plays S4 Taylor)
   - `PREV` (Returns to S2 Drake)

---

## 6. Conclusion
By combining core DSA concepts—Circular Lists, Hash Maps, and Stacks—we created an engine that balances algorithmic intelligence with user preference.
