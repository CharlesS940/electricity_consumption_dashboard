from django.test import Client as DjClient
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from dashboard.models import Client


class HttpCodeTestCase(TestCase):
    def setUp(self):
        self.djclient = DjClient()
        User = get_user_model()
        self.user = User.objects.create_user(username='admin', password='adminpass', is_staff=True)
        self.djclient.login(username='admin', password='adminpass')

    def assertSuccess(self, response, msg_prefix):
        status_code = response.status_code
        failure_msg = (
            msg_prefix and msg_prefix + " " or ""
        ) + f"expected success status code (200-299)"
        self.assertGreaterEqual(status_code, 200, failure_msg)
        self.assertLess(status_code, 300, failure_msg)

    def assertGet(self, path):
        response = self.djclient.get(path)
        self.assertSuccess(response, f"{path}")

    def assert404(self, path):
        response = self.djclient.get(path)
        self.assertEqual(response.status_code, 404)

    def test_clients_list_view(self):
        path = "/admin/clients"
        self.assertGet(path)

    def test_404_consumption_view(self):
        client_id = 0
        path = reverse("dashboard:consumption_details", kwargs={"client_id": client_id})
        self.assert404(path)

    def test_consumption_view(self):
        clients_ids = Client.objects.values_list("pk", flat=True)
        for cid in clients_ids:
            path = reverse("dashboard:consumption_details", kwargs={"client_id": cid})
            self.assertGet(path)
