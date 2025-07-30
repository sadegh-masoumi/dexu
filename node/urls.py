# urls.py
from django.urls import path
from .views import CreateRelationView

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Relation API",
      default_version='v1',
      description="API to create Node-Relation from @mentions",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/create-relation/', CreateRelationView.as_view(), name='create-relation'),

    # Swagger UI
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
