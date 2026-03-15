from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cycle, Contribution

@receiver(post_save, sender=Cycle)
def create_contributions(sender, instance, created, **kwargs):
  if created:
    group = instance.group
    members = group.members.all()
    for member in members:
      contribution = Contribution.objects.create(member=member, cycle=instance)