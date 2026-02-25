from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class PostForm(forms.ModelForm):

    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

def save(self, commit=True):

        post = super().save(commit=False)

        if commit:
            post.save()

            tag_names = self.cleaned_data['tags'].split(',')

            for tag_name in tag_names:

                tag_name = tag_name.strip()

                if tag_name:

                    tag, created = Tag.objects.get_or_create(name=tag_name)

                    post.tags.add(tag)

        return post    

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['content']