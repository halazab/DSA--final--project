# DSA Solutions

**Three Python implementations of data structure problems**

---

## Problems Included

### 1. Problem 23: Tiered Service Desk
**File:** `problem_23_service_desk.py`

A customer support system using **Weighted Round Robin (WRR)** scheduling with three priority tiers.

**Data Structure:** Array of 3 queues (Platinum, Gold, Silver)  
**Algorithm:** WRR (3:2:1 ratio), FIFO within each tier

**Commands:**
- `ARRIVE <name> <tier>` - Add customer to queue
- `PROCESS_NEXT` - Serve next customer using WRR
- `STATUS` - Show all queues
- `QUIT` - Exit

---

### 2. Problem 24: Deadline-Aware Task Executor
**File:** `problem_24_task_executor.py`

A task scheduling system using **Earliest Deadline First (EDF)** algorithm.

**Data Structure:** Min-Heap (priority queue by deadline)  
**Algorithm:** EDF with expiration detection

**Commands:**
- `ADD_TASK <id> <duration> <deadline> <value>` - Add task
- `TICK` - Advance time by 1 unit
- `RUN_ALL` - Simulate until completion
- `REPORT` - Show final report
- `QUIT` - Exit

---

### 3. Problem 55: Bounded History Manager
**File:** `problem_55_history_manager.py`

A memory-efficient undo system using a **Deque** with fixed capacity.

**Data Structure:** Double-ended queue (deque) with maxlen  
**Algorithm:** FIFO eviction when at capacity

**Commands:**
- `SET_LIMIT <n>` - Set max capacity
- `ACTION <name>` - Add action
- `UNDO` - Undo last action
- `SHOW_HISTORY` - Display history
- `QUIT` - Exit

---

## Installation

**Requirements:** Python 3.6 or higher

No external packages needed - all programs use Python standard library only.

```bash
# Optional: Verify Python version
python3 --version

# No pip install needed - standard library only!
```

See `requirements.txt` for details.

---

## Running the Programs

```bash
# Problem 23: Service Desk
python3 problem_23_service_desk.py

# Problem 24: Task Executor
python3 problem_24_task_executor.py

# Problem 55: History Manager
python3 problem_55_history_manager.py
```

---

## Requirements

- **Python 3.6+**
- **Standard Library Only** (no external packages)
  - `collections.deque`
  - `heapq`
  - `dataclasses`

---

## Example Usage

### Problem 23: Service Desk
```
> ARRIVE Alice Platinum
Alice added to Platinum queue
> ARRIVE Bob Gold
Bob added to Gold queue
> STATUS
=== Queue Status ===
Platinum: ['Alice']
Gold: ['Bob']
Silver: [Empty]
```

### Problem 24: Task Executor
```
> ADD_TASK T1 3 5 100
Task T1 added (Duration: 3, Deadline: 5, Value: 100)
> RUN_ALL
=== Running all tasks ===
Time 0: Picking task with earliest deadline...
- T1 (Deadline 5) selected. Processing (0/3).
...
All tasks processed.
> REPORT
=== REPORT ===
Completed: T1. Total Value: 100.
Expired: None.
```

### Problem 55: History Manager
```
> SET_LIMIT 3
History limit set to 3
> ACTION A
Action 'A' added
> ACTION B
Action 'B' added
> SHOW_HISTORY
History (2/3):
Hist: ['A', 'B']
```

---

## Data Structures & Algorithms

| Problem | Data Structure | Algorithm | Complexity |
|---------|---------------|-----------|------------|
| 23 | Array of Queues | Weighted Round Robin | O(1) per operation |
| 24 | Min-Heap | Earliest Deadline First | O(log n) insert/extract |
| 55 | Deque | FIFO with capacity limit | O(1) per operation |

---

## License

Educational use only.
