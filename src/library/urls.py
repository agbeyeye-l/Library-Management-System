from django.urls import path
from library.views import (BookItemDetailView, LibraryAPIView, 
                        LibraryDetailView, AuthorAPIView, AuthorDetailView, 
                        RackAPIView, BookItemAPIView, RackDetailView,ViewBooksAPIView,
                        ViewBookDetailAPIView,LendBookAPIView, ReserveBookAPIView,ReservationListAPIView)

urlpatterns = [
    path('libs/',LibraryAPIView.as_view(), name='libs'),
    path('lib-detail/<int:pk>',LibraryDetailView.as_view(), name='lib-detail'),
    path('author/',AuthorAPIView.as_view(), name='author'),
    path('author-detail/<int:pk>',AuthorDetailView.as_view(), name='author-detail'),
    path('rack/',RackAPIView.as_view(), name='rack'),
    path('rack-detail/<int:pk>',RackDetailView.as_view(), name='rack-detail'),
    path('book-item/',BookItemAPIView.as_view(), name='book-item'),
    path('book-item-detail/<int:pk>',BookItemDetailView.as_view(), name='book-item-detail'),
    path('book/',ViewBooksAPIView.as_view(), name='book'),
    path('book-detail/<int:pk>',ViewBookDetailAPIView.as_view(), name='book-detail'),
    path('lend-book/',LendBookAPIView.as_view(), name='lend-book'),
    path('reserve/', ReserveBookAPIView.as_view(), name='reserve-book'),
    path('reservation-list/', ReservationListAPIView.as_view(), name='reservation-list'),
]