from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Project = Table('Project', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    Column('description', String(length=10000)),
    Column('tools', String(length=10000)),
    Column('from_time', DateTime),
    Column('to_time', DateTime),
)

ProjectAssignment = Table('ProjectAssignment', post_meta,
    Column('project_id', Integer, primary_key=True, nullable=False),
    Column('user_id', Integer, primary_key=True, nullable=False),
    Column('request_sent', Boolean),
    Column('request_accepted', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Project'].create()
    post_meta.tables['ProjectAssignment'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Project'].drop()
    post_meta.tables['ProjectAssignment'].drop()
