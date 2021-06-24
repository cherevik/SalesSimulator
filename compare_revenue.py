import pandas as pd
from matplotlib import pyplot as plt

from sales_simulator import SalesSimulator, average_cycle_length

NUM_OPPORTUNITIES = 500

in_person = [('Discovery Meeting with Initiator', 0.8, 14, 'Remote'),
             ('Discovery Meeting with Champion', 0.9, 5, 'Remote'),
             ('Demo with Champion/Decider', 0.85, 13, 'In-Person'),
             ('Demo with Members of the Broader Team', 0.85, 14, 'Remote'),
             ('Workshop with Group of Stakeholders', 0.85, 24, 'In-Person'),
             ('Proof of Concept', 0.8, 38, 'In-Person'),
             ('Meeting to Address Issues from PoC', 0.98, 3, 'Remote'),
             ('Meeting with Gatekeeper', 0.9, 12, 'In-Person'),
             ('Meeting to Address Concerns', 0.98, 7, 'Remote'),
             ('Meeting to Discuss Proposal', 0.96, 17, 'In-Person'),
             ('Proposal/Agreement on Price', 0.98, 10, 'Remote'),
             ('Proposal/Agreement on Terms', 0.99, 7, 'Remote')]
in_person_cycle = average_cycle_length(in_person)
in_person_opportunities = NUM_OPPORTUNITIES

remote = [('Discovery Meeting with Initiator', 0.85, 14, 'Remote'),
          ('Discovery Meeting with Champion', 0.95, 5, 'Remote'),
          ('Demo with Champion/Decider', 0.95, 3, 'Remote'),
          ('Demo with Members of the Broader Team', 0.90, 14, 'Remote'),
          ('Workshop with Group of Stakeholders', 0.90, 14, 'Remote'),
          ('Proof of Concept', 0.85, 28, 'Remote'),
          ('Meeting to Address Issues from PoC', 0.98, 3, 'Remote'),
          ('Meeting with Gatekeeper', 0.9, 2, 'Remote'),
          ('Meeting to Address Concerns', 1.0, 7, 'Remote'),
          ('Meeting to Discuss Proposal', 0.96, 17, 'Remote'),
          ('Proposal/Agreement on Price', 0.98, 10, 'Remote'),
          ('Proposal/Agreement on Terms', 0.99, 7, 'Remote')]
remote_cycle = average_cycle_length(remote)
remote_opportunities = int(NUM_OPPORTUNITIES * in_person_cycle / remote_cycle)

remote_and_meetingless = [('Discovery Meeting with Initiator', 0.85, 14, 'Remote'),
                          ('Discovery Meeting with Champion', 0.95, 5, 'Remote'),
                          ('Meetingless Demo and Offer Discussion', 0.95, 7, 'Meetingless'),
                          ('Proof of Concept', 0.85, 28, 'Remote'),
                          ('Meeting to Address Issues from PoC', 0.98, 3, 'Remote'),
                          ('Meeting with Gatekeeper', 0.9, 2, 'Remote'),
                          ('Meeting to Address Concerns', 1.0, 7, 'Remote'),
                          ('Meetingless Discussion of Proposal', 0.96, 7, 'Meetingless'),
                          ('Proposal/Agreement on Price', 0.98, 10, 'Remote'),
                          ('Proposal/Agreement on Terms', 0.99, 7, 'Remote')]
remote_and_meetingless_cycle = average_cycle_length(remote_and_meetingless)
remote_and_meetingless_opportunities = int(NUM_OPPORTUNITIES * in_person_cycle / remote_and_meetingless_cycle)

revenue = pd.DataFrame()
revenue['In-Person'] = SalesSimulator(stages=in_person,
                                      num_opportunities=in_person_opportunities).simulate()
revenue['Remote'] = SalesSimulator(stages=remote,
                                   num_opportunities=remote_opportunities).simulate()
revenue['Remote and Meetingless'] = SalesSimulator(stages=remote_and_meetingless,
                                                   num_opportunities=remote_and_meetingless_opportunities).simulate()
revenue.to_excel('bookings.xlsx')

revenue.plot()
plt.show()
