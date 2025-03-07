from django.contrib.auth import get_user_model
from django.db.models import IntegerField
from django.db.models.base import Model
from django.forms import fields
from rest_framework import serializers
from rest_framework.exceptions import server_error
from rest_framework.fields import ListField, MinValueValidator
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import AvatarModel, ProfileModel
from django.db.transaction import atomic
from django.conf import settings

UserModel = get_user_model()


class AvatarSerializer(ModelSerializer):
    class Meta:
        model = AvatarModel
        fields = ('image',)
        
        extra_kwargs = {
            "image":{
                "required":True,
            }
        }



class ProfileSerializer(ModelSerializer):
    avatar = AvatarSerializer(many=True)
    class Meta:
        model = ProfileModel
        fields = ["id", "name", "surname", "birthday", "bio", 'avatar']
        read_only_fields = ("id",)


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = UserModel
        fields = ["id", "email", "password", "phone", "nickname", "is_active", "is_block", "is_superuser", "is_staff", "profile", "is_online", "contacts"]
        
        read_only_fields = (
            "id",
            "is_active",
            "is_block",
            "is_staff",
            "is_superuser",
            "last_login",
            "is_online",
            "contacts",
        )

        extra_kwargs ={
            "password": {
                "write_only":True,
            }
        }
        

    @atomic
    def create(self, validated_data):
        profile = validated_data.pop("profile")
        profile = ProfileModel.objects.create(**profile)
        user = UserModel.objects.create_user(**validated_data, profile=profile)
        return user

    @atomic
    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if profile_data:
            profile = instance.profile 
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance


class UserRegistrationSerializer(ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 'nickname', )
        read_only_fields = (
            'id',
        )
        extra_kwargs = {
            "password": {
                "write_only":True,
            }
        }

    @atomic 
    def create(self, validated_data):
        profile = ProfileModel.objects.create()
        user = UserModel.objects.create_user(**validated_data, profile=profile)
        return user

   
class UserNicknameSerializers(serializers.Serializer):
    nickname = serializers.CharField(max_length=128)

    def validate(self, attrs):
        attrs['nickname'] = "@" + attrs.get('nickname')
        return super().validate(attrs)

class UserIdSerializers(serializers.Serializer):
    id = serializers.IntegerField()


class UserContactsSerializers(ModelSerializer):
    contacts = UserSerializer(many=True, read_only=True)
    class Meta:
        model = UserModel
        fields = ('contacts',)






#Representation 
class ProfileNameSurnameSerializer(ModelSerializer):
    avatar = SerializerMethodField()
    class Meta:
        model = ProfileModel
        fields = ('name', 'surname', 'avatar')

    def get_avatar(self, obj):
        last_image  =  obj.avatar.order_by('-id').first()
        return AvatarSerializer(last_image).data.get('image', None) if last_image else None
    

class UserShortSerializer(ModelSerializer):
    profile = ProfileNameSurnameSerializer(read_only=True)
    class Meta:
        model = UserModel
        fields = ('id', 'nickname', 'is_online', 'profile',)

class MyContactsSerializer(ModelSerializer):
    contacts = UserShortSerializer(read_only=True, many=True)
    class Meta:
        model = UserModel
        fields = ('id', 'contacts')

