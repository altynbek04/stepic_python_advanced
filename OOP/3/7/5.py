class TimeZone:
    def __init__(self, name, offset_hours, offset_minutes):
        self.name = name
        self.offset_hours = offset_hours
        self.offset_minutes = offset_minutes

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        original = value

        if not isinstance(value, str):
            raise ValueError(f"Timezone bad name - {original}")

        stripped = value.strip()
        if stripped == "":
            raise ValueError(f"Timezone bad name - {original}")

        self._name = stripped

    @property
    def offset_hours(self):
        return self._offset_hours

    @offset_hours.setter
    def offset_hours(self, value):
        if not isinstance(value, int):
            raise ValueError("Hour offset must be an integer.")

        if value < -12 or value > 14:
            raise ValueError("Offset must be between -12:00 and +14:00.")

        self._offset_hours = value

    @property
    def offset_minutes(self):
        return self._offset_minutes

    @offset_minutes.setter
    def offset_minutes(self, value):
        if not isinstance(value, int):
            raise ValueError("Minutes offset must be an integer.")

        if value < -59 or value > 59:
            raise ValueError("Minutes offset must between -59 and 59.")

        self._offset_minutes = value
