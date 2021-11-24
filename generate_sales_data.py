from sales_simulator import SalesSimulator, average_cycle_length

NUM_OPPORTUNITIES = 10

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

sales_data = SalesSimulator(stages=in_person, num_opportunities=in_person_opportunities).single_run()
sales_data.to_excel('sales_data.xlsx')
