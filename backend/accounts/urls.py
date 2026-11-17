
from accounts.views import OrganizationViewSet, RegisterView, UserProfileView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(
    r'organizations',
    OrganizationViewSet,
    basename='organization'
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
]
