from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkOrderViewSet, WorkOrderCompletionViewSet

router = DefaultRouter()
router.register(r'work-orders', WorkOrderViewSet)
router.register(r'work-order-completions', WorkOrderCompletionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
