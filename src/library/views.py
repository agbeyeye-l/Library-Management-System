import datetime
from django.http import response
from django.shortcuts import render
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView,RetrieveDestroyAPIView,
                                         ListAPIView, RetrieveAPIView, GenericAPIView)
from library.models import Author, BookItem, BookLending, BookReservation, Library, Rack
from library.serializers import (AuthorSerializer, BookSerializer, LendedBookSerializer, LendingSerializer, LibrarySerializer,
                                    RackSerializer, ReservationSerializer)
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
    
    def post(self,request,*args,**kwargs):
        """
        This method implements the reservation of a book by a user or librarian
        """
        barcode = request.data['barcode']
        library = request.data['library']
        memberId = request.data['user']
        # check if user is authenticated
        if not request.user.is_authenticated:
            return Response(APIResponses.Response.UNAUTHENTICATED, status= status.HTTP_401_UNAUTHORIZED)
        book = BookItem.objects.filter(barcode=barcode,library=library).first()
        if not book:
            return Response(APIResponses.Response.BOOK_NOT_FOUND_MESSAGE, status = status.HTTP_200_OK)
        # if book is referenced only
        if book.isReferenceOnly:
            return Response(APIResponses.Response.BOOK_IS_REFERENCED_ONLY_MESSAGE, status = status.HTTP_200_OK)
        # get user making reservation
        account = Account.objects.filter(user=memberId).first()
        if not account:
            return Response(APIResponses.Response.USER_DOES_EXIST, status = status.HTTP_404_NOT_FOUND)
        # check if there is existing reservation made on this book by user
        reservation = BookReservation.objects.filter(reservationStatus=schemes.ReservationStatus.WAITING,bookItem=book).first()
        if reservation:
            # if existing reservation is made by same member
            reservation_by_this_member = BookReservation.objects.filter( Q(reservationStatus=schemes.ReservationStatus.WAITING) | Q(reservationStatus=schemes.ReservationStatus.PENDING),bookItem=book, user=account).first()
            if reservation_by_this_member:
                return Response(APIResponses.Response.EXISTING_RESERVATION_BY_MEMBER, status = status.HTTP_200_OK)
        # if there is existing reservation set new reservation's status to pending else set to waiting
        reservation_status = schemes.ReservationStatus.PENDING if reservation else schemes.ReservationStatus.WAITING
        new_reservation = BookReservation.objects.create(user = account,bookItem=book, reservationStatus=reservation_status)
        new_reservation.save()
        serialized_data = ReservationSerializer(instance = new_reservation)
        return Response(serialized_data.data, status = status.HTTP_200_OK)

    def get(self,request,*args,**kwargs):
        """
        This method allows a user to retrieve a specific reservation details
        """
        # get input data
        barcode = request.data['barcode']
        library = request.data['library']
        user = request.data['user']
        # get book with given barcode
        book = BookItem.objects.filter(barcode=barcode,library=library).first()
        # check if book exist
        if not book:
            return Response(APIResponses.Response.BOOK_NOT_FOUND_MESSAGE, status = status.HTTP_200_OK)
        # get reservation for obtained book with input user
        reservation = BookReservation.objects.filter( bookItem=book, user=user, reservationStatus=schemes.ReservationStatus.WAITING).first()
        # if reservation is not made, return reservation not found message
        if not reservation:
            return Response(APIResponses.Response.RESERVATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        # return reservation details
        return Response(ReservationSerializer(instance=reservation).data, status=status.HTTP_200_OK)


    def delete(self,request,*args, **kwargs):
        """
        This method allows a user to cancel their reservation
        """
        reservation_id = request.data['id']
        # check existence of reservation
        reservation = BookReservation.objects.filter(pk=reservation_id).first()
        if not reservation:
            return Response(APIResponses.Response.RESERVATION_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
        # cancel reservation
        reservation.reservationStatus = schemes.ReservationStatus.CANCELLED
        reservation.save()
        return Response(APIResponses.Response.RESERVATION_CANCELLED_SUCCESSFULLY, status = status.HTTP_204_NO_CONTENT)




class ReservationListAPIView(ListAPIView):
    """
    This class implements a view for a librarian to view
    list of reservations by a user, a bookitem, creation date, or reservation status
    """
    queryset = BookReservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsLibrarianPermission]
    search_fields = ['user', 'bookItem', 'creationDate', 'reservationStatus']



class ReservationDetailAPIView(RetrieveDestroyAPIView):
    """
    This class implements a view for a librarian to view or
    cancel a book reservation
    """
    queryset = BookReservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsLibrarianPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.reservationStatus = schemes.ReservationStatus.CANCELLED
        instance.save()
        return Response(APIResponses.Response.RESERVATION_CANCELLED_SUCCESSFULLY,status=status.HTTP_204_NO_CONTENT)

        


        