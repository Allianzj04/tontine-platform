from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Membre, Groupe, Cycle, Cotisation


@login_required
def liste(request):
  membre = get_object_or_404(Membre, user=request.user)
  groupes = membre.groupes.all()
  return render(request, 'core/liste_groupes.html', {'groupes': groupes})

@login_required
def detail_groupe(request, pk):
  groupe = get_object_or_404(Groupe, id=pk)
  cycle = Cycle.objects.filter(groupe=groupe, statut='en_cours').first()
  cotisations = Cotisation.objects.filter(cycle=cycle)
  membres = groupe.membres.all()
  cotisation_membre = []
  for membre in membres:
    cotisation = cotisations.filter(membre=membre).first()
    cotisation_membre.append((membre, cotisation))
  if request.method == "POST":
    cotisation_id = request.POST.get("cotisation_id")
    cotisation_paye = get_object_or_404(Cotisation, id=cotisation_id)
    cotisation_paye.statut = "paye"
    cotisation_paye.save()
    return redirect('detail_groupe', pk)

  return render(request, 'core/detail_groupe.html', {'membres': membres, 'cycle': cycle, 'cotisation_membre': cotisation_membre})
