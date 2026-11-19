from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import WasteUpdates, MuncipalityReg, LoginTable, DriverReg

@receiver(post_save, sender=WasteUpdates)
def send_email_if_weight_exceeds(sender, instance, created, **kwargs):
    if float(instance.weight) >= 100:  # Check if the weight is greater than or equal to 100kg
        # Get the municipality of the dustbin
        dustbin = instance.dustbin_id
        municipality = MuncipalityReg.objects.get(login_id=dustbin.login_id)

        # Get the driver related to the municipality
        driver = DriverReg.objects.filter(municipality=municipality).first()

        if driver:
            # Get the driver's login entry with usertype 'driver'
            driver_login = LoginTable.objects.get(id=driver.login_id.id, usertype='driver')

            # Send email to the driver
            send_mail(
                'Dustbin Weight Alert: Exceeded 100kg',
                f'Alert: The waste collected at dustbin {dustbin.dustbin_id} has exceeded 100kg.',
                'donalini120@gmail.com',  # Replace with your email address
                [driver_login.email],  # Driver's email
                fail_silently=False,
            )
