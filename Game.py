# !/usr/bin/python
# -*- coding: utf-8 -*-

from Database import *
from GameQuestion import GameQuestion
from GameSubject import GameSubject


class Game:
    def __init__(self, database: Database):
        self.__db = database
        self.__questions = None
        self.__subjects = None
        self.__answers = None

    def __SortByEntropy(self, q: GameQuestion):
        return q.entropy

    def __SortByProb(self, s: GameSubject):
        return s.prob

    def StartLoop(self):
        self.__questions = self.__db.Questions.copy()
        self.__subjects = self.__db.Subjects.copy()
        self.__answers = []
        guessed = False
        subj = None
        while len(self.__questions) > 0:
            print()
            print('Database: {}'.format(json.dumps(self.__db.Content)))
            print()
            self.CalculateSubjectsProbabilityes()
            self.CalculateQuestionsEnthropy()
            self.PrintStats()
            print('{} questions to go'.format(len(self.__questions)))
            question = self.__questions.pop(0)
            answer = self.AskQuestion(question)
            self.__answers.append(answer)
            guessed, subj = self.TryAskGuess()
            if guessed:
                print('Hooray! We found it!')
                break
        if not guessed:
            print('Enter correct subject!')
            sub = input(':> ')
            for subject in self.__db.Subjects:
                if subject.Name == sub:
                    subj = subject
                    break
        if subj:
            self.ApplyResultsForSubject(subj)
            print()
            print('Database: {}'.format(json.dumps(self.__db.Content)))
            print()
            print('Probabilities modified!')
        else:
            print('Unknown subject {}!'.format(sub))

    def PrintStats(self):
        print('Questions:')
        for question in self.__questions:
            print('{: >4} : {: <6} : {: <20}'.format(question.Id, question.entropy, question.Text))
        print('Subjects:')
        for subject in self.__subjects:
            print('{: >4} : {: <6} : {: <20}'.format(subject.Id, subject.prob, subject.Name))
        print('Answers:')
        for answer in self.__answers:
            print('{: >4} : {: <6}'.format(answer['qid'], answer['aid']))


    def AskQuestion(self, question: GameQuestion):
        print('[{}] {}'.format(question.Id, question.Text))
        size = len(question.Variants)
        print(''.join(['{: >4}: {: <20}'.format(i+1, question.Variants[i]) for i in range(size)]))
        limit = len(question.Variants)
        answer = int(input(':> ')) - 1
        while answer >= limit or answer < 0:
            print('Answer must be between 0 and {}!!!'.format(limit))
            answer = int(input(':> ')) - 1
        return {'qid': question.Id, 'aid': answer, 'question': question}

    def TryAskGuess(self):
        sub = self.__subjects[0]
        if sub.prob > .8:
            print('Is it \'{}\'? Y/N'.format(sub.Name))
            answer = input(':> ')
            return answer == 'Y', sub
        return False, None

    def ApplyResultsForSubject(self, subject):
        subject.IncrementCount()
        for answer in self.__answers:
            aid = answer['aid']
            group = subject.GetAnswerGroup(answer['question'])
            group.ApplyAnswer(aid)
        self.__db.Save()

    def CalculateSubjectsSumm(self):
        sum = 0
        for subject in self.__subjects:
            sum += subject.Count
        return sum

    def CalculateSubjectsProbabilityes(self):
        subj_sum = self.CalculateSubjectsSumm()
        for subject in self.__subjects:
            prob = 0
            for answer in self.__answers:
                aid = answer['aid']
                group = subject.GetAnswerGroup(answer['question'])
                prob += group.GetProbability(aid)
            prob += subject.Count / subj_sum
            prob /= len(self.__answers) + 1
            subject.prob = prob
        self.__subjects.sort(key=self.__SortByProb, reverse=True)

    def CalculateQuestionsEnthropy(self):
        amount = int(len(self.__subjects) / 2)
        for question in self.__questions:
            question.entropy = 0
            for subject in self.__subjects[0:amount]:
                group = subject.GetAnswerGroup(question)
                question.entropy += group.GetNormalizedEnthropy()
        self.__questions.sort(key=self.__SortByEntropy)
