#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Необходимо создать программу с реализацией алгоритма заливки.
Задача заключается в том, чтобы, зная узел заливки и цвета замены,
закрасить на указанный цвет все узлы, соседствующие с узлом
заливки и имеющие такой же цвет.
"""

import math
from abc import ABC, abstractmethod


class Problem(ABC):
    """
    Абстрактный класс для формальной постановки задачи.
    Новый домен (конкретная задача) должен специализировать этот класс,
    переопределяя методы actions и result, а при необходимости
    action_cost, h и is_goal.
    """

    def __init__(self, initial=None, goal=None, **kwargs):
        self.initial = initial
        self.goal = goal
        for k, v in kwargs.items():
            setattr(self, k, v)

    @abstractmethod
    def actions(self, state):
        """
        Вернуть доступные действия (операторы) из данного состояния.
        """
        pass

    @abstractmethod
    def result(self, state, action):
        """
        Вернуть результат применения действия к состоянию.
        """
        pass

    def is_goal(self, state):
        """
        Проверка на достижение цели.
        """
        return False

    def action_cost(self, s, a, s1):
        """
        Стоимость перехода; для заливки несущественно, оставим 1.
        """
        return 1

    def h(self, node):
        """
        Эвристическая функция, по умолчанию 0.
        """
        return 0


class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0.0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

    def __repr__(self):
        return f"<Node {self.state}>"

    def __lt__(self, other):
        return self.path_cost < other.path_cost


# Специальные «сигнальные» узлы
failure = Node("failure", path_cost=math.inf)
cutoff = Node("cutoff", path_cost=math.inf)


def expand(problem, node):
    """
    Генерация дочерних узлов, применяя actions к node.state.
    """

    s = node.state
    for action in problem.actions(s):
        s_next = problem.result(s, action)
        yield Node(state=s_next, parent=node, action=action)


class FloodFillProblem(Problem):
    """
    Задача алгоритма заливки:
    matrix: двумерный список (rows x cols),
    start: начальная координата (row, col),
    target_color: цвет, который нужно заменить,
    replacement_color: цвет, на который заменяем.
    """

    def __init__(self, matrix, start, target_color, replacement_color):
        super().__init__(initial=start)
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0

        self.target_color = target_color
        self.replacement_color = replacement_color

    def actions(self, state):
        """
        Выдаём список соседей по 4-м направлениям (вверх, вниз, влево, вправо),
        которые ещё имеют цвет target_color.
        """

        (r, c) = state
        neighbors = []
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.matrix[nr][nc] == self.target_color:
                    neighbors.append((nr, nc))
        return neighbors

    def result(self, state, action):
        (nr, nc) = action
        self.matrix[nr][nc] = self.replacement_color
        return action

    def is_goal(self, state):
        """
        В задаче заливки нет одной цели.
        """
        return False


def flood_fill_dfs(problem):
    """
    Алгоритм заливки по принципу поиска в глубину.
    Начинаем с problem.initial, затем красим начальную клетку
    (если она имеет target_color), затем рекурсивно обходим соседей.
    """

    start_state = problem.initial
    r, c = start_state

    # Если клетка уже залита
    if problem.matrix[r][c] != problem.target_color:
        return

    # Красим начальную клетку
    problem.matrix[r][c] = problem.replacement_color

    # Реализация поиска в глубину
    stack = [(r, c)]
    while stack:
        (cr, cc) = stack.pop()

        for nr, nc in problem.actions((cr, cc)):
            problem.result((cr, cc), (nr, nc))
            stack.append((nr, nc))


def main():
    """
    Главная функция программы.
    """

    # Матрица для заливки
    matrix = [
        ["Y", "Y", "Y", "G", "G", "G", "G", "G", "G", "G"],
        ["Y", "Y", "Y", "Y", "Y", "Y", "G", "X", "X", "X"],
        ["G", "G", "G", "G", "G", "G", "G", "X", "X", "X"],
        ["W", "W", "W", "W", "W", "G", "G", "G", "G", "X"],
        ["W", "R", "R", "R", "R", "R", "G", "X", "X", "X"],
        ["W", "W", "W", "R", "R", "G", "G", "X", "X", "X"],
        ["W", "B", "W", "R", "R", "R", "R", "R", "R", "X"],
        ["W", "B", "B", "B", "B", "R", "R", "X", "X", "X"],
        ["W", "B", "B", "X", "B", "B", "B", "B", "X", "X"],
        ["W", "B", "B", "X", "X", "X", "X", "X", "X", "X"],
    ]
    print("Изначальная матрица: ")
    for row in matrix:
        print(row)

    start_node = (3, 9)
    print("Узел заливки: ", start_node)

    target_color = "X"
    print("Цвет, который нужно поменять: ", target_color)

    replacement_color = "C"
    print("Цвет, на который нужно поменять: ", replacement_color)

    problem = FloodFillProblem(matrix, start_node, target_color, replacement_color)

    flood_fill_dfs(problem)

    # Выводим результат после заливки
    print("Закрашенная матрица: ")
    for row in matrix:
        print(row)


if __name__ == "__main__":
    main()
