from datetime import datetime


class PulseFilter:
    """Decide se um pulso pode ser enviado conforme o dia e o horario."""

    DAYS = (
        "segunda",
        "terca",
        "quarta",
        "quinta",
        "sexta",
        "sabado",
        "domingo",
    )

    def __init__(self, filters=None):
        self.filters = {day: [] for day in self.DAYS}
        self.replace_filters(filters or {})

    def replace_filters(self, filters):
        new_filters = {day: [] for day in self.DAYS}
        for day, intervals in filters.items():
            if day not in self.filters:
                raise ValueError(f"Dia invalido: {day}")
            new_filters[day] = [self._validate_interval(interval) for interval in intervals]
        self.filters = new_filters
        return self.filters

    @staticmethod
    def _validate_interval(interval):
        if len(interval) != 2:
            raise ValueError("Cada intervalo deve ter inicio e fim")

        start, end = interval
        if not all(isinstance(value, int) and 0 <= value <= 1439 for value in (start, end)):
            raise ValueError("Os horarios devem ser minutos inteiros entre 0 e 1439")

        return start, end

    def filter(self, current_time=None):
        """Retorna False quando o pulso deve ser ignorado e True quando pode ser enviado."""
        current_time = current_time or datetime.now()
        day = self.DAYS[current_time.weekday()]
        minute_of_day = current_time.hour * 60 + current_time.minute

        for start, end in self.filters[day]:
            if start <= end and start <= minute_of_day <= end:
                return False
            if start > end and (minute_of_day >= start or minute_of_day <= end):
                return False

        return True
    def add_filter(self, day, start, end):
        """Adiciona um filtro para um dia específico."""
        if day not in self.filters:
            raise ValueError(f"Dia invalido: {day}")
        self.filters[day].append(self._validate_interval((start, end)))


# Mantem compatibilidade com o nome usado anteriormente.
Pulse_filter = PulseFilter