from django import forms
from .models import Post, Comment


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )

#mitonesti chon in 2ta eyne haman ye form dashte bashi ba esm PostCreateUpdateForm


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', )


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'class':'form-control'})
        }


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', )

class PostSearchForm(forms.Form):
    search = forms.CharField()