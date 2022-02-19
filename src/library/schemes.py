
class BookFormat:
    HARDCOVER = "Hardcover"
    PAPERBACK = "Paperback"
    AUDIOBOOK = "Audiobook"
    NEWSPAPER = "Newspaper"
    MAGAZINE = "Magazine"
    JOURNAL = "Journal"


class BookStatus:
    AVAILABLE = "Available"
    RESERVED = "Reserved"
    LOANED = "Loaned"
    LOST = "Lost"


class ReservationStatus:
    WAITING = "Waiting"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    PENDING = "Pending"
    NONE = "None"

class AccountStatus:
    ACTIVE = "Active"
    CANCELLED = "Cancelled"
    BLACKLISTED = "Blacklisted"
    CLOSED = "Closed"
    