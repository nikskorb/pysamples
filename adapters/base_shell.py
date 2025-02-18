# -*- coding: utf-8 -*-
__author__ = 'Nikolay Skorobogatko'
__date__ = '2024-07-06 18:08:39'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = ['Aleksandr Dragunkin']
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'
from abc import ABC, ABCMeta, abstractmethod
import copy
from dataclasses import dataclass, field
from .. import constants as localconst

class SingletonMeta(ABCMeta):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

@dataclass
class AbstractRSH_Shell(ABC):
    """Абстрактный класс RSH посредника для прототипа с обязательным к реализации методом proparsinit
    """    
    @abstractmethod
    def proparsinit(*wards, **kwards):
        pass

class BasedRSH_shell(AbstractRSH_Shell, metaclass=SingletonMeta):
    """Родитель класса с общими параметрами прототипа (посредник) с реализацие методов:
    def save_initial_state(cls)
    def reset_to_initial(cls)
    """    
    _initial_state = None
    knot_behavior: localconst.KnotBehavior = localconst.KnotBehavior.DEFAULT

    def __init__(self):
        super().__init__()
        if BasedRSH_shell._initial_state is None:
            BasedRSH_shell._initial_state = self.save_initial_state()

    @classmethod
    def proparsinit(cls):
        raise NotImplementedError()

    @classmethod
    def save_initial_state(cls):
        """Метод сохранит текущее состояние RSH
        """
        initial_state = {}
        for k, v in vars(cls).items():
            if not k.startswith("__") and not callable(v) and not isinstance(v, classmethod):
                try:
                    initial_state[k] = copy.deepcopy(v)
                except:
                    print("Невозможно сохраниить данный атрибут")
        return initial_state

    @classmethod
    def reset_to_initial(cls):
        """Метод вернёт текущее состояние RSH до save_initial_state()
        """
        if cls._initial_state is not None:
            for k, v in cls._initial_state.items():
                try:
                    setattr(cls, k, copy.deepcopy(v))
                except:
                    print("Невозможно вернуть данный атрибут")

@dataclass
class Point:
    """Класс координат точки
    >>> p = Point(100, 200, 300)
    >>> p
    Point(x=100, y=200, z=300)
    >>> p()
    (100, 200, 300)
    """

    x: float = 0.
    y: float = 0.
    z: float = 0.

    def __call__(self, *args, **kwards):
        return self.x, self.y, self.z

@dataclass
class Gabs:
    """Класс габаритов по осям
    >>> p = Gabs(100, 200, 300)
    >>> p
    Gabs(x=100, y=200, z=300)
    >>> p()
    (100, 200, 300)
    """

    x: float = 0.
    y: float = 0.
    z: float = 0.

    def __call__(self, *args, **kwards):
        return self.x, self.y, self.z

@dataclass
class GabPanel:
    """Класс габарита панели Длина Ширина
    _______________________________________

>>> gb = GabPanel(1000, 500)
>>> gb
GabPanel(length=1000, width=500)
>>> gb()
(1000, 500)
    """
    length: float = None
    width: float = None

    def __call__(self, *args, **kwards):
        return self.length, self.width
