import sys
from collections import deque

class SongNode:
    def __init__(self, song_id, artist, title):
        self.id = song_id
        self.artist = artist
        self.title = title
        self.next = None
        self.prev = None
        self.priority = False  # To ignore spacing rule on NEXT

    def __str__(self):
        return f"{self.id} ({self.artist})"

class PlaylistManager:
    def __init__(self):
        self.head = None
        self.cursor = None
        self.history = []  # Stack for PREV
        self.k = 0
        self.cooldown_deque = deque()  # Sliding window of last K artists
        self.cooldown_map = {}  # Artist frequency map for cooldown efficiency

    def set_restriction_k(self, k):
        self.k = k
        # Clear cooldown when K is set? 
        # The sample shows K being set BEFORE the first PLAY.
        # Let's keep existing cooldown for now.
        pass

    def add_song(self, song_id, artist, title):
        new_node = SongNode(song_id, artist, title)
        if not self.head:
            self.head = new_node
            self.head.next = self.head
            self.head.prev = self.head
            self.cursor = self.head
        else:
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

    def add_next(self, song_id):
        target_node = self._find_song_by_id(song_id)
        if not target_node or not self.cursor:
            return

        if target_node == self.cursor:
            return

        # Set priority to ignore spacing rule
        target_node.priority = True

        # Remove from current position
        target_node.prev.next = target_node.next
        target_node.next.prev = target_node.prev
        
        if target_node == self.head:
            self.head = target_node.next

        # Insert after cursor
        next_node = self.cursor.next
        self.cursor.next = target_node
        target_node.prev = self.cursor
        target_node.next = next_node
        next_node.prev = target_node

    def _find_song_by_id(self, song_id):
        if not self.head:
            return None
        curr = self.head
        while True:
            if curr.id == song_id:
                return curr
            curr = curr.next
            if curr == self.head:
                break
        return None

    def _is_artist_on_cooldown(self, artist):
        return self.cooldown_map.get(artist, 0) > 0

    def _update_cooldown(self, artist):
        expired_artist = None
        # Add new artist to cooldown
        self.cooldown_deque.append(artist)
        self.cooldown_map[artist] = self.cooldown_map.get(artist, 0) + 1
        
        # If deque exceeds K, remove the oldest
        if len(self.cooldown_deque) > self.k:
            expired_artist = self.cooldown_deque.popleft()
            self.cooldown_map[expired_artist] -= 1
            if self.cooldown_map[expired_artist] == 0:
                del self.cooldown_map[expired_artist]
        
        return expired_artist

    def play(self):
        if not self.cursor:
            return

        self.history.append(self.cursor)
        expired = self._update_cooldown(self.cursor.artist)
        
        cooldown_str = ", ".join(list(self.cooldown_deque))
        expired_str = f" ({expired} expired)" if expired else ""
        print(f"Playing: {self.cursor.id} ({self.cursor.artist}). Cooldown: [{cooldown_str}].{expired_str}")
        
        # Reset priority flag after playing
        self.cursor.priority = False

    def next_song(self):
        if not self.cursor:
            return

        candidate = self.cursor.next
        start_node = self.cursor
        
        while candidate != start_node:
            print(f"(Natural next is {candidate.id} {candidate.artist}... Valid? ", end="")
            
            # User intent overrides spacing rule
            if candidate.priority:
                print("Yes - Priority)")
                self.cursor = candidate
                self.play()
                return
                
            if self._is_artist_on_cooldown(candidate.artist):
                print(f"NO! Recent {candidate.artist}. Skipping {candidate.id}...)")
                candidate = candidate.next
            else:
                print("Yes)")
                self.cursor = candidate
                self.play()
                return
        
        # Fallback
        self.cursor = self.cursor.next
        self.play()

    def prev_song(self):
        if len(self.history) < 2:
            return

        # The current song is what we just pushed in play()
        self.history.pop()  # Remove current
        prev_node = self.history[-1] # Peak previous
        
        self.cursor = prev_node
        print(f"Playing: {self.cursor.id} ({self.cursor.artist}) - Restored from History.")

def main():
    manager = PlaylistManager()
    
    print("=== Smart-Shuffle Streaming Engine CLI ===")
    print("Type 'HELP' to see available commands or 'EXIT' to quit.")
    
    while True:
        try:
            # Use 'playlist > ' as a prompt for interactive use
            sys.stdout.write("playlist > ")
            sys.stdout.flush()
            
            line = sys.stdin.readline()
            if not line:
                break
            
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            # Allow copy-pasting lines with '> ' prefix from documentation
            if line.startswith("> "):
                line = line[2:]
            
            cmd_parts = line.split()
            cmd = cmd_parts[0].upper()
            
            if cmd == "ADD_SONG":
                if len(cmd_parts) >= 4:
                    s_id = cmd_parts[1]
                    artist = cmd_parts[2]
                    title = " ".join(cmd_parts[3:])
                    manager.add_song(s_id, artist, title)
                    print(f"Added: {title} by {artist} ({s_id})")
                else:
                    print("Usage: ADD_SONG <id> <artist> <title>")
            elif cmd == "PLAY":
                manager.play()
            elif cmd == "NEXT":
                manager.next_song()
            elif cmd == "PREV":
                manager.prev_song()
            elif cmd == "ADD_NEXT":
                if len(cmd_parts) >= 2:
                    manager.add_next(cmd_parts[1])
                    node = manager._find_song_by_id(cmd_parts[1])
                    if node:
                        print(f"Queued Next: {node.title} by {node.artist}")
                    else:
                        print(f"Error: Song {cmd_parts[1]} not found.")
                else:
                    print("Usage: ADD_NEXT <id>")
            elif cmd == "SET_RESTRICTION_K":
                if len(cmd_parts) >= 2:
                    k = int(cmd_parts[1])
                    manager.set_restriction_k(k)
                    print(f"Restriction K set to {k}")
                else:
                    print("Usage: SET_RESTRICTION_K <k>")
            elif cmd == "HELP":
                print("\nAvailable Commands:")
                print("  ADD_SONG <id> <artist> <title> - Add a new song to the playlist")
                print("  PLAY                           - Play the current song")
                print("  NEXT                           - Play the next valid song (respecting K)")
                print("  PREV                           - Go back to the previous played song")
                print("  ADD_NEXT <id>                  - Force a specific song to play next")
                print("  SET_RESTRICTION_K <k>          - Set artist repetition gap")
                print("  EXIT                           - Close the program\n")
            elif cmd == "EXIT" or cmd == "QUIT":
                print("Goodbye!")
                break
            else:
                print(f"Unknown command: {cmd}. Type 'HELP' for assistance.")
        except ValueError:
            print("Error: Invalid numeric value provided.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
