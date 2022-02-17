from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status 

class userProfileTestCase(APITestCase):
    profile_list_url=reverse('account')
    def setUp(self):
        # create a new user making a post request to djoser endpoint
        self.user=self.client.post('/auth/users/',data={'username':'user2','password':'password@12345','email':'dnewlife0@gmail.com'})
        # obtain a json web token for the newly created user
        response=self.client.post('/auth/jwt/create/',data={'username':'user2','password':'password@12345'})
        self.token=response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)

    # retrieve a list of all user profiles while the request user is authenticated
    def test_userprofile_list_authenticated(self):
        response=self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # retrieve a list of all user profiles while the request user is unauthenticated
    def test_userprofile_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response=self.client.get(self.profile_list_url)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    # check to retrieve the profile details of the authenticated user
    def test_userprofile_detail_retrieve(self):
        response=self.client.get(reverse('detail-account',kwargs={'pk':1}))
        # print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    # populate the user profile that was automatically created using the signals
    def test_userprofile_profile(self):
        profile_data={'accountType':'2'}
        response=self.client.put(reverse('detail-account',kwargs={'pk':1}),data=profile_data)
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

