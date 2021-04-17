import npyscreen
from MetaTrader5 import AccountInfo


class AccountInfo(npyscreen.MultiLineEdit):
    def __init__(self, *args, **keywords):
        super(AccountInfo, self).__init__(*args, **keywords)
        self._value = "Carregando..."

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, info):
        if type(info).__name__ == "AccountInfo":
            self._value = (
                f"\n{'Nome':<10}: {info.name}\n"
                f"{'Servidor':<10}: {info.server}\n"
                f"{'Saldo':<10}: {info.balance}\n"
                f"{'Resultado':<10}: {info.profit}\n"
                f"{'Posição':<10}: {info.equity}"
            )
        else:
            self._value = info


class AccountInfoDisplay(npyscreen.BoxTitle):
    """
        A framed widget containing multiline text
    """

    _contained_widget = AccountInfo
