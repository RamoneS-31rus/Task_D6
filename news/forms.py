from django.forms import ModelForm, TextInput, Textarea, Select, SelectMultiple
from .models import Post


class PostForm(ModelForm):

    class Meta:
        model = Post
        fields = ['post_author', 'post_type', 'post_category', 'post_title', 'post_text']
        widgets = {
            'post_author': Select(attrs={
                'class': 'custom-select',
                #'option selected': 'Выбрать...'
            }),
            'post_type': Select(attrs={
                'class': 'custom-select',
                #'option selected': 'Выбрать...'
            }),
            'post_category': SelectMultiple(attrs={
                'multiple class': 'form-control',
            }),
            'post_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст'
            }),
        }