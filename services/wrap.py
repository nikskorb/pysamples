# -*- coding: utf-8 -*-
from based_build import Panel
import functools
__author__ = 'Aleksandr Dragunkin'
__date__ = '2024-06-05 17:40:20'
__copyright__ = 'Copyright 2023, For K3Mebel Project'
__credits__ = []
__license__ = 'GPL'
__maintainer__ = 'Nikolay Skorobogatko'
__email__ = ''
__status__ = 'Development'
__version__ = '0.0.1'


def add_bands_wrap_shelf(list_sides=[]):
    '''декоратор для Make - метода панели
    назначить кромку на стороны панели по списку
    list_sides

    Example:
    @add_bands_wrap(list_sides = (
            Constants.PANELSIDE_ANG3,
            Constants.PANELSIDE_E
        ))
    def _MakeLeftPanel(self):
        Бла-бла-бла
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwards):
            pan = func(*args, **kwards)
            for b in list_sides:
                band = Panel.Band()
                a = list(filter(lambda inst: hasattr(
                    inst, 'mater_shelves'), args))
                a.extend(list(filter(lambda inst: hasattr(
                    inst, 'mater_shelves'), kwards.values())))
                for btype in filter(lambda inst: hasattr(inst, 'mater_shelves'), a):
                    band.SetCommon(b, btype.mater_shelves.band_type)
                    break
                pan.panel.AddBand(band)
            return pan
        return wrapper
    return decorator


def add_bands_wrap_side(list_sides=[]):
    '''декоратор для Make - метода панели
    назначить кромку на стороны панели по списку
    list_sides

    Example:
    @add_bands_wrap(list_sides = (
            Constants.PANELSIDE_ANG3,
            Constants.PANELSIDE_E
        ))
    def _MakeLeftPanel(self):
        Бла-бла-бла
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwards):
            pan = func(*args, **kwards)
            for b in list_sides:
                band = Panel.Band()
                a = list(filter(lambda inst: hasattr(inst, 'mater_sides'), args))
                a.extend(list(filter(lambda inst: hasattr(
                    inst, 'mater_sides'), kwards.values())))
                for btype in filter(lambda inst: hasattr(inst, 'mater_sides'), a):
                    band.SetCommon(b, btype.mater_sides.band_type)
                    break
                pan.panel.AddBand(band)
            return pan
        return wrapper
    return decorator
