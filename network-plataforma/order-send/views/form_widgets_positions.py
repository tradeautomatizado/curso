from collections import namedtuple


class FormWidgetsPositions:
    def __init__(self, max_x, max_y) -> None:
        #####      Defaults            #######
        self.Y_SCALING_FACTOR = float(max_y) / 28
        self.X_SCALING_FACTOR = float(max_x) / 104

        self.LEFT_OFFSET = 1
        self.TOP_OFFSET = 1

    @property
    def account(self):
        ######    Account info widget  #########
        account = namedtuple(
            "account",
            ["REL_X", "REL_Y", "HEIGHT", "WIDTH",],
            defaults=(
                self.LEFT_OFFSET,
                self.TOP_OFFSET + 1,
                int(6 * self.Y_SCALING_FACTOR),
                int(100 * self.X_SCALING_FACTOR),
            ),
        )

        return account()

    @property
    def stock_graph(self):
        ######    Stock Graph widget  #########
        account = self.account
        sg = namedtuple(
            "stock_graph",
            ["REL_X", "REL_Y", "HEIGHT", "WIDTH",],
            defaults=(
                self.LEFT_OFFSET,
                account.REL_Y + account.HEIGHT,
                int(10 * self.Y_SCALING_FACTOR),
                int(50 * self.X_SCALING_FACTOR),
            ),
        )

        return sg()

    @property
    def ordens(self):
        ######    Ordens widget  #########
        sg = self.stock_graph

        p = namedtuple(
            "ordens",
            ["REL_X", "REL_Y", "HEIGHT", "WIDTH",],
            defaults=(sg.REL_X + sg.WIDTH, sg.REL_Y, sg.HEIGHT, sg.WIDTH),
        )

        return p()

    @property
    def posicoes(self):
        ######    Posicoes widget  #########
        ods = self.ordens
        ai = self.account

        p = namedtuple(
            "posicoes",
            ["REL_X", "REL_Y", "HEIGHT", "WIDTH",],
            defaults=(self.LEFT_OFFSET, ods.REL_Y + ods.HEIGHT, int(8 * self.Y_SCALING_FACTOR), ai.WIDTH),
        )

        return p()
