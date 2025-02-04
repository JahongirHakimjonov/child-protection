from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from apps.users.models.users import User
from apps.moderator.serializers.user import ModeratorUserSerializer
from apps.shared.permissions.admin import IsAdmin
from apps.shared.pagination.custom import CustomPagination


class ModeratorUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorUserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get(self, request):
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")
        queryset = self.get_queryset()
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                    Q(phone__icontains=search_term)
                    | Q(username__icontains=search_term)
                    | Q(role__icontains=search_term)
                )
        paginator = CustomPagination
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(paginated_queryset, many=True)
        return Response(
            {"success": True, "message": "User list", "data": serializer.data}
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "User created", "data": serializer.data}
            )

        return Response(
            {
                "success": False,
                "message": serializer.errors,
            }
        )


class ModeratorUserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorUserSerializer

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User does not exist"})

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = self.serializer_class(data=user)
        return Response(
            {
                "success": True,
                "message": "User detail",
                "data": serializer.data,
            }
        )

    def patch(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = self.serializer_class(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "User updated",
                    "data": serializer.data,
                }
            )
        return Response({"success": False, "message": "User does not exist"})

    def delete(self, request, pk):
        user = self.get_object(pk=pk)
        user.delete()
        return Response({"success": True, "message": "User deleted"})
