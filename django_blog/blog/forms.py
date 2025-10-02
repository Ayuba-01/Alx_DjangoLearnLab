from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        if commit:
            user.save()
        return user
    

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email")
        
    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"rows": 10, "placeholder": "Write your post..."}),
        }

    
class CommentForm(forms.ModelForm):
    # Override the default to control label, widget, and max length
    content = forms.CharField(
        label="Add a comment",
        widget=forms.Textarea(attrs={
            "rows": 3,
            "placeholder": "Be respectful and stay on topic…",
        }),
        max_length=2000,  
        help_text="Max 2000 characters."
    )

    class Meta:
        model = Comment
        fields = ("content")  

    def clean_content(self):
        text = (self.cleaned_data.get("content") or "").strip()
        if not text:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(text) < 3:
            raise forms.ValidationError("Comment is too short.")
        return text