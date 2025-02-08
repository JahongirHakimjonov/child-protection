from calendar import month_name, day_name, monthrange
from collections import defaultdict
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth, TruncHour
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
        """Choose between User or Victim model."""
        return {"user": User, "victim": Victim}.get(type_)

    @extend_schema(
        summary="Get victim statistics",
        description=(
            "Retrieve daily, weekly, monthly, or yearly statistics for users or victims. "
            " - **daily**: statistics for the current day grouped by hour\n"
            " - **weekly**: statistics for the past 7 days grouped by day name\n"
            " - **monthly**: statistics for the current month grouped by day\n"
            " - **yearly**: statistics for the current year grouped by month"
        ),
        parameters=[
            OpenApiParameter(
                name="distance",
                type=str,
                required=True,
                enum=["daily", "weekly", "monthly", "yearly"],
                description=(
                    "Specify the time period for statistics: "
                    "daily, weekly, monthly, or yearly."
                ),
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

        # Daily statistics: current day grouped by hour (24 hours)
        if distance == "daily":
            today = now().date()
            labels = [f"{hour:02d}:00" for hour in range(24)]
            stats = (
                model.objects.filter(created_at__date=today)
                .annotate(period=TruncHour("created_at"))
                .values("period")
                .annotate(count=Count("id"))
                .order_by("period")
            )
            data_dict = {
                data["period"].strftime("%H:00"): data["count"] for data in stats
            }

        # Weekly statistics: past 7 days grouped by day name
        elif distance == "weekly":
            start_date = now() - timedelta(days=7)
            labels = list(day_name)  # ["Monday", "Tuesday", ... "Sunday"]
            stats = (
                model.objects.filter(created_at__gte=start_date)
                .annotate(period=TruncDay("created_at"))
                .values("period")
                .annotate(count=Count("id"))
                .order_by("period")
            )
            data_dict = {data["period"].strftime("%A"): data["count"] for data in stats}

        # Monthly statistics: current month grouped by day of the month
        elif distance == "monthly":
            current_date = now()
            year = current_date.year
            month = current_date.month
            num_days = monthrange(year, month)[1]
            labels = [str(day) for day in range(1, num_days + 1)]
            stats = (
                model.objects.filter(created_at__year=year, created_at__month=month)
                .annotate(period=TruncDay("created_at"))
                .values("period")
                .annotate(count=Count("id"))
                .order_by("period")
            )
            # Map each record to its day of the month as a string
            data_dict = {str(data["period"].day): data["count"] for data in stats}

        # Yearly statistics: current year grouped by month
        elif distance == "yearly":
            labels = [month_name[i] for i in range(1, 13)]
            stats = (
                model.objects.filter(created_at__year=now().year)
                .annotate(period=TruncMonth("created_at"))
                .values("period")
                .annotate(count=Count("id"))
                .order_by("period")
            )
            data_dict = {data["period"].strftime("%B"): data["count"] for data in stats}

        else:
            return Response(
                {"success": False, "message": "Invalid distance parameter"},
                status=status.HTTP_400_BAD_REQUEST,
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
