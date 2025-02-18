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
from core_k.rdnomenclature import priceinfo
import typing
from MKitchen.shell_corner import constants as localconst
import k3
from based_build import Panel
import based_build.Constants as Constants
import putcutr
import core_k
import mAttribute
import math
DEPTH = 16-12 # заглубиление ЗС в паз (4мм)
HALF_HITCH = 16 # нахлест ЗС на угловую планку в случае BEHAVE_1
CORNER_SLICE = 73 # отступ до ЗС в случае BEHAVE_1
MAX_SZS = 300 # max отступ до ЗС в случае BEHAVE_1
@dataclass
class RSH_backwalls:
    _behave: localconst.KnotBehavior = localconst.KnotBehavior.DEFAULT
    _prmater: float = 0
    _back_wall_prmater = 0
    _h_hdf: float = 0

    # расстояние от стены до ЗС (прав и лев)
    _szs1: float = 0
    _szs2: float = 0

    # координаты внутренних плоскостей ниши внутри вызывающей секции
    # вычисляются и переопределяются для разных поведений в адаптерах
    top : float = 0
    bottom : float = 0
    left : float = 0
    right : float = 0
    back : float = 0
    front : float = 0
    _naveses = None

class BackWall(Panel.Panel):
    """Объект ЗС
    """    
    def __init__(self, side: str = ''):
        super().__init__()
        self.side = side

class PsewdoObj(uFurnObject.FurnObject):
    """Псевдообъект для предотвращения создания единственного объекта в группе
    """
    def __init__(self,*w,psobilder=None,**kw):
        super().__init__()
        self.psobilder=psobilder

    def Draw(self):
        if self.psobilder is None:
            self._object=k3.line(0,0,0,1,0,0)[0]
        else:
            self._object=self.psobilder()
        return self._object
    def _AssignAttributes(self):
        mAttribute.attach_fromdelete(self._object)

class KnotCornerBackWalls(uFurnObject.FurnObject):
    """Объект узла задних стенок для поведений DEFAULT, BEHAVE_1,2,3 прототипа V-86
    """    
    def __init__(self, knot_props: RSH_backwalls):
        super().__init__()
        self.SetFurnType('011300')
        self.knot_props = knot_props
        self._elemname = "Задние стенки"  # Узел
        self.knot_props._back_wall_prmater = int(priceinfo(self.knot_props._prmater, "HDF_Color", 0))
        self.knot_props._h_hdf = k3.priceinfo(self.knot_props._back_wall_prmater, "Thickness", 4)

    def __MakeBackWalls(self):
        "ЗC"
        self.objects = []
        if self.knot_props._behave in [localconst.KnotBehavior.DEFAULT, localconst.KnotBehavior.BEHAVE_1]:
            h = self.knot_props.top - self.knot_props.bottom + DEPTH * 2
            dl = self.knot_props.left - self.knot_props.right + DEPTH - CORNER_SLICE
            dr = self.knot_props.front - self.knot_props.back + DEPTH - CORNER_SLICE
            pos_z = self.knot_props.bottom - DEPTH
            pos_x_r = self.knot_props._szs2
            pos_y_r = self.knot_props.back + CORNER_SLICE
            pos_x_l = self.knot_props.right + CORNER_SLICE
            pos_y_l = self.knot_props._szs1
            right_backwall = BackWall('R')
            left_backwall =  BackWall('L')
            right_backwall.SetMater(self.knot_props._back_wall_prmater)
            left_backwall.SetMater(self.knot_props._back_wall_prmater)
            right_backwall.SetElemName('Задняя стенка R')
            left_backwall.SetElemName('Задняя стенка L')
            right_backwall.SetMajorPlace(Constants.MAJORPLACE_POST)
            left_backwall.SetMajorPlace(Constants.MAJORPLACE_WALL)
            right_backwall.SetGabs(h, dr)
            left_backwall.SetGabs(h, dl)
            right_backwall.SetPosition(pos_x_r, pos_y_r, pos_z)
            left_backwall.SetPosition(pos_x_l, pos_y_l, pos_z)

            self.objects.append(left_backwall)
            self.objects.append(right_backwall)

        elif self.knot_props._behave is localconst.KnotBehavior.BEHAVE_2:
            h = self.knot_props.top - self.knot_props.bottom + DEPTH * 2
            d = self.knot_props.left - self.knot_props.right + DEPTH * 2
            pos_z = self.knot_props.bottom - DEPTH
            pos_x = self.knot_props.right - DEPTH
            pos_y = self.knot_props._szs1
            left_backwall = Panel.Panel()
            left_backwall.SetMater(self.knot_props._back_wall_prmater)
            left_backwall.SetElemName('Задняя стенка S')
            left_backwall.SetMajorPlace(Constants.MAJORPLACE_WALL)
            left_backwall.SetGabs(h, d)
            left_backwall.SetPosition(pos_x, pos_y, pos_z)

            self.objects.append(left_backwall)
            pso=PsewdoObj()
            self.objects.append(pso)

        elif self.knot_props._behave is localconst.KnotBehavior.BEHAVE_3:
            h = self.knot_props.top - self.knot_props.bottom + DEPTH * 2
            d = self.knot_props.front - self.knot_props.back + DEPTH * 2
            pos_z = self.knot_props.bottom - DEPTH
            pos_x = self.knot_props._szs2
            pos_y = self.knot_props.back - DEPTH
            left_backwall = Panel.Panel()
            left_backwall.SetMater(self.knot_props._back_wall_prmater)
            left_backwall.SetElemName('Задняя стенка S')
            left_backwall.SetMajorPlace(Constants.MAJORPLACE_POST)
            left_backwall.SetGabs(h, d)
            left_backwall.SetPosition(pos_x, pos_y, pos_z)
            self.objects.append(left_backwall)
            pso=PsewdoObj()
            self.objects.append(pso)
        else:
            raise ValueError("Выбрано несуществующее поведение задних стенок")

        return self.objects
    def get_cutout_create(self, naves: k3.K3Obj) -> bool:
        """
        Свойство номенклатуры создавать вырез в панели CutoutCreate
        """
        acc_id = mAttribute.get_priceid(naves)
        return bool(priceinfo(acc_id, 'CutoutCreate',
                            defvalue=0, tableid=1, arr_name=''))

    def get_hole_backwall(self, naves: k3.Group) -> typing.Set[k3.K3Obj]:
        '''найти в группе на первом уровне владельца атрибута HoleBackWall'''
        return set(filter(lambda x: mAttribute.getattr_holebackwall(x)==True,core_k.structobject.getArrObjG(naves)))

    def build_cutouts_in_back_wall(self, naveses: typing.List[k3.K3Obj] = [],
                                   handle_back:'drawprof.mPanel.PanelRectangle' = None
                                   )->k3.Group:
        '''Построить сквозные вырезы или отверстия для навесов в задней(их) стенке(ах)'''
        if not naveses:
            return

        bild = putcutr.PutCutrEx(panel=handle_back, cut_type=1, dept=0, mapp=6)
        bild.init_panel()
        putcutr_result=False
        if self.get_cutout_create(naveses[0]):
            if 'L' in handle_back.Name or 'l' in handle_back.Name:
                cuts = putcutr.get_cut_line_object(naveses[1])
                if cuts:
                    cut = cuts[0]
                    bild.pat=cut
                    bild.set_position_v()
                    bild.add_comment()
                    putcutr_result=True
            if 'R' in handle_back.Name or 'r' in handle_back.Name:
                cuts = putcutr.get_cut_line_object(naveses[0])
                if cuts:
                    cut = cuts[0]
                    bild.pat=cut
                    bild.set_position_v()
                    bild.add_comment()
                    putcutr_result=True

            if 'S' in handle_back.Name or 's' in handle_back.Name:
                for naves in naveses:
                    cuts = putcutr.get_cut_line_object(naves)
                    if cuts:
                        cut = cuts[0]
                        bild.pat=cut
                        bild.set_position_v()
                        bild.add_comment()
                        putcutr_result=True
        if putcutr_result:
            with core_k.structobject.ExtractContext(bild.mpanel.holder) as manager:
                bild.mpanel.panel_execute()
                handle_back = bild.mpanel.holder
                manager._object=handle_back
            return handle_back

        elif self.get_hole_backwall(naveses[0]) and self.knot_props._behave in [localconst.KnotBehavior.BEHAVE_1, localconst.KnotBehavior.DEFAULT]:
            temp_ymin1 = core_k.objgab.obj_k3_gab3(handle_back.holder)[4]
            temp_ymin2 = core_k.objgab.obj_k3_gab3(handle_back.holder)[3]
            handle_back_ymin = temp_ymin1 if temp_ymin1 < MAX_SZS else temp_ymin2
            if 'L' in handle_back.Name or 'l' in handle_back.Name:
                hole_line=self.get_hole_backwall(naveses[1]).pop()
                temp_new_depth1=math.ceil(abs(handle_back_ymin - core_k.objgab.obj_k3_gab3(hole_line)[1]))
                temp_new_depth2=math.ceil(abs(handle_back_ymin - core_k.objgab.obj_k3_gab3(hole_line)[0]))
                new_depth = temp_new_depth1 if temp_new_depth1 < MAX_SZS else temp_new_depth2
                with core_k.structobject.ExtractContext(hole_line) as manager:
                    k3.holes(k3.k_edit, hole_line, new_depth, 15, 0, 0, k3.k_no)
                    pnt=k3.Var()
                    k3.objident(k3.k_last,1,pnt)
                    manager._object=pnt.value
                return handle_back
            elif 'R' in handle_back.Name or 'r' in handle_back.Name:
                hole_line=self.get_hole_backwall(naveses[0]).pop()
                temp_new_depth1=math.ceil(abs(handle_back_ymin - core_k.objgab.obj_k3_gab3(hole_line)[1]))
                temp_new_depth2=math.ceil(abs(handle_back_ymin - core_k.objgab.obj_k3_gab3(hole_line)[0]))
                new_depth = temp_new_depth1 if temp_new_depth1 < MAX_SZS else temp_new_depth2
                with core_k.structobject.ExtractContext(hole_line) as manager:
                    k3.holes(k3.k_edit, hole_line, new_depth, 15, 0, 0, k3.k_no)
                    pnt=k3.Var()
                    k3.objident(k3.k_last,1,pnt)
                    manager._object=pnt.value
                return handle_back

        elif self.get_hole_backwall(naveses[0]) and self.knot_props._behave is localconst.KnotBehavior.BEHAVE_2:
            handle_back_ymin = core_k.objgab.obj_k3_gab3(handle_back.holder)[4]
            for naves in naveses:
                hole_line=self.get_hole_backwall(naves).pop()
                new_depth=math.ceil(abs(handle_back_ymin - core_k.objgab.obj_k3_gab3(hole_line)[1]))
                # новые параметры  сверловки h1 d1 h2 d2
                with core_k.structobject.ExtractContext(hole_line) as manager:
                    k3.holes(k3.k_edit, hole_line, new_depth, 15, 0, 0, k3.k_no)
                    pnt=k3.Var()
                    k3.objident(k3.k_last,1,pnt)
                    manager._object=pnt.value
            return handle_back
        elif self.get_hole_backwall(naveses[0]) and self.knot_props._behave is localconst.KnotBehavior.BEHAVE_3:
            handle_back_ymin = core_k.objgab.obj_k3_gab3(handle_back.holder)[3]
            for naves in naveses:
                hole_line=self.get_hole_backwall(naves).pop()
                new_depth=math.ceil(abs(handle_back_ymin - core_k.objgab.obj_k3_gab3(hole_line)[0]))
                # новые параметры  сверловки h1 d1 h2 d2
                with core_k.structobject.ExtractContext(hole_line) as manager:
                    k3.holes(k3.k_edit, hole_line, new_depth, 15, 0, 0, k3.k_no)
                    pnt=k3.Var()
                    k3.objident(k3.k_last,1,pnt)
                    manager._object=pnt.value
            return handle_back
        return False

    def postDrawBackwalls(self, backwalls, *arg, **kwargs):
        """метод который вызывается в PostDraw родительской группы
        создаст вырезы, подменит старые ЗС на новые
        """        
        if self.knot_props._naveses:
            from drawprof import mPanel
            if self.knot_props._behave in [localconst.KnotBehavior.BEHAVE_2,
                                           localconst.KnotBehavior.BEHAVE_3]:
                i = backwalls.objects[0]
                mpanel = mPanel.PanelRectangle()
                mpanel.panelInit(i._object)
                naveses = []
                for obj in self.knot_props._naveses.objects:
                    naveses.append(obj._object)
                i._object = self.build_cutouts_in_back_wall(naveses, mpanel)
            else:    
                for i in backwalls.objects:
                    mpanel = mPanel.PanelRectangle()
                    mpanel.panelInit(i._object)
                    naveses = []
                    for obj in self.knot_props._naveses.objects:
                        naveses.append(obj._object)
                    i._object = self.build_cutouts_in_back_wall(naveses, mpanel)


    def Make(self):
        try:
            return self.__MakeBackWalls()
        except:
            raise ValueError("ЗС не были построены")
