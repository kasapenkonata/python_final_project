import pygame
from classes import Wall, Button, Ray
import numpy as np

# --- НАСТРАИВАЕМЫЕ ПЕРЕМЕННЫЕ ---
number_of_rays = 2  # Max 360
wall_thicknes = 2
boundarySpacing = 0
# ------------------------------


# Настройки
pygame.init()
size = (700, 500)
menuSize = (90, 80)
surface = pygame.display.set_mode(size, pygame.RESIZABLE)
menuSurface = pygame.Surface(menuSize)
pygame.display.set_caption("Rays")
font = pygame.font.SysFont("monospace", 15)

# Цвета
WHITE = (100, 100, 100)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 50)

# Переменные для обработки
walls = []
rays1 = []
rays2 = []
drawing = False
wall_starting_pos = (0, 0)
play = False
finished = False
clock = pygame.time.Clock()
counter = 1

# --- НАЧАЛЬНАЯ НАСТРОЙКА ---

# Buttons
resetButton = Button(10, size[1] - menuSize[1] + 10, 70, 25, 'Очистить', RED)
playButton = Button(10, resetButton.y + 10 + resetButton.height, 70, 25, 'Начать', GREEN)


# Границы
def addBoundaries():
    walls.insert(0, Wall((boundarySpacing, boundarySpacing), (size[0] - boundarySpacing, boundarySpacing)))
    walls.insert(0, Wall((boundarySpacing, boundarySpacing), (boundarySpacing, size[1] - boundarySpacing)))
    walls.insert(0, Wall((boundarySpacing, size[1] - boundarySpacing),
                         (size[0] - boundarySpacing, size[1] - boundarySpacing)))
    walls.insert(0, Wall((size[0] - boundarySpacing, size[1] - boundarySpacing),
                         (size[0] - boundarySpacing, boundarySpacing)))


addBoundaries()


# Рисование меню
def drawMenu():
    # Установить цвет и прозрачность окна меню
    menuSurface.fill(WHITE)
    menuSurface.set_alpha(126)

    # Окно меню рисования
    surface.blit(menuSurface, (0, size[1] - menuSize[1]))

    # Кнопки рисования
    resetButton.draw(surface)
    playButton.draw(surface)


# -------- Основной цикл программы -----------
while not finished:

    # --- ГЛАВНЫЙ ЦИКЛ СОБЫТИЙ ---
    for event in pygame.event.get():
        # Если пользователь хочет уйти
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                finished = True

        # Пользователь изменил размер окна
        if event.type == pygame.VIDEORESIZE:
            size = (event.w, event.h)
            surface = pygame.display.set_mode(size, pygame.RESIZABLE)

            # Изменить границы
            walls = walls[4:]
            addBoundaries()

            # Кнопки изменения
            resetButton.y = size[1] - menuSize[1] + 10
            playButton.y = resetButton.y + 10 + resetButton.height

        # Пользователь нажал кнопку мыши
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()

            if event.button == 1:  # Левый клик
                # Проверка, нажал ли пользователь одну из кнопок
                if resetButton.clicked(pos):
                    walls = []
                    addBoundaries()

                elif playButton.clicked(pos):
                    # Изменить статус кнопки воспроизведения
                    if play:
                        playButton.color = GREEN
                        playButton.text = 'Начать'
                    else:
                        playButton.color = YELLOW
                        playButton.text = 'Остановить'

                    drawing = False
                    play = not play

                elif not play:  # Рисование стены

                    # Убедитесь, что пользователь уже рисует стену
                    if drawing:
                        # Завершить рисунок и добавьте новую стену
                        drawing = False
                        walls.append(Wall(wall_starting_pos, pos))
                    else:
                        # Начать рисовать
                        drawing = True
                        wall_starting_pos = pos

            elif event.button == 3:  # Правый клик
                drawing = False

    # --- ИГРОВАЯ ЛОГИКА ---
    # Рассчитать новые лучи из источника
    if play:
        rays1 = []
        rays2 = []
        for i in range(0, number_of_rays):
            # Создать новый луч
            # все созданные лучи помещаем в массив rays2
            ray = Ray(pygame.mouse.get_pos(), i * 360 / number_of_rays)
            rays2.append(ray)
            counter = 1
        print('NewRayDone')
        while counter != 0:
            print('DoNewItteration')
            counter = 0
            closest = 10000000000000000000000
            # Проверить каждую стену
            for ray in rays2:
                for wall in walls:
                    # Проверка, есть ли пересечение со стенкой
                    if wall.intersecting(ray) is not None:
                        point = wall.intersecting(ray)
                        distance = ((point[0] - ray.start_pos[0]) ** 2 + (point[1] - ray.start_pos[1]) ** 2) ** (1 / 2)
                        # Проверка, является ли это ближайшей стеной
                        if closest > distance:
                            ray.end_point = point
                            closest = distance
                            reflect_angle = wall.reflection(ray)
                    else:
                        continue
            '''for ray in rays2:
                for walls in wall:
                    # должны вызвать функцию отражения, которая создаст отраженный луч
                    wall.reflection()
                rays1.append(ray)
                if reflect_angle[1] > 0.3:
                    new_ray = Ray(point, reflect_angle[0])
                    new_ray.brightness = reflect_angle[1]
                    rays2.append(new_ray)
                else:
                    continue'''
            rays1.append(ray)
            if ray in rays2:
                rays2.remove(ray)
            if reflect_angle[1] > 0.2:
                new_ray = Ray(point, reflect_angle[0])
                new_ray.brightness = reflect_angle[1]
                counter += 1
                rays2.append(new_ray)
                break
        print(counter)

    # --- РИСОВАНИЕ ---
    surface.fill(BLACK)

    # Рисование рисующихся стен
    if drawing:
        pygame.draw.line(surface, WHITE, wall_starting_pos, pygame.mouse.get_pos(), wall_thicknes)

    # Рисование существующих стен
    for wall in walls:
        pygame.draw.line(surface, WHITE, wall.A, wall.B, wall_thicknes)

    # Рисование лучей
    if play:
        pygame.draw.circle(surface, WHITE, pygame.mouse.get_pos(), 10)

        for ray in rays1:
            pygame.draw.line(surface, (100 * ray.brightness, 100 * ray.brightness, 100 * ray.brightness), ray.start_pos,
                             ray.end_point, 1)

    # Рисование меню и кнопок
    drawMenu()

    # --- ОБНОВЛЕНИЕ ЭКРАНА ---
    pygame.display.flip()

    clock.tick(60)

pygame.quit()