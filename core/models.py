from django.db import models

class Groupe(models.Model):
  nom = models.CharField(max_length=100)
  montant_cotisation = models.DecimalField(max_digits=10, decimal_places=2)
  date_creation = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.nom


class Membre(models.Model):
  nom = models.CharField(max_length=100)
  prenom = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  groupes = models.ManyToManyField(Groupe, related_name="membres")

  def __str__(self):
    return f"{self.prenom} {self.nom}"
  

class Cycle(models.Model):
  STATUT_CHOICES = [
    ('en_cours', 'En cours'),
    ('termine', 'Terminé'),
  ]
  date_debut = models.DateField()
  groupe = models.ForeignKey(Groupe, on_delete=models.CASCADE, related_name="cycles")
  statut = models.CharField(max_length=100, choices=STATUT_CHOICES, default='en_cours')

class Cotisation(models.Model):
  STATUT_CHOICES = [
    ('paye', 'Payé'),
    ('non_paye', 'Non Payé'),
  ]
  membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name="cotisations")
  cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name="cotisations")
  statut = models.CharField(max_length=100, choices=STATUT_CHOICES, default='non_paye')
  date_paiement = models.DateField(null=True, blank=True)


class Tour(models.Model):
  STATUT_CHOICES = [
    ('verse', 'Versé'),
    ('non_verse', 'Non versé'),
  ]
  membre = models.ForeignKey(Membre, on_delete=models.CASCADE, related_name='tours')
  cycle = models.OneToOneField(Cycle, on_delete=models.CASCADE, related_name='tour')
  statut = models.CharField(max_length=100, choices=STATUT_CHOICES, default='non_verse')

