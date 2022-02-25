from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status 
from django.contrib.auth.models import User

from identity_manager.models import Account


class Info:
    user_data = { 'username':'user2','password':'password@123',
                're_password': 'password@123','email':'dnewlife0@gmail.com', 
                'role':'Librarian'}
    login_credentials = {'username':'user2','password':'password@123'}
    update_profile={'role':'Member'}
    profile_list_url=reverse('account')
    a_profile_url = reverse('detail-account',kwargs={'pk':1})
    login_url = '/api/v1/jwt/create/'
    create_user_url = '/api/v1/users/'



class userProfileTestCase(APITestCase):
    
    def setUp(self):
        # create a new user making a post request to djoser endpoint
        self.user=self.client.post(Info.create_user_url, data=Info.user_data)
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
        response=self.client.post(Info.login_url,data=Info.login_credentials)
        self.token=response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)

    # retrieve a list of all user profiles while the request user is authenticated
    def test_userprofile_list_authenticated(self):
        response=self.client.get(Info.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # retrieve a list of all user profiles while the request user is unauthenticated
    def test_userprofile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response=self.client.get(Info.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    # check to retrieve the profile details of the authenticated user
    def test_userprofile_detail_retrieve(self):
        response=self.client.get(Info.a_profile_url,)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    # Update user role
    def test_userprofile_profile(self):
        response=self.client.put(Info.a_profile_url,data=Info.update_profile)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

