# -*- coding: utf-8 -*-
import os

from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import *

def create_database(path='test.db'):
    """Create database.
    
    Setup a temporary sqlite database and populate
    with some test data.
    
    Returns the engine and a session bound to the database.
    
    """
    # If database already exists, remove it
    if os.path.exists(path):
        os.remove(path)

    # Create test database
    engine = create_engine('sqlite:///%s' % (path, ), echo=False)
    metadata.create_all(engine)

    # Create a bound Session class
    Session = sessionmaker(bind=engine)

    # Some sample data
    fuel_type_data = [
        {'id': 1, 'name': u'Vortex 98', 'vendor': u'Shell', 'ron': u'98'},
        {'id': 2, 'name': u'E10 Unleaded', 'vendor': u'Caltex', 'ron': u'91'},
        {'id': 3, 'name': u'Synergy 8000', 'vendor': u'Mobil', 'ron': u'98'},
    ]
    outlet_data = [
        {'id': 1, 'name': u'Mobil Sydney', 'location': u'1 Main St'},
        {'id': 2, 'name': u'Shell Hornsby', 'location': u'Hornsby'},
        {'id': 3, 'name': u'Cherrybrook Caltex', 'location': u'Cherrybrook'},
        {'id': 4, 'name': u'Newcastle Mobil', 'location': u'F3 Freeway'},
    ]
    vehicle_data = [
        {'rego': u'ABC-123', 'year': u'1991', 'make': u'Toyota', 'model': u'Corolla', 
         'purchased': datetime(2001, 8, 25), 'initial_km': 85324, 'odometer': 146814, },
        {'rego': u'XYZ-987', 'year': u'2003', 'make': u'Toyota', 'model': u'Camry'},
         'purchased': datetime(2008, 6, 15), 'initial_km': 15920, 'odometer': 24921, },
        {'rego': u'AB-12-CD', 'year': u'2009', 'make': u'Subaru', 'model': u'Liberty'}
         'purchased': datetime(2010, 1, 7), 'initial_km': 0, 'odometer': 915, },
    ]
    purchase_data = [
        {'purchased': datetime(2010, 1, 1, 9, 30), 'vehicle_rego': u'ABC-123', 'odometer': 145675, 'quantity': 33.55,
        'fuel_price': 124.9, 'fuel_type_id': 1, 'filled_tank': 1},
        {'purchased': datetime(2010, 1, 3, 13, 0), 'vehicle_rego': u'XYZ-987', 'odometer': 23987, 'quantity': 55.12,
        'fuel_price': 119.9, 'fuel_type_id': 2, 'outlet_id': 3, 'filled_tank': 1},
        {'purchased': datetime(2010, 1, 10, 17, 45), 'vehicle_rego': u'ABC-123', 'odometer': 146017, 'quantity': 36.09,
        'fuel_price': 127.9, 'fuel_type_id': 1, 'outlet_id': 2, 'filled_tank': 1},
        {'purchased': datetime(2010, 1, 15, 16, 5), 'vehicle_rego': u'AB-12-CD', 'odometer': 305, 'quantity': 13.28,
        'fuel_price': 132.5, 'fuel_type_id': 3, 'filled_tank': 0},
        {'purchased': datetime(2010, 1, 17, 20, 12), 'vehicle_rego': u'AB-12-CD', 'odometer': 480, 'quantity': 46.71,
        'fuel_price': 129.9, 'fuel_type_id':1, 'outlet_id': 2, 'filled_tank': 1},
        {'purchased': datetime(2010, 1, 25, 17, 35), 'vehicle_rego': u'ABC-123', 'odometer': 146395, 'quantity': 30.67,
        'fuel_price': 117.9, 'fuel_type_id': 1, 'filled_tank': 1},
        {'purchased': datetime(2010, 1, 28, 12, 8), 'vehicle_rego': u'XYZ-987', 'odometer': 24631, 'quantity': 54.87,
        'fuel_price': 114.9, 'fuel_type_id': 2, 'outlet_id': 3, 'filled_tank': 1},
        {'purchased': datetime(2010, 2, 2, 10, 51), 'vehicle_rego': u'XYZ-987', 'odometer': 24921, 'quantity': 23.60,
        'fuel_price': 111.5, 'fuel_type_id': 2, 'outlet_id': 3, 'filled_tank': 0, 'discount': 0.04},
        {'purchased': datetime(2010, 2, 5, 14, 0), 'vehicle_rego': u'AB-12-CD', 'odometer': 915, 'quantity': 48.17,
        'fuel_price': 129.9, 'fuel_type_id': 3, 'filled_tank': 1},
        {'purchased': datetime(2010, 2, 8, 17, 46), 'vehicle_rego': u'ABC-123', 'odometer': 146814, 'quantity': 37.03,
        'fuel_price': 136.5, 'fuel_type_id': 1, 'filled_tank': 1},
    ]

    # Create some object instances and add them to the database
    session = Session()

    session.add_all([FuelType(**data_dict) for data_dict in fuel_type_data])
    session.add_all([Outlet(**data_dict) for data_dict in outlet_data])
    session.add_all([Vehicle(**data_dict) for data_dict in vehicle_data])
    session.add_all([Purchase(**data_dict) for data_dict in purchase_data])

    session.commit()

    # Return the engine and Session
    return engine, Session

if __name__ == '__main__':
    engine, Session = create_database()
