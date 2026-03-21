import pandas as pd
import numpy as np
from core.models import Contribution


def get_analytics():
  data = Contribution.objects.all().values(
  'id',
  'member__id',
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

  rate = df.groupby('member__id')['status'].value_counts(normalize=True)*100
  df_rate_member = rate.loc[:, 'paid'].reset_index()
  df_names = df[['member__id', 'member__first_name', 'member__last_name']].drop_duplicates()
  df_rate_member = df_rate_member.merge(df_names, on='member__id')
  df_rate_member = df_rate_member.rename(columns={'proportion': 'reliability_rate'})
  df_rate_member = df_rate_member.sort_values('reliability_rate', ascending=False)
  # print(df_rate_member.columns.tolist())
  # print(df_rate_member)

  df_financial = pd.DataFrame()
  df_financial['amount_expected'] = df.groupby('cycle__group__name')['cycle__group__amount'].sum()
  df_financial['amount_paid'] = df.groupby('cycle__group__name')['amount_paid'].sum()
  df_financial['amount_missing'] = df_financial['amount_expected'] - df_financial['amount_paid']

  return {
    'participation_rate': df_rate.to_dict(),
    'defaulters': df_defaulters.to_dict('records'), 'total_collected': total_groups.to_dict(),
    'rate_member': df_rate_member.to_dict('records'),
    'financial': df_financial.reset_index().to_dict('records') }