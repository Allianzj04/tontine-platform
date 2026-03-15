from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
  name = models.CharField(max_length=100, unique=True)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  created_at = models.DateField(auto_now_add=True)

  def __str__(self):
    return self.name


class Member(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(unique=True)
  groups = models.ManyToManyField(Group, related_name="members")
  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"
  

class Cycle(models.Model):
  STATUT_CHOICES = [
    ('active', 'Active'),
    ('completed', 'Completed'),
  ]
  start_date = models.DateField()
  group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="cycles")
  status = models.CharField(max_length=100, choices=STATUT_CHOICES, default='active')

class Contribution(models.Model):
  STATUT_CHOICES = [
    ('paid', 'Paid'),
    ('unpaid', 'Unpaid'),
  ]
  member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="contributions")
  cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE, related_name="contributions")
  status = models.CharField(max_length=100, choices=STATUT_CHOICES, default='unpaid')
  payment_date = models.DateField(null=True, blank=True)


class Round(models.Model):
  STATUT_CHOICES = [
    ('paid', 'Paid'),
    ('unpaid', 'Unpaid'),
  ]
  member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='rounds')
  cycle = models.OneToOneField(Cycle, on_delete=models.CASCADE, related_name='round')
  status = models.CharField(max_length=100, choices=STATUT_CHOICES, default='unpaid')

