
from django.db import models
from django.forms import CharField
from identity_manager.models import Account
from library.schemes import BookStatus, ReservationStatus, LendingStatus
import datetime 
from library import constants


# the author of a book
class Author(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def getName(self):
        return self.name

    def __str__(self):
        return self.name


class Library(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name


class Rack(models.Model):
    number = models.IntegerField(primary_key=True)
    locationIdentifier = models.CharField(max_length=150)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.number)

class BookItem(models.Model):
    CHOICES = (
        ("English", "English"),
        ("French","French"),
        ("German","German"),
        ("Spanish","Spanish"),
    )
    ISBN = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    publisher = models.CharField(max_length=200)
    language = models.CharField(max_length=200, choices=CHOICES)
    numOfPages = models.IntegerField()
    barcode = models.CharField(max_length=500)
    isReferenceOnly = models.BooleanField(default=False)
    borrowed = models.DateField()
    dueDate = models.DateField()
    price = models.DecimalField(decimal_places=2, max_digits=4)
    status = models.CharField(max_length=100, default=BookStatus.AVAILABLE)
    format = models.CharField(max_length=100)
    datePurchase = models.DateField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    rack = models.ForeignKey(Rack, on_delete= models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)


    def __str__(self):
        return str(self.title)

    def isLendable(self):
        return self.status == BookStatus.AVAILABLE

    def updateBookAfterLend(self):
        today = datetime.datetime.now()
        self.status = BookStatus.LOANED
        self.borrowed = today
        self.dueDate = today + datetime.timedelta(days=constants.BOOK_LEND_DURATION)
        self.save()
        return

    def returnBook(self):
        self.status = BookStatus.AVAILABLE
        self.save()

    def reserveBook(self):
        pass


class BookReservation(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    bookItem = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    creationDate =  models.DateTimeField(auto_now_add=True)
    reservationStatus = models.CharField(max_length=100,default=ReservationStatus.WAITING)

    def __str__(self):
        return self.bookItem.title

    def getReservationStatus(self):
        return self.reservationStatus

    def completed(self):
        self.reservationStatus = ReservationStatus.COMPLETED
        self.save()


    def hasReservation(self,user):
        return True if (self.user == user and self.reservationStatus == ReservationStatus.COMPLETED) else False

      

class BookLending(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    book = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    dueDate = models.DateTimeField()
    returnedDate = models.DateTimeField()
    status = models.CharField(max_length=50,default=LendingStatus.HOLDING)

    def getReturnedDate(self):
        return str(self.returnedDate)

    def returnedBook(self):
        self.status = LendingStatus.RELEASE
        self.save()

    def __str__(self):
        return self.book.title

