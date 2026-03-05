from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Membre


@login_required
def liste(request):
  membre = get_object_or_404(Membre, user=request.user)
  groupes = membre.groupes.all()
  return HttpResponse(f"{groupes}")