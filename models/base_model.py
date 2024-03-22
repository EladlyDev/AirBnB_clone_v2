#!/usr/bin/env python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DATETIME
from os import getenv

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'latin1'}
    id = Column(String(60), primary_key=True)
    created_at = Column(DATETIME, default=datetime.utcnow, nullable=False)
    updated_at = Column(DATETIME, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if kwargs:
            tf = '%Y-%m-%dT%H:%M:%S.%f'
            if 'updated_at' in kwargs:
                kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                         tf)
            if 'created_at' in kwargs:
                kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                         tf)
            if '__class__' in kwargs:
                del kwargs['__class__']

            for prop in kwargs:
                setattr(self, prop, kwargs[prop])
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        out = dict(self.__dict__)
        if '_sa_instance_state' in out:
            del out['_sa_instance_state']
        return '[{}] ({}) {}'.format(cls, self.id, out)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)  # Last line of if not kwargs from __init__()
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        if "_sa_instance_state" in dictionary:
            del dictionary["_sa_instance_state"]
        return dictionary

    def delete(self):
        """Deletes the current instance from the storage"""
        from models import storage
        storage.delete(self)
