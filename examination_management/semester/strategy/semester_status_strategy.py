import abc


class SemesterStatusStrategy(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, cg_sum, total_credit):
        raise NotImplemented('Please implement a concrete strategy first')


class DefaultSemesterStatusStrategy(SemesterStatusStrategy):
    def evaluate(self, cg_sum, total_credit):
        # TODO: Add logic to find status using cg_sum and total_credit
        return 'A'
