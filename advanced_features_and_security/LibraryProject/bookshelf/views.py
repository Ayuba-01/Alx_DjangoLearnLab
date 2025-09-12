from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser

@permission_required("bookshelf.can_create", raise_exception=True)
def add_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        date_of_birth = request.POST.get("date_of_birth")
        profile_photo = request.POST.get("profile_photo")
        CustomUser.objects.create(email=email, date_of_birth=date_of_birth, profile_photo=profile_photo)
        return redirect("bookshelf:list_user") 
    users = CustomUser.objects.all()
    return render(request, "bookshelf/add_user.html", {"users": users})


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        email = request.POST.get("email")
        date_of_birth = request.POST.get("date_of_birth")
        profile_photo = request.POST.get("profile_photo")
        if email:
            user.email = email
        if date_of_birth:
            user.date_of_birth = date_of_birth
        if profile_photo:
            user.profile_photo = profile_photo
        user.save()
        return redirect("bookshelf:list_users")
    users = CustomUser.objects.all()
    return render(request, "relationship_app/edit_book.html", {"user": users})


@permission_required("bookshelf.Can Delete", raise_exception=True)
def delete_book(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == "POST":
        user.delete()
        return redirect("bookshelf:list_users")
    return render(request, "bookshelf/confirm_delete_user.html", {"book": user})
