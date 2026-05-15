from rich.console import Console
from random import random
from calendar import Calendar
from rich.text import Text
from graphical.group import Horizontal, Vertical
from graphical.heat import Heat
from graphical.scale.chromatic.sequential import GREENS


def week_calendar(year: int, pivot: bool = True):
    result = []
    for month_row in Calendar(firstweekday=6).yeardatescalendar(year, width=1):
        for week in month_row[0]:
            if week not in result:
                result.append([d if d.year == year else None for d in week])
    return list(zip(*result)) if pivot else result


weekday_labels = [None, "Mon ", None, "Wed ", None, "Fri ", None]
weekday_graphs = Vertical()
for weekday, weeks in enumerate(week_calendar(2026)):
    line = Horizontal()
    line.append(Text(weekday_labels[weekday] or " " * 4))
    for day in weeks:
        if day is None:
            line.append(Text("  "))
        else:
            line.append(
                Heat(
                    data=random(),
                    value_range=(0, 1),
                    scheme=GREENS,
                    repeat_x=2,
                )
            )
    weekday_graphs.append(line)
console = Console()
console.print(weekday_graphs)
