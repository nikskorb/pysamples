__author__ = 'Nikolay Skorobogatko'
__date__ = '2024-06-05 22:06:16'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = ['Aleksandr Dragunkin']
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'
from user_build import uFurnObject
from dataclasses import dataclass
import k3
from mlogger import logger
import typing
from MKitchen.filling_niche import fix_shelves #, fix_shelves_k3
from core_k.rdnomenclature import priceinfo
from MKitchen.shell_corner import constants as localconst
from based_build import Panel
import based_build.Constants as Constants
from MKitchen import constants
from MKitchen.shell_corner.services.shelf_macros import CountorObj

SHELF_CUT_DSP = 10 # подрезка по переду
SHELF_CUT_GLASS = 4.3 # подрезка по переду (стекло)
RADIUS_DSP = 15 # скругление полок
RADIUS_GLASS = 0 # скругление полок (стекло)
ZAZORS = 0 # зазоры между полкой и боковиной

GLASS_SHIFT_BACK_CORNER = 101.2
DSP_SHIFT_BACK_CORNER = 95.5



@dataclass
class RSH_Shelves:
    _behave: localconst.KnotBehavior = localconst.KnotBehavior.DEFAULT
    _prmater: float = 0
    _prmater_korp: float = _prmater
    _h_korp: float = k3.priceinfo(_prmater_korp, "Thickness", 16)
    _h_shelf = k3.priceinfo(_prmater_korp, "Thickness", 16)
    _bandtype: float = 0
    _polk_mater_g: float = 0
    _polk: float = 0

    # координаты внутренних плоскостей ниши внутри вызывающей секции
    # вычисляются и переопределяются для разных поведений в адаптерах
    top : float = 0
    bottom : float = 0
    left : float = 0
    right : float = 0
    back : float = 0
    front : float = 0

    _dy : float = 324
    _dx: float = 324

    _r1: float = 0
    _r2: float = 0
    _delta: float = 0
    _back_corner: float = 0

    _rp: float = 0

    _amount_shelves: float = 0
    _move_panel_z: float = 0
    _custom_distans = []

    _kp1: float = 0
    _kp2: float = 0
    _kp3: float = 0
    _kp4: float = 0


    _shelf_builder = None # Метод построитель полок
    _contour = None # Контур для фаски

    _krep_polk: float = 0
    _krep_polk_gl: float = 0

    _cutsh: float = ZAZORS

    @property
    def _shelf_fix(self):
        if self._polk == constants._POLK_MATER_DSP.value:
            return self._krep_polk
        elif self._polk == constants._POLK_MATER_GLASS.value:
            return self._krep_polk_gl

    @property
    def _h_between_shelves(self):
        return (self._h + self._h_korp) / (self._amount_shelves + 1)
    @property
    def _h(self):
        return self.top - self.bottom
    @property
    def _w(self):
        return self.left - self.right
    @property
    def _d(self):
        return self.front - self.back

class KnotCornerShelves(uFurnObject.FurnObject):
    def __init__(self, knot_props: RSH_Shelves):
        super().__init__()

        self.SetFurnType('010100')
        self.knot_props = knot_props
        self.put_shelves_params()
        self.countorObj = CountorObj(self.knot_props)
        self.knot_props._contour = self.countorObj.put_polyline_contour()
        self._elemname = "Полки"  # Узел

    def setFixShelves(self, v):
        self.knot_props._shelf_fix = v

    def setCustomDistans(self,*wards, startdelta=16.5,h_dsp=16):
        """Высоты установки полок определяемых пользователем"""
        for kp in wards:
            if kp>0:
                if kp >= self.knot_props.top:
                    kp = self.knot_props.top - h_dsp
                elif kp <= self.knot_props.bottom:
                    kp = self.knot_props.bottom + h_dsp
                else:
                    self.knot_props._custom_distans.append(kp-startdelta-h_dsp/2)

        self.knot_props._custom_distans=list(set(self.knot_props._custom_distans))
        if 0 in self.knot_props._custom_distans:
            self.knot_props._custom_distans.remove(0)

    def getCustomDistans(self):
        """Высоты установки полок определяемых пользователем"""
        return self.knot_props._custom_distans
        # инициализация координат положения полок в нише


    def shelf_dsp_params_factory(self):
        """Задать парметры полок из ДСП"""
        self.knot_props._back_corner = DSP_SHIFT_BACK_CORNER
        self.knot_props._delta = SHELF_CUT_DSP
        self.knot_props._r1 = RADIUS_DSP
        self.knot_props._r2 = RADIUS_DSP

    def shelf_glass_params_factory(self):
        """Задать парметры стеклянных полок"""
        self.knot_props._prmater = self.knot_props._polk_mater_g
        self.knot_props._h_shelf = k3.priceinfo(self.knot_props._polk_mater_g, "Thickness", 16)
        _cutfixed_be = priceinfo(self.knot_props._krep_polk_gl, "CutFixed", defvalue=0, tableid=2)
        _move_panel_z = priceinfo(self.knot_props._krep_polk_gl, "MovePanelZ", defvalue=0, tableid=2)
        self.knot_props._bandtype = 0  # Случай для полок из стекла кромки нет
        self.knot_props._cutsh = _cutfixed_be
        self.knot_props._move_panel_z = _move_panel_z
        self.knot_props._r1 = RADIUS_GLASS
        self.knot_props._r2 = RADIUS_GLASS
        self.knot_props._delta = SHELF_CUT_GLASS
        self.knot_props._back_corner = GLASS_SHIFT_BACK_CORNER



    def put_shelves_params(self):
        if self.knot_props._polk == constants._POLK_MATER_DSP.value:
            self.shelf_dsp_params_factory()
        elif self.knot_props._polk == constants._POLK_MATER_GLASS.value:
            self.shelf_glass_params_factory()

        self.setCustomDistans(
            self.knot_props._kp1,
            self.knot_props._kp2,
            self.knot_props._kp3,
            self.knot_props._kp4,
            startdelta=self.knot_props.bottom,
            h_dsp=self.knot_props._h_shelf
        )

        # niche.SetHingeMoverProc(utilites_hinge_mover.PostHingeMoverN04(niche))


    def __MakeShelves(self):
        """Полки жесткие"""
        self.shelf_builder = ShelvesCornerBuilder(self.knot_props)
        self.knot_props._shelf_builder = self.shelf_builder.fill_corner_same_distance # default
        self.knot_props._shelf_builder = self.shelf_builder.corner_niche_builders(self.knot_props._rp)
        shelves = self.knot_props._shelf_builder()
        return shelves

    def Make(self):
        # try:
        return self.__MakeShelves()
        # except:
        #     raise ValueError("Полки не были построены")


class ShelvesCornerBuilder:
    def __init__(self, knot_props: RSH_Shelves):
        self.knot_props = knot_props
        self.contour = knot_props._contour


    def add_one_fix_shelv_corner(self, i: int, z_pos: float = 0, **kwards) -> Panel.Panel:

        shelf = Panel.Panel()
        shelf.SetElemName("Полка")
        shelf.SetFurnType("010100")
        #shelf.SetKonsCode("ПОЛК", width - 2 * cutsh, depth - shelfcut)
        shelf.set_kons_code(Constants.PAN_CONTEXT.SHELVE)
        shelf.SetUnitCode(str(1107 + i))
        shelf.SetMater(self.knot_props._prmater)
        shelf.SetMajorPlace(Constants.MAJORPLACE_SHELF)
        # shelf.SetCuts(Constants.PANELSIDE_E, shelfcut)
        shelf.SetCuts(Constants.PANELSIDE_E, self.knot_props._cutsh)
        shelf.SetCuts(Constants.PANELSIDE_C, self.knot_props._cutsh)
        shelf.SetGabs(self.knot_props._w, self.knot_props._d)
        if z_pos > 0:
            shelf.SetPosition(self.knot_props.right, self.knot_props.back, z_pos + 16.5)
        band = Panel.Band()
        band.SetCommon(Constants.PANELSIDE_ALL, self.knot_props._bandtype)
        band.SetBandFace(True)
        shelf.AddBand(band)

        fixlineC = Panel.Fixline()
        fixlineC.SetCommon(Constants.PANELSIDE_C, self.knot_props._shelf_fix)
        fixlineC.SetUseSpot(False)
        shelf.AddFixline(fixlineC)
        fixlineE = Panel.Fixline()
        fixlineE.SetCommon(Constants.PANELSIDE_E, self.knot_props._shelf_fix)
        fixlineE.SetUseSpot(False)
        shelf.AddFixline(fixlineE)

        cutLine = Panel.Cutline()
        cutLine.SetCutline(Constants.MAP_ANG3, Constants.CUTLINETYPE_CUT, Constants.CUTLINEFORM_FREE, self.contour)
        cutLine.SetPosition(plane=Constants.PANELSIDE_THROUGH, side=Constants.PANELSIDE_E,ismiddle=False,
                            posx=0,posy=0,angle=180,depth=0,depthshift=0)
        shelf.AddCutline(cutLine)
        band = Panel.Band()
        band.SetCommon(Constants.PANELSIDE_ALL, self.knot_props._bandtype)
        cutLine.AddBand(band)

        if self.knot_props._behave in [localconst.KnotBehavior.DEFAULT,localconst.KnotBehavior.BEHAVE_1]:
            shelf.SetCutAngles(1,1,self.knot_props._back_corner,self.knot_props._back_corner)
            fixlineCorner = Panel.Fixline()
            fixlineCorner.SetType(self.knot_props._shelf_fix)
            fixlineCorner.SetSegment2(1,8)
            shelf.AddFixline(fixlineCorner)

        elif self.knot_props._behave is localconst.KnotBehavior.BEHAVE_2:
            shelf.SetCuts(Constants.PANELSIDE_B, self.knot_props._cutsh)
            fixlineD = Panel.Fixline()
            fixlineD.SetCommon(Constants.PANELSIDE_B, self.knot_props._shelf_fix)
            fixlineD.SetUseSpot(False)
            shelf.AddFixline(fixlineD)
        elif self.knot_props._behave is localconst.KnotBehavior.BEHAVE_3:
            shelf.SetCuts(Constants.PANELSIDE_D, self.knot_props._cutsh)
            fixlineB = Panel.Fixline()
            fixlineB.SetCommon(Constants.PANELSIDE_D, self.knot_props._shelf_fix)
            fixlineB.SetUseSpot(False)
            shelf.AddFixline(fixlineB)

        return shelf


    def fill_corner_same_distance(self) -> typing.List[Panel.Panel]:
        shelves = []
        if self.knot_props._amount_shelves == 0:
            return shelves
        h_dsp_etalon=16
        for i in range(self.knot_props._amount_shelves):
            z_pos = (self.knot_props._h_between_shelves) * (i + 1) - self.knot_props._h_shelf - (h_dsp_etalon - self.knot_props._h_shelf) / 2
            z_pos += self.knot_props._move_panel_z
            shelf = self.add_one_fix_shelv_corner(
                i,
                z_pos=z_pos
            )
            shelves.append(shelf)
        return shelves


    def fill_corner_user_custom_distance(self) -> typing.List[Panel.Panel]:
        shelves = []
        pz = 0
        for i, z_pos in enumerate(self.knot_props._custom_distans):
            if z_pos < pz + self.knot_props._h_shelf:
                raise ValueError("Слишком маленький зазор между полками")
            z_pos += self.knot_props._move_panel_z
            shelf = self.add_one_fix_shelv_corner(
                i,
                z_pos=z_pos
            )
            shelves.append(shelf)
        return shelves


    def fill_corner_standart_distance_315(self) -> typing.List[Panel.Panel]:
        key: float = 315
        shelves = []
        for i, z_pos in enumerate(
            fix_shelves.calculate_standart_position_z(size=self.knot_props._h, h_panel=self.knot_props._h_shelf, index=key)
        ):
            z_pos += self.knot_props._move_panel_z
            shelf = self.add_one_fix_shelv_corner(
                i,
                z_pos=z_pos
            )
            shelves.append(shelf)
        return shelves


    def fill_corner_standart_distance_560(self) -> typing.List[Panel.Panel]:
        key: float = 560
        shelves = []
        for i, z_pos in enumerate(
            fix_shelves.calculate_standart_position_z(size=self.knot_props._h, h_panel=self.knot_props._h_shelf, index=key)
        ):
            z_pos += self.knot_props._move_panel_z
            shelf = self.add_one_fix_shelv_corner(
                i,
                z_pos=z_pos)
            shelves.append(shelf)
        return shelves

    def corner_niche_builders(self, _rp):
        CORNER_NICHE_BUILDERS = {
            constants.MR_RP.EVENLY.value: self.fill_corner_same_distance,
            constants.MR_RP.CUSTOM.value: self.fill_corner_user_custom_distance,
            constants.MR_RP.S315.value: self.fill_corner_standart_distance_315,
            constants.MR_RP.S560.value: self.fill_corner_standart_distance_560,
        }
        return CORNER_NICHE_BUILDERS[_rp]

# @logger.catch()
# def main():
#     from MKitchen.shell_corner.shelf_macros import CountorObj
#     data = RSH_Shelves()
#     obj = CountorObj(data)
#     obj.put_polyline_contour()


# if __name__ == "__main__":
#     main()
