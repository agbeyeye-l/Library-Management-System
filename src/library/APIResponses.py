
class Response:
    UNAUTHENTICATED = "Unauthorized, please login to continue"
    BOOK_TRESHOLD_MESSAGE = "You have borrowed maximum number of books. Please return some of the previously borrowed books"
    BOOK_NOT_FOUND_MESSAGE = "Book with this barcode cannot be found in the system"
    BOOK_IS_REFERENCED_ONLY_MESSAGE = "Sorry, this book cannot be given out at the moment"
    BOOK_UNVAILABLE_MESSAGE = "Sorry, this book is currently unvailable, you may go ahead and make a reservation"