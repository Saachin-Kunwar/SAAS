from accounts.models import Membership, Organization, User
from django.contrib.auth import authenticate
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    #serializer for user model
    class Meta:
        model=User
        fields = ('id','username','email','phone_number','first_name','last_name')
        read_only_fields=('id',)

class OrganizationSerializer(serializer.ModelSerializer):
    #serializers for organization model
    class Meta:
        model=Organization
        fields=('id','name','slug','created_at')
        read_only_fields=('id','created_at','slug')
    
class MembershipSerializer(serializer.ModelSerializer):
    #serializer for Membership model
    user= UserSerializer(read_only=True)
    organization= OrganizationSerializer(read_only_True)

    class Meta:
        model=Membership
        fields=('id','user','organization','role','joined_at')
        read_only_fields=('id','joined_at')

class RegisterSerializer(serializers.ModelSerializer):
    #serializer for user registration with password validation
    password= serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model=User
        fields=('username','email','password','first_name','last_name')
    
    def create(self, validation_data):
        ##create user securely using Django create_user method
        user= User.objects.create_user(
            username=validated_data['username'],
            email=validate_data['email'],
            password=validate_data['password'],
            first_name=validate_data.get('first_name',''),
            last_name=validate_data.get('last_name',''),
        )
        return user