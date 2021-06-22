import datetime
from datetime import datetime as dt

import matplotlib
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def weighted_pick(weights, n_picks):
    t = np.cumsum(weights)
    s = np.sum(weights)
    return np.searchsorted(t, np.random.rand(n_picks)*s)

pre_stages = [('Contact initiated', 0.8, 10), ('Meeting booked', 0.6, 20), ('Trial booked', 0.4, 15), ('Proposal sent', 0.3, 25), ('Contract sent', 0.2, 10)]

closed_stages = ['Closed Won', 'Closed Lost']

success_stages = ['Closed Won']

WORDS = open('/usr/share/dict/words', 'rb').read().splitlines()

NUM_POINTS = 200
AVERAGE_SALE_PRICE = 3500
SD_SALE_PRICE = 1000

sales_opportunities = [(entry.title(), np.random.normal(AVERAGE_SALE_PRICE, SD_SALE_PRICE))
                       for entry in np.random.choice(WORDS, NUM_POINTS, replace=False)]

start_date = datetime.datetime.now() - datetime.timedelta(days=365*2)
days_range = range(365*2)
y = [float(entry)/365. for entry in days_range]

indices = weighted_pick(np.exp(y), NUM_POINTS)

sales_data = [[pre_stages[0][0], name_value_pair[0], name_value_pair[1], start_date + datetime.timedelta(days = index)] for name_value_pair, index in zip(sales_opportunities, indices.astype(float))]

remaining_opportunities_frame = pd.DataFrame(sales_data)
remaining_opportunities_frame.columns = ['Stage', 'Name', 'Value', 'Days']

sales_data_frame = pd.DataFrame(sales_data)
sales_data_frame.columns = ['Stage', 'Name', 'Value', 'Days']

finished_list = set([])

for stage_index, stage in enumerate(pre_stages[1:]):

    next_stage = pd.DataFrame([(sales_opp[1], index, np.argmax(entry)) for sales_opp in sales_data for index, entry in enumerate(np.random.multinomial(1, [0.99, (1. - stage[1])/100., stage[1]/100.0], (datetime.datetime.now() - sales_opp[3]).days)) if entry[0] != 1 and sales_opp[1] not in finished_list])
    next_stage.columns = ['Name', 'Days', 'Status']

    meh = next_stage.loc[next_stage.groupby('Name').Days.idxmin()]
    tempy_frame = meh.merge(remaining_opportunities_frame[['Name', 'Value', 'Days']], how='inner', on='Name')
    tempy_frame['new_date'] = tempy_frame.apply(lambda x: x.Days_y + datetime.timedelta(days=x.Days_x), axis=1)
    tempy_frame = tempy_frame[['Name', 'Value', 'new_date', 'Status']]
    tempy_frame.columns = ['Name', 'Value', 'Days', 'Status']

    success_frame = tempy_frame[tempy_frame.Status == 1]
    success_frame = success_frame.drop('Status', 1)
    success_frame.insert(0, 'Stage', pre_stages[stage_index + 1][0] if stage_index + 1 < len(pre_stages) - 1 else success_stages[0])

    failure_frame = tempy_frame[tempy_frame.Status == 2]
    failure_frame = failure_frame.drop('Status', 1)
    failure_frame.insert(0, 'Stage', closed_stages[1])

    sales_data_frame = sales_data_frame.append(success_frame).append(failure_frame)

    finished_frame = sales_data_frame.groupby('Name').apply(lambda x: x.Stage.isin(closed_stages).any())
    finished_list = set(finished_list).union(set(finished_frame[finished_frame == True].index.values))
    remaining_opportunities = remaining_opportunities_frame[~remaining_opportunities_frame.Name.isin(finished_list)]

## Plot overall company revenue
dates = matplotlib.dates.date2num(sales_data_frame[sales_data_frame.Stage == success_stages[0]].sort_values('Days').Days)
revenue = sales_data_frame[sales_data_frame.Stage == success_stages[0]].sort_values('Days').Value.cumsum().values

plt.plot_date(dates, revenue, 'b-')
plt.xlabel('Date')
plt.ylabel('Revenue')
plt.title('Company revenue over time')
plt.xticks(rotation=-45)
plt.show()
