#!/usr/bin/env python3
"""
Problem 24: Deadline-Aware Task Executor
Basic implementation with EDF scheduling
"""

import heapq
from typing import List, Optional
from dataclasses import dataclass, field


@dataclass(order=True)
class Task:
    """Represents a task with deadline and value"""
    deadline: int = field(compare=True)
    task_id: str = field(compare=False)
    duration: int = field(compare=False)
    value: int = field(compare=False)
    
    def can_complete(self, current_time: int) -> bool:
        """Check if task can be completed before deadline"""
        return current_time + self.duration <= self.deadline


class TaskExecutor:
    """Deadline-Aware Task Executor using EDF scheduling"""
    
    def __init__(self):
        self.task_heap: List[Task] = []
        self.current_task: Optional[Task] = None
        self.task_progress: int = 0
        self.current_time: int = 0
        
        self.completed: List[Task] = []
        self.expired: List[Task] = []
        self.total_value_earned: int = 0
    
    def add_task(self, task_id: str, duration: int, deadline: int, value: int):
        """Add a new task to the heap"""
        task = Task(
            task_id=task_id,
            duration=duration,
            deadline=deadline,
            value=value
        )
        
        heapq.heappush(self.task_heap, task)
        print(f"Task {task_id} added (Duration: {duration}, Deadline: {deadline}, Value: {value})")
    
    def tick(self):
        """Advance time by 1 unit and process current task or pick new one"""
        print(f"\nTime {self.current_time}:", end=" ")
        
        # If we have a current task, work on it
        if self.current_task:
            self.task_progress += 1
            
            if self.task_progress >= self.current_task.duration:
                # Task completed!
                self._complete_task()
                print(f"{self.current_task.task_id} completed! Value earned: {self.current_task.value}.")
                self.current_task = None
                self.task_progress = 0
            else:
                # Still working
                print(f"Processing {self.current_task.task_id} ({self.task_progress}/{self.current_task.duration}).")
        
        # Advance time
        self.current_time += 1
        
        # If no current task, pick next one
        if not self.current_task:
            next_task = self._pick_next_task()
            if next_task:
                print(f"Time {self.current_time}: Picking task with earliest deadline...")
                print(f"- {next_task.task_id} (Deadline {next_task.deadline}) selected. Processing (0/{next_task.duration}).")
    
    def run_all(self):
        """Simulate until all tasks are completed or expired"""
        print("\n=== Running all tasks ===\n")
        
        iterations = 0
        max_iterations = 10000
        
        while (self.task_heap or self.current_task) and iterations < max_iterations:
            self.tick()
            iterations += 1
        
        print("\nAll tasks processed.\n")
    
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
    
    def _complete_task(self):
        """Mark current task as completed"""
        if self.current_task:
            self.completed.append(self.current_task)
            self.total_value_earned += self.current_task.value
    
    def _expire_task(self, task: Task):
        """Mark a task as expired"""
        self.expired.append(task)
        print(f"Time {self.current_time}: Task {task.task_id} expired (can't finish by deadline {task.deadline}).")
    
    def show_report(self):
        """Generate report"""
        print("\n=== REPORT ===")
        
        if self.completed:
            completed_ids = ", ".join([t.task_id for t in self.completed])
            print(f"Completed: {completed_ids}. Total Value: {self.total_value_earned}.")
        else:
            print("Completed: None.")
        
        if self.expired:
            expired_ids = ", ".join([t.task_id for t in self.expired])
            print(f"Expired: {expired_ids}.")
        else:
            print("Expired: None.")
        print()


def main():
    """Main interactive CLI"""
    executor = TaskExecutor()
    print("Deadline-Aware Task Executor")
    print("Commands: ADD_TASK <id> <duration> <deadline> <value>, TICK, RUN_ALL, REPORT, QUIT\n")
    
    while True:
        try:
            user_input = input("> ").strip()
            
            if not user_input:
                continue
            
            parts = user_input.split()
            command = parts[0].upper()
            
            if command in ['QUIT', 'EXIT']:
                break
            
            elif command == 'ADD_TASK':
                if len(parts) < 5:
                    print("Usage: ADD_TASK <id> <duration> <deadline> <value>")
                else:
                    try:
                        task_id = parts[1]
                        duration = int(parts[2])
                        deadline = int(parts[3])
                        value = int(parts[4])
                        executor.add_task(task_id, duration, deadline, value)
                    except ValueError:
                        print("Error: Duration, deadline, and value must be integers")
            
            elif command == 'TICK':
                executor.tick()
            
            elif command == 'RUN_ALL':
                executor.run_all()
            
            elif command == 'REPORT':
                executor.show_report()
            
            else:
                print(f"Unknown command: {command}")
        
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
