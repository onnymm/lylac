from datetime import timedelta

class Duration(timedelta):
    _HOURS = 3600
    _MINUTES = 60

    def __repr__(
        self,
    ) -> str:

        total_seconds = int(round(self.total_seconds(), 0))

        hours = total_seconds // self._HOURS
        total_seconds -= self._HOURS * hours

        minutes = total_seconds // self._MINUTES
        total_seconds -= self._MINUTES * minutes

        display_value = f'{hours:02d}:{minutes:02d}:{total_seconds:02d}'

        return display_value

    def __str__(
        self,
    ) -> str:

        return self.__repr__()
