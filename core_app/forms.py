from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': "ВВедите заголовок", 'class': 'my-form'}),
            'content': forms.Textarea(attrs={
                'class': 'my-form',
                'rows': 5,
                'placeholder': 'О чем вы думаете?'

            }),

        }
