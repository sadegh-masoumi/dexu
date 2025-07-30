import re

from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from node.domain import process_user_relations
from node.serializers import RelationCreateSerializer, RelationCreateResponseSerializer


class CreateRelationView(APIView):

    @swagger_auto_schema(
        request_body=RelationCreateSerializer,
        responses={
            201: openapi.Response(
                description="Relations created or updated successfully.",
                schema=RelationCreateResponseSerializer
            ),
        }
    )
    def post(self, request):
        serializer = RelationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        data = serializer.validated_data["data"]

        result = process_user_relations(username, data)

        response_serializer = RelationCreateResponseSerializer(result)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)