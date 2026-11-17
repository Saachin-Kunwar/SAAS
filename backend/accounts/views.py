
from accounts.models import Membership, Organization, User
from accounts.serializers import (
    OrganizationSerializer,
    RegisterSerializer,
    UserSerializer,
)

from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


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
class OrganizationViewSet(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Superusers can access all organizations
        if user.is_superuser:
            return Organization.objects.all()

        # Regular users can only access organizations
        # where they have membership
        user_org_ids = user.memberships.values_list(
            'organization_id',
            flat=True
        )

        return Organization.objects.filter(id__in=user_org_ids)

    def perform_create(self, serializer):
        # Save the organization
        organization = serializer.save()

        # Automatically make the creator an OWNER
        Membership.objects.create(
            user=self.request.user,
            organization=organization,
            role='OWNER'
        )
