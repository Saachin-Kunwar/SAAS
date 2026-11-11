from accounts.serializers import UserSerializer
from crm.models import ActivityLog, Contact, Customer,Deal,Load,Task
from rest_framework import serializers

class CustomerSerializer(serializers.ModelSerializer):
    #serializer for customer enterprises
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model=Customer
        fields=('id','organization','name','industry','website','phone','address','created_by','created_by_username','created_at','updated_at',)
        read_only_fields = ('id', 'organization', 'created_by', 'created_at', 'updated_at')

class ContactSerializer(serializers.ModelSerializer):
    #serializer for individual contacts associated with customers

    customer_name= serializers.ReadOnlyField(source='customer.name')
    class Meta:
        model= Contact
        fields=('id','organization','customer','customer_name','first_name','last_name','email','phone','position','created_at',)
        read_only_fields = ('id', 'organization', 'created_at')

class LeadSerializer(serializers.ModelSerializer):
    #serializer for sales leads
    class Meta:
        model=Lead
        fields=('id','organization','first_name','last_name','email','phone','company_name','status','assigned_to_username','created_at','updated_at',)
        read_only_fields=('id','organization','created_at','updated_at')

class DealSerializer(serializers.ModelSerializer):
    #serializer for sales pipeline deals

    customer_name= serializers.ReadOnlyField(source='customer.name')
    assigned_to_username= serializers.ReadOnlyField(source='assigned_to.username')

    class Meta:
        model=Deal
        fields=('id','organization','title','customer','customer_name','value','stage','expected_close_date','assigned_to','assigned_to_username','created_at','updated_at',)
        read_only_fields=('id','organization','created_at','updated_at')

class TaskSerializer(serializers.ModelSerializer):
  """Serializer for Tasks and Follow-ups."""

  assigned_to_username = serializers.ReadOnlyField(source='assigned_to.username')
  customer_name = serializers.ReadOnlyField(source='customer.name', default=None)

  class Meta:
    model = Task
    fields = (
        'id',
        'organization',
        'title',
        'description',
        'due_date',
        'is_completed',
        'assigned_to',
        'assigned_to_username',
        'customer',
        'customer_name',
        'created_at',
    )
    read_only_fields = ('id', 'organization', 'created_at')


class ActivityLogSerializer(serializers.ModelSerializer):
  """Serializer for Audit and Activity history."""

  user_username = serializers.ReadOnlyField(source='user.username', default=None)

  class Meta:
    model = ActivityLog
    fields = (
        'id',
        'organization',
        'user',
        'user_username',
        'action',
        'description',
        'created_at',
    )
    read_only_fields = ('id', 'organization', 'user', 'created_at')