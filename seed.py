import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tontine.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Member, Group, Cycle
from faker import Faker
import random
from datetime import date

fake = Faker('en_US')

# --- Cleanup ---
Cycle.objects.all().delete()
Group.objects.all().delete()
Member.objects.all().delete()
User.objects.filter(is_superuser=False).delete()

# --- Create members ---
members = []
for _ in range(20):
  user = User.objects.create_user(
    username=fake.user_name(),
    password='password123',
    email=fake.email()
  )

  member = Member.objects.create(
    first_name=fake.first_name(),
    last_name=fake.last_name(),
    email=user.email,
    user=user
  )
  members.append(member)

# --- Create groups ---
groups = []
for _ in range(3):
  group = Group.objects.create(
    name=f"Tontine {fake.city()}",
    amount=random.choice([10000, 25000, 50000])
  )
  groups.append(group)

# --- Assign members to groups ---
for group in groups:
  selected_members = random.sample(members, k=random.randint(5, 10))
  for member in selected_members:
    group.members.add(member)

# --- Create cycles ---
for group in groups:
  Cycle.objects.create(
    group=group,
    start_date = date.today(),
    status='active'
  )

print("Seed completed.")
print(f"Members: {Member.objects.count()}")
print(f"Groups: {Group.objects.count()}")
print(f"Cycles: {Cycle.objects.count()}")

