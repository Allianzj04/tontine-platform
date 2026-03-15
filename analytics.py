import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tontine.settings')
django.setup()

import pandas as pd
import numpy as np
from core.models import Contribution

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

df_rate = df.groupby('cycle__group__name')['status'].value_counts(normalize=True)*100
print(df_rate)

df_defaulters = df[df['status'] == 'unpaid']
# print(df_defaulters)

df_paid = df[df['status'] == 'paid']
total_groups = df_paid.groupby('cycle__group__name')['cycle__group__amount'].sum()
# print(total_groups)

df['amount_due'] = np.where(df['status'] == 'paid', 0, df['cycle__group__amount'])
df['amount_paid'] = np.where(df['status'] == 'paid', df['cycle__group__amount'], 0)
# print(df[['member__name', 'status', 'cycle__group__amount', 'amount_due', 'amount_paid']].tail(10))

df.to_csv('contributions_analytics.csv', index=False)