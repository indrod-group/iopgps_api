from django_filters import FilterSet
from .models import Route

class RouteFilter(FilterSet):
    class Meta:
        model = Route
        fields = ['name']
