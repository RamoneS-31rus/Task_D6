from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.models import User




class PostList(ListView):
    model = Post
    template_name = 'news/posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        post_category = {}
        for post in Post.objects.all():
            category = []
            id = post.id
            for i in list(Post.objects.get(pk=id).post_category.all()):
                category.append(i)
            post_category.update({post: category})
        context['post_category']=post_category
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        id = self.kwargs.get('pk')
        category = []
        for i in list(Post.objects.get(pk=id).post_category.all()):
            category.append(i)
        context['post_category'] = category
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm()
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/sign/login/')
        return super().dispatch(request, *args, **kwargs)


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_update.html'
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
    template_name = 'news/post_delete.html'
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
    template_name = 'news/search.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['is_authors'] = self.request.user.groups.filter(name='authors').exists()
        return context


class PostCategoryList(ListView):
    template_name = 'news/categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()


class PostCategoryDetails(DetailView):
    template_name = 'news/category.html'
    context_object_name = 'category'
    queryset = Category.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        category = Category.objects.get(pk=id)
        posts = []
        for i in list(Post.objects.filter(post_category__title=category)):
            posts.append(i)
        context['category_posts'] = posts
        return context



class AddSubscribers(UpdateView):
    template_name = 'news/category_add.html'
    model = Category
    fields = []

    def post(self, request, *args, **kwargs):
        user = self.request.user
        id = self.kwargs.get('pk')
        Category.objects.get(pk=id).subscribers.add(User.objects.get(username=str(user)))
        return redirect('/categories/')
