from django.urls import include, path

from rest_framework import routers

from spendings.views import SpendingsViewSet

router = routers.DefaultRouter()

router.register(r'spendings', SpendingsViewSet)

urlpatterns = [
   path('', include(router.urls)),
]
