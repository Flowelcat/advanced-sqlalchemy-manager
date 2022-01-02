"""
alchmanager
"""
__author__ = 'Roman Gladkov, Flowelcat'

import functools
import sys
import types
import inspect

if sys.version_info[0] == 3 and sys.version_info[1] <= 5:
    from sqlalchemy.ext.declarative.api import DeclarativeMeta
else:
    from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.orm.mapper import Mapper
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from sqlalchemy.sql.functions import GenericFunction

not_doubleunder = lambda name: not name.startswith('__')
not_under = lambda name: not name.startswith('_')


class BaseQueryManager:
    pass


class ManagedQuery(Query):
    """Managed Query object."""

    @staticmethod
    def __get_query_manager(entity):
        # search query manager
        # class_members = [cm[1] for cm in inspect.getmembers(BaseQueryManager.__subclasses__(), inspect.isclass)]
        class_members = BaseQueryManager.__subclasses__()
        for query_manager in class_members:
            if hasattr(query_manager, "__model__"):
                model = getattr(query_manager, "__model__")
                if model.__name__ == entity.__name__ or issubclass(entity, model):
                    manager_cls = query_manager
                    break
        else:
            manager_cls = BaseQueryManager

        return manager_cls

    def __init__(self, entities, *args, **kwargs):
        self.binds = {}
        self.manager = None
        entity = None

        if isinstance(entities, tuple) and len(entities):
            entity = entities[0]

        if isinstance(entity, GenericFunction):
            entity = entity.entity_namespace

        if isinstance(entities, Mapper):
            entity = entities.entity

        if isinstance(entity, DeclarativeMeta):
            manager_cls = self.__get_query_manager(entity)
            self.manager = manager_cls
            for fname in filter(not_doubleunder, dir(manager_cls)):
                fn = getattr(manager_cls, fname)
                setattr(self, fname, types.MethodType(fn, self))
                self.binds.update({fname: fn})

        # print("Created new query")
        super(ManagedQuery, self).__init__(entities, *args, **kwargs)

    def __getattribute__(self, name):
        returned = object.__getattribute__(self, name)
        if name != '_ManagedQuery__rebind' \
                and name != 'manager' \
                and not_under(name) \
                and (inspect.isfunction(returned) or inspect.ismethod(returned)):

            def update_filter(func):
                @functools.wraps(func)
                def wrapper(*args, **kwargs):
                    # print(name, "was called")
                    value = func(*args, **kwargs)
                    if isinstance(value, ManagedQuery):
                        value.__rebind()
                    return value

                return wrapper

            return update_filter(returned)
        return returned

    def __rebind(self):
        if len(self.binds):
            for fname, fn in self.binds.items():
                setattr(self, fname, types.MethodType(fn, self))


class ManagedSession(Session):

    def load_manager(self):
        def loader(manager_cls):
            for fname in filter(not_doubleunder, dir(manager_cls)):
                fn = getattr(manager_cls, fname)
                if not hasattr(self._query_cls, fname):
                    setattr(self._query_cls, fname, fn)

        return loader
