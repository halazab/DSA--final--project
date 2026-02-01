#!/usr/bin/env python3
"""
Problem 55: The Bounded History Manager
Basic implementation with deque
"""

from collections import deque


class HistoryManager:
    """Bounded History Manager with fixed capacity"""
    
    def __init__(self):
        self.max_limit = 10
        self.history: deque = deque(maxlen=self.max_limit)
        self.dropped_count = 0
    
    def set_limit(self, n: int):
        """Set the history capacity limit"""
        if n <= 0:
            print("Error: Limit must be positive")
            return
        
        old_limit = self.max_limit
        self.max_limit = n
        
        # Create new deque with new maxlen
        new_history = deque(maxlen=n)
        
        # Keep the most recent n items
        for action in list(self.history)[-n:]:
            new_history.append(action)
        
        dropped = len(self.history) - len(new_history)
        self.history = new_history
        
        if dropped > 0:
            self.dropped_count += dropped
        
        print(f"History limit set to {n}")
    
    def add_action(self, name: str):
        """Add an action to history"""
        if not name:
            print("Error: Action name cannot be empty")
            return
        
        # Track if we're at capacity
        was_full = len(self.history) == self.max_limit
        oldest_dropped = None
        
        if was_full:
            oldest_dropped = self.history[0]
        
        self.history.append(name)
        
        # Format output
        if was_full and oldest_dropped:
            self.dropped_count += 1
            print(f"Full. Dropped {oldest_dropped}.")
        
        print(f"Action '{name}' added")
    
    def undo(self):
        """Undo the last action"""
        if not self.history:
            print("Nothing to undo")
            return
        
        action = self.history.pop()
        print(f"Reverted {action}.")
    
    def show_history(self):
        """Display the history"""
        print(f"\nHistory ({len(self.history)}/{self.max_limit}):")
        
        if not self.history:
            print("[Empty]")
        else:
            hist_list = list(self.history)
            print(f"Hist: {hist_list}")
        print()


def main():
    """Main interactive CLI"""
    manager = HistoryManager()
    print("Bounded History Manager")
    print("Commands: SET_LIMIT <n>, ACTION <name>, UNDO, SHOW_HISTORY, QUIT\n")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split(maxsplit=1)
            command = parts[0].upper()
            
            if command in ['QUIT', 'EXIT']:
                break
            
            elif command == 'SET_LIMIT':
                if len(parts) < 2:
                    print("Usage: SET_LIMIT <n>")
                else:
                    try:
                        n = int(parts[1])
                        manager.set_limit(n)
                    except ValueError:
                        print("Error: Limit must be an integer")
            
            elif command == 'ACTION':
                if len(parts) < 2:
                    print("Usage: ACTION <name>")
                else:
                    name = parts[1]
                    manager.add_action(name)
            
            elif command == 'UNDO':
                manager.undo()
            
            elif command == 'SHOW_HISTORY':
                manager.show_history()
            
            else:
                print(f"Unknown command: {command}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
