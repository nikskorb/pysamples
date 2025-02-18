__author__ = 'Nikolay Skorobogatko'
__date__ = '2024-06-05 22:07:26'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = ['Aleksandr Dragunkin']
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'
# -*- coding: utf-8 -*-
from MKitchen.shell_corner import constants as localconst
from MKitchen.shell_corner.constants import PanPosition
from based_build import Panel, Constants
from MKitchen.shell_corner.adapters.base_shell import GabPanel, BasedRSH_shell, Point
from MKitchen import constants

FIX_TYPE_EXCENTER = 2731
FIX_TYPE_EURO = 2726
CORNER_SLICE = 50

class GabAdapter():
    @staticmethod
    def adapt(obj: Panel.Panel, unit_inst, panposition, *wards, **kwards):
        if not isinstance(unit_inst, type(BasedRSH_shell)):
            raise TypeError(
                "unit_inst должен быть экземпляром (data класс узла, наследник uRSH_shell) RSH_shell")
        if panposition in [localconst.PanPosition.TOP, localconst.PanPosition.BOTTOM]:
            # фиксированный отступ от края боковины до начала дна (в стандарте 315 - 1.21 = 313,79 мм)
            _magic_reduce = 1.21
            _corner_shift = CORNER_SLICE  # фиксированный отступ для углового скоса
            gabsp = GabPanel()
            # 16 поменять на толщину prmater боковой стенки
            gabsp.width = unit_inst.width - unit_inst.mater_sides.h_dsp
            gabsp.length = unit_inst.depth - unit_inst.mater_sides.h_dsp
            Dx = unit_inst.depth - unit_inst.right_side_width + \
                _magic_reduce - unit_inst.mater_sides.h_dsp
            Dy = unit_inst.width - unit_inst.left_side_width + \
                _magic_reduce - unit_inst.mater_sides.h_dsp
            obj.SetCutAngles(3, 1, Dx, Dy)
            unit_inst.data_shelves.dx = Dx
            unit_inst.data_shelves.dy = Dy
            unit_inst.data_shelves._corner_shift = _corner_shift
            if unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_1]:
                obj.SetCutAngles(1, 1, _corner_shift, _corner_shift)
            return gabsp
        if panposition in [localconst.PanPosition.LEFT, localconst.PanPosition.RIGHT]:
            gabsp = GabPanel()
            if panposition is localconst.PanPosition.LEFT:
                gabsp.length = unit_inst.height
                gabsp.width = unit_inst.left_side_width
            if panposition is localconst.PanPosition.RIGHT:
                gabsp.length = unit_inst.height
                gabsp.width = unit_inst.right_side_width
            return gabsp
        if panposition is localconst.PanPosition.BACK:
            gabsp = GabPanel()
            gabsp.length = unit_inst.height - 2 * unit_inst.mater_shelves.h_dsp - \
                constants.ToleranceShellTaile.POSDNO.value - \
                constants.ToleranceShellTaile.POSTOP.value
            gabsp.width = 135
            butt1 = Panel.Butt(butttype=Constants.BUTTTYPE_CHAMFER,
                               map_=Constants.MAP_E, params=(0, 0, 45), idline=1)
            butt2 = Panel.Butt(butttype=Constants.BUTTTYPE_CHAMFER,
                               map_=Constants.MAP_E, params=(0, 0, 45), idline=5)
            obj.AddButt(butt1)
            obj.AddButt(butt2)
            return gabsp
        if panposition is localconst.PanPosition.LEFT_BACK:
            gabsp = GabPanel()
            gabsp.length = unit_inst.height - 2 * unit_inst.mater_shelves.h_dsp - \
                constants.ToleranceShellTaile.POSDNO.value - \
                constants.ToleranceShellTaile.POSTOP.value
            gabsp.width = unit_inst.depth - unit_inst.mater_sides.h_dsp
            return gabsp
        if panposition is localconst.PanPosition.RIGHT_BACK:
            gabsp = GabPanel()
            gabsp.length = unit_inst.height - 2 * unit_inst.mater_shelves.h_dsp - \
                constants.ToleranceShellTaile.POSDNO.value - \
                constants.ToleranceShellTaile.POSTOP.value
            gabsp.width = unit_inst.width - unit_inst.mater_sides.h_dsp
            return gabsp


class PositionAdapter():
    @staticmethod
    def adapt(obj: Panel.Panel, unit_inst, panposition, *wards, **kwards):
        if not isinstance(unit_inst, type(BasedRSH_shell)):
            raise TypeError(
                "unit_inst должен быть экземпляром (data класс узла, наследник uRSH_shell) RSH_shell")
        points = Point()
        if panposition is localconst.PanPosition.BOTTOM:
            points.z += constants.ToleranceShellTaile.POSDNO.value
            unit_inst.into_box_planes_positions.bottom = points.z + unit_inst.mater_shelves.h_dsp
        elif panposition is localconst.PanPosition.TOP:
            points.z = unit_inst.height - unit_inst.mater_shelves.h_dsp - \
                constants.ToleranceShellTaile.POSTOP.value
            unit_inst.into_box_planes_positions.top = points.z
        elif panposition is localconst.PanPosition.LEFT:
            obj.SetMajorPlace(Constants.MAJORPLACE_POST)
            points.x = unit_inst.depth - unit_inst.mater_sides.h_dsp
            unit_inst.into_box_planes_positions.left = points.x
        elif panposition is localconst.PanPosition.RIGHT:
            obj.SetMajorPlace(Constants.MAJORPLACE_WALL)
            points.y = unit_inst.width - unit_inst.mater_sides.h_dsp
            unit_inst.into_box_planes_positions.front = points.y
        elif panposition is localconst.PanPosition.BACK:
            obj.SetMajorPlace(Constants.MAJORPLACE_POST)
            shiftX = 84.2  # высчитанный отступ по X
            shiftY = 11.3  # высчитанный отступ по Y
            points.x = unit_inst.slotpars._depthbp_straight + \
                unit_inst.slotpars._h_dvp + shiftX
            points.y = unit_inst.slotpars._depthbp_left + unit_inst.slotpars._h_dvp - shiftY
            points.z = unit_inst.mater_shelves.h_dsp + \
                constants.ToleranceShellTaile.POSDNO.value
            obj.SetRotatePos(45, points.x, points.y, points.z,
                             points.x, points.y, points.z+1)
            unit_inst.into_box_planes_positions.back = points.y + shiftY
        elif panposition is localconst.PanPosition.LEFT_BACK:
            obj.SetMajorPlace(Constants.MAJORPLACE_WALL)
            points.z = unit_inst.mater_shelves.h_dsp + \
                constants.ToleranceShellTaile.POSDNO.value
            unit_inst.into_box_planes_positions.back = unit_inst.mater_shelves.h_dsp
        elif panposition is localconst.PanPosition.RIGHT_BACK:
            obj.SetMajorPlace(Constants.MAJORPLACE_POST)
            points.z = unit_inst.mater_shelves.h_dsp + \
                constants.ToleranceShellTaile.POSDNO.value
            unit_inst.into_box_planes_positions.back = unit_inst.slotpars._depthbp_left + \
                unit_inst.slotpars._h_dvp
            unit_inst.into_box_planes_positions.right = unit_inst.mater_shelves.h_dsp
        return points


class SlotAdapter():
    @staticmethod
    def adapt(obj: Panel.Panel, unit_inst, panposition, *wards, **kwards):
        if not isinstance(unit_inst, type(BasedRSH_shell)):
            raise TypeError(
                "unit_inst должен быть экземпляром (data класс узла, наследник uRSH_shell) RSH_shell")
        _cpr = 0  # отступ от стороны или координата X (для свободного пропила)
        _cpd = unit_inst.slotpars._incutbp  # глубина пропила
        _cpw = unit_inst.slotpars._h_dvp  # ширина пропила
        # длина пропила (для ограниченного Constants.SLOTTYPE_BOUNDED пропила)
        _cpl = 0
        _angle = 0  # угол пропила (в градусах)
        if panposition is PanPosition.LEFT and unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_1,
                                                                           localconst.KnotBehavior.BEHAVE_2]:
            slot = Panel.Slot()
            slot.SetSlot(True,
                         Constants.PANELSIDE_D,
                         Constants.SLOTTYPE_THROUGH,
                         cpr=_cpr, cps=unit_inst.slotpars._depthbp_left, cpd=_cpd,
                         # cps - отступ от начала или координата Y (для свободного пропила)
                         cpw=_cpw, cpl=_cpl, angle=_angle,
                         map_=Constants.MAP_D)
            obj.AddSlot(slot)
            unit_inst.into_box_planes_positions.right = unit_inst.slotpars._depthbp_straight + _cpw
            # unit_inst.into_box_planes_positions.back = unit_inst.slotpars._depthbp_left + _cpw

        elif panposition is PanPosition.RIGHT and unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_1,
                                                                              localconst.KnotBehavior.BEHAVE_3]:
            slot = Panel.Slot()
            slot.SetSlot(False,
                         Constants.PANELSIDE_D,
                         Constants.SLOTTYPE_THROUGH,
                         cpr=_cpr, cps=unit_inst.slotpars._depthbp_straight, cpd=_cpd,
                         cpw=_cpw, cpl=_cpl, angle=_angle,
                         map_=Constants.MAP_D)
            obj.AddSlot(slot)
            unit_inst.into_box_planes_positions.right = unit_inst.slotpars._depthbp_straight + _cpw

        elif panposition is PanPosition.BOTTOM:
            if unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_1,
                                           localconst.KnotBehavior.BEHAVE_2]:
                slot1 = Panel.Slot()
                slot1.SetSlot(True,
                              Constants.PANELSIDE_D,
                              Constants.SLOTTYPE_THROUGH,
                              cpr=_cpr, cps=unit_inst.slotpars._depthbp_left, cpd=_cpd,
                              cpw=_cpw, cpl=_cpl, angle=_angle,
                              map_=Constants.MAP_D)
                obj.AddSlot(slot1)
            if unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_1,
                                           localconst.KnotBehavior.BEHAVE_3]:
                slot2 = Panel.Slot()
                slot2.SetSlot(True,
                              Constants.PANELSIDE_B,
                              Constants.SLOTTYPE_THROUGH,
                              cpr=_cpr, cps=unit_inst.slotpars._depthbp_straight, cpd=_cpd,
                              cpw=_cpw, cpl=_cpl, angle=_angle,
                              map_=Constants.MAP_B)
                obj.AddSlot(slot2)

        elif panposition is PanPosition.TOP:
            if unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_1,
                                           localconst.KnotBehavior.BEHAVE_2]:
                slot1 = Panel.Slot()
                slot1.SetSlot(False,
                              Constants.PANELSIDE_D,
                              Constants.SLOTTYPE_THROUGH,
                              cpr=_cpr, cps=unit_inst.slotpars._depthbp_left, cpd=_cpd,
                              cpw=_cpw, cpl=_cpl, angle=_angle,
                              map_=Constants.MAP_D)
                obj.AddSlot(slot1)
            if unit_inst.knot_behavior in [localconst.KnotBehavior.BEHAVE_1,
                                           localconst.KnotBehavior.BEHAVE_3]:
                slot2 = Panel.Slot()
                slot2.SetSlot(False,
                              Constants.PANELSIDE_B,
                              Constants.SLOTTYPE_THROUGH,
                              cpr=_cpr, cps=unit_inst.slotpars._depthbp_straight, cpd=_cpd,
                              cpw=_cpw, cpl=_cpl, angle=_angle,
                              map_=Constants.MAP_B)
                obj.AddSlot(slot2)
        elif panposition is PanPosition.LEFT_BACK and unit_inst.knot_behavior is localconst.KnotBehavior.BEHAVE_3:
            slot = Panel.Slot()
            slot.SetSlot(True,
                         Constants.PANELSIDE_D,
                         Constants.SLOTTYPE_THROUGH,
                         cpr=_cpr, cps=unit_inst.slotpars._depthbp_straight, cpd=_cpd,
                         cpw=_cpw, cpl=_cpl, angle=_angle,
                         map_=Constants.MAP_B)
            obj.AddSlot(slot)
            # unit_inst.into_box_planes_positions.right = unit_inst.slotpars._depthbp_straight + unit_inst.slotpars._h_dvp
        elif panposition is PanPosition.RIGHT_BACK and unit_inst.knot_behavior is localconst.KnotBehavior.BEHAVE_2:
            slot = Panel.Slot()
            slot.SetSlot(False,
                         Constants.PANELSIDE_D,
                         Constants.SLOTTYPE_THROUGH,
                         cpr=_cpr, cps=unit_inst.slotpars._depthbp_left, cpd=_cpd,
                         cpw=_cpw, cpl=_cpl, angle=_angle,
                         map_=Constants.MAP_D)
            obj.AddSlot(slot)


class FixAdapter():
    def adapt(obj: Panel.Panel, unit_inst, panposition, *wards, **kwards):
        if not isinstance(unit_inst, type(BasedRSH_shell)):
            raise TypeError(
                "unit_inst должен быть экземпляром (data класс узла, наследник uRSH_shell) RSH_shell")
        if panposition in [localconst.PanPosition.TOP, localconst.PanPosition.BOTTOM]:
            for i in [Constants.PANELSIDE_C, Constants.PANELSIDE_E]:
                fix = Panel.Fixline()
                fix.SetCommon(i, unit_inst.fix_type, True)
                obj.AddFixline(fix)
        if panposition is localconst.PanPosition.BACK:
            for i in [Constants.PANELSIDE_C, Constants.PANELSIDE_B]:
                fix = Panel.Fixline()
                fix.SetCommon(i, unit_inst.custom_fix_type, True)
                obj.AddFixline(fix)
        if panposition is localconst.PanPosition.LEFT_BACK and unit_inst.knot_behavior is localconst.KnotBehavior.BEHAVE_3:
            for i in [Constants.PANELSIDE_C, Constants.PANELSIDE_B]:
                fix = Panel.Fixline()
                fix.SetCommon(i, FIX_TYPE_EXCENTER, False)
                obj.AddFixline(fix)
        if panposition is localconst.PanPosition.RIGHT_BACK and unit_inst.knot_behavior is localconst.KnotBehavior.BEHAVE_2:
            for i in [Constants.PANELSIDE_C, Constants.PANELSIDE_B]:
                fix = Panel.Fixline()
                fix.SetCommon(i, FIX_TYPE_EXCENTER, True)
                obj.AddFixline(fix)
