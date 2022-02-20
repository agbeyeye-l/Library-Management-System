import datetime
from django.http import response
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,
                                         ListAPIView, RetrieveAPIView, GenericAPIView)
from library.models import Author, BookItem, BookLending, BookReservation, Library, Rack
from library.serializers import (AuthorSerializer, BookSerializer, LendedBookSerializer, LendingSerializer, LibrarySerializer,
                                    RackSerializer)
from identity_manager.permissions import IsLibrarianPermission, IsAdminPermission
from library import APIResponses 
from identity_manager.models import Account
from library import constants, schemes



class AuthorAPIView(ListCreateAPIView):
    """
    This class creates and retrieves the list of authors
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated,IsLibrarianPermission]


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    """
    This class encapsulates the retrieval, update, and deletion of authors
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated,IsLibrarianPermission]


class LibraryAPIView(ListCreateAPIView):
    """
    This class creates and retrieves the list of libraries in the system
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated,IsAdminPermission] 


class LibraryDetailView(RetrieveUpdateDestroyAPIView):
    """
    This class encapsulates the retrieval, update, and deletion of a library in the system
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated,IsAdminPermission] 


class RackAPIView(ListCreateAPIView):
    """
    This class creates and retrieves the list of racks in a library
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    permission_classes = [IsAuthenticated,IsLibrarianPermission] 


class RackDetailView(RetrieveUpdateDestroyAPIView):
    """
    This class encapsulates the retrieval, update, and deletion of a racl in a library
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    permission_classes = [IsAuthenticated,IsLibrarianPermission] 


class BookItemAPIView(ListCreateAPIView):
    """
    This class creates and retrieves the list of bookitems in a library
    """
    queryset = BookItem.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated,IsLibrarianPermission]


class BookItemDetailView(RetrieveUpdateDestroyAPIView):
    """
    This class encapsulates the retrieval, update, and deletion of a bookitem in a library
    """
    queryset = BookItem.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated,IsLibrarianPermission] 



class ViewBooksAPIView(ListAPIView):
    """
    This class encapsulates the retrieval of a list of bookitems in a library
    by a member
    """
    queryset = BookItem.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]



class ViewBookDetailAPIView(RetrieveAPIView):
    """
    This class encapsulates the retrieval of a single bookitem in a library
    by a member
    """
    queryset = BookItem.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 


class LendBookAPIView(GenericAPIView):
    """
    This class implements reserving a book
    """
    def post(self,request,*args, **kwargs):
        barcode = request.data['barcode']
        library = request.data['library']
        if request.user.is_authenticated:
            account = Account.objects.get(user=request.user.id)
            if account:
                num_of_borrowed_books = account.heldBooks()
                if num_of_borrowed_books >= constants.MAX_HOLDING_BOOKS:
                    return Response(APIResponses.Response.BOOK_TRESHOLD_MESSAGE, status = status.HTTP_200_OK)
                book = BookItem.objects.filter(barcode=barcode,library=library).first()
                if not book:
                    return Response(APIResponses.Response.BOOK_NOT_FOUND_MESSAGE, status = status.HTTP_200_OK)
                # if book is referenced only
                if book.isReferenceOnly:
                    return Response(APIResponses.Response.BOOK_IS_REFERENCED_ONLY_MESSAGE, status = status.HTTP_200_OK)
                reservation = BookReservation.objects.filter(user=account, bookItem=book, reservationStatus=schemes.ReservationStatus.WAITING).first()
                # if book is available or reservation is made
                if book.isLendable() or reservation:
                    # save book lend details
                    dueDate = datetime.datetime.now()+datetime.timedelta(days=constants.BOOK_LEND_DURATION)
                    lendBook = BookLending.objects.create(user= account,book=book,dueDate=dueDate, returnedDate= datetime.datetime.now())
                    lendBook.save()
                    #update the book status to loaned
                    book.updateBookAfterLend()
                    # update member reservation from waiting to completed
                    if reservation:
                        reservation.completed() 
                    # book lend information to return to client
                    book_serializer = LendedBookSerializer(instance=lendBook)
                    return Response(book_serializer.data, status = status.HTTP_200_OK)
                # inform user to make reservation if book is unvailable
                return Response(APIResponses.Response.BOOK_UNVAILABLE_MESSAGE, status = status.HTTP_200_OK)
                
        return Response(APIResponses.Response.UNAUTHENTICATED, status= status.HTTP_401_UNAUTHORIZED)



class ReserveBookAPIView(GenericAPIView):
    """
    This class implements reserving a book
    """
    def post(self,request,*args,**kwargs):
        barcode = request.data['barcode']
        library = request.data['library']
        if not request.user.is_authenticated:
            return Response(APIResponses.Response.UNAUTHENTICATED, status= status.HTTP_401_UNAUTHORIZED)
        book = BookItem.objects.filter(barcode=barcode,library=library).first()
        if not book:
            return Response(APIResponses.Response.BOOK_NOT_FOUND_MESSAGE, status = status.HTTP_200_OK)
        # if book is referenced only
        if book.isReferenceOnly:
            return Response(APIResponses.Response.BOOK_IS_REFERENCED_ONLY_MESSAGE, status = status.HTTP_200_OK)
        account = Account.objects.filter(user=request.user.id).first()
        reservation = BookReservation.objects.filter( bookItem=book, reservationStatus=schemes.ReservationStatus.WAITING).first()
        reservation_status = schemes.ReservationStatus.PENDING if reservation else schemes.ReservationStatus.WAITING
        new_reservation = BookReservation.objects.create(user = account,bookItem=book, reservationStatus=reservation_status)
        new_reservation.save()

        