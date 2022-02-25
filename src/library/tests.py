from tkinter import END
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from identity_manager.tests import userProfileTestCase
from django.contrib.auth.models import User

from identity_manager.models import Account

class ENDPOINTS:
    PROFILE=reverse('account')
    PROFILE_DETAIL = reverse('detail-account',kwargs={'pk':1})
    LOGIN = '/api/v1/jwt/create/'
    USER = '/api/v1/users/'
    LIBRARY_DETAIL = reverse('lib-detail', kwargs={"pk":1})
    LIBRARY = reverse('libs')
    RACK= reverse('rack')
    RACK_DETAIL = reverse('rack-detail', kwargs={"pk":1})
    AUTHOR= reverse('author')
    AUTHOR_DETAIL= reverse('author-detail',kwargs={"pk":1})
    BOOK_ITEM = reverse('book-item')
    BOOK_ITEM_DETAIL = reverse('book-item-detail',kwargs={"pk":1})
    VIEW_BOOK_LIST = reverse('book')
    VIEW_BOOK = reverse('book-detail',kwargs={"pk":1})


class Info:
    user_data = { 'username':'user2','password':'password@123',
                're_password': 'password@123','email':'dnewlife0@gmail.com', 
                'role':'Librarian'}
    login_credentials = {'username':'user2','password':'password@123'}
    update_profile={'role':'Member'}
    book = {
            "ISBN": "ISB45466334345",
            "title": "Software Architecture",
            "subject": "Software Engineering",
            "publisher": "Dr. Potassio Cessare",
            "language": "English",
            "numOfPages": 400,
            "barcode": "SAFKDDDDFDKDAF111D",
            "isReferenceOnly": False,
            "borrowed": "2022-02-17",
            "dueDate": "2022-02-17",
            "price": "50.00",
            "status": "Available",
            "format": "Hardcopy",
            "datePurchase": "2022-02-17",
            "rack": 1,
            "library": 1,
            "author":1
        }


class CustomTestCase(userProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.post(ENDPOINTS.LIBRARY, data={"name": "Community Library 1","description": "General community library"})
        self.client.post(ENDPOINTS.RACK, data={"number": "1","locationIdentifier": "North-east","library": 1})
        self.client.post(ENDPOINTS.AUTHOR, data={"name": "Ben Key","description": "Best selling author"})
        self.client.post(ENDPOINTS.BOOK_ITEM, data=Info.book)
        


class LibraryTestCase(CustomTestCase):
    """
    Test cases for creating, updating, and removing library
    """
    def test_create_library(self):
        response = self.client.post(ENDPOINTS.LIBRARY, data={"name": "Community Library 1","description": "General community library"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_library(self):
        
        response = self.client.patch(ENDPOINTS.LIBRARY_DETAIL, data={"description": "General xc community library"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_library(self):
        response = self.client.delete(ENDPOINTS.LIBRARY_DETAIL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RackTestCase(CustomTestCase):
    """
    Test case for creating, updating, and removing racks
    """
    def test_create_rack(self):
        response = self.client.post(ENDPOINTS.RACK, data={"number": "35","locationIdentifier": "North-east","library": 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_rack(self):
        
        response = self.client.patch(ENDPOINTS.RACK_DETAIL, data={"locationIdentifier": "South-east"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_rack(self):
        response = self.client.delete(ENDPOINTS.RACK_DETAIL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class AuthorTestCase(CustomTestCase):
    """
    Test case for adding, updating, and removing an author
    """
    def test_add_author(self):
        response = self.client.post(ENDPOINTS.AUTHOR, data={"name": "Ben Key","description": "Best selling author"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_author(self):
        
        response = self.client.patch(ENDPOINTS.AUTHOR_DETAIL, data={"description": "South-east"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_author(self):
        response = self.client.delete(ENDPOINTS.AUTHOR_DETAIL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class BookItemTestCase(CustomTestCase):
    """
    Test cases for adding, updating, and removing book items by librarian
    """
    def test_add_book_item(self):
        response = self.client.post(ENDPOINTS.BOOK_ITEM,data=Info.book)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_update_book_item(self):
        response = self.client.patch(ENDPOINTS.BOOK_ITEM_DETAIL, data = {"title":"AS 1290"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_book_item(self):
        response = self.client.delete(ENDPOINTS.BOOK_ITEM_DETAIL)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)


class ViewBookTestCase(CustomTestCase):
    """
    Test cases for viewing list and detail info  of single book by members
    """
    def test_view_book_list(self):
        response = self.client.get(ENDPOINTS.VIEW_BOOK_LIST)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_single_book(self):
        response = self.client.get(ENDPOINTS.VIEW_BOOK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)