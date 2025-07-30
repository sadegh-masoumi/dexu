# urls.py
from django.urls import path
from .views import CreateRelationView

urlpatterns = [
    path('api/create-relation/', CreateRelationView.as_view(), name='create-relation'),

]
