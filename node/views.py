import re

from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from node.serializers import RelationCreateSerializer
from node.models import Node, Relation



class CreateRelationView(APIView):

    @swagger_auto_schema(
        request_body=RelationCreateSerializer,
        responses={
            201: openapi.Response(
                description="Relations created or updated successfully.",
                examples={
                    "application/json": {
                        "origin": "alice",
                        "relations_created": [
                            "alice -> bob (new)",
                            "alice -> charlie (updated)"
                        ],
                        "destination_count": 2
                    }
                }
            ),
            400: "Invalid input"
        }
    )
    def post(self, request):
        serializer = RelationCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        data = serializer.validated_data["data"]

        origin_node, _ = Node.objects.get_or_create(name=username)

        found_usernames = set(re.findall(r'@(\w+)', data))

        relations_result = []
        for uname in found_usernames:
            if uname == username:
                continue

            destination_node, _ = Node.objects.get_or_create(name=uname)

            try:
                relation = Relation.objects.filter(
                    origin=origin_node,
                    destination=destination_node
                ).first()

                if relation:
                    relation.weight += 1
                    relation.save()
                    relations_result.append(f"{origin_node.name} -> {destination_node.name} (updated)")
                else:
                    new_relation = Relation.objects.create(
                        origin=origin_node,
                        destination=destination_node,
                        weight=1
                    )
                    relations_result.append(f"{origin_node.name} -> {destination_node.name} (new)")

            except ValidationError:
                continue

        return Response({
            "origin": origin_node.name,
            "relations_created": relations_result,
            "destination_count": len(relations_result)
        }, status=status.HTTP_201_CREATED)
