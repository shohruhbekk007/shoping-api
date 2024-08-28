from rest_framework import serializers
from .models import  Xaridor, Mahsulot, Partiya, Sklad, Sotuv
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class XaridorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xaridor
        fields = '__all__'

class MahsulotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahsulot
        fields = '__all__'

class PartiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partiya
        fields = '__all__'

class SkladSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sklad
        fields = '__all__'

class SotuvSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sotuv
        fields = '__all__'
