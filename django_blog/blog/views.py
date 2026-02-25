from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django import forms
from .forms import CustomeUserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm
from .forms import CommentForm
from django.shortcuts import get_object_or_404

# for the registration

def register_view(request):
    if request.method == 'POST':
        form = CustomeUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully! You can now login")
            return redirect('login')
        else:
            form = CustomeUserCreationForm()
        return render(request, 'blog/register.html', {'form': form})
    
# for login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'blog/login.html')

# for logout view

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')

# profile view

def profile_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.user.email = email
        request.user.save()
        messages.success(request, "Profile updated successfully!")
    return render(request, 'blog/profile.html')


# postlist view -shows list of objects

class PostListView(ListView):
    model =Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']

# post detail view shows single obj

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# postcreate view creates new posts

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# postupdate view used to edit obj

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model =Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return super().test_func()
    
# post delete view

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return super().test_func()
    
# comment views
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Comment, Post
from .forms import CommentForm

# create comment
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return self.object.post.get_absolute_url()

# Update comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

# Delete comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    # to search
from django.db.models import Q
from django.shortcuts import render
from .models import Post

def search_posts(request):
    query = request.GET.get('q', '')
    results = Post.objects.filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(tags__name__icontains=query)
    ).distinct()
    return render(request, 'blog/search_results.html', {'results': results, 'query': query})

from django.views.generic import ListView
from taggit.models import Tag

class PostByTagListView(ListView):  # <-- renamed to match checker
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags__slug=self.tag.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context

# ADD COMMENT
@login_required
def add_comment(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)

            comment.post = post

            comment.author = request.user

            comment.save()

            return redirect('post-detail', pk=post.pk)


# EDIT COMMENT
@login_required
def edit_comment(request, pk):

    comment = get_object_or_404(Comment, pk=pk)

    if comment.author != request.user:
        return redirect('post-detail', pk=comment.post.pk)

    if request.method == 'POST':

        form = CommentForm(request.POST, instance=comment)

        if form.is_valid():

            form.save()

            return redirect('post-detail', pk=comment.post.pk)

    else:

        form = CommentForm(instance=comment)

    return render(request, 'blog/edit_comment.html', {'form': form})


# DELETE COMMENT
@login_required
def delete_comment(request, pk):

    comment = get_object_or_404(Comment, pk=pk)

    post_pk = comment.post.pk

    if comment.author == request.user:

        comment.delete()

    return redirect('post-detail', pk=post_pk)
