# Presentation: Data Structures & Algorithms in Action

---

## Introduction

This presentation covers three distinct problems, each solved using specific data structures and algorithms. The goal is to demonstrate a practical understanding of how to choose the right tools for the job based on system requirements like efficiency, priority, and memory constraints.

Each solution is implemented in Python and can be run as a standalone interactive command-line application.

---

## Problem 1: The Tiered Service Desk (`problem_23`)

### Problem Description

A customer support center needs to handle users from three different subscription tiers (Platinum, Gold, Silver). The system must prioritize higher-tiered users but ensure that lower-tiered users are not completely ignored.

### Core Data Structure: Array of Queues

*   **Structure**: A simple array `[q1, q2, q3]` where each element is a **Queue**.
*   **Reasoning**: This perfectly models the real-world scenario of having separate waiting lines for each tier. Queues enforce **First-In, First-Out (FIFO)**, which is a requirement for users within the same tier.

### Core Algorithm: Weighted Round Robin (WRR)

*   **Logic**: The system serves customers in a repeating cycle with a `3:2:1` ratio:
    1.  Process up to **3** Platinum customers.
    2.  Process up to **2** Gold customers.
    3.  Process **1** Silver customer.
*   **Implementation**: Counters track how many customers from each tier have been processed in the current cycle. If a tier's queue is empty or its quota is met, the algorithm moves to the next tier. The cycle resets when all quotas are met or all queues are empty.
*   **Benefit**: This algorithm provides a fair, predictable, and starvation-free way to handle prioritized tasks.

### Code Snippet (`process_next`)

```python
def _select_next_customer(self):
    # Try current tier in cycle order
    for attempt in range(3):
        tier_idx = self.current_cycle_tier
        
        # Check if this tier has quota remaining and customers waiting
        if (self.cycle_counters[tier_idx] < self.TIER_WEIGHTS[tier_idx] and 
            len(self.queues[tier_idx]) > 0):
            customer = self.queues[tier_idx].popleft()
            return customer, tier_idx, self.cycle_counters[tier_idx] + 1
        
        # Move to next tier in cycle
        self.current_cycle_tier = (self.current_cycle_tier + 1) % 3
```

---

## Problem 2: Deadline-Aware Task Executor (`problem_24`)

### Problem Description

A system needs to execute tasks that each have a specific duration, a deadline, and a value. The goal is to maximize the total value earned by completing tasks before their deadlines.

### Core Data Structure: Min-Heap

*   **Structure**: A **Min-Heap** (Priority Queue) where the priority of each task is its **deadline**.
*   **Reasoning**: A Min-Heap is extremely efficient (`O(log n)`) for always finding the item with the smallest value. This makes it perfect for an **Earliest Deadline First (EDF)** scheduling strategy.

### Core Algorithm: Earliest Deadline First (EDF)

*   **Logic**:
    1.  Always pick the task from the Min-Heap with the earliest deadline.
    2.  Before starting the task, perform a critical check: `current_time + task_duration <= task_deadline`.
    3.  If the check fails, the task is **expired** and discarded. Otherwise, it is executed.
*   **Implementation**: The main loop extracts the minimum element from the heap. A `current_time` variable is incremented to simulate the passage of time.
*   **Benefit**: EDF is an optimal scheduling algorithm for maximizing throughput when tasks have deadlines.

### Code Snippet (`_pick_next_task`)

```python
def _pick_next_task(self) -> Optional[Task]:
    """Pick next task from heap, discarding expired ones"""
    while self.task_heap:
        task = heapq.heappop(self.task_heap)
        
        if task.can_complete(self.current_time):
            self.current_task = task
            self.task_progress = 0
            return task
        else:
            self._expire_task(task)
    
    return None
```

---

## Problem 3: The Bounded History Manager (`problem_55`)

### Problem Description

An application needs an "undo" feature, but storing an infinite history of actions would consume too much memory. The history should be limited to a fixed capacity, `N`.

### Core Data Structure: Double-Ended Queue (Deque)

*   **Structure**: A **Deque** with its `maxlen` property set to the desired capacity `N`.
*   **Reasoning**: A deque is highly efficient (`O(1)`) for adding and removing items from *both ends*. When a deque with `maxlen` is full, it automatically discards the item from the opposite end, which is exactly the behavior required. A standard list or stack would be inefficient (`O(n)`) at removing the oldest element.

### Core Algorithm: FIFO Eviction with LIFO Access

*   **Logic**:
    1.  **Adding an Action**: `deque.append(action)` adds the new action to the right side (the "end"). If the deque is full, it automatically pushes the oldest item off the left side.
    2.  **Undo**: `deque.pop()` removes the most recent action from the right side.
*   **Implementation**: The `collections.deque(maxlen=N)` object handles almost all the complexity automatically.
*   **Benefit**: This provides a highly memory-efficient and performant solution for managing bounded histories.

### Code Snippet (Initialization and Add)

```python
from collections import deque

class HistoryManager:
    def __init__(self):
        self.max_limit = 10
        # The deque handles the capacity limit automatically
        self.history: deque = deque(maxlen=self.max_limit)

    def add_action(self, name: str):
        # When full, the deque automatically discards the oldest item
        self.history.append(name)
```

---

## Summary of Problems

| Feature | Problem 23 (Service Desk) | Problem 24 (Task Executor) | Problem 55 (History Manager) |
| :--- | :--- | :--- | :--- |
| **Goal** | Fairness & Prioritization | Maximize Value & Meet Deadlines| Memory Efficiency |
| **Core DS** | Array of Queues | Min-Heap | Deque with `maxlen` |
| **Algorithm** | Weighted Round Robin | Earliest Deadline First | FIFO Eviction |
| **Complexity**| O(1) | O(log n) | O(1) |

---

## Conclusion

These three problems highlight the importance of selecting the correct data structure.

*   For simple, ordered grouping, an **array of queues** is effective.
*   For priority-based selection, a **heap** is the optimal choice.
*   For managing a fixed-size, sequential collection, a **deque** provides the most elegant and efficient solution.

By analyzing the specific rules and constraints of a problem, we can build solutions that are not only correct but also performant and resource-efficient.
