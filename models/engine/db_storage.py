#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
from sqlalchemy import create_engine, MetaData, select
import sqlalchemy.orm as orm
import os


class DBStorage:
    """This class manages storage of hbnb models using a DB"""
    __engine = None
    __session = None

    def __init__(self):
        """Returns a sqlachemy orm object of models currently the storage"""
        from models.base_model import Base

        USER = os.getenv("HBNB_MYSQL_USER")
        PWD = os.getenv("HBNB_MYSQL_PWD")
        HOST = os.getenv("HBNB_MYSQL_HOST")
        DB = os.getenv("HBNB_MYSQL_DB")
        ENV = os.getenv("HBNB_ENV")
        conn_str = "mysql+mysqldb://{}:{}@{}/{}".format(USER, PWD, HOST, DB)
        self.__engine = create_engine(conn_str, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)

        if ENV == "test":
            metadata = MetaData()  # Meta data object
            metadata.reflect(self.__engine)  # Analyze db relationships
            # Drop all tables in their dependencies order
            metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Retrieve all objects depending of the class name"""
        from models.city import City
        from models.state import State
        from models.user import User
        from models.review import Review
        from models.place import Place
        from models.amenity import Amenity


        models = [State, City, User, Review, Place, Amenity]  # all models
        cls_model = None  # temp var for cls's real model
        # If cls argument is given, query that only else query all of them
        if cls:
            for model in models:
                if model.__name__ == cls.__name__:
                    cls_model = model
                    break
            if cls_model:
                models = [cls_model]
        out = {}  # The dictionary to be returned
        results = []  # The results to be compiled from db queries

        for m in models:
            results += self.__session.query(m).all()

        for inst in results:
            # obj = inst.to_dict()
            # obj["created_at"] = repr(inst.created_at)
            # obj["updated_at"] = repr(inst.updated_at)
            key = inst.__class__.__name__
            # val = f"[{key}] ({inst.id}) "
            # if "__class__" in obj:
            #     del obj["__class__"]
            # val += str(obj)
            out[key+"."+inst.id] = inst
        # User, State, City, Amenity, Place and Review
        return out

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        # self.__session.add(self)
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        """create all tables in the database"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        from models.base_model import Base

        # for model in [BaseModel, User, Place, State, City, Amenity, Review]:
        # self.new(model)

        Base.metadata.create_all(self.__engine)
        factory = orm.sessionmaker(bind=self.__engine)
        Session = orm.scoped_session(factory)
        self.__session = Session(bind=self.__engine, expire_on_commit=False)

    def close(self):
        """ closes the self.__session which stops all the transactions """
        self.__session.close()
