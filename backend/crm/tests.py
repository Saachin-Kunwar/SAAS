from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Membership, Organization
from crm.models import Customer


User = get_user_model()


class CustomerApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='crmuser',
            email='crm@example.com',
            password='strong-password-123',
        )
        self.organization = Organization.objects.create(
            name='Test Org',
            slug='test-org',
        )
        Membership.objects.create(
            user=self.user,
            organization=self.organization,
            role='OWNER',
        )
        self.client.force_authenticate(self.user)

    def test_create_customer_uses_active_organization(self):
        response = self.client.post(
            '/api/crm/customers/',
            {'name': 'Acme Inc', 'industry': 'Technology'},
            HTTP_X_ORGANIZATION_ID=str(self.organization.id),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        customer = Customer.objects.get(name='Acme Inc')
        self.assertEqual(customer.organization, self.organization)
        self.assertEqual(customer.created_by, self.user)

    def test_customers_are_isolated_by_organization(self):
        other_org = Organization.objects.create(name='Other Org', slug='other-org')
        Customer.objects.create(
            organization=self.organization,
            name='Visible Customer',
            created_by=self.user,
        )
        Customer.objects.create(
            organization=other_org,
            name='Hidden Customer',
        )

        response = self.client.get(
            '/api/crm/customers/',
            HTTP_X_ORGANIZATION_ID=str(self.organization.id),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item['name'] for item in response.data['results']]
        self.assertEqual(names, ['Visible Customer'])

    def test_unknown_organization_header_is_denied(self):
        response = self.client.get(
            '/api/crm/customers/',
            HTTP_X_ORGANIZATION_ID='999999',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
