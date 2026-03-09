from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Membre, Groupe, Cycle, Cotisation
from .forms import InscriptionForm, GroupeForm, AjouterMembreForm, CycleForm


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


def inscription(request):
  if request.method == 'POST':
    form = InscriptionForm(request.POST)
    if form.is_valid():
      user = form.save()
      Membre.objects.create(
        user=user,
        nom = form.cleaned_data['nom'],
        prenom = form.cleaned_data['prenom'],
        email = form.cleaned_data['email'],
      )
      return redirect('login')
  else:
    form = InscriptionForm()
  return render(request, 'core/inscription.html', {'form': form})

@login_required
def creer_groupe(request):
  if request.method == 'POST':
    form = GroupeForm(request.POST)
    if form.is_valid():
      groupe = form.save()
      user = request.user
      membre = get_object_or_404(Membre, user=user)
      membre.groupes.add(groupe)
      return redirect('liste_groupes')
  else:
    form = GroupeForm()
  return render(request, 'core/creer_groupe.html', {'form': form})


@login_required
def ajouter_membre(request, pk):
  if request.method == 'POST':
    form = AjouterMembreForm(request.POST)
    if form.is_valid():
      membre = form.cleaned_data['membre']
      groupe = get_object_or_404(Groupe, id=pk)
      groupe.membres.add(membre)
      return redirect('detail_groupe', pk)
  else:
    form = AjouterMembreForm()
  return render(request, 'core/ajouter_membre.html', {'form': form})


@login_required
def creer_cycle(request, pk):
  if request.method == 'POST':
    form = CycleForm(request.POST)
    if form.is_valid():
      cycle = form.save(commit=False)
      groupe = get_object_or_404(Groupe, id=pk)
      cycle.groupe = groupe
      cycle.save()
      return redirect('detail_groupe', pk)
  else:
    form = CycleForm()
  return render(request, 'core/creer_cycle.html', {'form': form})