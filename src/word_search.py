#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Дана матрица символов размером M×N. Задача – найти и вывести список
всех возможных слов, которые могут быть сформированы из последовательности
соседних символов в этой матрице. При этом слово может формироваться
во всех восьми возможных направлениях (север, юг, восток, запад,
северо-восток, северо-запад, юго-восток, юго-запад), и каждая клетка
может быть использована в слове только один раз.
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


class WordSearchProblem(Problem):
    """
    Описывает задачу поиска всех слов из dictionary
    в матрице board (список списков символов).
    """

    def __init__(self, board, dictionary):
        super().__init__(board=board, dictionary=dictionary)
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0

    def actions(self, state):
        return []

    def result(self, state, action):
        return state


def can_form_word_dfs(board, word):
    """
    Функция проверяющая можно ли составить слово в матрице в 8-ми направлениях.
    Возвращает True, если слово word можно найти в матрице символов,
    двигаясь во все 8 направлений, используя каждую клетку не более одного раза.
    """

    rows = len(board)
    cols = len(board[0]) if rows > 0 else 0

    # Смещения по 8 направлениям
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

    def dfs(r, c, index, visited):
        """
        Поиск слова начиная с клетки (r,c).
        """
        if index == len(word):
            return True  # все буквы совпали

        if not (0 <= r < rows and 0 <= c < cols):
            return False
        if board[r][c] != word[index]:
            return False
        if (r, c) in visited:
            return False

        # Помечаем текущую клетку как использованную
        visited.add((r, c))

        # Переходим к следующей букве
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            if dfs(nr, nc, index + 1, visited):
                return True

        # Если не получилось найти дальше, снимаем отметку и идём другим путём
        visited.remove((r, c))
        return False

    # Ищем все вхождения первой буквы во всей матрице
    first_char = word[0]
    for r in range(rows):
        for c in range(cols):
            if board[r][c] == first_char:
                # Пробуем начать DFS с (r,c)
                if dfs(r, c, 0, set()):
                    return True

    return False


def find_all_words(problem):
    """
    Возвращает множество слов, которые можно сформировать
    в матрице символов из словаря слов.
    """
    result = set()
    for w in problem.dictionary:
        if can_form_word_dfs(problem.board, w):
            result.add(w)
    return result


def main():
    """
    Главаная функция программы.
    """

    board = [["М", "И", "Р", "У", "П"], ["А", "П", "А", "П", "А"], ["О", "Р", "А", "Г", "Д"], ["Л", "Е", "Т", "О", "М"]]
    print("Исходная матрица символов: ")
    for row in board:
        print(row)

    dictionary = [
        "МИР",
        "ЛЕТО",
        "УРАЛ",
        "ПАРОГ",
        "МАРТ",
        "ПИР",
    ]
    print("Доступный словарь слов: ", dictionary)

    problem = WordSearchProblem(board, dictionary)

    found_words = find_all_words(problem)

    print("Найденные слова:", found_words)


if __name__ == "__main__":
    main()
