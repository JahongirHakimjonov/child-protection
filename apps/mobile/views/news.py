from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.mobile.models.news import News
from apps.mobile.serializers.news import NewsSerializer
from apps.shared.pagination import CustomPagination


class NewsView(APIView):
    permission_classes = (IsAuthenticated,)
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
