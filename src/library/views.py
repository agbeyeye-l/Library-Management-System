from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from library.models import Author, BookItem, BookLending, BookReservation, Library, Rack
from library.serializers import AuthorSerializer, BookSerializer, LibrarySerializer,RackSerializer
from identity_manager.permissions import IsAuthorized


class AuthorAPIView(ListCreateAPIView):
    """
    This class creates and retrieves the list of authors
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated,IsAuthorized]


class AuthorDetailView(RetrieveUpdateDestroyAPIView):
    """
    This class encapsulates the retrieval, update, and deletion of authors
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated,IsAuthorized]


class LibraryAPIView(ListCreateAPIView):
    """
    This class creates and retrieves the list of libraries in the system
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated,IsAuthorized] 


class LibraryDetailView(RetrieveUpdateDestroyAPIView):
    """
    This class encapsulates the retrieval, update, and deletion of a library in the system
    """
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    permission_classes = [IsAuthenticated,IsAuthorized] 


class RackAPIView(ListCreateAPIView):
    """
    This class creates and retrieves the list of racks in a library
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    permission_classes = [IsAuthenticated,IsAuthorized] 


class RackDetailView(RetrieveUpdateDestroyAPIView):
    """
    This class encapsulates the retrieval, update, and deletion of a racl in a library
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    permission_classes = [IsAuthenticated,IsAuthorized] 


class BookItemAPIView(ListCreateAPIView):
    """
    This class creates and retrieves the list of bookitems in a library
    """
    queryset = BookItem.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookItemDetailView(RetrieveUpdateDestroyAPIView):
    """
    This class encapsulates the retrieval, update, and deletion of a bookitem in a library
    """
    queryset = BookItem.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated,IsAuthorized] 