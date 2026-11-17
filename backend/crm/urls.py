from crm.views import (
    ActivityLogViewSet,
    ContactViewSet,
    CustomerViewSet,
    DealViewSet,
    LeadViewSet,
    TaskViewSet,
)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'contacts', ContactViewSet, basename='contact')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'deals', DealViewSet, basename='deal')
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'activities', ActivityLogViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
]