
from accounts.models import Membership, Organization, User
from accounts.serializers import (
    OrganizationSerializer,
    RegisterSerializer,
    UserSerializer,
)

from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsOrganizationOwnerOrAdmin
from django.utils.text import slugify


# User Registration API
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


# User Profile API
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# Organization Management API
from accounts.permissions import IsOrganizationOwnerOrAdmin
# ... keep existing imports ...


class OrganizationViewSet(viewsets.ModelViewSet):
  """API endpoint for managing Organizations and Memberships (Tenants)."""

  serializer_class = OrganizationSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_permissions(self):
    """Enforce strict RBAC: Only Owners/Admins can update or delete organizations."""
    if self.action in ['update', 'partial_update', 'destroy']:
      return [permissions.IsAuthenticated(), IsOrganizationOwnerOrAdmin()]
    return [permissions.IsAuthenticated()]

  def get_queryset(self):
    user = self.request.user
    if user.is_superuser:
      return Organization.objects.all().order_by('id')
    user_org_ids = user.memberships.values_list('organization_id', flat=True)
    return Organization.objects.filter(id__in=user_org_ids).order_by('id')

  def perform_create(self, serializer):
    organization = serializer.save(slug=slugify(serializer.validated_data['name']))
    Membership.objects.create(
        user=self.request.user, organization=organization, role='OWNER'
    )
