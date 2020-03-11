global_init(input())
session = create_session()
for user in session.query(User).filter(
        User.address == 'module_1',
        User.position.notlike('%ingeneer%'),
        User.speciality.notlike('%ingeneer%')).all():
    print(user.id)
