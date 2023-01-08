from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                        BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):

    def create_user(self, personnel_id, password=None, **extra_fields):
        if not personnel_id:
            raise ValueError('The Username must be set')
        user = self.model(personnel_id=personnel_id, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, personnel_id, password, **extra_fields):
        if not personnel_id:
            raise ValueError('The Username must be set')
        superuser = self.model(personnel_id=personnel_id, **extra_fields)
        superuser.role = "admin"
        superuser.set_password(password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save()
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    
    ROLE_CHOICE = (
        ('technician_phoneline', 'Technician_PhoneLine'),
        ('technician_device', 'Technician_Device'),
        ('storekeeper', 'Storekeeper'),
        ('inspector', 'Inspector'),
        ('admin', 'Admin'),
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    personnel_id = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    USERNAME_FIELD = 'personnel_id'
    role = models.CharField(max_length=255, choices=ROLE_CHOICE)
    objects = UserManager()

    def __str__(self):
        return self.personnel_id