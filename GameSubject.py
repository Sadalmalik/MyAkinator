# !/usr/bin/python
# -*- coding: utf-8 -*-

from AnswerGroup import AnswerGroup


class GameSubject:
    def __init__(self, subject, database):
        self.value = subject
        self.db = database
        self.prob = subject['count']

    @property
    def Id(self):
        return self.value['id']

    @property
    def Name(self):
        return self.value['name']

    @property
    def Count(self):
        return self.value['count']

    def IncrementCount(self):
        self.value['count'] += 1

    def GetAnswerGroup(self, question):
        ans = self.value['answers']
        key = str(question.Id)
        if key not in ans:
            ans[key] = [1] * len(question.Variants)
        return AnswerGroup(ans[key])
