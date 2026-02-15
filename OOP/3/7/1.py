class Celsius:
    def __init__(self, temperature):
        self.temperature = temperature
    def to_fahrenheit(self):
        return (self.temperature * 9 / 5) + 32
    @property
    def temperature(self):
        return self._temperature
    @temperature.setter
    def temperature(self, value):
        if value < -273.15:
            raise ValueError
        self._temperature = value
