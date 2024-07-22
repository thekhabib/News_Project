from django.urls import path
from .views import newsdetail, HomePageView, ContactPageView, about_view, \
    LocalNewsView, WorldNewsView, TechnologyNewsView, SportNewsView, \
    NewsDeleteView, NewsUpdateView, NewsCreateView, admin_page_view, NewsDetailView, SearchResultsListView


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/create/', NewsCreateView.as_view(), name='news_create'),
    # path('news/<slug:slug>/', newsdetail, name='news_detail_page'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news_detail_page'),
    path('news/<slug>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    path('news/<slug>/edit/', NewsUpdateView.as_view(), name='news_update'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('about/', about_view, name='about_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('world/', WorldNewsView.as_view(), name='world_news_page'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsListView.as_view(), name='search_results'),
]
