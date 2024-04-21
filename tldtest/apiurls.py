from django.urls import path, include
from rest_framework import routers, serializers, viewsets, permissions
import tldtester.views

api = routers.DefaultRouter()
api.register(r'tld', tldtester.views.TLDViewSet)
api.register(r'rootzone', tldtester.views.RootZoneViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(api.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
