from django import forms
from .models import Post


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )

#mitonesti chon in 2ta eyne haman ye form dashte bashi ba esm PostCreateUpdateForm


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )

