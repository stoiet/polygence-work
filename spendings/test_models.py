from django.test import TestCase

from spendings.models import Spendings

AMOUNT = 1200.00
CURRENCY = "HUF"
DESCRIPTION = "test"

class SpendingsTestCase(TestCase):
    def setUp(self):
        Spendings.objects.create(amount=AMOUNT, currency=CURRENCY, description=DESCRIPTION)

    def test_spending_have_amount_field(self):
        spending = Spendings.objects.latest('created_at')
        self.assertEqual(spending.amount, AMOUNT)

    def test_spending_have_currency_field(self):
        spending = Spendings.objects.latest('created_at')
        self.assertEqual(spending.currency, CURRENCY)

    def test_spending_have_description_field(self):
        spending = Spendings.objects.latest('created_at')
        self.assertEqual(spending.description, DESCRIPTION)