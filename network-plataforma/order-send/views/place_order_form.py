import npyscreen
from .form_widgets_positions import FormWidgetsPositions


class PlaceOrderForm(npyscreen.ActionForm):
    DEFAULT_LINES = 12
    DEFAULT_COLUMNS = 60
    SHOW_ATX = 10
    SHOW_ATY = 2

    def create(self):
        super(PlaceOrderForm, self).create()

        self.show_aty = 20
        self.stock_name = self.add(npyscreen.TitleText, name="Cód. papel:", value=self.parentApp.stock)
        self.stock_qty = self.add(npyscreen.TitleText, name="Qtde:", value="100")
        self.stock_price = self.add(npyscreen.TitleText, name="Preço:")

        self.tipo = self.add(
            npyscreen.TitleSelectOne,
            max_height=4,
            value=[0,],
            name="Tipo da ordem",
            values=["Compra", "Venda"],
            scroll_exit=True,
        )
        self.display()

    # def afterEditing(self):
    #    self.parentApp.setNextForm("MAIN")

    def _validate_field_values(self):
        validation_error_template = "O campo <{0}> não foi preenchido"
        validation_error_field = None

        if not self.stock_name.value:
            validation_error_field = self.stock_name.name
        if not self.stock_qty.value:
            validation_error_field = self.stock_qty.name
        if not self.stock_price.value:
            validation_error_field = self.stock_price.name

        if validation_error_field:
            error_message = validation_error_template.format(validation_error_field)

            npyscreen.notify_confirm(error_message, title="Ops!", form_color="STANDOUT", wrap=True, wide=False)

            return False

        return True

    def on_ok(self):
        is_form_valid = self._validate_field_values()
        if not is_form_valid:
            return

        stock_name = self.stock_name.value.upper()
        stock_qty = self.stock_qty.value
        stock_price = self.stock_price.value

        try:
            if self.stock_price.value[0]:
                self.parentApp.broker.buy(stock_name, stock_qty, stock_price)
            else:
                self.parentApp.broker.sell(stock_name, stock_qty, stock_price)

            self.parentApp.switchFormPrevious()
        except Exception as err:
            npyscreen.notify_confirm(str(err), title="Ops!", form_color="STANDOUT", wrap=True, wide=False)

    def on_cancel(self):
        self.parentApp.switchFormPrevious()
