import pandas as pd
import numpy as np
from core.models import Cotisation


def get_analytics():
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
  # print(df)

  df['montant_du'] = np.where(df['statut'] == 'paye', 0, df['cycle__groupe__montant_cotisation'])
  df['montant_verse'] = np.where(df['statut'] == 'paye', df['cycle__groupe__montant_cotisation'], 0)

  df_taux = df.groupby('cycle__groupe__nom')['statut'].value_counts(normalize=True)*100
  # print(df_taux)

  df_retard = df[df['statut'] == 'non_paye']
  # print(df_retard)

  df_paye = df[df['statut'] == 'paye']
  total_groupes = df_paye.groupby('cycle__groupe__nom')['cycle__groupe__montant_cotisation'].sum()
  # print(total_groupes)

  return {'taux_participation': df_taux.to_dict(),'retardataires': df_retard.to_dict('records'), 'total_collecte': total_groupes.to_dict(), 'df': df }