import sqlalchemy
from sqlalchemy import orm
from db.db_session import SqlAlchemyBase


class Departments(SqlAlchemyBase):
    __tablename__ = 'departments'
    id = sqlalchemy.Column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True
    )

    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    chief_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('users.id')
    )

    email = sqlalchemy.Column(
        sqlalchemy.String,
        index=True,
        unique=True,
        nullable=True
    )

    chief = orm.relation('User')
    members = orm.relationship('User')
