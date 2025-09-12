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
    
    
class CustomUserManager(BaseUserManager):
    """Manager for custom user model."""
    def create_user(self, email, password=None,**extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None,**extra_fields):
        """Create a superuser with full permissions."""
        user = self.create_user(
            email,
            password=password,
            **extra_fields,
        )
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return user

class CustomUser(AbstractUser):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateTimeField(null=True, blank=True)
    profile_photo = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    class Meta:
        permissions = [
            ("can_view", "Can View"), 
            ("can_create", "Can Create"), 
            ("can_edit", "Can Edit"),
            ("can_delete", "Can Delete" )
        ]