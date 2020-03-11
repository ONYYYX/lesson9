global_init(input())
session = create_session()
jobs = []
max_team = 0
for job in session.query(Jobs).all():
    n = len(job.collaborators.split(', '))
    if n > max_team:
        max_team = n
    jobs.append(job)
for job in jobs:
    c = job.collaborators.split(', ')
    if len(c) >= max_team:
        user = session.query(User).filter(User.id == job.team_leader).first()
        print(user.surname, user.name)
