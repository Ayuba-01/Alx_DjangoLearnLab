from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import UserProfile

def _is_librarian(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == UserProfile.Roles.LIBRARIAN
    )

@user_passes_test(_is_librarian, login_url="relationship_app:login")
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")