global_init(input())
session = create_session()
jobs = []
max_team = 0
for job in session.query(Jobs).all():
    n = len(job.collaborators.split(', '))
    if n > max_team:
        max_team = n
    jobs.append(job)
tl = []
for job in jobs:
    c = job.collaborators.split(', ')
    if len(c) >= max_team:
        user = session.query(User).filter(User.id == job.team_leader).first()
        tl.append(f'{user.surname} {user.name}')
print('\n'.join(set(tl)))
