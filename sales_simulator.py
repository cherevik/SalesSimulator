import datetime
from typing import List, Tuple

import numpy as np
import pandas as pd


def weighted_pick(weights, n_picks):
    t = np.cumsum(weights)
    s = np.sum(weights)
    return np.searchsorted(t, np.random.rand(n_picks) * s)


def average_cycle_length(stages: List[Tuple[str, float, int]]):
    average_length = 0
    total_length = 0
    prob = 1.0
    for stage in stages:
        total_length += stage[2]
        average_length += total_length * prob * (1. - stage[1])
        prob = prob * stage[1]
    average_length += total_length * prob
    return average_length


class SalesSimulator(object):
    closed_stages = ['Closed Won', 'Closed Lost']
    success_stages = ['Closed Won']

    def __init__(self,
                 stages: List[Tuple[str, float, int]],
                 num_years: int = 3,
                 num_opportunities: int = 300,
                 average_sales_price: float = 100000.0,
                 sales_price_std: float = 20000.0):
        self.stages = stages
        words = open('/usr/share/dict/words', 'rb').read().splitlines()
        opportunities = [(entry.title(), np.random.normal(average_sales_price, sales_price_std))
                         for entry in np.random.choice(words, num_opportunities, replace=False)]

        y = [float(entry) / 365. for entry in range(365 * num_years)]
        days = weighted_pick(np.exp(y), num_opportunities)
        start_date = datetime.datetime.now() - datetime.timedelta(days=365 * num_years)

        self.sales_data = [
            ['Contact Initiated', name_value_pair[0], name_value_pair[1], start_date + datetime.timedelta(days=days)]
            for name_value_pair, days in zip(opportunities, days.astype(float))]

    def single_run(self) -> pd.DataFrame:
        remaining_opportunities_frame = pd.DataFrame(self.sales_data)
        remaining_opportunities_frame.columns = ['Stage', 'Name', 'Value', 'Date']

        sales_data_frame = pd.DataFrame(self.sales_data)
        sales_data_frame.columns = ['Stage', 'Name', 'Value', 'Date']

        finished_list = set([])

        for stage_index, stage in enumerate(self.stages):
            p_no_meeting = (1. - 1 / stage[2])
            p_success = stage[1] / stage[2]
            p_failure = (1. - stage[1]) / stage[2]
            next_stage = pd.DataFrame([(sales_opp[1], index, np.argmax(entry)) for sales_opp in self.sales_data
                                       for index, entry in enumerate(np.random.multinomial(1, [p_no_meeting, p_success, p_failure], (datetime.datetime.now() - sales_opp[3]).days))
                                       if entry[0] != 1 and sales_opp[1] not in finished_list],
                                      columns=['Name', 'Days', 'Status'])
            next_stage = next_stage.loc[next_stage.groupby('Name').Days.idxmin()]

            tempy_frame = next_stage.merge(remaining_opportunities_frame[['Name', 'Value', 'Date']], how='inner', on='Name')
            tempy_frame['Date'] = tempy_frame.apply(lambda x: x.Date + datetime.timedelta(days=x.Days), axis=1)

            success_frame = tempy_frame[tempy_frame.Status == 1].drop(['Status', 'Days'], 1)
            success_frame.insert(0, 'Stage', self.stages[stage_index + 1][0] if stage_index + 1 < len(self.stages) - 1 else self.success_stages[0])

            failure_frame = tempy_frame[tempy_frame.Status == 2].drop(['Status', 'Days'], 1)
            failure_frame.insert(0, 'Stage', self.closed_stages[1])

            sales_data_frame = sales_data_frame.append(success_frame).append(failure_frame)

            finished_frame = sales_data_frame.groupby('Name').apply(lambda x: x.Stage.isin(self.closed_stages).any())
            finished_list = set(finished_list).union(set(finished_frame[finished_frame].index.values))
            remaining_opportunities = remaining_opportunities_frame[~remaining_opportunities_frame.Name.isin(finished_list)]

        return sales_data_frame

    def simulate(self, n_iterations: int = 10) -> pd.Series:
        revenue_df = None
        for i in range(0, n_iterations):
            sales = self.single_run()
            deals = pd.DataFrame(sales[sales.Stage == self.success_stages[0]]).set_index('Date').sort_index()
            value = deals.resample('M')['Value'].sum()
            revenue = value.cumsum().to_frame(f'revenue_{i}')
            if revenue_df is None:
                revenue_df = revenue
            else:
                revenue_df = revenue_df.join(revenue)
        return revenue_df.mean(axis=1)
