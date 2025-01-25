from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.saved import Saved
from apps.mobile.serializers.saved import SavedSerializer
from apps.shared.pagination import CustomPagination


class SavedApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedSerializer
    pagination_class = CustomPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"rq": request})
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response(
                    {
                        "success": True,
                        "message": "The course has been saved successfully.",
                    },
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                try:
                    existing_entry = Saved.objects.get(
                        user=request.user, lesson=request.data["lesson"]
                    )
                    existing_entry.delete()
                    return Response(
                        {
                            "success": True,
                            "message": "The course has been removed from the saved list.",
                        },
                        status=status.HTTP_200_OK,
                    )
                except ObjectDoesNotExist:
                    return Response(
                        {
                            "success": False,
                            "message": "No saved entry found to delete.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
        return Response(
            {"success": False, "message": "Action failed.", "data": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request):
        saved = Saved.objects.filter(user=request.user).select_related("lesson", "user")
        paginator = self.pagination_class()
        paginated_saved = paginator.paginate_queryset(saved, request)
        serializer = self.serializer_class(
            paginated_saved, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)
