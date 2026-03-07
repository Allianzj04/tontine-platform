from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cycle, Cotisation

@receiver(post_save, sender=Cycle)
def creer_cotisations(sender, instance, created, **kwargs):
  if created:
    groupe = instance.groupe
    membres = groupe.membres.all()
    for membre in membres:
      cotisation = Cotisation.objects.create(membre=membre, cycle=instance)