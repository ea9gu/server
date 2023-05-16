from datetime import date
from rest_framework import serializers
from .models import User

class UserJWTSignupSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        write_only=True,
        max_length=20
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    name = serializers.CharField(
        required=True,
        write_only=True,
    )

    flag = serializers.DateField(
        required=True,
        write_only=True,
    )

    email = serializers.EmailField(
        required=False,
        allow_blank=True,
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'name', 'flag']

    def save(self, **kwargs):
        user = User(
            username=self.validated_data['username'],
            name=self.validated_data['name'],
            flag=self.validated_data['flag']
        )

        user.set_password(self.validated_data['password'])
        user.subscription_date = date.today()
        user.save()

        return user

    def validate(self, data):
        username = data.get('username', None)

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User already exists")

        return data
