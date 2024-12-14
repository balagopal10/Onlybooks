from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order, UserProfile

@receiver(post_save, sender=Order)
def increment_orders_this_month(sender, instance, created, **kwargs):
    if created:
        try:
            user_profile = UserProfile.objects.get(user=instance.user)
            user_profile.orders_this_month += 1
            user_profile.save()
        except UserProfile.DoesNotExist:
            pass  # Handle the case where the UserProfile is missing
            