#!/usr/bin/python3
'''
    Implementation of the Amenity class
'''
from models import BaseModel, Base
from models import place_amenity
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    '''
        Implementation for the Amenities.
    '''
    __tablename__ = "amenities"

    name = Column(String(128), nullable=False)
    place_amenities = relationship("Place", secondary=place_amenity)
