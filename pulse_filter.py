from datetime import datetime
import json

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
        if not self.load_from_file():  # Carrega os filtros do arquivo JSON ao inicializar a classe
            self.replace_filters(filters or {})
        

    def load_from_file(self, file_path=".\\ignorar.json"):
        try:
            with open(file_path, "r") as f:
                filters = json.load(f)
                self.replace_filters(filters)
            return True
        except FileNotFoundError:
            print(f"Arquivo {file_path} nao encontrado. Usando filtros padrao.")
            
        except json.JSONDecodeError:
            print(f"Erro ao decodificar o arquivo {file_path}. Usando filtros padrao.")
        finally:
            return False

    def save_file(self, filters, file_path=".\\ignorar.json"):
        try:
            with open(file_path, "w") as f:
                json.dump(filters, f, indent=4)
        except IOError as e:
            print(f"Erro ao salvar o arquivo {file_path}: {e}")


    def replace_filters(self, filters):
        print("Filtros substituidos:", self.filters)
        print("Filtros novos:", filters)

        new_filters = {day: [] for day in self.DAYS}
        for day, intervals in filters.items():
            if day not in self.filters:
                raise ValueError(f"Dia invalido: {day}")
            new_filters[day] = [self._validate_interval(interval) for interval in intervals]
        self.filters = new_filters
        print("Filtros finais:", self.filters)
        self.save_file(self.filters)
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
        self.save_file(self.filters)

# Mantem compatibilidade com o nome usado anteriormente.
Pulse_filter = PulseFilter