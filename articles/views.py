from django.views import View
from django.views.generic import ListView, DetailView, FormView, TemplateView  # new
from django.views.generic.detail import SingleObjectMixin  # new
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy, reverse  # new
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CommentForm
from .models import Article

# Create your views here.

class TestView(TemplateView):
    template_name = "_base.html"
    
class ArticleListView(ListView):
    model = Article
    template_name = 'article/article_list.html'
    context_object_name = 'articles'


class CommentGet(DetailView):  # new
    model = Article
    template_name = "article/articleDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm()
        return context


class CommentPost(SingleObjectMixin, FormView):  # new
    model = Article
    form_class = CommentForm
    template_name = "article/articleDetail.html"

    # context_object_name = 'article'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        article = self.get_object()
        return reverse("articles:article_detail", kwargs={"pk": article.pk})


class ArticleDetailView(LoginRequiredMixin, DetailView):
    model = Article
    template_name = 'article/articleDetail.html'
    context_object_name = 'article'
    # slug_field = 'slug'
    # slug_url_kwarg = 'slug'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'article/article_new.html'
    context_object_name = 'articles'
    fields = ['title', 'body']
    success_url = reverse_lazy("articles:article_list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ["title", "body"]
    template_name = "article/article_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "article/article_delete.html"
    success_url = reverse_lazy("articles:article_list")

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
