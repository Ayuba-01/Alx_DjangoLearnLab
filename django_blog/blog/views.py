# blog/views.py
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages

from .models import Post, Comment
from .forms import PostForm, CommentForm

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
    
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # comments for this post (newest first via Comment.Meta.ordering)
        ctx["comments"] = self.object.comments.select_related("author").all()
        # empty form for the “Leave a comment” box
        ctx["comment_form"] = CommentForm()
        return ctx

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
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    # No template here; the form lives on the post detail page

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["post_id"])
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, "Comment posted.")
        return super().form_valid(form)

    def get_success_url(self):
        # Back to the post, jump to comments
        return reverse("blog:post-detail", kwargs={"pk": self.kwargs["post_id"]}) + "#comments"
    

class CommentAuthorOnlyMixin(UserPassesTestMixin):
    """Allow only the comment author to edit/delete."""
    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.id

class CommentUpdateView(LoginRequiredMixin, CommentAuthorOnlyMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.post_id}) + f"#comment-{self.object.pk}"
    

class CommentDeleteView(LoginRequiredMixin, CommentAuthorOnlyMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted.")
        return super().delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.post_id}) + "#comments"
