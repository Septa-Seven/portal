from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

news_list = views.NewsViewSet.as_view(
    actions={
        'get': 'list',
    })

news_create = views.NewsViewSet.as_view(
    actions={
        'post': 'create',
    })

news_detail = views.NewsViewSet.as_view(
    actions={
        'get': 'retrieve',
        'put': 'update',
        # 'patch': 'partial_update',
        'delete': 'destroy'
    })

urlpatterns = format_suffix_patterns([
    path('', news_list, name='news-list'),
    path('create/', news_create, name='news-create'),
    path('<int:pk>/', news_detail, name='news-detail'),
])


# urlpatterns = [
#     path('', views.NewsListView.as_view()),
#     path('<int:pk>/', views.NewsDetailView.as_view()),
# ]
