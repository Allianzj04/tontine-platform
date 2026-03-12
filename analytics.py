import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tontine.settings')
django.setup()

import pandas as pd
from core.models import Cotisation

data = Cotisation.objects.all().values(
  'id',
  'membre__nom',
  'membre__prenom',
  'cycle__groupe__nom',
  'statut',
  'date_paiement',
  'cycle__groupe__montant_cotisation'
)

df = pd.DataFrame(data)
print(df)

taux = df.groupby('cycle__groupe__nom')['statut'].value_counts(normalize=True)*100
print(taux)

df_retard = df[df['statut'] == 'non_paye']
print(df_retard)

df_paye = df[df['statut'] == 'paye']
total_groupes = df_paye.groupby('cycle__groupe__nom')['cycle__groupe__montant_cotisation'].sum()
print(total_groupes)