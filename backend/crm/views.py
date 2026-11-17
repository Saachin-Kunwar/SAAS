from accounts.models import Membership
from crm.models import ActivityLog, Contact, Customer, Deal, Lead, Task
from crm.serializers import (ActivityLogSerializer,ContactSerializer,CustomerSerializer,DealSerializer, LeadSerializer,TaskSerializer,)
from rest_framework import ppermissions, viewsets
from rest_framework.exceptions import PermissionDenied

class TenanrModelViewSet(viewsets.ModelViewSet):
    permission_classes=[permissions.IsAuthenticated]

    def get_active_orginazation(self):
        #Extract the active orginazations from request headers or user memberships.
        org_ig = self.request.headers.get('X-Organization-ID')
        user= self.request.user

        if org_id:
            #verify user has membership in this organizations
            if Membership.objects.filter(user=user, organization_id=org_id).exists():
                return org_id
            raise PermissionDenied('You do not belongs to this orginazation or it does not exist.')
        #default to users first organization membership
        first_membershipp= user.memberships.first()
        if first_membership:
            return first_membership.organization.id 
        raise PermissionDenied('User does not belong to any organization.Please create or join one')

    def get_queryset(self):
        #filter queryset strictly by the active organization
        org_id = self.get_active_organization()
        return self.queryset.filter(organization_id=org_id)

    def perform_create(Self,serializer):
        #Automatically attach active organization and creates_by user opon creation
        from accounts.models import Organization

        org_id = self.get_active_organization()
        organization = Organization.objects.get(id=org_id)

        # check if model has 'created_by' or 'user' fiels
        if 'created_by' in serializer.fields:
            serializer.save(organization=organization, created_by=self.request.user)
        elif 'user' in serializer.fields:
            serializer.save(organization=organization, user=self.request.user)
        else:
            serializer.save(organization=organization)


class CustomerViewSet(TenantModelsViewSer):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ContactViewSet(TenantModelViewSet):
  queryset = Contact.objects.all()
  serializer_class = ContactSerializer


class LeadViewSet(TenantModelViewSet):
  queryset = Lead.objects.all()
  serializer_class = LeadSerializer


class DealViewSet(TenantModelViewSet):
  queryset = Deal.objects.all()
  serializer_class = DealSerializer

class TaskViewSet(TenantModelViewSet):
  queryset = Task.objects.all()
  serializer_class = TaskSerializer

class ActivityLogViewSet(TenantModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializer
    http_method_names = ['get', 'head', 'options']


