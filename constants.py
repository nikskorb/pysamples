# -*- coding: utf-8 -*-
__author__ = 'Aleksandr Dragunkin'
__date__ = '2024-06-05 17:29:52'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = []
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'

from enum import Enum, unique


@unique
class PanPosition(Enum):
    """Косвенное положение панели
    __________________________________

    Для идентификации одинаковых конкретных классов.

    Например есть жёсткая полка, которая может быть верхняя и нижняя.
    Для каждой детали в рамках узла должна
    быть своя уникальная.

    - NONE   # нет
    - LEFT   # левый
    - RIGHT  # правый
    - TOP    # верхний
    - BOTTOM  # нижний
    - CUSTOM  # специальный
    - FRONT    # передний
    - BACK     # задний

    """
    NONE: int = 0         # нет
    LEFT: int = 1         # левый
    RIGHT: int = 2        # правый
    TOP: int = 3          # верхний
    BOTTOM: int = 4       # нижний
    CUSTOM: int = 99      # специальный
    MIDDLE: int = 5       # срудний
    FRONT: int = 6        # передний
    BACK: int = 7         # задний
    LEFT_BACK: int = 8   # задняя левая
    RIGHT_BACK: int = 9  # задняя левая


class KnotBehavior(Enum):
    """Варианты конструкции задних стенок


        - DEFAULT:  int = 0
        - BEHAVE_1: int = 1  # Две стенки ДВП НАвесы по углам
        - BEHAVE_2: int = 2  # Одна стенка ДСП два навес на 1 стенку
        - BEHAVE_3: int = 3  # уникальный признак узла
    Args:
        Enum (_type_): _description_
    """
    DEFAULT:  int = 0
    BEHAVE_1: int = 1  # уникальный признак узла
    BEHAVE_2: int = 2  # Одна стенка LCG два навес на 1 стенку
    BEHAVE_3: int = 3  # уникальный признак узла
