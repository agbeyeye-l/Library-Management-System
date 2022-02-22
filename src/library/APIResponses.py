
class Response:
    UNAUTHENTICATED = "Unauthorized, please login to continue"
    BOOK_TRESHOLD_MESSAGE = "You have borrowed maximum number of books. Please return some of the previously borrowed books"
    BOOK_NOT_FOUND_MESSAGE = "Book with this barcode cannot be found in the system"
    BOOK_IS_REFERENCED_ONLY_MESSAGE = "Sorry, this book cannot be given out at the moment"
    BOOK_UNVAILABLE_MESSAGE = "Sorry, this book is currently unvailable, you may go ahead and make a reservation"
    RESERVATION_NOT_FOUND= "Sorry, no such reservation could be found"
    RESERVATION_CANCELLED_SUCCESSFULLY = "Reservation has been cancelled successfully"
    EXISTING_RESERVATION_BY_MEMBER = "There is an existing reservation made on this book by this user. To make a new reservation, kindly cancel the previous reservation made on this book"
    USER_DOES_EXIST = "This user does not exist"