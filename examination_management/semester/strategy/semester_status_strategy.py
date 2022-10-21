import abc


class SemesterStatusStrategy(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, grades):
        raise NotImplemented('Please implement a concrete strategy first')


class DefaultSemesterStatusStrategy(SemesterStatusStrategy):
    def evaluate(self, grades):
        for grade in grades:
            if grade >= 'F':
                return 'R'
        return 'P'
