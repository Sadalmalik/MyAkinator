# !/usr/bin/python
# -*- coding: utf-8 -*-

class GameAnswer:
    def __init__(self, qid, answer):
        self.__qid = qid
        self.__answer = answer

    @property
    def QuestionID(self):
        return self.__qid

    @property
    def AnswerID(self):
        return self.__answer