import pygame
import numpy as np
import random


# Класс стены
class Wall():
    def __init__(self, A, B):
        # A, B - концы стены
        self.A = A
        self.B = B
        # проекции стены
        self.x = self.A[0] - self.B[0]
        self.y = self.A[1] - self.B[1]
        self.angle_reflect = 0
        self.point = []

    def reflection(self, obj):
        # проекции луча
        xobj = obj.start_pos[0] - obj.end_point[0]
        yobj = obj.start_pos[1] - obj.end_point[1]
        # try:
        self.angle_reflect = obj.angle + 2 * np.arccos(
            np.abs((self.x * xobj + self.y * yobj) / (((self.x ** 2 + self.y ** 2) * (xobj ** 2 + yobj ** 2)) ** 0.5)))
        '''except ZeroDivisionError:
            print(xobj, yobj, obj.start_pos, obj.end_point)'''
        return (self.angle_reflect, obj.brightness * 0.5)

    def intersecting(self, obj):
        # начало и конец луча

        x1, y1 = obj.start_pos
        x2, y2 = obj.end_point

        x3, y3 = self.A
        x4, y4 = self.B

        # считаем определитель. Если он оказывается равным 0, то луч и стенка параллельны
        div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if div != 0:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / div
            s = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / div
            # Проверить, есть ли точка пересечения
            if 0.1 < t and s >= 0.000 and s <= 1.000:
                self.point = (int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1)))
                return (self.point)
            else:
                return (None)
        else:
            return (None)

# Класс зеркала
class Mirror():
    def __init__(self, A, B):
        # coord1, coord2 - крайние точки отрезка, задающего зеркало
        self.A = A
        self.B = B

        # проекции зеркала
        self.x = self.A[0] - self.B[0]
        self.y = self.A[1] - self.B[1]
        self.angle_reflect = 0
        # self.point = []

    # отражение от зеркала
    # функция принимает на вход луч
    # функция возвращает: 1) угол, под которым отразился луч
    #                     2) яркость отраженного луча
    def reflection(self, obj):
        # проекции луча
        xobj = obj.start_pos[0] - obj.end_point[0]
        yobj = obj.start_pos[1] - obj.end_point[1]
        # try:
        self.angle_reflect = obj.angle + 2 * np.arccos(
            np.abs((self.x * xobj + self.y * yobj) / (((self.x ** 2 + self.y ** 2) * (xobj ** 2 + yobj ** 2)) ** 0.5)))
        '''except ZeroDivisionError:
            print(xobj, yobj, obj.start_pos, obj.end_point)'''
        return (self.angle_reflect, obj.brightness)

    # функция возвращает ближайшее препятствие с которым встречается луч
    # функция принимает луч
    def intersection(self, obj):
        # начало и конец луча
        x1, y1 = obj.start_pos
        x2, y2 = obj.end_point

        x3, y3 = self.A
        x4, y4 = self.B

        # считаем определитель. Если он оказывается равным 0, то луч и стенка параллельны
        div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if div != 0:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / div
            s = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / div
            # Проверить, есть ли точка пересечения
            if 0.1 < t and s >= 0.000 and s <= 1.000:
                self.point = (int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1)))
                return (self.point)
            else:
                return (None)
        else:
            return (None)

# Класс стенки
class Absorber():
    def __init__(self, A, B):
        # A, B - крайние точки отрезка, задающего зеркало
        self.A = A
        self.B = B

        # проекции стенки
        self.x = self.A[0] - self.B[0]
        self.y = self.A[1] - self.B[1]
        self.angle_dispersed = 0

    # функция принимает на вход луч
    # функция возвращает : 1) углы, под которыми идут рассеянные лучи (их от 0 до 20) как массив,
    #                      2) яркость рассеянных лучей (она одинакова для всех лучей)
    def dispersion(self, obj):
        # проекции луча
        xobj = obj.start_pos[0] - obj.end_point[0]
        yobj = obj.start_pos[1] - obj.end_point[1]

        number_of_dispersed_rays = random.random() * 20
        dispersed_rays = []
        brightness = 0.5 * obj.brightness / number_of_dispersed_rays
        for i in range (number_of_dispersed_rays):
            angle_refracted = obj.angle + np.arccos(
                np.abs((self.x * xobj + self.y * yobj) / (((self.x ** 2 + self.y ** 2) * (xobj ** 2 + yobj ** 2)) ** 0.5))) + random.random() * 2 * np.pi
            dispersed_rays.append(angle_refracted)
        return (self.dispersed_rays, brightness)

    def intersection(self, obj):
        # начало и конец луча
        x1, y1 = obj.start_pos
        x2, y2 = obj.end_point

        x3, y3 = self.A
        x4, y4 = self.B

        # считаем определитель. Если он оказывается равным 0, то луч и стенка параллельны
        div = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if div != 0:
            t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / div
            s = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / div
            # Проверить, есть ли точка пересечения
            if 0.1 < t and s >= 0.000 and s <= 1.000:
                self.point = (int(x1 + t * (x2 - x1)), int(y1 + t * (y2 - y1)))
                return (self.point)
            else:
                return (None)
        else:
            return (None)


class Plate():
    def __init__(self, A, B, flag_in, n):
        # A, B - крайние точки отрезка, задающего плоскопараллельную пластину
        self.A = A
        self.B = B
        self.flag_in = False
        self.n = n

        # проекции пластины
        self.x = self.A[0] - self.B[0]
        self.y = self.A[1] - self.B[1]

    # функуия принимает луч, коэффициент преломления n, flag_in, показывающий, находится луч вне или внутри пластины
    # функция возвращает угол, под которым выходит новый луч
    def reflection(self, obj, n, flag_in):
        # луч
        xobj = obj.start_pos[0] - obj.end_point[0]
        yobj = obj.start_pos[1] - obj.end_point[1]

        # угол падения луча на стенку
        tetta = ( self.x * xobj + self.y * xobj ) / ((self.x ** 2 + self.y ** 2 ) * (xobj ** 2 + yobj ** 2)) ** 0.5
        # угол преломления луча  от стенки
        fi = np.arcsin(np.sin(tetta) / self.n)
        # угол под которым пойдет луч после преломления
        angle = 0
        if (flag_in == False):
            fi = np.arcsin(np.sin(tetta) / self.n)
            delta = tetta - fi
            angle = tetta - delta
            return(fi)
        if (flag_in == True):
            fi = (np.sin(tetta) * self.n)
            delta = fi - tetta
            angle = tetta + delta
            return(fi)








class Ray():
    def __init__(self, start_pos, angle):
        self.brightness = 1
        self.start_pos = start_pos
        self.angle = angle
        self.end_point = self.getHelperPoint()

    def getHelperPoint(self):
        # Требуется для расчета пересечений
        # Получение вектора от начальной позиции, угла и длины вектора
        return (np.cos(self.angle) + self.start_pos[0], np.sin(self.angle) + self.start_pos[1])


class Button():
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, t):
        self._text = t
        self.label = pygame.font.SysFont("monospace", 10).render(t, 1, (0, 0, 0))

    def values(self):
        return (self.x, self.y, self.width, self.height)

    def draw(self, surface):
        # Рисование кнопки
        pygame.draw.rect(surface, self.color, self.values())
        # Рисование метки
        surface.blit(self.label, (self.x + (self.width / 2 - self.label.get_width() / 2),
                                  self.y + (self.height / 2 - self.label.get_height() / 2)))

    def clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False