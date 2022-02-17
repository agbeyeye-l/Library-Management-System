from dbm.ndbm import library
from django.db import models
from django.forms import CharField
from identity_manager.models import Account


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
        return self.name

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
    price = models.DecimalField(decimal_places=2)
    status = models.CharField(max_length=100)
    format = models.CharField(max_length=100)
    datePurchase = models.DateField()
    rack = models.ForeignKey(Rack, on_delete= models.CASCADE)
    library = models.ForeignKey(Library, on_delete=models.CASCADE)


    def __str__(self):
        return self.title


class BookReservation(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    bookItem = models.ForeignKey(BookItem, on_delete=models.CASCADE)
    creationDate =  models.DateField(auto_now_add=True)
    reservationStatus = models.CharField(max_length=100)

    def __str__(self):
        return self.bookItem.title

    def getReservationStatus(self):
        return self.reservationStatus


class BookLending(models.Model):
    creationDate = models.DateField(auto_now_add=True)
    dueDate = models.DateField()
    returnedDate = models.DateField()

    def getReturnedDate(self):
        return self.returnedDate
