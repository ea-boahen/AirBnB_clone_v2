#!/usr/bin/python3
'''
    Define the class Place.
'''
from os import getenv
from models import BaseModel, Base
from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


place_amenity = Table('place_amenity', Base.metadata,
                      Column("place_id", String(60), ForeignKey("places.id"),
                             primary_key=True, nullable=False),
                      Column("amenity_id", String(60),
                             ForeignKey("amenities.id"),
                             primary_key=True, nullable=False)
                      )


class Place(BaseModel, Base):
    '''
        Define the class Place that inherits from BaseModel.
    '''
    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place",
                           cascade="all, delete-orphan")
    amenity_ids = []
    amenities = relationship("Amenity", backref="places",
                             secondary=place_amenity, viewonly=False)

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def reviews(self):
            '''
                Getter for the reviews property
            '''
            records = models.storage.all("Review").values()
            return [record for record in records if place_id == self.id]

        @property
        def amenities(self):
            '''
                Getter for the amenities property
            '''
            return self.amenity_ids

        @amenities.setter
        def amenities(self, instance=None):
            '''
                Setter for the amenities property
            '''
            if type(instance) is Amenity:
                if instance.place_amenity.place_id == self.id:
                    self.amenity_ids.append(instance.id)
