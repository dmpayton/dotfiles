import datetime
from libqtile import bar
from libqtile.widget import base


class Deadline(base._TextBox):
    """
    simple date-based deadline countdown thing.
    """

    def __init__(self, deadline, date, timeout=120, **config):
        base._TextBox.__init__(self, "", bar.CALCULATED, **config)
        self._deadline = deadline
        self._date = date
        self._timeout = timeout

        self.text = self.deadline_text()
        self.timeout_add(self._timeout, self.update)

    def deadline_text(self):
        delta = self._date - datetime.datetime.now()
        return '{0}: {1} days'.format(self._deadline, delta.days)

    def update(self):
        if self.configured:
            newText = self.deadline_text()
            if newText != self.text:
                self.text = newText
                self.bar.draw()
        return True
