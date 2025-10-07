from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()  

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "full_name", "bio", "profile_picture")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 8},
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = get_user_model().objects.create_user( 
            password=password,
            **validated_data
        )
    
        Token.objects.create(user=user)  
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "full_name", "bio", "profile_picture")
        read_only_fields = ("email",)
