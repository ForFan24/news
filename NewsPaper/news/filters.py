from django_filters import FilterSet, DateTimeFilter, CharFilter, ModelChoiceFilter
from django.forms import DateTimeInput
from .models import Category, PostCategory


class PostFilter(FilterSet):
    add_title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок',
    )
    add_date = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        label='Новости с даты',
        widget=DateTimeInput(
            format='%b %d %Y',
            attrs={'type': 'datetime-local'},
        )
    )
    add_category = ModelChoiceFilter(
        field_name='postcategory__categoryThrough',
        queryset=Category.objects.all(),
        label='Категория поста',
        empty_label='all',

    )
    add_news_category = ModelChoiceFilter(
        field_name='postcategory__categoryThrough',
        queryset=PostCategory.objects.all(),
        label='Категория поста',
        empty_label='all',

    )
