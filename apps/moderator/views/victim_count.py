from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.mobile.models.victim import Victim, VictimStatus


class VictimCount(APIView):
    def get(self, request):
        statuses = VictimStatus.objects.exists()
        if not statuses:
            return Response(
                {"success": False, "message": "No status found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        status_count = {}
        all_status = VictimStatus.objects.all()
        for victim_status in all_status:
            status_count[victim_status.name] = Victim.objects.filter(
                status=victim_status
            ).count()
        return Response(
            {
                "success": True,
                "message": "Victim count statistics",
                "data": status_count,
            },
            status=status.HTTP_200_OK,
        )
