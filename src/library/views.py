from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, RetrieveAPIView
from library.models import Author, BookItem, BookLending, BookReservation, Library, Rack
from library.serializers import AuthorSerializer, BookSerializer, LibrarySerializer,RackSerializer
from identity_manager.permissions import IsLibrarianPermission, IsAdminPermission


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

class ViewBooksAPIView(RetrieveAPIView):
    """
    This class encapsulates the retrieval of a single bookitem in a library
    by a member
    """
    queryset = BookItem.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 