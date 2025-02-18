__author__ = 'Nikolay Skorobogatko'
__date__ = '2024-06-05 22:06:16'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = ['Aleksandr Dragunkin']
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'
# -*- coding: utf-8 -*-
from .factorys.v86 import HorisontPanel, PlankaPanel, VerticalPanel, DSPBackWall
# from MKitchen.shell_corner.entitys.v86 import RSH_shell, RSH_Slot
from MKitchen.shell_corner.entitys.v86 import RSH_shell
from MKitchen.shell_corner import constants as localconst
from MKitchen import constants
import traceback
from enum import Enum, unique
from dataclasses import dataclass
from user_build import uFurnObject, uConstantsDeclare
from based_build import Panel, Constants, ConstantsDeclare
from MKitchen.shell_corner.factorys.v86 import AbstractObject


class Shell(uFurnObject.FurnObject):
    def __init__(self, unit_inst: RSH_shell):
        super().__init__()
        self._furntype = "110000"
        self.unit_inst = unit_inst
        self._elemname = "Корпус V86"  # может заиметь свою карточку

    def material_obj_observer(self):
        ...

    def gab_obj_observer(self):
        ...

    def position_obj_observer(self):
        ...

    def Make(self):
        self._objects = []

        # # боковая стенка левая
        self.leftside = FactoryObjects(abstract_entity_behavior=VerticalPanel, elemname='Стенка левая',
                                       panposition=localconst.PanPosition.LEFT, unit_inst=self.unit_inst)
        self._objects.append(self.leftside.object)

        # # Боковая стенка правая
        self.rightside = FactoryObjects(abstract_entity_behavior=VerticalPanel, elemname='Стенка правая',
                                        panposition=localconst.PanPosition.RIGHT, unit_inst=self.unit_inst)
        self._objects.append(self.rightside.object)

        # дно
        self.downside = FactoryObjects(abstract_entity_behavior=HorisontPanel, elemname='Дно',
                                       panposition=localconst.PanPosition.BOTTOM, unit_inst=self.unit_inst, unit_code='1103')
        self._objects.append(self.downside.object)

        # # крышка
        self.upside = FactoryObjects(abstract_entity_behavior=HorisontPanel, elemname='Крышка',
                                     panposition=localconst.PanPosition.TOP, unit_inst=self.unit_inst)
        self._objects.append(self.upside.object)
        self.is_top_wall = True
        if self.unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_1]:
            # угловая планка
            self.planka = FactoryObjects(abstract_entity_behavior=PlankaPanel, elemname='Угловая планка',
                                         panposition=localconst.PanPosition.BACK, unit_inst=self.unit_inst)
            self._objects.append(self.planka.object)
        if self.unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_3]:
            self.back_wall = FactoryObjects(abstract_entity_behavior=DSPBackWall, elemname="Задняя стенка ЛДСП лев.",
                                            panposition=localconst.PanPosition.LEFT_BACK, unit_inst=self.unit_inst)
            self._objects.append(self.back_wall.object)
        if self.unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_2]:
            self.back_wall = FactoryObjects(abstract_entity_behavior=DSPBackWall, elemname="Задняя стенка ЛДСП прав.",
                                            panposition=localconst.PanPosition.RIGHT_BACK, unit_inst=self.unit_inst)
            self._objects.append(self.back_wall.object)

        return self._objects


class FactoryObjects:
    def __init__(self, abstract_entity_behavior: AbstractObject = None,
                 panposition: localconst.PanPosition = None,
                 unit_inst: RSH_shell = None,
                 elemname: str = None, unit_code=None
                 ):
        self.unit_inst = unit_inst
        self.panposition = panposition
        self.abstract_entity_behavior = abstract_entity_behavior
        self.elemname = elemname
        self.object: Panel.Panel = self.perform_factory()
        if unit_code:
            self.object.SetUnitCode(unit_code)

    def perform_factory(self) -> Panel.Panel:
        try:
            object = self.abstract_entity_behavior.factory(
                unit_inst=self.unit_inst, elemname=self.elemname, panposition=self.panposition)
            return object.panel
        except:
            traceback.print_exc()

# Demo:


def main():
    RSH_shell.proparsinit()
    RSH_shell._initial_state = RSH_shell.save_initial_state()
    RSH_shell.reset_to_initial()
    RSH_shell.height = 500
    RSH_shell.slotpars._depthbp_left = 22
    RSH_shell.depth = 500
    RSH_shell.slotpars._depthbp_straight = 33

    shell = Shell(RSH_shell)
    shell.Make()
    shell.Draw()


if __name__ == "__main__":
    main()
