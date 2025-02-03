from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.faq import FAQ
from apps.mobile.serializers.faq import FAQSerializer
from apps.shared.pagination import CustomPagination


class FAQList(APIView):
    permission_classes = [AllowAny]
    serializer_class = FAQSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        return FAQ.objects.filter(is_active=True)

    def get(self, request):
        queryset = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True)
        return Response({
            "success": True,
            "message": "FAQs fetched successfully",
            "data": serializer.data
        })
