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

class Info:
    user_data = { 'username':'user2','password':'password@123',
                're_password': 'password@123','email':'dnewlife0@gmail.com', 
                'role':'Librarian'}
    login_credentials = {'username':'user2','password':'password@123'}
    update_profile={'role':'Member'}


class CustomTestCase(APITestCase):
    def setUp(self):
        # create a new user making a post request to djoser endpoint
        self.user=self.client.post(ENDPOINTS.USER, data=Info.user_data)
        # activate account
        user = User.objects.filter(pk=self.user.data['id']).first()
        user.is_active=True
        user.is_superuser=True
        user.save()
        # set account to librarian
        account = Account.objects.get(user=user)
        account.role = 'Librarian'
        account.save()
        # obtain a json web token for the newly created user
        response=self.client.post(ENDPOINTS.LOGIN,data=Info.login_credentials)
        self.token=response.data['access']
        self.api_authentication()
        self.client.post(ENDPOINTS.LIBRARY, data={"name": "Community Library 1","description": "General community library"})
        self.client.post(ENDPOINTS.RACK, data={"number": "1","locationIdentifier": "North-east","library": 1})
        self.client.post(ENDPOINTS.AUTHOR, data={"name": "Ben Key","description": "Best selling author"})
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)



class LibraryTestCase(CustomTestCase):
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
    def test_add_author(self):
        response = self.client.post(ENDPOINTS.AUTHOR, data={"name": "Ben Key","description": "Best selling author"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_author(self):
        
        response = self.client.patch(ENDPOINTS.AUTHOR_DETAIL, data={"description": "South-east"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_remove_author(self):
        response = self.client.delete(ENDPOINTS.AUTHOR_DETAIL)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


