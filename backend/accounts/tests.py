from django.test import TestCase

# Create your tests here.
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import Membership, Organization


User = get_user_model()


class AuthenticationApiTests(APITestCase):
    def test_registration_login_and_profile(self):
        registration = self.client.post(
            reverse('register'),
            {
                'username': 'apiuser',
                'email': 'api@example.com',
                'password': 'strong-password-123',
            },
            format='json',
        )
        self.assertEqual(registration.status_code, status.HTTP_201_CREATED)

        login = self.client.post(
            reverse('token_obtain_pair'),
            {'email': 'api@example.com', 'password': 'strong-password-123'},
            format='json',
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn('access', login.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        profile = self.client.get(reverse('profile'))
        self.assertEqual(profile.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.data['email'], 'api@example.com')


class OrganizationApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='strong-password-123',
        )
        self.client.force_authenticate(self.user)

    def test_create_organization_assigns_owner_membership(self):
        response = self.client.post(
            reverse('organization-list'),
            {'name': 'Acme Corporation'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        organization = Organization.objects.get(name='Acme Corporation')
        self.assertEqual(organization.slug, 'acme-corporation')
        self.assertTrue(
            Membership.objects.filter(
                user=self.user,
                organization=organization,
                role='OWNER',
            ).exists()
        )

    def test_unrelated_organization_is_not_visible(self):
        own_org = Organization.objects.create(name='Own Org', slug='own-org')
        Membership.objects.create(user=self.user, organization=own_org, role='OWNER')
        Organization.objects.create(name='Other Org', slug='other-org')

        response = self.client.get(reverse('organization-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        names = [item['name'] for item in response.data['results']]
        self.assertEqual(names, ['Own Org'])
