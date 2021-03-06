from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Account
        fields = "__all__"