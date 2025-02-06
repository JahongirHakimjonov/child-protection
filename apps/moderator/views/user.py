from django.db.models import Q
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.moderator.serializers.user import ModeratorUserSerializer
from apps.shared.exceptions.http404 import get_object_or_404
from apps.shared.pagination.custom import CustomPagination
from apps.shared.permissions.admin import IsAdmin
from apps.users.models.users import User


class ModeratorUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = ModeratorUserSerializer

    def get_queryset(self):
        return User.objects.all()

    def get(self, request):
        search = request.query_params.get("search")
        is_active = request.query_params.get("is_active")
        role = request.query_params.get("role")
        queryset = self.get_queryset()

        tf = {"true": True, "false": False}
        if is_active is not None:
            queryset = queryset.filter(is_active=tf.get(is_active.lower(), None))

        if role:
            queryset = queryset.filter(role=role)

        if search:
            search_terms = search[:100].split()
            query = Q()
            for search_term in search_terms:
                query &= (
                        Q(phone__icontains=search_term)
                        | Q(username__icontains=search_term)
                        | Q(role__icontains=search_term)
                )
            queryset = queryset.filter(query)
        paginator = CustomPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(
            paginated_queryset, many=True, context={"rq": request}
        )
        return paginator.get_paginated_response(serializer.data)

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

    @extend_schema(
        operation_id="moderator_user_detail_get",
    )
    def get(self, request, pk):
        user = get_object_or_404(User, pk)
        serializer = self.serializer_class(user)
        return Response(
            {
                "success": True,
                "message": "User detail",
                "data": serializer.data,
            }
        )

    @extend_schema(
        operation_id="moderator_user_detail_patch",
    )
    def patch(self, request, pk):
        user = get_object_or_404(User, pk)
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
        return Response(
            {
                "success": False,
                "message": "Some error",
                "data": serializer.errors
            }
        )

    @extend_schema(
        operation_id="moderator_user_detail_delete",
    )
    def delete(self, request, pk):
        user = get_object_or_404(User, pk)
        user.delete()
        return Response({"success": True, "message": "User deleted"})
