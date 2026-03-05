from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Membre, Groupe, Cycle


@login_required
def liste(request):
  membre = get_object_or_404(Membre, user=request.user)
  groupes = membre.groupes.all()
  return render(request, 'core/liste_groupes.html', {'groupes': groupes})

@login_required
def detail_groupe(request, pk):
  groupe = get_object_or_404(Groupe, id=pk)
  cycle = Cycle.objects.filter(groupe=groupe, statut='en_cours').first()
  membres = groupe.membres.all()
  return render(request, 'core/detail_groupe.html', {'membres': membres, 'cycle': cycle})
