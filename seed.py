import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tontine.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Membre, Groupe, Cycle
from faker import Faker
import random
from datetime import date

fake = Faker('fr_FR')

# --- Nettoyage ---
Cycle.objects.all().delete()
Groupe.objects.all().delete()
Membre.objects.all().delete()
User.objects.filter(is_superuser=False).delete()

# --- Création membres ---
membres = []
for _ in range(20):
  user = User.objects.create_user(
    username=fake.user_name(),
    password='password123',
    email=fake.email()
  )

  membre = Membre.objects.create(
    nom=fake.last_name(),
    prenom=fake.first_name(),
    email=user.email,
    user=user
  )
  membres.append(membre)

# --- Création groupes ---
groupes = []
for _ in range(3):
  groupe = Groupe.objects.create(
    nom=f"Tontine {fake.city()}",
    montant_cotisation=random.choice([10000, 25000, 50000])
  )
  groupes.append(groupe)

# --- Ajout membres aux groupes ---
for groupe in groupes:
  membres_choisis = random.sample(membres, k=random.randint(5, 10))
  for membre in membres_choisis:
    groupe.membres.add(membre)

# --- Création cycles ---
for groupe in groupes:
  Cycle.objects.create(
    groupe=groupe,
    date_debut = date.today(),
    statut='en_cours'
  )

print("Seed terminé.")
print(f"Membres: {Membre.objects.count()}")
print(f"Groupes: {Groupe.objects.count()}")
print(f"Cycles: {Cycle.objects.count()}")

