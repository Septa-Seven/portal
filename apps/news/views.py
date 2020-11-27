from rest_framework.response import Response
from rest_framework.views import APIView

from .models import News
from .serializers import NewsListSerializer, NewsDetailSerializer


class NewsListView(APIView):
    """Here's all published news"""
    def get(self, request):
        all_news = News.objects.filter(status='published')
        serializer = NewsListSerializer(all_news, many=True)
        return Response(serializer.data)


class NewsDetailView(APIView):
    """Here's detailed news"""
    def get(self, request, pk):
        news = News.objects.get(id=pk, status='published')
        serializer = NewsDetailSerializer(news)
        return Response(serializer.data)
