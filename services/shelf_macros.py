__author__ = 'Nikolay Skorobogatko'
__date__ = '2024-06-05 22:06:16'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = ['Aleksandr Dragunkin']
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'
import k3
import core_k
# from . import shelves
# from MKitchen.shell_corner.shelves import RSH_Shelves
import typing
import math
import mAttribute
from mlogger import logger



# macro
def line_create( *args:float)->typing.Tuple[k3.K3Obj]:
    """Создать линии и присвоить им атрибут на удаление

    Returns:
        typing.Tuple[k3.K3Obj]: Сама линия
    """
    obj=k3.line(*args)
    # mAttribute.attach_fromdelete(obj)
    return obj

def fillet_create(rad,l1,l2,*a,**k)->k3.Arc:
    """Построить скругление двум отрезкам

    Returns:
        k3.Arc: _description_
    """
    # arc=k3.fillet(k3.k_radius,rad,l1,l2)[0]
    ps=k3.VarArray(9)
    k3.skrug(l1,l2,rad,ps)
    result=[a.value for a in ps]
    ps=core_k.ptrans.ptransGcsToPsc(args=result)
    return ps
    # mAttribute.attach_fromdelete(arc)
    # return arc
class CountorObj:
    def __init__(self, knot_props):
        self.x = knot_props._dx
        self.y = knot_props._dy
        self.r1 = knot_props._r1
        self.r2 = knot_props._r2
        self.delta = knot_props._delta # как отступ от переда
        self.ps = [0] * 10
        self.ps1 = [0] * 10
        self.contour = None  # ссылка на объект контура

    def recalculate_parameters(self):
        dx = 0
        dy = 0
        if self.delta > 0:
            dx = self.delta / math.cos(math.atan(self.x / self.y))
            dy = self.delta / math.sin(math.atan(self.x / self.y))
        self.x += dx
        self.y += dy
        return dx, dy

    def params_line(self):
        self.zln1 = 0

        # Фаска
        self.xln1 = self.x
        self.yln1 = 0
        self.xlk1 = 0
        self.ylk1 = self.y

        # X
        self.xln2 = self.x
        self.yln2 = 0
        self.xlk2 = self.x + self.x
        self.ylk2 = 0

        # Y
        self.xln3 = 0
        self.yln3 = self.y
        self.xlk3 = 0
        self.ylk3 = self.y + self.y

    def make_line(self):
        # Создание линий в K3
        self.l1 = line_create(self.xln1, self.yln1, self.zln1,
                          self.xlk1, self.ylk1, self.zln1)
        self.l2 = line_create(self.xln2, self.yln2, self.zln1,
                          self.xlk2, self.ylk2, self.zln1)
        self.l3 = line_create(self.xln3, self.yln3, self.zln1,
                          self.xlk3, self.ylk3, self.zln1)
        return self.l1, self.l2, self.l3



    def params_contour(self):
        # Замыкание контура
        return line_create(self.ps1[0], self.ps1[1], self.ps1[2],
                           self.ps1[0], self.ps1[1]-10, self.ps1[2],
                           -10, -10, 0,
                           self.ps[3]-10, self.ps[4], self.ps[5],
                           self.ps[3], self.ps[4], self.ps[5])

    def put_polyline_contour(self):
        # arr = []
        initial_nobj=k3.sysvar(60)
        self.recalculate_parameters()
        self.params_line()

        # Построить полилинию выреза для формирования фаски со скруглениями у полки
        # Сформировать список аргументов для передачи команде построения полилинии
        poly_arguments=[k3.k_normal,(0,0,1),] # Задать нормаль плскости построения поллинии
        if self.r1 == 0: self.r1 = 0.1
        if self.r2 == 0: self.r2 = 0.1
        self.l1, self.l2, self.l3 = self.make_line() # Построить 3 линии абриса фаски у полки
        # Построить Контур выреза для формирования фаски со скруглениями у полки
        if self.r1 > 0:
            # Если первый радиус определён

            ps1=fillet_create(self.r1, self.l1, self.l2) # Вычислить точки дуги сопряжения

            # Добавить в список аргументов полилинии дугу
            poly_arguments.extend([ps1[3:6], # Начальная точка полилинии
                                    k3.k_arc,
                                    ps1[6:9],
                                    ps1[:3]]) # Конечная точка дуги
        else:
            raise NotImplementedError() # Просто начало полилинии Но! Этот вариант не работает радиус должен быть всегда

        if self.r2>0:
            # Если второй  радиус определён

            ps2=fillet_create(self.r2, self.l3, self.l1) # Вычислить точки дуги сопряжения

            # Добавить в список аргументов линию соединяющую дуги
            poly_arguments.extend([k3.k_line, ps2[3:6]])
            # Добавить дугу
            poly_arguments.extend([k3.k_arc, ps2[:3]])
        else:
            raise NotImplementedError()

        # Добавить замыкающие сегменты
        poly_arguments.extend([k3.k_line, # Линия
                                k3.k_relative, # В приращении относительно текущей точки
                                (-10, -0, 0), # горизонтально на -10 мм
                                (-10, -10, 0), # вертикально в точку
                                (ps1[3], -10, 0) ,
                                ps1[3:6] # k3.k_close # ЗАмыкаем
                                ])

        # Удалить вспомогательные линии
        k3.delete(self.l1, self.l2, self.l3)


        # logger.debug(f'poly_arguments  {poly_arguments}')
        # Построить полилинию
        self.contour = k3.pline(poly_arguments)
        # Пометить её на удаление
        mAttribute.attach_fromdelete(self.contour)
        return self.contour
