from django.contrib import admin
from library.models import BookLending, BookReservation, BookItem, Library, Author, Rack


admin.site.register(BookItem)
admin.site.register(BookLending)
admin.site.register(BookReservation)
admin.site.register(Library)
admin.site.register(Author)
admin.site.register(Rack)
