import pandas as pd
from matplotlib import pyplot as plt

from sales_simulator import SalesSimulator, average_cycle_length

NUM_OPPORTUNITIES = 500

in_person = [('Discovery Meeting with Initiator', 0.8, 14),
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
in_person_cycle = average_cycle_length(in_person)
in_person_opportunities = NUM_OPPORTUNITIES

remote = [('Discovery Meeting with Initiator', 0.85, 14),
          ('Discovery Meeting with Champion', 0.95, 5),
          ('Demo with Champion/Decider', 0.95, 3),
          ('Demo with Members of the Broader Team', 0.90, 14),
          ('Workshop with Group of Stakeholders', 0.90, 14),
          ('Proof of Concept', 0.85, 28),
          ('Meeting to Address Issues from PoC', 0.98, 3),
          ('Meeting with Gatekeeper', 0.9, 2),
          ('Meeting to Address Concerns', 1.0, 7),
          ('Meeting to Discuss Proposal', 0.96, 17),
          ('Proposal/Agreement on Price', 0.98, 10),
          ('Proposal/Agreement on Terms', 0.99, 7)]
remote_cycle = average_cycle_length(remote)
remote_opportunities = int(NUM_OPPORTUNITIES * in_person_cycle / remote_cycle)

remote_and_meetingless = [('Discovery Meeting with Initiator', 0.85, 14),
                          ('Discovery Meeting with Champion', 0.95, 5),
                          ('Meetingless Demo and Offer Discussion', 0.95, 7),
                          ('Proof of Concept', 0.85, 28),
                          ('Meeting to Address Issues from PoC', 0.98, 3),
                          ('Meeting with Gatekeeper', 0.9, 2),
                          ('Meeting to Address Concerns', 1.0, 7),
                          ('Meetingless Discussion of Proposal', 0.96, 7),
                          ('Proposal/Agreement on Price', 0.98, 10),
                          ('Proposal/Agreement on Terms', 0.99, 7)]
remote_and_meetingless_cycle = average_cycle_length(remote_and_meetingless)
remote_and_meetingless_opportunities = int(NUM_OPPORTUNITIES * in_person_cycle / remote_and_meetingless_cycle)

revenue = pd.DataFrame()
revenue['In-Person'] = SalesSimulator(stages=in_person,
                                      num_opportunities=in_person_opportunities).simulate()
revenue['Remote'] = SalesSimulator(stages=remote,
                                   num_opportunities=remote_opportunities).simulate()
revenue['Remote and Meetingless'] = SalesSimulator(stages=remote_and_meetingless,
                                                   num_opportunities=remote_and_meetingless_opportunities).simulate()
revenue.plot()
plt.show()
