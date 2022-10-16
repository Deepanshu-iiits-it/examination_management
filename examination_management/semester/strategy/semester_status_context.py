class SemesterStatusContext:
    def __init__(self, semester_status_strategy):
        self._semester_status_strategy = semester_status_strategy

    @property
    def semester_status_strategy(self):
        return self._semester_status_strategy

    @semester_status_strategy.setter
    def semester_status_strategy(self, semester_status_strategy):
        self._semester_status_strategy = semester_status_strategy

    def evaluate(self, cg_sum, total_credit):
        return self._semester_status_strategy.evaluate(cg_sum, total_credit)
