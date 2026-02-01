# Problem 23: The Tiered Service Desk

## Problem Description
A customer support center handles users with different subscription levels. The goal is to prioritize higher tiers while ensuring lower tiers don't starve completely.

### The System Rules
1.  **Tiers**:
    *   **Platinum**: Highest priority.
    *   **Gold**: Medium.
    *   **Silver**: Low.
2.  **Weighted Round Robin Algorithm**:
    *   In every cycle of service, the agent processes:
    *   Up to **3** Platinum customers.
    *   Then up to **2** Gold customers.
    *   Then **1** Silver customer.
    *   Repeat.
3.  **Strict Ordering**: Inside a tier, it's strictly FIFO.

## Must Use Data Structures
*   **Array of Queues**: `queues[0]`=Platinum, `queues[1]`=Gold, etc.
*   **Counters**: To track processed count in current cycle.

## Operations to Implement (CLI Commands)
*   `ARRIVE <user> <tier>`
*   `PROCESS_NEXT`: Pick one user based on WRR logic.
*   `STATUS`: Show queues.

## Sample Execution

```text
> ARRIVE A Platinum
> ARRIVE B Platinum
> ARRIVE C Platinum
> ARRIVE D Platinum
> ARRIVE E Gold
> ARRIVE F Silver

> PROCESS_NEXT
A (Plat #1)
> PROCESS_NEXT
B (Plat #2)
> PROCESS_NEXT
C (Plat #3)
> PROCESS_NEXT
E (Gold #1 - Switched tier because Plat quota 3 met)
> PROCESS_NEXT
F (Silver #1? No, wait, Gold quota is 2. But Gold empty? Yes -> Silver)
F (Silver #1)
> PROCESS_NEXT
D (Back to Plat #1)
```
