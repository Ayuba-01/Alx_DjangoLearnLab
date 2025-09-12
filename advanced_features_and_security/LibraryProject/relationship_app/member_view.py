from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import UserProfile

def _is_member(user):
    return (
        user.is_authenticated
        and hasattr(user, "profile")
        and user.profile.role == UserProfile.Roles.MEMBER
    )

@user_passes_test(_is_member, login_url="relationship_app:login")
def member_view(request):
    return render(request, "relationship_app/member_view.html")