from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import CustomUser
from businessmodel.models import Investor

@receiver(post_save, sender=CustomUser)
def create_investor(sender, instance, created, **kwargs):
    if created and not instance.is_farmer:  # Only create an investor if NOT a farmer
        Investor.objects.create(user=instance)
