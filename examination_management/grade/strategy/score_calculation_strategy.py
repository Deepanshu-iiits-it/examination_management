import abc


class ScoreCalculationStrategy(abc.ABC):
    @abc.abstractmethod
    def calculate(self, credit, grade):
        raise NotImplemented('Please implement a concrete strategy first')


class DefaultScoreCalculationStrategy(ScoreCalculationStrategy):
    def calculate(self, credit, grade):
        score = 0
        if grade == 'A+':
            score = 10 * credit
        elif grade == 'A':
            score = 9 * credit
        elif grade == 'B+':
            score = 8 * credit
        elif grade == 'B':
            score = 7 * credit
        elif grade == 'C+':
            score = 6 * credit
        elif grade == 'C':
            score = 5 * credit
        elif grade == 'D+':
            score = 4 * credit
        elif grade == 'D':
            score = 3 * credit
        elif grade == 'E+':
            score = 2 * credit
        elif grade == 'E':
            score = 1 * credit
        else:
            score = 0
        return score
