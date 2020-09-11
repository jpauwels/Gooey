from contextlib import contextmanager

from gooey.gui.components.widgets.bases import TextContainer
import wx

from gooey.gui import formatters
from gooey.gui.lang.i18n import _


class Dropdown(TextContainer):

    def getWidget(self, parent, *args, **options):
        choices = [str(choice) for choice in self._meta['choices']]
        if self._meta['default'] is None:
            default = _('select_option')
            choices = [str(default)] + choices
        else:
            default = self._meta['default']
        return wx.Choice(
            parent=parent,
            id=-1,
            # str conversion allows using stringyfiable values in addition to pure strings
            choices=choices)

    def setOptions(self, options):
        with self.retainSelection():
            self.widget.Clear()
            select_option = [_('select_option')] if self._meta['default'] is None else []
            self.widget.SetItems(select_option + options)

    def setValue(self, value):
        ## +1 to offset the default placeholder value
        index = self._meta['choices'].index(value) + 1 if self._meta['default'] is None else 0
        self.widget.SetSelection(index)

    def getWidgetValue(self):
        value = self.widget.GetValue()
        # filter out the extra default option that's
        # appended during creation
        if value == _('select_option'):
            return None
        return value

    def formatOutput(self, metadata, value):
        return formatters.dropdown(metadata, value)

    @contextmanager
    def retainSelection(self):
        """"
        Retains the selected dropdown option (when possible)
        across mutations due to dynamic updates.
        """
        prevSelection = self.widget.GetSelection()
        prevValue = self.widget.GetValue()
        try:
            yield
        finally:
            current_at_index = self.widget.GetString(prevSelection)
            if prevValue == current_at_index:
                self.widget.SetSelection(prevSelection)
            else:
                self.widget.SetSelection(0)
