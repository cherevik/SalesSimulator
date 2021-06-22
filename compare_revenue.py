import pandas as pd
from matplotlib import pyplot as plt
from sales_simulator import SalesSimulator, average_cycle_length

NUM_OPPORTUNITIES = 500

before = [('Discovery Meeting with Initiator', 0.9, 14),
          ('Discovery Meeting with Champion', 0.9, 5),
          ('Demo with Champion/Decider', 0.85, 13),
          ('Demo with Members of the Broader Team', 0.85, 14),
          ('Workshop with Group of Stakeholders', 0.85, 24),
          ('Proof of Concept', 0.8, 38),
          ('Meeting to Address Issues from PoC', 0.98, 3),
          ('Meeting with Gatekeeper', 0.9, 12),
          ('Meeting to Address Concerns', 0.98, 7),
          ('Meeting to Discuss Proposal', 0.96, 17),
          ('Proposal/Agreement on Price', 0.98, 10),
          ('Proposal/Agreement on Terms', 0.99, 7)]
cycle_before = average_cycle_length(before)

after = [('Discovery Meeting with Initiator', 0.9, 14),
         ('Discovery Meeting with Champion', 0.9, 5),
         ('Meetingless Offer and Demo', 0.8, 7),
         ('Proof of Concept', 0.8, 38),
         ('Meeting to Address Issues from PoC', 0.98, 3),
         ('Meeting with Gatekeeper', 0.9, 12),
         ('Meeting to Address Concerns', 0.98, 7),
         ('Meetingless Discussion of Proposal', 0.96, 7),
         ('Proposal/Agreement on Price', 0.98, 10),
         ('Proposal/Agreement on Terms', 0.99, 7)]
cycle_after = average_cycle_length(after)

revenue = pd.DataFrame()
revenue['Before'] = SalesSimulator(stages=before, num_opportunities=NUM_OPPORTUNITIES).simulate()
revenue['After'] = SalesSimulator(stages=after, num_opportunities=int(NUM_OPPORTUNITIES*cycle_before/cycle_after)).simulate()
revenue.plot()
plt.show()
