from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from core.models import CoreModel
from .manager import UserManager




class ProfileModel(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    surname = models.CharField(max_length=50, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    bio = models.CharField(max_length=50, blank=True, null=True)


class AvatarModel(models.Model):
    class Meta:
        db_table = "avatar"
    image = models.ImageField(upload_to="image/", blank=True)
    profile = models.ForeignKey(ProfileModel, on_delete=models.CASCADE, related_name='avatar')


class MetaDataModel(models.Model):
    class Meta:
        db_table = "meta_data"
    
    data_style =  models.JSONField()

class UserModel(AbstractBaseUser, PermissionsMixin, CoreModel):
    class Meta:
        db_table = "auth_users"

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=128)
    nickname = models.CharField(max_length=128, unique=True, blank=True, null=True)
    


    #base_parametr
    is_online = models.BooleanField(default=False)

    # type_account
    is_active = models.BooleanField(default=True)
    is_block = models.BooleanField(default=False)
    

    # Permissions
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    # Account
    profile = models.OneToOneField(ProfileModel, on_delete=models.CASCADE, blank=True, null=True, related_name='user')
    contacts = models.ManyToManyField("self", symmetrical=False, blank=True, null=True, related_name="contact_by")
    block_users = models.ManyToManyField("self", symmetrical=False, blank=True, null=True, related_name='block_by' )
    meta_data = models.OneToOneField(MetaDataModel, on_delete=models.CASCADE, blank=True, null=True)
    USERNAME_FIELD = "email"
    objects = UserManager() 


    