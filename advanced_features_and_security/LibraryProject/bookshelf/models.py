from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    
    @classmethod
    def create(cls, title, author, publication_year):
        book = cls(title=title, author=author, publication_year=publication_year)
        return book
    
    
class UserManager(BaseUserManager):
    """Manager for custom user model."""
    def create_user(self, email, date_of_birth, profile_photo, password=None,**extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, date_of_birth=date_of_birth, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,  email, date_of_birth, password=None,**extra_fields):
        """Create a superuser with full permissions."""
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        return user

class CustomeUser(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateTimeField()
    profile_photo = models.ImageField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]
    
    def __str__(self):
        return self.email