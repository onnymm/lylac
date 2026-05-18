from typing import Generic
from .._typing.generics import EngineHub
from .._typing.type_parameters import _M
from .._typing.literals import DMLTransaction

from typing import TypeVar

_H = TypeVar('_H')

class Slot(Generic[_M, _H]):
    create: EngineHub[_M, _H]
    update: EngineHub[_M, _H]
    delete: EngineHub[_M, _H]

    def __init__(
        self,
    ) -> None:

        self.create = {}
        self.update = {}
        self.delete = {}

    def __getitem__(
        self,
        name: DMLTransaction,
    ) -> EngineHub[_M, _H]:

        if name == 'create':
            return self.create
        if name == 'update':
            return self.update
        if name == 'delete':
            return self.delete

        raise AssertionError('El acceso no existe.')
