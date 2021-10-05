from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from spendings.models import Spendings


AMOUNT = 1200.00
CURRENCY = "HUF"
DESCRIPTION = "test"

class SpendingsTestCase(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()

    def test_list_spendings(self):
        Spendings.objects.create(amount=AMOUNT, currency=CURRENCY, description=DESCRIPTION)

        response = self.client.get("/api/spendings/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_spendings(self):
        response = self.client.post("/api/spendings/", {
            "amount": AMOUNT,
            "currency": CURRENCY,
            "description": DESCRIPTION,
        })

        spendings = Spendings.objects.all()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(spendings), 1)
        
    def test_update_spendings(self):
        expected_amount = 1300.00

        self.client.post("/api/spendings/", {
            "amount": AMOUNT,
            "currency": CURRENCY,
            "description": DESCRIPTION,
        })

        spending = Spendings.objects.first()

        response = self.client.put("/api/spendings/%s/" % spending.id, {
            "amount": expected_amount,
            "currency": CURRENCY,
            "description": DESCRIPTION,
        })

        spending = Spendings.objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(spending.amount, expected_amount)

    def test_delete_spendings(self):
        expected_amount = 1300.00

        self.client.post("/api/spendings/", {
            "amount": AMOUNT,
            "currency": CURRENCY,
            "description": DESCRIPTION,
        })

        spending = Spendings.objects.first()

        response = self.client.delete("/api/spendings/%s/" % spending.id)

        spendings = Spendings.objects.all()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(spendings), 0)