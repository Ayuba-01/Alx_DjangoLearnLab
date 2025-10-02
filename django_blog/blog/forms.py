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
    tags_csv = forms.CharField(
        required=False,
        label="Tags",
        help_text="Comma-separated (e.g., django, web, tips)",
        widget=forms.TextInput(attrs={"placeholder": "django, web, tips"})
    )
    class Meta:
        model = Post
        fields = ("title", "content", "tags_csv")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Post title"}),
            "content": forms.Textarea(attrs={"rows": 10, "placeholder": "Write your post..."}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prefill when editing
        if self.instance and self.instance.pk:
            names = list(self.instance.tags.values_list("name", flat=True))
            if names:
                self.fields["tags_csv"].initial = ", ".join(names)

    def _parse_tags(self):
        raw = (self.cleaned_data.get("tags_csv") or "").strip()
        if not raw:
            return []
        # split on comma, trim blanks, collapse spaces
        names = [t.strip() for t in raw.split(",") if t.strip()]
        # de-duplicate, preserve order
        seen, unique = set(), []
        for n in names:
            if n.lower() not in seen:
                seen.add(n.lower())
                unique.append(n)
        return unique

    def save(self, commit=True):
        post = super().save(commit=commit)
        # when commit=False on create, ensure we have a PK before setting M2M
        if not post.pk and commit:
            post.save()
        tag_names = self._parse_tags()
        tag_objs = []
        for name in tag_names:
            tag, _ = Tag.objects.get_or_create(name=name)
            tag_objs.append(tag)
        # set (replace) the M2M
        # if post has no pk yet, save first
        if not post.pk:
            post.save()
        post.tags.set(tag_objs)
        return post

    
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
        fields = ("content",)  

    def clean_content(self):
        text = (self.cleaned_data.get("content") or "").strip()
        if not text:
            raise forms.ValidationError("Comment cannot be empty.")
        if len(text) < 3:
            raise forms.ValidationError("Comment is too short.")
        return text