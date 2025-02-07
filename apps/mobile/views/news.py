from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.news import News
from apps.mobile.serializers.news import NewsSerializer
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination import CustomPagination


class NewsView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = NewsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return News.objects.filter(is_active=True)

    def get(self, request):
        news = self.get_queryset()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(news, request)
        serializer = self.serializer_class(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class NewsDetailView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = NewsSerializer

    def get(self, request, pk):
        news = get_object_or_404(News, pk=pk)
        news.increase_view_count()
        serializer = self.serializer_class(news)
        return Response(
            {
                "success": True,
                "message": "News detail",
                "data": serializer.data,
            }
        )
