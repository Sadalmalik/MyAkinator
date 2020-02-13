# !/usr/bin/python
# -*- coding: utf-8 -*-

class GameQuestion:
    def __init__(self, question, database):
        self.value = question
        self.db = database
        self.entropy = 0
        # entropy

    @property
    def Id(self):
        return self.value['id']

    @property
    def Text(self):
        return self.value['text']

    @property
    def Variants(self):
        return self.value['variants']

    def CalculateEnthropy(self):
        self.entropy = 0
        for subj in self.db.Subjects:
            group = subj.GetAnswerGroup(self.Id)
            self.entropy += group.GetNormalizedEnthropy()
        # Я решил пока никак не усреднять это значение
        # Ибо не ясно что будет