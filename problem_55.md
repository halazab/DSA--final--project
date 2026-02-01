# Problem 55: The Bounded History Manager

## Problem Description
Infinite undo history consumes too much memory. Most apps only remember the last `N` actions.

### The System Rules
1.  **Capacity**: `MaxHistory = N`.
2.  **Add Action**:
    *   If size < N, append.
    *   If size == N, drop the **Oldest** action (Front) and append new (Back).
3.  **Undo**: Pop from Back.

## Must Use Data Structures
*   **Double-Ended Queue (Deque)**: Efficient adding to back and removing from front.
*   (A Stack cannot efficiently remove the bottom element).

## Operations to Implement (CLI Commands)
*   `SET_LIMIT <n>`
*   `ACTION <name>`
*   `UNDO`
*   `SHOW_HISTORY`

## Sample Execution

```text
> SET_LIMIT 3
> ACTION A
> ACTION B
> ACTION C
Hist: [A, B, C]

> ACTION D
Full. Dropped A.
Hist: [B, C, D]

> UNDO
Reverted D.
Hist: [B, C]
```
