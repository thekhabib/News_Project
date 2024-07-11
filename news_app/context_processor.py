from .models import News, Category


def latest_news(request):
    categories = Category.objects.all()
    latest_news = News.published.order_by('-published_time')[:5]
    context = {
        'latest_news': latest_news,
        'categories': categories,
    }
    return context
