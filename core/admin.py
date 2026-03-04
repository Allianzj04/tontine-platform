from django.contrib import admin
from .models import Groupe, Membre, Cotisation, Cycle, Tour


admin.site.register(Groupe)
admin.site.register(Membre)
admin.site.register(Cotisation)
admin.site.register(Cycle)
admin.site.register(Tour)
