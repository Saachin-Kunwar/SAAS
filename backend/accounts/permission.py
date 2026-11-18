from accounts.models import Membership
from rest_framework import permissions


class IsOrganizationOwnerOrAdmin(permissions.BasePermission):
  """Allows access only to users who are Owners or Admins of the active organization."""

  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False

    # Superusers bypass organization checks
    if request.user.is_superuser:
      return True

    # Extract active organization from header
    org_id = request.headers.get('X-Organization-ID')
    if not org_id:
      return False

    # Check if user has OWNER or ADMIN role in this organization
    return Membership.objects.filter(
        user=request.user, organization_id=org_id, role__in=['OWNER', 'ADMIN']
    ).exists()


class IsSalesRepresentativeOrAbove(permissions.BasePermission):
  """Allows access to Sales Reps, Managers, Admins, and Owners."""

  def has_permission(self, request, view):
    if not request.user or not request.user.is_authenticated:
      return False

    if request.user.is_superuser:
      return True

    org_id = request.headers.get('X-Organization-ID')
    if not org_id:
      return False

    # Check if user has a valid membership in this org
    return Membership.objects.filter(
        user=request.user, organization_id=org_id
    ).exists()