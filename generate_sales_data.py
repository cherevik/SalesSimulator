import datetime

import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def weighted_pick(weights, n_picks):
    t = np.cumsum(weights)
    s = np.sum(weights)
    return np.searchsorted(t, np.random.rand(n_picks) * s)


stages = [('Contact Initiated', 0, 0),
          ('Discovery Meeting with Initiator', 0.9, 14),
          ('Discovery Meeting with Champion', 0.9, 5),
          ('Demo with Champion/Decider', 0.85, 13),
          ('Demo with Members of the Broader Team', 0.85, 14),
          ('Workshop with Group of Stakeholders', 0.85, 24),
          ('Proof of Concept', 0.8, 38),
          ('Meeting to Address Issues from PoC', 0.98, 3),
          ('Meeting with Gatekeeper', 0.9, 12),
          ('Meeting to Address Concerns', 0.98, 7),
          ('Meeting to Discuss Deliverables', 0.96, 17),
          ('Proposal/Agreement on Price', 0.98, 10),
          ('Proposal/Agreement on Terms', 0.99, 7)]

closed_stages = ['Closed Won', 'Closed Lost']
success_stages = ['Closed Won']

WORDS = open('/usr/share/dict/words', 'rb').read().splitlines()
NUM_YEARS = 3
NUM_POINTS = 300
AVERAGE_SALE_PRICE = 50000
SD_SALE_PRICE = 10000

opportunities = [(entry.title(), np.random.normal(AVERAGE_SALE_PRICE, SD_SALE_PRICE))
                 for entry in np.random.choice(WORDS, NUM_POINTS, replace=False)]

start_date = datetime.datetime.now() - datetime.timedelta(days=365 * NUM_YEARS)

y = [float(entry) / 365. for entry in range(365 * NUM_YEARS)]
days = weighted_pick(np.exp(y), NUM_POINTS)

sales_data = [[stages[0][0], name_value_pair[0], name_value_pair[1], start_date + datetime.timedelta(days=days)]
              for name_value_pair, days in zip(opportunities, days.astype(float))]

remaining_opportunities_frame = pd.DataFrame(sales_data)
remaining_opportunities_frame.columns = ['Stage', 'Name', 'Value', 'Date']

sales_data_frame = pd.DataFrame(sales_data)
sales_data_frame.columns = ['Stage', 'Name', 'Value', 'Date']

finished_list = set([])

for stage_index, stage in enumerate(stages[1:]):
    p_no_meeting = (1. - 1 / stage[2])
    p_success = stage[1] / stage[2]
    p_failure = (1. - stage[1]) / stage[2]
    next_stage = pd.DataFrame([(sales_opp[1], index, np.argmax(entry)) for sales_opp in sales_data
                               for index, entry in enumerate(np.random.multinomial(1, [p_no_meeting, p_success, p_failure], (datetime.datetime.now() - sales_opp[3]).days))
                               if entry[0] != 1 and sales_opp[1] not in finished_list])

    next_stage.columns = ['Name', 'Days', 'Status']
    next_stage = next_stage.loc[next_stage.groupby('Name').Days.idxmin()]

    tempy_frame = next_stage.merge(remaining_opportunities_frame[['Name', 'Value', 'Date']], how='inner', on='Name')
    tempy_frame['Date'] = tempy_frame.apply(lambda x: x.Date + datetime.timedelta(days=x.Days), axis=1)

    success_frame = tempy_frame[tempy_frame.Status == 1].drop(['Status', 'Days'], 1)
    success_frame.insert(0, 'Stage', stages[stage_index + 1][0] if stage_index + 1 < len(stages) - 1 else success_stages[0])

    failure_frame = tempy_frame[tempy_frame.Status == 2].drop(['Status', 'Days'], 1)
    failure_frame.insert(0, 'Stage', closed_stages[1])

    sales_data_frame = sales_data_frame.append(success_frame).append(failure_frame)

    finished_frame = sales_data_frame.groupby('Name').apply(lambda x: x.Stage.isin(closed_stages).any())
    finished_list = set(finished_list).union(set(finished_frame[finished_frame].index.values))
    remaining_opportunities = remaining_opportunities_frame[~remaining_opportunities_frame.Name.isin(finished_list)]


## Plot overall company revenue
deals_frame = sales_data_frame[sales_data_frame.Stage == success_stages[0]].sort_values('Date')
dates = matplotlib.dates.date2num(deals_frame.Date)
revenue = deals_frame.Value.cumsum().values

plt.plot_date(dates, revenue, 'b-')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Company revenue over time')
plt.xticks(rotation=-45)
plt.show()
