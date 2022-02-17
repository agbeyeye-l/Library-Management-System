from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from identity_manager.models import Account
from identity_manager.serializer import AccountSerializer 
from rest_framework.permissions import IsAuthenticated
from identity_manager.permissions import IsOwnerProfileOrReadOnly, IsLibrarianPermission
from django.contrib.auth.models import User


class AccountListCreateAPIView(ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated,IsLibrarianPermission]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user = user)



class AccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated,IsLibrarianPermission]

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs["id"])
        user.delete()
        return super().destroy(request, *args, **kwargs)


