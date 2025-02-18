__author__ = 'Nikolay Skorobogatko'
__date__ = '2024-06-05 22:06:16'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = ['Aleksandr Dragunkin']
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'
import user_build.Accessory_user as Accessory
from user_build import uFurnObject
from dataclasses import dataclass
from core_k.rdnomenclature import priceinfo
import typing
from user_build import uFurnFuncs
from ..placement_naves_auto import ErrorAutoSearshNaves, NavesTypesForCorner, N04_Naves, BaseNaves, NavesTypesWitchNOG
from k3_widgets import ErrMsgBox
from MKitchen import constants
from MKitchen.shell_corner import constants as localconst


MAX_SHIFT = 21  # максимальный отступ для SAH 130 и SAH 807
SHIFT_Y_SAH_215 = 11  # конст сдвига от зада для SAH_215
SAH_215 = 5444
SAH_215_AUTO = 5797

@dataclass
class RSH_Accessory:
    naves_id: float = 0
    _behave: localconst.KnotBehavior = localconst.KnotBehavior.DEFAULT    
    # габариты ниши внутри порождающей секции
    top: float = 0
    bottom: float = 0
    left: float = 0
    right: float = 0
    back: float = 0
    front: float = 0

    #
    _h: float = 0
    _d: float = 0
    _w: float = 0

    # расстояние от стены до ЗС (прав и лев)
    _szs1: float = 0
    _szs2: float = 0

    # высоты боковых стенок
    _h_right_wall: float = 0
    _h_left_wall: float = 0

    # глубины боковин
    _d_left_wall: float = 0
    _d_right_wall: float = 0


class KnotNaveses(uFurnObject.FurnObject):
    def __init__(self, knot_props: RSH_Accessory):
        super().__init__()
        self.SetFurnType('042300')
        self.knot_props = knot_props
        self._elemname = "Навесы"  # Узел
        self._id_naves = knot_props.naves_id
        self.SetNaves()
        self._naves_lev = None
        self._naves_prw = None
        self.objects = []

    def get_complect_naves(self, acc):
        alias = self.get_alias(acc)
        if alias == 'R':
            id_right, id_left = self.calculate_complect_naves(acc)
        elif alias == 'L':
            id_left, id_right = self.calculate_complect_naves(acc)
        else:
            raise ValueError("Invalid naves alias")
        return id_right, id_left

    def get_alias(self, accessory: Accessory.Accessory) -> str:
        """свойство номенклатуры Alias экземпляра Accessory"""
        alias = priceinfo(accessory.GetMater(), 'alias', 'r').upper()
        return alias

    def calculate_complect_naves(self, acc):
        '''Вычислить значение id второго навеса в свостве NomId1 в справочнике номенклатуры'''
        return int(acc.GetMater()), int(priceinfo(acc.GetMater(), 'NomId1', 0))

    def SetNaves(self):
        """Задать id навеса для корпуса. Левого или правого, неважно.
        Метод выполнит вычисление комплекта из левого и правого при помощи get_complect_naves"""
        acc = Accessory.Accessory(int(self._id_naves))
        self.__naves = self.get_complect_naves(acc)

    def GetNaves(self) -> typing.Tuple[int, int]:
        """комплект Id навесов корпуса из левого и правого"""
        return self.__naves

    def appendNaves(self,_naves_prw = None, _naves_lev = None):
        if _naves_prw is not None:
            self.objects.append(_naves_prw)
        if _naves_lev is not None:
            self.objects.append(_naves_lev)


    def __MakeNaves(self):
        "Навески"
        self._id_prw, self._id_lev = self.GetNaves()
        _is_SAH_215 = bool(self._id_prw == SAH_215)  # поправка для навесов hettich
        _naves_prw, _naves_lev = 0, 0
        if all(self.GetNaves()):
            "Спозиционировать правый и левый навес"
            _naves_lev = Accessory.Accessory(self._id_lev)
            _naves_prw = Accessory.Accessory(self._id_prw)
            _z = self.knot_props.top
            if self.knot_props._behave in [localconst.KnotBehavior.DEFAULT, localconst.KnotBehavior.BEHAVE_2]:
                _xr = self.knot_props.right
                _xl = self.knot_props.left
                _y = SHIFT_Y_SAH_215 if _is_SAH_215 else self.knot_props.back
                if _is_SAH_215 or not _is_SAH_215 and self.knot_props.back <= MAX_SHIFT:
                    _naves_prw.SetPosition(_xr, _y, _z)
                    _naves_lev.SetPosition(_xl, _y, _z)
                    self.appendNaves(_naves_prw,_naves_lev)

            elif self.knot_props._behave is localconst.KnotBehavior.BEHAVE_3:
                _x = SHIFT_Y_SAH_215 if _is_SAH_215 else self.knot_props.right
                _yl = self.knot_props.back
                _yr = self.knot_props.front
                if _is_SAH_215 or not _is_SAH_215 and self.knot_props.right <= MAX_SHIFT:
                    _naves_prw.SetPosition(_x, _yr, _z)
                    _naves_lev.SetPosition(_x, _yl, _z)
                    _naves_prw.SetAngles(0, 270, 0)
                    _naves_lev.SetAngles(0, 270, 0)
                    self.appendNaves(_naves_prw,_naves_lev)

            elif self.knot_props._behave is localconst.KnotBehavior.BEHAVE_1:
                _xr = SHIFT_Y_SAH_215 if _is_SAH_215 else self.knot_props.right
                _xl = self.knot_props.left
                _yl = SHIFT_Y_SAH_215 if _is_SAH_215 else self.knot_props.back
                _yr = self.knot_props.front
                if _is_SAH_215 or not _is_SAH_215 and self.knot_props.right <= MAX_SHIFT:
                    _naves_prw.SetPosition(_xr, _yr, _z)
                    _naves_prw.SetAngles(0, 270, 0)
                    self.objects.append(_naves_prw)
                if _is_SAH_215 or not _is_SAH_215 and self.knot_props.back <= MAX_SHIFT:
                    _naves_lev.SetPosition(_xl, _yl, _z)
                    _naves_lev.SetAngles(0, 360, 0)
                    self.appendNaves(_naves_lev = _naves_lev)
            else:
                raise ValueError("Выбрано несуществующее поведение навесов")

            return self.objects

        elif self.GetNaves()[0]:
            auto_naves = self.GetNaves()[0]
            _classname = uFurnFuncs.get_class_name(
                auto_naves, default="user_build.Accessory.Accessory", tableid=1)
            naveses_class = globals()[_classname]
            psz_scene = [
                max([self.knot_props._szs1, self.knot_props._szs2])] * 2

            def get_gabz(bb): return round(bb, 1)
            height_scene = [
                max([get_gabz(self.knot_props._h_right_wall),
                    get_gabz(self.knot_props._h_left_wall)])
            ] * 2
            def get_gaby(bb): return round(bb, 1)
            depth_scene = [
                max([get_gaby(self.knot_props._d_left_wall),
                    get_gaby(self.knot_props._d_right_wall)])
            ] * 2

            class_Naves = NavesTypesForCorner
            if not self.parent.is_top:
                # Если нижний
                if not self.parent._nog in [constants.NOG.NONE.value, constants.NOG.NAVES.value]:
                    # Если опоры есть
                    class_Naves = NavesTypesWitchNOG

            try:
                self._id_prw, self._id_lev = naveses_class.get_complect_naves(
                    psz_scene, height_scene, depth_scene, class_Naves=class_Naves
                )
                _naves_lev = Accessory.Accessory(self._id_lev)
                _naves_prw = Accessory.Accessory(self._id_prw)
                # поправка для навесов hettich
                _z = self.knot_props.top
                if self.knot_props._behave in [localconst.KnotBehavior.DEFAULT, localconst.KnotBehavior.BEHAVE_2]:
                    _xr = self.knot_props.right
                    _xl = self.knot_props.left
                    _y = SHIFT_Y_SAH_215 if self.knot_props.back > MAX_SHIFT else self.knot_props.back
                    _naves_prw.SetPosition(_xr, _y, _z)
                    _naves_lev.SetPosition(_xl, _y, _z)
                    self.appendNaves(_naves_prw, _naves_lev)
                elif self.knot_props._behave is localconst.KnotBehavior.BEHAVE_3:
                    _x = SHIFT_Y_SAH_215 if self.knot_props.right > MAX_SHIFT else self.knot_props.right
                    _yl = self.knot_props.back
                    _yr = self.knot_props.front
                    _naves_prw.SetPosition(_x, _yr, _z)
                    _naves_lev.SetPosition(_x, _yl, _z)
                    _naves_prw.SetAngles(0, 270, 0)
                    _naves_lev.SetAngles(0, 270, 0)
                    self.appendNaves(_naves_prw, _naves_lev)
                elif self.knot_props._behave is localconst.KnotBehavior.BEHAVE_1:
                    (_xr, _yl) = (SHIFT_Y_SAH_215, SHIFT_Y_SAH_215) if self.knot_props.right > MAX_SHIFT or self.knot_props.back > MAX_SHIFT else (self.knot_props.right, self.knot_props.back)
                    _xl = self.knot_props.left
                    _yr = self.knot_props.front
                    _naves_prw.SetPosition(_xr, _yr, _z)
                    _naves_prw.SetAngles(0, 270, 0)
                    self.appendNaves(_naves_prw = _naves_prw)
                    _naves_lev.SetPosition(_xl, _yl, _z)
                    _naves_lev.SetAngles(0, 360, 0)
                    self.appendNaves(_naves_lev = _naves_lev)
                else:
                    raise ValueError(
                        "Выбрано несуществующее поведение навесов")
                return self.objects

            except ErrorAutoSearshNaves:
                ebox = ErrMsgBox(
                    "Ошибка подбора мебельного навеса",
                    text="Изготовление требует согласования с сотрудниками фабрики",
                )
                ebox.view()
                naveses = (None, None)
                return naveses

    def Make(self):
        try:
            return self.__MakeNaves()
        except:
            raise ValueError("Навесы не были построены")
