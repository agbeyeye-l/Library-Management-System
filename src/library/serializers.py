from django.template import Library
from rest_framework import serializers
from library.models import Author, BookItem, BookLending, BookReservation, Library, Rack



# serializer for library
class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'



# serializer class for racks
class RackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rack
        fields = '__all__'



# serializer class for Author
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'



# serializer class for bookitem
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = '__all__'


# serializer class for book reservation
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReservation
        fields = '__all__'



# serializer class for book lending
class LendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookLending
        fields = '__all__'


# serializer class for bookitem
class BookItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookItem
        fields = ['title','subject','publisher','author','barcode','format']


# serializer class for successful book lending
class LendedBookSerializer(serializers.ModelSerializer):
    book = BookItemSerializer()
    class Meta:
        model = BookLending
        fields = ['dueDate','book']