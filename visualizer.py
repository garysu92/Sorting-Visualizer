import pygame
import random
import math
pygame.init()


class info:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    RED = 255, 0, 0
    GREEN = 0, 255, 0
    GREY = 127, 127, 127
    SIDE_PADDING = 120
    TOP_PADDING = 150
    FONT = pygame.font.SysFont('verdana', 20)

    def __init__(self, w, h, lst):
        self.width = w
        self.height = h

        self.window = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.minVal = min(lst)
        self.maxVal = max(lst)

        # calculate the width of each bar
        self.barWidth = round(self.width - self.SIDE_PADDING) / (2 * len(lst))
        # calculate the height of each block of the bar
        self.blockHeight = math.floor((self.height - self.TOP_PADDING) /
                                      (self.maxVal - self.minVal))
        self.startX = self.SIDE_PADDING // 2


def draw(draw_info):
    draw_info.window.fill(draw_info.BLACK)
    options = draw_info.FONT.render(
        "R (reset) | SPACE (sort) | A (ascending) | D (descending)", 1, draw_info.WHITE)
    algo = draw_info.FONT.render(
        "B (bubble sort) | I (insertion sort) | S (selection sort) | M (merge sort) | Q (quick sort)", 1, draw_info.WHITE)
    draw_info.window.blit(
        algo, (draw_info.width/2 - algo.get_width()/2, 40))
    draw_info.window.blit(
        options, (draw_info.width/2 - options.get_width()/2, 15))
    drawBars(draw_info, -1, -1)
    pygame.display.update()


def bubbleSort(draw_info, ascending):
    lst = draw_info.lst
    frames = pygame.time.Clock()
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            frames.tick(150)
            if (ascending and lst[i] > lst[j]) or (not ascending and lst[i] < lst[j]):
                lst[i], lst[j] = lst[j], lst[i]
            drawBars(draw_info, i, j, -1, True)


def insertionSort(draw_info, ascending):
    lst = draw_info.lst
    frames = pygame.time.Clock()
    for i in range(len(lst)):
        for j in range(i, 0, -1):
            frames.tick(50)
            if (ascending and lst[j] < lst[j - 1]) or (not ascending and lst[j] > lst[j - 1]):
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
            drawBars(draw_info, j, j - 1, -1, True)


def selectionSort(draw_info, ascending):
    lst = draw_info.lst
    frames = pygame.time.Clock()
    idx = 0
    for i in range(len(lst)):
        idx = i
        for j in range(i, len(lst)):
            frames.tick(150)
            if (ascending and lst[j] < lst[idx]) or (not ascending and lst[j] > lst[idx]):
                idx = j
            drawBars(draw_info, idx, j, -1, True)
        lst[i], lst[idx] = lst[idx], lst[i]


def quickSort(draw_info, ascending):
    quickSortRange(draw_info, ascending, 0, len(draw_info.lst))


def quickSortRange(draw_info, ascending, start, end):
    lst = draw_info.lst
    if end <= start:
        return
    pos = end - 1
    frames = pygame.time.Clock()
    for i in range(end - 1, start, -1):
        frames.tick(150)
        if (ascending and lst[i] > lst[start]) or (not ascending and lst[i] < lst[start]):
            lst[pos], lst[i] = lst[i], lst[pos]
            pos -= 1
        drawBars(draw_info, start, i, pos, True)
    lst[pos], lst[start] = lst[start], lst[pos]
    quickSortRange(draw_info, ascending, start, pos)
    quickSortRange(draw_info, ascending, pos + 1, end)


def merge(draw_info, lst, lst1, lst2, ascending):
    x1 = x2 = 0
    frames = pygame.time.Clock()
    for pos in range(len(lst1) + len(lst2)):
        frames.tick(100)
        tempList = lst
        p1 = p2 = -1
        list1 = True
        if x1 == len(lst1) or (x2 < len(lst2) and ((ascending and lst2[x2] < lst1[x1]) or (not ascending and lst2[x2] > lst1[x1]))):
            lst[pos] = lst2[x2]
            x2 += 1
            list1 = False
        else:
            lst[pos] = lst1[x1]
            x1 += 1
        for i in range(len(lst)):
            if lst[i] != tempList[i]:
                if p1 == -1:
                    p1 = i
                else:
                    p2 = i
        drawBars(draw_info, p1, p2, -1, True)
        if list1:
            x1 += 1
        else:
            x2 += 1
    return lst


def mergeSort(draw_info, ascending):
    mergeSortHelper(draw_info, draw_info.lst, ascending, 0)


def merge(draw_info, lst, lst1, lst2, ascending, start):
    x1 = x2 = 0
    frames = pygame.time.Clock()
    for pos in range(len(lst1) + len(lst2)):
        frames.tick(150)
        if x1 == len(lst1) or (x2 < len(lst2) and ((ascending and lst2[x2] < lst1[x1]) or (not ascending and lst2[x2] > lst1[x1]))):
            lst[pos] = lst2[x2]
            x2 += 1
            drawBars(draw_info, pos + start, len(lst1) + start + x2, -1, True)
        else:
            lst[pos] = lst1[x1]
            drawBars(draw_info, pos + start, start + x1, -1, True)
            x1 += 1
    return lst


def mergeSortHelper(draw_info, lst, ascending, start):
    if len(lst) == 1:
        return
    ll = len(lst) // 2
    rl = len(lst) - ll
    llist = []
    rlist = []
    for i in range(ll):
        llist.append(lst[i])
    for i in range(rl):
        rlist.append(lst[i + ll])
    mergeSortHelper(draw_info, llist, ascending, start)
    mergeSortHelper(draw_info, rlist, ascending, start + len(lst) // 2)
    lst = merge(draw_info, lst, llist, rlist, ascending, start)


def drawBars(draw_info, a, b, c=-1, clr=False):
    lst = draw_info.lst

    if clr:
        rect = (draw_info.SIDE_PADDING//2, draw_info.TOP_PADDING, draw_info.width -
                draw_info.SIDE_PADDING, draw_info.height)
        pygame.draw.rect(draw_info.window, draw_info.BLACK, rect)

    for i, val in enumerate(lst):
        x = draw_info.startX + (2 * i) * draw_info.barWidth
        y = draw_info.height - (val - draw_info.minVal +
                                1) * draw_info.blockHeight
        colour = (0, 51, 102)
        if i == a or i == b or i == c:
            colour = draw_info.GREEN

        pygame.draw.rect(draw_info.window, colour,
                         (x, y, draw_info.barWidth, draw_info.height))
    if clr:
        pygame.display.update()


def generateArray(n, minV, maxV):
    lst = []

    for i in range(n):
        k = random.randint(minV, maxV)
        lst.append(k)

    return lst


def main():
    run = True
    frames = pygame.time.Clock()

    n = 50
    minVal = 0
    maxVal = 200

    sorting = False
    ascending = True

    lst = generateArray(n, minVal, maxVal)
    draw_info = info(1000, 800, lst)
    algo = mergeSort

    while run:
        frames.tick(120)
        draw(draw_info)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generateArray(n, minVal, maxVal)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                algo(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                algo = insertionSort
            elif event.key == pygame.K_s and not sorting:
                algo = selectionSort
            elif event.key == pygame.K_q and not sorting:
                algo = quickSort
            elif event.key == pygame.K_b and not sorting:
                algo = bubbleSort
            elif event.key == pygame.K_m and not sorting:
                algo = mergeSort

    pygame.quit()


if __name__ == "__main__":
    main()
