from django.urls import path
#from rest_framework.routers import DefaultRouter
from .views import AccountListCreateAPIView, AccountDetailAPIView

urlpatterns = [
    path('all-account/', AccountListCreateAPIView.as_view(), name="account"),
    path('account/<int:pk>', AccountDetailAPIView.as_view(), name='detail-account'),

]