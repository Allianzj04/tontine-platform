import pandas as pd
import numpy as np
from core.models import Contribution


def get_analytics():
  data = Contribution.objects.all().values(
  'id',
  'member__first_name',
  'member__last_name',
  'cycle__group__name',
  'status',
  'payment_date',
  'cycle__group__amount'
)

  df = pd.DataFrame(data)
  # print(df)

  df['amount_due'] = np.where(df['status'] == 'paid', 0, df['cycle__group__amount'])
  df['amount_paid'] = np.where(df['status'] == 'paid', df['cycle__group__amount'], 0)

  df_rate = df.groupby('cycle__group__name')['status'].value_counts(normalize=True)*100
  # print(df_rate)

  df_defaulters = df[df['status'] == 'unpaid']
  # print(df_defaulters)

  df_paid = df[df['status'] == 'paid']
  total_groups = df_paid.groupby('cycle__group__name')['cycle__group__amount'].sum()
  # print(total_groups)

  return {'participation_rate': df_rate.to_dict(),'defaulters': df_defaulters.to_dict('records'), 'total_collected': total_groups.to_dict(), 'df': df }