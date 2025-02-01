from calendar import month_name, day_name
from collections import defaultdict
from datetime import timedelta

from django.db.models import Count
from django.db.models.functions import TruncDay, TruncMonth
from django.utils.timezone import now
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.victim import Victim
from apps.users.models.users import User


class VictimStat(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        distance = request.query_params.get("distance")
        type_ = request.query_params.get(
            "type"
        )  # "type" o'zgaruvchisi Python'da maxsus so'z

        if distance == "weekly":
            start_date = now() - timedelta(days=7)
            query_model = (
                User if type_ == "user" else Victim if type_ == "victim" else None
            )

            if query_model:
                stats = (
                    query_model.objects.filter(created_at__gte=start_date)
                    .annotate(day=TruncDay("created_at"))
                    .values("day")
                    .annotate(count=Count("id"))
                    .order_by("day")
                )

                # Default qiymat bilan bo'sh joylarni to'ldirish
                weekly_data = defaultdict(
                    int, {data["day"].strftime("%A"): data["count"] for data in stats}
                )

                response_data = {
                    "labels": [
                        day_name[i] for i in range(7)
                    ],  # ["Monday", "Tuesday", ...]
                    "info": [weekly_data[day] for day in day_name],
                }
                return Response(
                    {"success": True, "message": "Weekly stats", "data": response_data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"success": False, "message": "Invalid type parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        elif distance == "yearly":
            query_model = (
                User if type_ == "user" else Victim if type_ == "victim" else None
            )

            if query_model:
                stats = (
                    query_model.objects.filter(created_at__year=now().year)
                    .annotate(month=TruncMonth("created_at"))
                    .values("month")
                    .annotate(count=Count("id"))
                    .order_by("month")
                )

                # Default qiymat bilan bo'sh joylarni to'ldirish
                yearly_data = defaultdict(
                    int, {data["month"].month: data["count"] for data in stats}
                )

                response_data = {
                    "labels": [
                        month_name[i] for i in range(1, 13)
                    ],  # ["January", "February", ...]
                    "info": [yearly_data[i] for i in range(1, 13)],  # [0, 45, 28, ...]
                }
                return Response(
                    {"success": True, "message": "Yearly stats", "data": response_data},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"success": False, "message": "Invalid type parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"success": False, "message": "Invalid distance parameter"},
            status=status.HTTP_400_BAD_REQUEST,
        )
