
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Email as primary login instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Organization(models.Model):
    # Represent company in SaaS multi-tenant
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Membership(models.Model):

    ROLE_CHOICES = (
        ('OWNER', 'Organization Owner'),
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('SALES_REP', 'Sales Representative'),
        ('STAFF', 'Staff'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='memberships'
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='members'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='SALES_REP'
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'organization')

    def __str__(self):
        return f'{self.user.email} - {self.organization.name} ({self.role})'
