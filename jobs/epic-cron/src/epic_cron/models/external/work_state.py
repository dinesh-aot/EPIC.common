"""Work State Enum - Defines valid work states for filtering."""

import enum


class WorkState(enum.Enum):
    """Enum for work states that should be excluded from proponent eligibility checks."""
    
    # Excluded states - works in these states don't count toward proponent eligibility
    COMPLETED = "COMPLETED"
    TERMINATED = "TERMINATED"
    CLOSED = "CLOSED"
    WITHDRAWN = "WITHDRAWN"
    
    @classmethod
    def excluded_states(cls):
        """Return list of work states that should be excluded from eligibility checks."""
        return [cls.COMPLETED.value, cls.TERMINATED.value, cls.CLOSED.value, cls.WITHDRAWN.value]
