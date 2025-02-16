from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['username', 'location', 'profile_pic', 'post_image', 'caption']
