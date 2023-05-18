from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'categoryType', 'title', 'text', 'postCategory']

        def clean(self):
            cleaned_data = super().clean()
            description = cleaned_data.get("description")
            name = cleaned_data.get("name")

            if name == description:
                raise ValidationError(
                    "Описание не должно быть идентично названию."
                )

            return cleaned_data