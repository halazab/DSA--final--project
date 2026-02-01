# Problem 24: Deadline-Aware Task Executor

## Problem Description
You are building an execution engine for time-sensitive tasks. Each task has a deadline, and if the task cannot be completed before its deadline, it must be discarded. The system should maximize the number of tasks completed.

### The System Rules
1.  **Task Properties**: Each task has:
    *   `Task ID`
    *   `Duration` (time units to complete)
    *   `Deadline` (absolute time by which it must finish)
    *   `Value` (reward for completing this task)
2.  **Execution Logic**:
    *   The executor runs one task at a time.
    *   Tasks are picked based on **Earliest Deadline First (EDF)**.
    *   Before starting a task, check if `Current Time + Duration <= Deadline`. If not, the task is **expired** and discarded.
3.  **Goal**: Maximize total value of completed tasks.
4.  **Late Arrivals**: Tasks can arrive at any time. Newly arrived tasks with earlier deadlines may preempt the current order but NOT a task already in progress.

## Must Use Data Structures
*   **Min-Heap**: Keyed by `Deadline` to always pick the task with the earliest deadline.
*   **Queue**: For expired tasks (for logging/audit).
*   **Stack** (Optional): If implementing "Undo last pick" for debugging.
*   **Array**: To track completed tasks and calculate total value.

## Operations to Implement (CLI Commands)
*   `ADD_TASK <id> <duration> <deadline> <value>`: Add a task.
*   `TICK`: Advance time by 1 unit. Work on the current task or pick a new one.
*   `RUN_ALL`: Simulate until all tasks are completed or expired.
*   `REPORT`: Show completed tasks, expired tasks, and total value earned.

## Sample Execution

```text
> ADD_TASK T1 3 5 100   (Duration 3, Deadline 5, Value 100)
> ADD_TASK T2 2 4 80    (Duration 2, Deadline 4, Value 80)
> ADD_TASK T3 1 10 50   (Duration 1, Deadline 10, Value 50)

> RUN_ALL
Time 0: Picking task with earliest deadline...
- T2 (Deadline 4) selected. Processing (0/2).
Time 1: Processing T2 (1/2).
Time 2: T2 completed! Value earned: 80.
Time 2: Picking next... T1 (Deadline 5). Check: 2 + 3 = 5 <= 5. OK.
Time 3: Processing T1 (1/3).
Time 4: Processing T1 (2/3).
Time 5: T1 completed! Value earned: 100.
Time 5: Picking next... T3 (Deadline 10). 5 + 1 = 6 <= 10. OK.
Time 6: T3 completed! Value earned: 50.
All tasks processed.

> REPORT
Completed: T2, T1, T3. Total Value: 230.
Expired: None.
```
