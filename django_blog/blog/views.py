# blog/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Post
from .forms import PostForm

from .forms import RegisterForm, ProfileForm
class CustomLoginView(LoginView):
    template_name = "blog/login.html"            
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    template_name = "blog/logout.html"

def registerview(request):
    """
    GET: show registration form
    POST: create user, auto-login (optional), redirect to profile or home
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log them in immediately after signup
            auth_login(request, user)
            messages.success(request, "Your account was created successfully.")
            return redirect("blog:profile")  
        messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profileview(request):
    """
    View + edit the authenticated user's basic details.
    GET: show form with current values
    POST: validate + save; on success redirect to /profile with a success message
    """
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
        messages.error(request, "Please fix the errors below.")
    else:
        form = ProfileForm(instance=request.user)

    return render(request, "blog/profile.html", {"form": form})

class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10  # optional; remove if you don't want pagination

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_create_edit.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Post created.")
        return response

class AuthorRequiredMixin(UserPassesTestMixin):
    """Only the author may edit/delete."""
    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.id

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Post updated.")
        return response

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post-list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted.")
        return super().delete(request, *args, **kwargs)