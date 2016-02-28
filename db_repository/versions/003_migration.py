from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Vol = Table('Vol', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('first_name', VARCHAR(length=120)),
    Column('last_name', VARCHAR(length=120)),
    Column('email', VARCHAR(length=120)),
    Column('phone', VARCHAR(length=120)),
    Column('occupation', VARCHAR(length=120)),
    Column('postal_code', INTEGER),
    Column('linkedin', VARCHAR(length=120)),
    Column('facebook', VARCHAR(length=120)),
    Column('is_disabled', BOOLEAN),
    Column('created', DATETIME),
    Column('updated', DATETIME),
    Column('mon', BOOLEAN),
    Column('tue', BOOLEAN),
    Column('wed', BOOLEAN),
    Column('thu', BOOLEAN),
    Column('fri', BOOLEAN),
    Column('sat', BOOLEAN),
    Column('sun', BOOLEAN),
)

Vol = Table('Vol', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=120)),
    Column('last_name', String(length=120)),
    Column('email', String(length=120)),
    Column('phone', String(length=120)),
    Column('occupation', String(length=120)),
    Column('postal_code', Integer),
    Column('linkedin', String(length=120)),
    Column('facebook', String(length=120)),
    Column('is_disabled', Boolean),
    Column('created_on', DateTime),
    Column('updated_on', DateTime),
    Column('accepts_texts', Boolean),
    Column('mon', Boolean),
    Column('tue', Boolean),
    Column('wed', Boolean),
    Column('thu', Boolean),
    Column('fri', Boolean),
    Column('sat', Boolean),
    Column('sun', Boolean),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Vol'].columns['created'].drop()
    pre_meta.tables['Vol'].columns['updated'].drop()
    post_meta.tables['Vol'].columns['accepts_texts'].create()
    post_meta.tables['Vol'].columns['created_on'].create()
    post_meta.tables['Vol'].columns['updated_on'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['Vol'].columns['created'].create()
    pre_meta.tables['Vol'].columns['updated'].create()
    post_meta.tables['Vol'].columns['accepts_texts'].drop()
    post_meta.tables['Vol'].columns['created_on'].drop()
    post_meta.tables['Vol'].columns['updated_on'].drop()
