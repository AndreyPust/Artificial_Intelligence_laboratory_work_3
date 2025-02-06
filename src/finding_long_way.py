#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дана матрица символов размером M×N. Необходимо найти длину самого
длинного пути в матрице, начиная с заданного символа. Каждый следующий
символ в пути должен алфавитно следовать за предыдущим без пропусков.
Поиск возможен во всех восьми направлениях.
"""

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


class LongestConsecutivePathProblem(Problem):
    """
    Задача поиска самого длинного пути в матрице.
    """

    def __init__(self, matrix, start_char):
        """
        :param matrix: двумерный массив символов (список списков).
        :param start_char: символ, с которого начинается путь.
        """

        super().__init__(initial=start_char)
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0]) if self.rows > 0 else 0
        self.start_char = start_char

    def actions(self, state):
        """
        Возвращает список соседей (nr, nc) по 8 направлениям,
        у которых символ == chr(ord(matrix[r][c]) + 1).
        """

        (r, c) = state
        curr_char = self.matrix[r][c]
        next_char = chr(ord(curr_char) + 1)

        neighbors = []

        # Направления
        deltas = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                if self.matrix[nr][nc] == next_char:
                    neighbors.append((nr, nc))
        return neighbors

    def result(self, state, action):
        """
        Просто переходим в соседнюю ячейку (action).
        """
        return action


def dfs_longest(problem, r, c):
    """
    Поиск всех соседей, у которых символ = current_char + 1 по алфавиту
    Для каждого соседа вызывается dfs_longest, и берется максимум
    Возвращается 1 + max(...) или 1, если нет соседей
    """

    children = problem.actions((r, c))
    best_len = 1  # хотя бы текущая клетка
    for nr, nc in children:
        length_child = 1 + dfs_longest(problem, nr, nc)
        if length_child > best_len:
            best_len = length_child
    return best_len


def find_longest_consecutive_path(problem):
    """
    Ищет максимальную длину цепочки, начинающейся с problem.start_char.
    Перебирает все ячейки, где стоит start_char,
    и берёт максимум результата поиска.
    """

    matrix = problem.matrix
    rows, cols = problem.rows, problem.cols
    start_char = problem.start_char

    longest_path = 0
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == start_char:
                length = dfs_longest(problem, r, c)
                if length > longest_path:
                    longest_path = length
    return longest_path


def main():
    """
    Главная функция программы.
    """

    matrix = [
        ["K", "L", "M", "N", "O", "P", "Q"],
        ["J", "A", "B", "C", "D", "E", "R"],
        ["I", "Z", "Y", "X", "W", "F", "S"],
        ["H", "G", "T", "U", "V", "G", "T"],
        ["G", "F", "E", "D", "C", "B", "U"],
        ["F", "E", "D", "C", "B", "A", "V"],
        ["E", "D", "C", "B", "A", "Z", "W"],
    ]
    print("Исходная матрица: ")
    for row in matrix:
        print(row)

    start_char = "C"
    problem = LongestConsecutivePathProblem(matrix, start_char)
    answer = find_longest_consecutive_path(problem)
    print(f"Длина самого длинного пути, начиная с символа '{start_char}': {answer}")


if __name__ == "__main__":
    main()
