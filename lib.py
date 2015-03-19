# -*- coding: utf-8 -*-
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import metadata

def get_engine(path, echo=True):
    """Returns a connection to the database.

    If the database path does not exist a new blank database
    is created using defined metadata.

    """
    engine = create_engine('sqlite:///%s' % (path, ), echo=echo)

    if not os.path.exists(path):
        metadata.create_all(engine)

    return engine

def get_sessionmaker(engine=None):
    """Returns a sessionmaker.

    By default returns an unbound sessionmaker.  Optionally an engine
    may be passed to bind the sessionmaker to.

    """
    return sessionmaker(bind=engine)
