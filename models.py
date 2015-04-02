# -*- coding: utf-8 -*-
from datetime import datetime

from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
    MetaData, Numeric, Table, Unicode, UnicodeText)
from sqlalchemy.orm import mapper, relation

metadata = MetaData()

fueltype_table = Table('fueltype', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode),
    Column('vendor', Unicode),
    Column('ron', Unicode),
)

outlet_table = Table('outlet', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', Unicode),
    Column('location', Unicode),
)

vehicle_table = Table('vehicle', metadata,
    Column('rego', Unicode, primary_key=True),
    Column('year', Unicode),
    Column('make', Unicode),
    Column('model', Unicode),
    Column('series', Unicode),
    Column('body', Unicode),
    Column('colour', Unicode),
    Column('transmission', Unicode),
    Column('type', Unicode),
    Column('owner', Unicode),
    Column('manufactured', Date),
    Column('purchased', Date),
    Column('initial_km', Numeric(precision=8, scale=1)),
    Column('odometer', Numeric(precision=8, scale=1)),
    Column('notes', UnicodeText),
    Column('created', DateTime, default=datetime.now),
    Column('updated ', DateTime, default=datetime.now, onupdate=datetime.now),
)

purchase_table = Table('purchase', metadata,
    Column('purchased', DateTime),
    Column('vehicle_rego', Unicode, ForeignKey('vehicle.rego'), primary_key=True),
    Column('odometer', Numeric(precision=8, scale=1), primary_key=True),
    Column('quantity', Numeric(precision=5, scale=2)),
    Column('fuel_price', Numeric(precision=5, scale=2)),
    Column('fuel_type_id', Integer, ForeignKey('fueltype.id')),
    Column('filled_tank', Boolean),
    Column('outlet_id', Integer, ForeignKey('outlet.id')),
    Column('discount', Numeric(precision=3, scale=2)),
    Column('est_eff', Numeric(precision=3, scale=1)),
    Column('driving_notes', UnicodeText),
    Column('created', DateTime, default=datetime.now),
    Column('updated', DateTime, default=datetime.now, onupdate=datetime.now),
)


class EntityBase(object):
    """EntityBase Class.

    """
    def __init__(self, *args, **kwargs):
        if kwargs:
            [setattr(self, key, value) for key, value in kwargs.items()]


class FuelType(EntityBase):
    """FuelType Model.

    Represents one particular brand of fuel.

    """
    def __repr__(self):
        return '<FuelType(\'%s\', \'%s\', \'%s\')>' % (self.name, self.vendor, self.ron, )


class Outlet(EntityBase):
    """Outlet Model.

    Represents one particular fuel outlet where fuel was purchased.

    """
    def __repr__(self):
        return '<Outlet(\'%s\')>' % (self.name, )


class Vehicle(EntityBase):
    """Vehicle Model.

    Represents all the details of a Vehicle, including the manufacturer,
    make, year, date purchased, etc.

    """
    def __repr__(self):
        return '<Vehicle(\'%s\', \'%s\', \'%s\', \'%s\')>' % (self.rego, self.year, self.make, self.model, )


class Purchase(EntityBase):
    """Purchase Model.

    Represents the details of a particular purchase of fuel, including the
    vehicle it was purchased for, the amount, price and whether the tank
    was filled.

    """
    def __repr__(self):
        return '<Purchase(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')>' \
            % (self.purchased, self.vehicle, self.odometer, self.quantity,
               self.fuel_price, self.fuel_type, self.filled_tank, )


mapper(FuelType, fueltype_table,
    properties={
        'purchases': relation(Purchase)
    }
)
mapper(Outlet, outlet_table,
    properties={
        'purchases': relation(Purchase)
    }
)
mapper(Vehicle, vehicle_table,
    properties={
        'purchases': relation(Purchase)
    }
)
mapper(Purchase, purchase_table,
    properties={
        'vehicle': relation(Vehicle, uselist=False),
        'fuel_type': relation(FuelType, uselist=False),
        'outlet': relation(Outlet, uselist=False),
    }
)