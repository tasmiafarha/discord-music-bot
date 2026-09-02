"""Music queue management for the Discord bot."""

from collections import deque


class MusicQueue:
    """A queue for managing music songs."""

    def __init__(self, max_size=100):
        """Initialize the music queue.

        Args:
            max_size: Maximum number of songs in queue
        """
        self.queue = deque(maxlen=max_size)
        self.max_size = max_size

    def add(self, song):
        """Add a song to the queue.

        Args:
            song: Dictionary containing song information

        Returns:
            True if added, False if queue is full
        """
        if len(self.queue) >= self.max_size:
            return False
        self.queue.append(song)
        return True

    def get_next(self):
        """Get the next song from the queue.

        Returns:
            Song dictionary or None if queue is empty
        """
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self):
        """Check if the queue is empty.

        Returns:
            True if queue is empty, False otherwise
        """
        return len(self.queue) == 0

    def clear(self):
        """Clear all songs from the queue."""
        self.queue.clear()

    def size(self):
        """Get the current queue size.

        Returns:
            Number of songs in queue
        """
        return len(self.queue)

    def peek(self):
        """Peek at the next song without removing it.

        Returns:
            Next song dictionary or None if queue is empty
        """
        if self.queue:
            return self.queue[0]
        return None
