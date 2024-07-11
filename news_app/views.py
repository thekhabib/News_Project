from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import TemplateView, ListView

from .forms import ContactForm
from .models import News, Category


# Create your views here.
def newsdetail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context)


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
