from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Member, Group, Cycle, Contribution
from .forms import SignUpForm, GroupForm, AddMemberForm, CycleForm
from core.analytics import get_analytics


@login_required
def list_groups(request):
  member = get_object_or_404(Member, user=request.user)
  groups = member.groups.all()
  return render(request, 'core/list_groups.html', {'groups': groups})

@login_required
def detail_group(request, pk):
  group = get_object_or_404(Group, id=pk)
  cycle = Cycle.objects.filter(group=group, status='active').first()
  contributions = Contribution.objects.filter(cycle=cycle)
  members = group.members.all()
  member_contributions = []
  for member in members:
    contribution = contributions.filter(member=member).first()
    member_contributions.append((member, contribution))
  
  if request.method == "POST":
    contribution_id = request.POST.get("contribution_id")
    contribution_paid = get_object_or_404(Contribution, id=contribution_id)
    contribution_paid.status = "paid"
    contribution_paid.save()
    return redirect('detail_group', pk)

  return render(request, 'core/detail_group.html', {'members': members, 'cycle': cycle, 'member_contributions': member_contributions, 'group': group})


def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      Member.objects.create(
        user=user,
        name = form.cleaned_data['name'],
        last_name = form.cleaned_data['last_name'],
        email = form.cleaned_data['email'],
      )
      return redirect('login')
  else:
    form = SignUpForm()
  return render(request, 'core/signup.html', {'form': form})

@login_required
def create_group(request):
  if request.method == 'POST':
    form = GroupForm(request.POST)
    if form.is_valid():
      group = form.save()
      user = request.user
      member = get_object_or_404(Member, user=user)
      member.groups.add(group)
      return redirect('list_groups')
  else:
    form = GroupForm()
  return render(request, 'core/create_group.html', {'form': form})


@login_required
def add_member(request, pk):
  if request.method == 'POST':
    form = AddMemberForm(request.POST)
    if form.is_valid():
      member = form.cleaned_data['member']
      group = get_object_or_404(Group, id=pk)
      group.members.add(member)
      return redirect('detail_group', pk)
  else:
    form = AddMemberForm()
  return render(request, 'core/add_member.html', {'form': form})


@login_required
def create_cycle(request, pk):
  group = get_object_or_404(Group, id=pk)
  if request.method == 'POST':
    form = CycleForm(request.POST)
    if form.is_valid():
      cycle = form.save(commit=False)
      cycle.group = group
      cycle.save()
      return redirect('detail_group', pk)
  else:
    form = CycleForm()
  return render(request, 'core/create_cycle.html', {'form': form, 'group': group})


@login_required
def dashboard(request):
  data = get_analytics()
  return render(request, 'core/dashboard.html', data)