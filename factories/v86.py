# -*- coding: utf-8 -*-
from ..services.wrap import (add_bands_wrap_shelf, add_bands_wrap_side)
from .. import constants as localconst
from MKitchen import constants
from based_build import Panel
from MKitchen.shell_corner.adapters.base_shell import BasedRSH_shell
from user_build import uFurnObject, uConstantsDeclare
from based_build import Panel, Constants, ConstantsDeclare
from MKitchen.shell_corner.adapters.v86_2 import GabAdapter, SlotAdapter, PositionAdapter, FixAdapter
import traceback
from abc import ABC, abstractmethod
__author__ = 'Nikolay Skorobogatko'
__date__ = '2024-06-05 21:56:45'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = ['Aleksandr Dragunkin']
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'


class AbstractObject(ABC):
    @abstractmethod
    def factory(self, *wards, **kwards):
        pass


class PanelBehavior(AbstractObject):
    """Базовый класс детали корпуса из стандартной панели.
    """

    def __init__(self):
        self._commonpos = None
        self._positionshellpanel: localconst.PanPosition = localconst.PanPosition.NONE
        self.panel: Panel.Panel = Panel.Panel()
        self.unit_inst: BasedRSH_shell = None
        self.slot_panel_adapter = None
        self.fix_panel_adapter = None
        self.gab_panel_adapter = None
        self.position_adapter = None

    @classmethod
    def factory(*wards, **kwards):
        raise NotImplementedError

    @property
    def elemname(self):
        return self._elemname

    @elemname.setter
    def elemname(self, v):
        if v:
            self._elemname = v
            self.panel.SetElemName(self._elemname)

    @property
    def commonpos(self):
        return self._commonpos

    @commonpos.setter
    def commonpos(self, v):
        self._commonpos = v
        if self._commonpos:
            if self._commonpos > 0:
                self.panel.commonpos = self._commonpos

    def Draw(self):
        return self.panel.Draw()

    def gab_panel_observer(self):
        raise NotImplementedError

    def position_panel_observer(self):
        raise NotImplementedError

    def fix_panel_observer(self, *wards, **kwards):
        """Метод присвоения крепежа панели
        Д.б определён в конкретном классе
        """
        return None

    @property
    def panposition(self) -> localconst.PanPosition:
        """Косвенный признак положения панели
        верхняя или нижняя, левая или правая"""
        return self._positionshellpanel

    @panposition.setter
    def panposition(self, v):
        self._positionshellpanel = v

    def set_gab_panel_adapter(self, gab_panel_adapter):
        """Вычислитель габарита панели
        gab_panel_adapter(paninst: Panel.Panel, unit_inst = None) -> GabPanel:
        """
        self.gab_panel_adapter = gab_panel_adapter

    def set_fix_panel_adapter(self, fix_panel_adapter):
        """Вычислитель типа крепежа панели
        fix_panel_adapter(paninst: Panel.Panel, unit_inst = None):
        """
        self.fix_panel_adapter = fix_panel_adapter

    def set_position_adapter(self, position_adapter):
        """Вычислитель точки позиции панели/
        Назначается в конкретном изделии. в котором эта деталь используется.
        position_adapter(paninst: Panel.Panel, unit_inst = None) -> Point:
        """
        self.position_adapter = position_adapter

    def set_slot_panel_adapter(self, slot_panel_adapter):
        "Вычислитель положения и нанесения пропила"
        self.slot_panel_adapter = slot_panel_adapter

    def apply_adapters(self, unit_inst):
        if self.fix_panel_adapter:
            self.fix_panel_adapter(obj=self.panel,
                                   panposition=self.panposition, unit_inst=unit_inst)
        if self.slot_panel_adapter:
            self.slot_panel_adapter(obj=self.panel, panposition=self.panposition,
                                    unit_inst=unit_inst)
        if self.gab_panel_adapter:
            self.panel.SetGabs(*self.gab_panel_adapter(obj=self.panel,
                               panposition=self.panposition, unit_inst=unit_inst)())

    def put_all_props(self, unit_inst):
        """Установить габарит панели и точку установа"""
        try:
            point = self.position_adapter(obj=self.panel,
                                          panposition=self.panposition, unit_inst=unit_inst)
            self.panel.SetPosition(*point())
            self.apply_adapters(unit_inst)

        except:
            traceback.print_exc()

    # def change_fix(self, d: dict, zdown=False):
    #     """d ={ Constants.PANELSIDE_D : unit_inst.fix_vb,
    #          Constants.PANELSIDE_E : unit_inst.fix_vb,
    #          Constants.PANELSIDE_C : unit_inst.fix_konf,}
    #          """
    #     # Требуется добавить или заменить крепеж по сторонам
    #     for side in d.keys():
    #         fixline_side = Panel.Fixline()
    #         fixline_side.SetCommon(side, d.get(side, 0), zdown=zdown)
    #         self.panel.AddFixline(fixline_side)


class DownDryBehavior(AbstractObject):

    @classmethod
    def factory(self):
        raise NotImplementedError


class HorisontPanel(PanelBehavior):
    """Конкретный класс детали 'Горизонтальная панель'"""

    def __init__(self):
        super().__init__()

    @classmethod
    @add_bands_wrap_shelf(list_sides=(Constants.PANELSIDE_D, Constants.PANELSIDE_B, Constants.PANELSIDE_ANG1, Constants.PANELSIDE_ANG3,))
    def factory(cls, unit_inst: BasedRSH_shell, elemname: str = 'БезИмени', panposition: localconst.PanPosition = localconst.PanPosition.NONE, commonpos: float = None) -> 'HorisontPanel':
        """Фабричный метод создания детали 'Горизонтальной панели V86'"""
        inst = cls()
        inst.unit_inst = unit_inst
        inst.commonpos = commonpos
        inst.panposition = panposition
        inst.panel.SetElemName(elemname)
        inst.panel.SetMajorPlace(Constants.MAJORPLACE_SHELF)
        inst.panel.SetUnitCode("1103")
        inst.panel.SetMater(unit_inst.mater_shelves.prmater)
        inst.panel.SetTextureAngle(0)
        inst.set_gab_panel_adapter(GabAdapter.adapt)
        inst.set_position_adapter(PositionAdapter.adapt)
        inst.set_fix_panel_adapter(FixAdapter.adapt)
        inst.set_slot_panel_adapter(SlotAdapter.adapt)
        inst.put_all_props(unit_inst)
        return inst


class VerticalPanel(PanelBehavior):
    """Конкретный класс детали 'Вертикальная панель'"""

    def __init__(self):
        super().__init__()

    @classmethod
    @add_bands_wrap_side(list_sides=(Constants.PANELSIDE_ALL,))
    def factory(cls, unit_inst: BasedRSH_shell, elemname: str = 'БезИмени', panposition: localconst.PanPosition = localconst.PanPosition.NONE, commonpos: float = None) -> 'VerticalPanel':
        """Фабричный метод создания детали 'Вертикальная панель'"""
        inst = cls()
        inst.unit_inst = unit_inst
        inst.commonpos = commonpos
        inst.panposition = panposition
        inst.panel.SetElemName(elemname)
        inst.panel.SetUnitCode("1101")
        inst.panel.SetMater(unit_inst.mater_sides.prmater)
        inst.panel.SetTextureAngle(0)
        inst.set_gab_panel_adapter(GabAdapter.adapt)
        inst.set_position_adapter(PositionAdapter.adapt)
        inst.set_slot_panel_adapter(SlotAdapter.adapt)
        inst.set_fix_panel_adapter(FixAdapter.adapt)
        inst.put_all_props(unit_inst)
        return inst


class PlankaPanel(PanelBehavior):
    """Конкретный класс детали 'Планка'"""

    def __init__(self):
        super().__init__()

    @classmethod
    def factory(cls, unit_inst: BasedRSH_shell, elemname: str = 'БезИмени', panposition: localconst.PanPosition = localconst.PanPosition.NONE, commonpos: float = None) -> 'PlankaPanel':
        """Фабричный метод создания детали 'Планка'"""
        inst = cls()
        inst.unit_inst = unit_inst
        inst.commonpos = commonpos
        inst.panposition = panposition
        inst.panel.SetElemName(elemname)
        inst.panel.SetUnitCode("1101")
        inst.panel.SetMater(unit_inst.mater_shelves.prmater)
        inst.panel.SetTextureAngle(0)
        inst.set_gab_panel_adapter(GabAdapter.adapt)
        inst.set_position_adapter(PositionAdapter.adapt)
        inst.set_fix_panel_adapter(FixAdapter.adapt)
        inst.set_slot_panel_adapter(SlotAdapter.adapt)
        inst.put_all_props(unit_inst)
        return inst

# пример
# class DownDryer(DownDryBehavior):  # реализация посудосушилки вместо дна
#     def factory(cls, unit_inst: BasedRSH_shell, panposition: localconst.PanPosition = localconst.PanPosition.NONE, commonpos: float = None) -> 'DownDryer':
#         ...


class DSPBackWall(PanelBehavior):
    """Конкретный класс детали 'Вертикальная панель'"""

    def __init__(self):
        super().__init__()

    @classmethod
    @add_bands_wrap_side(list_sides=(Constants.PANELSIDE_ALL,))
    def factory(cls, unit_inst: BasedRSH_shell, elemname: str = 'БезИмени', panposition: localconst.PanPosition = localconst.PanPosition.NONE, commonpos: float = None) -> 'DSPBackWall':
        """Фабричный метод создания детали 'Вертикальная панель'"""
        inst = cls()
        inst.unit_inst = unit_inst
        inst.commonpos = commonpos
        inst.panposition = panposition
        inst.panel.SetElemName(elemname)
        inst.panel.SetUnitCode("1101")
        inst.panel.SetMater(unit_inst.mater_shelves.prmater)
        inst.panel.SetTextureAngle(0)
        inst.set_gab_panel_adapter(GabAdapter.adapt)
        inst.set_position_adapter(PositionAdapter.adapt)
        inst.set_slot_panel_adapter(SlotAdapter.adapt)
        inst.set_fix_panel_adapter(FixAdapter.adapt)
        inst.put_all_props(unit_inst)
        return inst
