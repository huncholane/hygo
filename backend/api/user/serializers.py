from rest_framework import serializers
from django.contrib.auth.models import User
from home.models import Account


class ListUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ('private', 'access_token',
                  'refresh_token', 'token_expires_at')
        extra_kwargs = {'access_token': {'write_only': True}, 'refresh_token': {
            'write_only': True}, 'token_expires_at': {'write_only': True}}


class SingleUserSerializer(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'password',
                  'first_name', 'last_name', 'account')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
