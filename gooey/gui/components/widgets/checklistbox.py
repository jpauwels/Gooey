import wx

from gooey.gui.components.widgets.listbox import Listbox


class CheckListbox(Listbox):

    def getWidget(self, parent, *args, **options):
        height = self._options.get('height', 60)
        return wx.CheckListBox(
            parent=parent,
            choices=self._meta['choices'],
            size=(-1, height),
            style=wx.LB_MULTIPLE
        )

    def setValue(self, values):
        self.widget.SetCheckedStrings(values)

    def getWidgetValue(self):
        return self.widget.GetCheckedStrings()
