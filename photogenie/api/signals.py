from django.db.models.signals import Signal
from django.dispatch import receiver

increment_views_signal = Signal()


@receiver(increment_views_signal)
def increment_post_views(sender, instance, **kwargs):
    instance.views += 1
    instance.save()

