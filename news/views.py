from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.shortcuts import render




class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 3
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = PostForm()
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/sign/login/')
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_update.html'
    permission_required = ('news.change_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/sign/login/')
        return super().dispatch(request, *args, **kwargs)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/'
    permission_required = ('news.delete_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/sign/login/')
        return super().dispatch(request, *args, **kwargs)


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context
