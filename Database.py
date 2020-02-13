# !/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os.path

from GameQuestion import GameQuestion
from GameSubject import GameSubject


class Database:
    def __init__(self, path):
        self.__path = path
        self.__content = None
        self.__questions = []
        self.__subjects = []

    @property
    def Content(self):
        return self.__content

    @property
    def Subjects(self):
        return self.__subjects

    @property
    def Questions(self):
        return self.__questions

    def Reset(self):
        self.__content = {'questions': [], 'subjects': []}
        self.__questions = []
        self.__subjects = []
        self.Save()

    def Load(self):
        self.__content = {'questions': [], 'subjects': []}
        if os.path.isfile(self.__path):
            with open(self.__path, "r") as read_file:
                self.__content = json.load(read_file)
        self.__questions = [GameQuestion(q, self) for q in self.__content['questions']]
        self.__subjects = [GameSubject(s, self) for s in self.__content['subjects']]

    def Save(self):
        with open(self.__path, "w") as write_file:
            json.dump(self.__content, write_file, indent=2)

    def AddSubject(self, name: str):
        value = {
            'id': len(self.__content['subjects']),
            'name': name,
            'count': 1,
            'answers': {}
        }
        self.__content['subjects'].append(value)
        self.__subjects.append(GameSubject(value, self))

    def AddQuestion(self, text: str, variants: list):
        value = {
            'id': len(self.__content['questions']),
            'text': text,
            'variants': variants
        }
        self.__content['questions'].append(value)
        self.__questions.append(GameQuestion(value, self))



