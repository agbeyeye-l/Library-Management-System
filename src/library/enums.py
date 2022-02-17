from enums import Enum

class BookFormat(Enum):
    HARDCOVER = "Hardcover"
    PAPERBACK = "Paperback"
    AUDIOBOOK = "Audiobook"
    NEWSPAPER = "Newspaper"
    MAGAZINE = "Magazine"
    JOURNAL = "Journal"


class BookStatus(Enum):
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    LOANED = "Loaned"
    LOST = "Lost"


class ReservationStatus(Enum):
    WAITING = "Waiting"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    PENDING = "Pending"
    NONE = "None"

class AccountStatus(Enum):
    ACTIVE = "Active"
    CANCELLED = "Cancelled"
    BLACKLISTED = "Blacklisted"
    CLOSED = "Closed"
    