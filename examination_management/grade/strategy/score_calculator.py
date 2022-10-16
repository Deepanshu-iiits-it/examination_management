
class ScoreCalculator:
    def __init__(self, calculation_strategy):
        self._calculation_strategy = calculation_strategy

    @property
    def calculation_strategy(self):
        return self._calculation_strategy

    @calculation_strategy.setter
    def calculation_strategy(self, calculation_strategy):
        self._calculation_strategy = calculation_strategy

    def calculate(self, credit, grade):
        return self._calculation_strategy.calculate(credit, grade)
