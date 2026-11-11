from accounts.models import Organization, User
from django.db import models


class Customer(models.Model):
  """Represents a client company or enterprise account."""

  organization = models.ForeignKey(
      Organization, on_delete=models.CASCADE, related_name='customers'
  )
  name = models.CharField(max_length=255)
  industry = models.CharField(max_length=100, blank=True, null=True)
  website = models.URLField(blank=True, null=True)
  phone = models.CharField(max_length=50, blank=True, null=True)
  address = models.TextField(blank=True, null=True)
  created_by = models.ForeignKey(
      User, on_delete=models.SET_NULL, null=True, related_name='created_customers'
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class Contact(models.Model):
  """Individual people working inside a Customer company."""

  organization = models.ForeignKey(
      Organization, on_delete=models.CASCADE, related_name='contacts'
  )
  customer = models.ForeignKey(
      Customer, on_delete=models.CASCADE, related_name='contacts'
  )
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField()
  phone = models.CharField(max_length=50, blank=True, null=True)
  position = models.CharField(max_length=100, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name} ({self.customer.name})'


class Lead(models.Model):
  """Potential sales prospects who are not yet converted customers."""

  STATUS_CHOICES = (
      ('NEW', 'New'),
      ('CONTACTED', 'Contacted'),
      ('QUALIFIED', 'Qualified'),
      ('LOST', 'Lost'),
      ('CONVERTED', 'Converted'),
  )

  organization = models.ForeignKey(
      Organization, on_delete=models.CASCADE, related_name='leads'
  )
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField()
  phone = models.CharField(max_length=50, blank=True, null=True)
  company_name = models.CharField(max_length=255, blank=True, null=True)
  status = models.CharField(
      max_length=20, choices=STATUS_CHOICES, default='NEW'
  )
  assigned_to = models.ForeignKey(
      User,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='assigned_leads',
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.first_name} {self.last_name} - {self.company_name or "Individual"}'


class Deal(models.Model):
  """Sales pipeline opportunities/deals being tracked."""

  STAGE_CHOICES = (
      ('DISCOVERY', 'Discovery'),
      ('PROPOSAL', 'Proposal Sent'),
      ('NEGOTIATION', 'Negotiation'),
      ('WON', 'Closed Won'),
      ('LOST', 'Closed Lost'),
  )

  organization = models.ForeignKey(
      Organization, on_delete=models.CASCADE, related_name='deals'
  )
  title = models.CharField(max_length=255)
  customer = models.ForeignKey(
      Customer, on_delete=models.CASCADE, related_name='deals'
  )
  value = models.DecimalField(
      max_digits=12, decimal_places=2, default=0.00
  )  # e.g., $50,000.00
  stage = models.CharField(
      max_length=20, choices=STAGE_CHOICES, default='DISCOVERY'
  )
  expected_close_date = models.DateField(blank=True, null=True)
  assigned_to = models.ForeignKey(
      User,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='assigned_deals',
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f'{self.title} (${self.value})'


class Task(models.Model):
  """To-dos and follow-ups assigned to users regarding deals or customers."""

  organization = models.ForeignKey(
      Organization, on_delete=models.CASCADE, related_name='tasks'
  )
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True, null=True)
  due_date = models.DateTimeField()
  is_completed = models.BooleanField(default=False)
  assigned_to = models.ForeignKey(
      User, on_delete=models.CASCADE, related_name='tasks'
  )
  customer = models.ForeignKey(
      Customer,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='tasks',
  )
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.title


class ActivityLog(models.Model):
  """Tracks audit history and activities (calls, emails, meetings) for leads/deals."""

  organization = models.ForeignKey(
      Organization, on_delete=models.CASCADE, related_name='activity_logs'
  )
  user = models.ForeignKey(
      User, on_delete=models.SET_NULL, null=True, related_name='activities'
  )
  action = models.CharField(
      max_length=255
  )  # e.g., "Called client", "Updated deal stage"
  description = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.user} - {self.action} at {self.created_at}'