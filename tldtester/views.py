from django.shortcuts import render
from .models import TLD, RootZone
from rest_framework import serializers, viewsets
from django.db.models import Q
# Create your views here.

# REST API !
class TLDSerializer(serializers.ModelSerializer):
    class Meta:
        model = TLD
        fields = '__all__'


class TLDViewSet(viewsets.ModelViewSet):
    queryset = TLD.objects.all().order_by('-tld')
    serializer_class = TLDSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = TLD.objects.all()
        query_params = self.request.query_params.copy()

        # Remove 'format' from query_params
        query_params.pop('format', None)
        query_params.pop('page', None)

        # Construct filters dynamically
        filters = Q()
        for key, value in query_params.items():
            field_lookup = f"{key}__exact"  # Assuming exact match for simplicity
            filters &= Q(**{field_lookup: value})

        # Apply filters to queryset
        queryset = queryset.filter(filters)
        return queryset

class RootZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = RootZone
        fields = '__all__'


class RootZoneViewSet(viewsets.ModelViewSet):
    queryset = RootZone.objects.all().order_by('-name')
    serializer_class = RootZoneSerializer
    http_method_names = ['get', 'head']

    def get_queryset(self):
        queryset = RootZone.objects.all()
        query_params = self.request.query_params.copy()

        # Remove 'format' from query_params
        query_params.pop('format', None)
        query_params.pop('page', None)

        # Construct filters dynamically
        filters = Q()
        for key, value in query_params.items():
            field_lookup = f"{key}__exact"  # Assuming exact match for simplicity
            filters &= Q(**{field_lookup: value})

        # Apply filters to queryset
        queryset = queryset.filter(filters)
        return queryset