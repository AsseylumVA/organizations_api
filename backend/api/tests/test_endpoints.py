from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from users.models import Organization, OrganizationUser

User = get_user_model()
Path_organizations = "/api/organizations/"
Path_users = "/api/users/"


class UrlTests(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = User.objects.create_user("testuser")
        for i in range(5):
            Organization.objects.create(
                name=f"name{i}", description=f"test{i}"
            )

    def setUp(self) -> None:
        self.guest_client = APIClient()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_organizations_get_unauthorized(self):
        response = self.guest_client.get(Path_organizations)
        self.assertEqual(response.status_code, 401)

    def test_organizations_get(self):
        response = self.client.get(Path_organizations)
        self.assertEqual(response.status_code, 200)

    def test_organizations_create(self):
        response = self.client.post(
            Path_organizations,
            {
                "name": "New organization",
                "description": "New organization description",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_organizations_create_unauthorized(self):
        response = self.guest_client.post(
            Path_organizations,
            {
                "name": "New organization",
                "description": "New organization description",
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_add_organizations_user(self):
        response = self.client.patch(
            Path_users + "me/", {"organizations": [1, 2, 3, 4, 5]}
        )
        self.assertEqual(response.status_code, 200)
        response_json = response.json()
        response_org = response_json.get("organizations")

        num_orgs = OrganizationUser.objects.filter(user=self.user).count()
        self.assertEqual(len(response_org), num_orgs)

    def test_user_create(self):
        response = self.guest_client.post(
            Path_users,
            {
                "email": "test@m.com",
                "password": "MySecretPas$word",
                "fitst_name": "first_name_1",
                "last_name": "last_name_1",
                "organizations": [1, 2, 3],
            },
        )
        self.assertEqual(response.status_code, 201)
        response_json = response.json()
        email = response_json.get("email")
        user = User.objects.filter(email=email).first()

        response_org = response_json.get("organizations")
        num_orgs = OrganizationUser.objects.filter(user=user).count()

        self.assertEqual(len(response_org), num_orgs)
