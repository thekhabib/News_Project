from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.views import HitCountDetailView

from config.custom_permissions import OnlyLoggedSuperUser
from .forms import ContactForm, CommentForm
from .models import News, Category


# Create your views here.
def newsdetail(request, slug):
    news = get_object_or_404(News, slug=slug, status=News.Status.Published)
    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            return redirect('news_detail_page', slug=news.slug)
    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments': comments,
        'comment_count': comment_count,
        'comment_form': comment_form,
    }
    return render(request, 'news/news_detail.html', context)


class NewsDetailView(HitCountDetailView):
    model = News
    template_name = 'news/news_detail.html'
    context_object_name = 'news'
    form = CommentForm
    count_hit = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = context['news'].comments.filter(active=True)
        context['comment_count'] = context['comments'].count()
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = News.objects.get(slug=kwargs['slug'])
            new_comment.user = request.user
            new_comment.save()
            return redirect('news_detail_page', slug=self.kwargs['slug'])


class HomePageView(ListView):
    """def homePageView(request):
        categories = Category.objects.all()
        news_list = News.published.all().order_by('-published_time')[:5]
        local_one = News.published.filter(category__name='Mahalliy').order_by('-published_time')[:1]
        local_news = News.published.filter(category__name='Mahalliy').order_by('-published_time')[1:6]
        context = {
            'categories': categories,
            'news_list': news_list,
            'local_one': local_one,
            'local_news': local_news,
        }
        return render(request, 'news/home.html', context)"""
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-published_time')[:5]
        context['local_news'] = News.published.filter(category__name='Mahalliy').order_by('-published_time')[:5]
        context['world_news'] = News.published.filter(category__name='Xorij').order_by('-published_time')[:5]
        context['technology_news'] = News.published.filter(category__name='Texnologiya').order_by('-published_time')[:5]
        context['sport_news'] = News.published.filter(category__name='Sport').order_by('-published_time')[:5]
        return context


class ContactPageView(TemplateView):
    """def contactPageView(request):
        form = ContactForm(request.POST or None)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse('<h2>Biz bilan bog\'langaningiz uchun tashakkur.</h2>')
        context = {
            'form': form,
        }
        return render(request, 'news/contact.html', context)"""
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse('<h2>Biz bilan bog\'langaningiz uchun tashakkur.</h2>')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'local_news'

    def get_queryset(self):
        news = News.published.filter(category__name='Mahalliy').order_by('-published_time')
        return news


class WorldNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'world_news'

    def get_queryset(self):
        news = News.published.filter(category__name='Xorij').order_by('-published_time')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/texnologiya.html'
    context_object_name = 'technology_news'

    def get_queryset(self):
        news = News.published.filter(category__name='Texnologiya').order_by('-published_time')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = News.published.filter(category__name='Sport').order_by('-published_time')
        return news


class NewsUpdateView(OnlyLoggedSuperUser, UpdateView):
    model = News
    fields = ['title', 'body', 'image', 'category', 'status']
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlyLoggedSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlyLoggedSuperUser, CreateView):
    model = News
    fields = ['title', 'slug', 'body', 'image', 'category', 'status']
    template_name = 'crud/news_create.html'

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
@user_passes_test(lambda user: user.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users,
    }

    return render(request, 'pages/admin_page.html', context)


class SearchResultsListView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'search_list'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.published.filter(Q(title__icontains=query) | Q(body__icontains=query))
