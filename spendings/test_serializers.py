from django.test import TestCase

from spendings.models import Spendings
from spendings.serializers import SpendingsSerializer

AMOUNT = 1200.00
CURRENCY = "HUF"
DESCRIPTION = "test"

class SpendingsSerializerTestCase(TestCase):
    def setUp(self):
        self.spendings_attributes = {
            "id": 1,
            "amount": AMOUNT,
            "currency": CURRENCY,
            "description": DESCRIPTION,
        }

        self.spending = Spendings.objects.create(**self.spendings_attributes)
        self.serializer = SpendingsSerializer(instance=self.spending)

    def test_contains_expected_fields(self):
        self.assertEqual(set(self.serializer.data.keys()), set(["id", "amount", "currency", "description"]))

    def test_contains_given_amount(self):
        self.assertEqual(float(self.serializer.data["amount"]), self.spendings_attributes["amount"])

    def test_contains_given_currency(self):
        self.assertEqual(self.serializer.data["currency"], self.spendings_attributes["currency"])

    def test_contains_given_description(self):
        self.assertEqual(self.serializer.data["description"], self.spendings_attributes["description"])