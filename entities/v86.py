# -*- coding: utf-8 -*-
__author__ = 'Nikolay Skorobogatko'
__date__ = '2024-06-05 22:08:39'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = ['Aleksandr Dragunkin']
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'
import core_k
from dataclasses import dataclass
from MKitchen.shell_corner.adapters.base_shell import BasedRSH_shell

@dataclass(frozen=False)
class RSH_Slot:
    """dataclass для определения дефолтных параметров пропилов
    """
    _depthbp_straight: float = 17  # отступ по правой стороне
    _depthbp_left: float = 17  # отступ по левой стороне
    _h_dvp: float = 4  # толщина пропила (хдф)
    _incutbp: float = 5  # глубина пропила

@dataclass(frozen=False)
class BoxPlanesPos:
    """dataclass для определения внутренних координат габаритов корпуса
    """
    ...

@dataclass(frozen=False)
class SpecificValues:
    """дата класс для определения специфических данных
    """
    ...

@dataclass(frozen=False)
class MaterShell:
    """dataclass параметров материала и авторасчёта его толщины 
    """    
    prmater: float = 0
    band_type: float = 0
    h_dsp: float = 0

    def __post_init__(self):
        if self.prmater is not None:
            self.h_dsp = core_k.rdnomenclature.getThickness(self.prmater)
            self.band_type = int(core_k.rdnomenclature.priceinfo(
                self.prmater, 'BandColor', 0))

class RSH_shell(BasedRSH_shell):
    """Единственный экземпляр класса с общими параметрами прототипа (посредник)
        cls.slotpars = RSH_Slot() # инициализация дополнительных классов для конкретного узла (Shell)
        cls.into_box_planes_positions = BoxPlanesPos() класс хранитель координат внутренней ниши (для Shelves, Naveses)
        cls.data_shelves = SpecificValues() # инициализация дополнительных классов для конкретного узла 
    """    
    def __init__(self):
        super().__init__()

    @classmethod
    def proparsinit(cls):
        # примеры предварительной инициализации:
        cls.custom_fix_type = 2869  # статичный не изменяемый крепеж
        # инициализация обязательных датаклассов для прототипа v86 (у каждого прототипа свои)
        cls.slotpars = RSH_Slot()
        cls.into_box_planes_positions = BoxPlanesPos()
        cls.data_shelves = SpecificValues()
