#!/usr/bin/env python3
"""
Problem 23: The Tiered Service Desk
Basic implementation with Weighted Round Robin scheduling
"""

from collections import deque
from typing import List


class ServiceDesk:
    """Tiered Service Desk with Weighted Round Robin scheduling"""
    
    TIER_NAMES = ['Platinum', 'Gold', 'Silver']
    TIER_WEIGHTS = [3, 2, 1]  # WRR weights
    
    def __init__(self):
        # Array of 3 queues (one per tier)
        self.queues: List[deque] = [deque(), deque(), deque()]
        
        # Cycle counters for WRR algorithm
        self.cycle_counters = [0, 0, 0]
        self.current_cycle_tier = 0
    
    def _get_tier_index(self, tier: str) -> int:
        """Convert tier name to index"""
        tier_map = {'platinum': 0, 'gold': 1, 'silver': 2}
        return tier_map.get(tier.lower(), -1)
    
    def arrive(self, name: str, tier: str):
        """Add a customer to their tier queue"""
        tier_idx = self._get_tier_index(tier)
        
        if tier_idx == -1:
            print(f"Error: Invalid tier '{tier}'")
            return
        
        self.queues[tier_idx].append(name)
        print(f"{name} added to {self.TIER_NAMES[tier_idx]} queue")
    
    def process_next(self):
        """Process next customer using Weighted Round Robin"""
        customer, tier_idx, cycle_num = self._select_next_customer()
        
        if customer is None:
            print("No customers waiting")
            return
        
        # Increment cycle counter
        self.cycle_counters[tier_idx] += 1
        
        tier_name = self.TIER_NAMES[tier_idx]
        print(f"{customer} (Plat #{cycle_num})" if tier_idx == 0 
              else f"{customer} (Gold #{cycle_num})" if tier_idx == 1 
              else f"{customer} (Silver #{cycle_num})")
        
        # Check if we completed a cycle phase
        self._check_cycle_complete()
    
    def _select_next_customer(self):
        """Select next customer using WRR algorithm"""
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
        
        # Reset cycle and try again
        if self._any_queue_has_customers():
            self._reset_cycle()
            return self._select_next_customer()
        
        return None, -1, 0
    
    def _any_queue_has_customers(self) -> bool:
        """Check if any queue has waiting customers"""
        return any(len(q) > 0 for q in self.queues)
    
    def _check_cycle_complete(self) -> bool:
        """Check if current cycle is complete and reset if so"""
        all_quotas_met = all(
            self.cycle_counters[i] >= self.TIER_WEIGHTS[i] or len(self.queues[i]) == 0
            for i in range(3)
        )
        
        if all_quotas_met and self._any_queue_has_customers():
            self._reset_cycle()
            return True
        return False
    
    def _reset_cycle(self):
        """Reset cycle counters"""
        self.cycle_counters = [0, 0, 0]
        self.current_cycle_tier = 0
    
    def show_status(self):
        """Display current queue status"""
        print("\n=== Queue Status ===")
        for i, tier_name in enumerate(self.TIER_NAMES):
            queue = self.queues[i]
            if len(queue) == 0:
                print(f"{tier_name}: [Empty]")
            else:
                customers = list(queue)
                print(f"{tier_name}: {customers}")
        print()


def main():
    """Main interactive CLI"""
    desk = ServiceDesk()
    print("Tiered Service Desk System")
    print("Commands: ARRIVE <name> <tier>, PROCESS_NEXT, STATUS, QUIT\n")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split()
            command = parts[0].upper()
            
            if command in ['QUIT', 'EXIT']:
                break
            
            elif command == 'ARRIVE':
                if len(parts) < 3:
                    print("Usage: ARRIVE <name> <tier>")
                else:
                    name = parts[1]
                    tier = parts[2]
                    desk.arrive(name, tier)
            
            elif command == 'PROCESS_NEXT':
                desk.process_next()
            
            elif command == 'STATUS':
                desk.show_status()
            
            else:
                print(f"Unknown command: {command}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
