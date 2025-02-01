from calendar import month_name, day_name
from collections import defaultdict
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.victim import Victim
from apps.users.models.users import User


class VictimStat(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get_model(type_):
        """User yoki Victim modelini tanlash."""
        return {"user": User, "victim": Victim}.get(type_)

    def get_statistics(self, model, truncate_function, labels):
        """Statistikani olish uchun umumiy funksiya."""
        stats = (
            model.objects.filter(created_at__gte=now().replace(month=1, day=1))
            .annotate(period=truncate_function("created_at"))
            .values("period")
            .annotate(count=Count("id"))
            .order_by("period")
        )

        # Ma'lumotlarni to'ldirish
        data_dict = defaultdict(int, {data["period"]: data["count"] for data in stats})

        return {
            "labels": labels,
            "info": [data_dict.get(label, 0) for label in labels],
        }

    @extend_schema(
        summary="Get victim statistics",
        description="Retrieve weekly or yearly statistics for users or victims.",
        parameters=[
            OpenApiParameter(
                name="distance",
                type=str,
                required=True,
                enum=["weekly", "yearly"],
                description="Specify whether to retrieve weekly or yearly statistics.",
            ),
            OpenApiParameter(
                name="type",
                type=str,
                required=True,
                enum=["user", "victim"],
                description="Specify whether to retrieve statistics for users or victims.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=dict,
                description="Returns labels and statistical data",
            ),
            400: OpenApiResponse(
                response=dict,
                description="Invalid query parameters",
            ),
        },
    )
    def get(self, request):
        distance = request.query_params.get("distance")
        type_ = request.query_params.get("type")

        model = self.get_model(type_)
        if not model:
            return Response(
                {"success": False, "message": "Invalid type parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if distance == "weekly":
            start_date = now() - timedelta(days=7)
            labels = list(day_name)  # ["Monday", "Tuesday", ...]
            stats = (
                model.objects.filter(created_at__gte=start_date)
                .annotate(period=TruncDay("created_at"))
                .values("period")
                .annotate(count=Count("id"))
                .order_by("period")
            )

        elif distance == "yearly":
            labels = [
                month_name[i] for i in range(1, 13)
            ]  # ["January", "February", ...]
            stats = (
                model.objects.filter(created_at__year=now().year)
                .annotate(period=TruncMonth("created_at"))
                .values("period")
                .annotate(count=Count("id"))
                .order_by("period")
            )

        else:
            return Response(
                {"success": False, "message": "Invalid distance parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data_dict = defaultdict(
            int,
            {
                data["period"].strftime("%A" if distance == "weekly" else "%B"): data[
                    "count"
                ]
                for data in stats
            },
        )

        response_data = {
            "labels": labels,
            "info": [data_dict.get(label, 0) for label in labels],
        }

        return Response(
            {
                "success": True,
                "message": f"{distance.capitalize()} stats",
                "data": response_data,
            },
            status=status.HTTP_200_OK,
        )
