import npyscreen
from .form_widgets_positions import FormWidgetsPositions


class SelectStockMainForm(npyscreen.ActionForm):
    DEFAULT_LINES = 12
    DEFAULT_COLUMNS = 60
    SHOW_ATX = 10
    SHOW_ATY = 2

    def create(self):
        super(SelectStockMainForm, self).create()

        self.show_aty = 20
        self.stock = self.add(npyscreen.TitleText, name="Cód. papel:", value=self.parentApp.stock)
        self.stock.display()

    # def afterEditing(self):
    #    self.parentApp.setNextForm("MAIN")

    def on_ok(self):
        self.parentApp.stock = self.stock.value.upper()
        self.parentApp.switchFormPrevious()

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
