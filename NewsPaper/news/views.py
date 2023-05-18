from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, PostCategory
from .filters import PostFilter
from .forms import PostForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class PostSearch(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_search'

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_news',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'


class PostUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_new',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'


class PostDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryListView(PostList):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.postCategory.subscribers.all()
        context['category'] = self.postCategory
        return context


@login_required
@csrf_protect
def subscriptions(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    massage = 'Вы успешно подписались на рассылку'
    return render(request, 'news/subscribe.html', {'category': category, 'massage': massage})
