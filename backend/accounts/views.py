from accounts.models import Membership, Organization, User
from accounts.serializers import(OrganizationSerializer, RegisterSerializer, UserSerializer,)
from rest_framework import generic, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class RegisterView(generics.CreateAPIView):
    #API endpoint for user registration
    queryset= User.onjects.all()
    serializer_class= RegisterSerializer
    permission_classes=[permissions.AllowAny] #anyone can register

class UserProfileView(APIView):
    # api endpoint to get the currently loggin user profile
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        serializer= UserSerializer(request.user)
        return Response(serializer.data)
    
class OrganizationViewSer(viewsets.ModelViewSet):
    #api endpoint for managing organizations and membership

    serializer_class= OrganizationSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
    # Users can only see organizations they belong to
    user = self.request.user
    if user.is_superuser:
      return Organization.objects.all()
    user_org_ids = user.memberships.values_list('organization_id', flat=True)
    return Organization.objects.filter(id__in=user_org_ids)


    def perform_create(self, serializer):
    # When an organization is created, automatically make the creator an 'OWNER'
    organization = serializer.save()
    Membership.objects.create(
        user=self.request.user, organization=organization, role='OWNER'
    )

   
