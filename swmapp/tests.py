from django.test import TestCase
from django.core import mail
from swmapp.models import WasteUpdates, HarithakarmaReg, LoginTable, Public_Dustbin_Register
from decimal import Decimal

class WasteUpdateSignalTest(TestCase):
    def setUp(self):
        # Create or get the necessary related models
        self.login = LoginTable.objects.create(email='test_harithasena@example.com', municipality='MunicipalityX')
        self.dustbin = Public_Dustbin_Register.objects.create(dustbin_id="1234", location="Some Location")
        self.harithakarma_reg = HarithakarmaReg.objects.create(login_id=self.login, municipality='MunicipalityX')

    def test_send_email_on_full_dustbin(self):
        # Create WasteUpdate instance with weight >= 100kg
        waste_update = WasteUpdates.objects.create(
            login_id=self.login,
            dustbin_id=self.dustbin,
            weight=Decimal('100.00'),  # 100 kg weight
            reward="Thank you for reporting."
        )

        # Check that one email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check email subject and recipient
        email = mail.outbox[0]
        self.assertEqual(email.subject, f'Dustbin ID {waste_update.dustbin_id} is Full')
        self.assertEqual(email.to, ['test_harithasena@example.com'])  # Email of Harithasena
        self.assertIn('The dustbin with ID', email.body)  # Check if the message contains the correct content

