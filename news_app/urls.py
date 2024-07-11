from django.urls import path
from .views import newsdetail, HomePageView, ContactPageView, \
    LocalNewsView, WorldNewsView, TechnologyNewsView, SportNewsView


urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/<slug:news>/', newsdetail, name='news_detail_page'),
    path('contact-us/', ContactPageView.as_view(), name='contact_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('world/', WorldNewsView.as_view(), name='world_news_page'),
    path('technology/', TechnologyNewsView.as_view(), name='technology_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
]
