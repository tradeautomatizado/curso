#!/usr/bin/env python
# encoding: utf-8
import logging
import sys
import npyscreen


class MultiLineWidget(npyscreen.BoxTitle):
    """
    A framed widget containing multiline text
    """

    _contained_widget = npyscreen.MultiLineEdit


class WindowForm(npyscreen.FormBaseNew):
    """
    Frameless Form
    """

    def create(self, *args, **kwargs):
        super(WindowForm, self).create(*args, **kwargs)

    def while_waiting(self):
        pass


class TradeAppGUI(npyscreen.NPSApp):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def draw(self):
        self.window = WindowForm(parentApp=self, name="Trade App [http://www.tradeautomatizado.com.br")

        MIN_ALLOWED_TERMINAL_WIDTH = 104
        MIN_ALLOWED_TERMINAL_HEIGHT = 28

        # global PREVIOUS_TERMINAL_HEIGHT, PREVIOUS_TERMINAL_WIDTH
        max_y, max_x = self.window.curses_pad.getmaxyx()
        PREVIOUS_TERMINAL_HEIGHT = max_y
        PREVIOUS_TERMINAL_WIDTH = max_x

        # Also make ptop exists cleanly if screen is drawn beyond the lower limit
        # if max_x < MIN_ALLOWED_TERMINAL_WIDTH or max_y < MIN_ALLOWED_TERMINAL_HEIGHT:
        #    self._logger.info("Terminal sizes than width = 104 and height = 28, exiting")
        #    sys.stdout.write(
        #        "Ptop does not support terminals with resolution smaller than 104*28. Please resize your terminal and try again."
        #    )
        #    raise KeyboardInterrupt

        self.Y_SCALING_FACTOR = float(max_y) / 28
        self.X_SCALING_FACTOR = float(max_x) / 104

        #####      Defaults            #######
        LEFT_OFFSET = 1
        TOP_OFFSET = 1

        #####      Overview widget     #######
        OVERVIEW_WIDGET_REL_X = LEFT_OFFSET
        OVERVIEW_WIDGET_REL_Y = TOP_OFFSET

        OVERVIEW_WIDGET_HEIGHT = int(6 * self.Y_SCALING_FACTOR)
        OVERVIEW_WIDGET_WIDTH = int(100 * self.X_SCALING_FACTOR)

        self.basic_stats = self.window.add(
            MultiLineWidget,
            name="Overview",
            relx=OVERVIEW_WIDGET_REL_X,
            rely=OVERVIEW_WIDGET_REL_Y,
            max_height=OVERVIEW_WIDGET_HEIGHT,
            max_width=OVERVIEW_WIDGET_WIDTH,
        )
        self.basic_stats.value = ""
        self.basic_stats.entry_widget.editable = False

        ######    Memory Usage widget  #########
        MEMORY_USAGE_WIDGET_REL_X = LEFT_OFFSET
        MEMORY_USAGE_WIDGET_REL_Y = OVERVIEW_WIDGET_REL_Y + OVERVIEW_WIDGET_HEIGHT
        MEMORY_USAGE_WIDGET_HEIGHT = int(10 * self.Y_SCALING_FACTOR)
        MEMORY_USAGE_WIDGET_WIDTH = int(50 * self.X_SCALING_FACTOR)

        ######    CPU Usage widget  #########
        CPU_USAGE_WIDGET_REL_X = MEMORY_USAGE_WIDGET_REL_X + MEMORY_USAGE_WIDGET_WIDTH
        CPU_USAGE_WIDGET_REL_Y = MEMORY_USAGE_WIDGET_REL_Y
        CPU_USAGE_WIDGET_HEIGHT = MEMORY_USAGE_WIDGET_HEIGHT
        CPU_USAGE_WIDGET_WIDTH = MEMORY_USAGE_WIDGET_WIDTH

        ######    Processes Info widget  #########
        PROCESSES_INFO_WIDGET_REL_X = LEFT_OFFSET
        PROCESSES_INFO_WIDGET_REL_Y = CPU_USAGE_WIDGET_REL_Y + CPU_USAGE_WIDGET_HEIGHT
        PROCESSES_INFO_WIDGET_HEIGHT = int(8 * self.Y_SCALING_FACTOR)
        PROCESSES_INFO_WIDGET_WIDTH = OVERVIEW_WIDGET_WIDTH

        ACTIONS_WIDGET_REL_X = LEFT_OFFSET
        ACTIONS_WIDGET_REL_Y = PROCESSES_INFO_WIDGET_REL_Y + PROCESSES_INFO_WIDGET_HEIGHT
        self.actions = self.window.add(npyscreen.FixedText, relx=ACTIONS_WIDGET_REL_X, rely=ACTIONS_WIDGET_REL_Y)
        self.actions.value = (
            "^K:Kill\t\t^N:Memory Sort\t\t^T:Time Sort\t\t^R:Reset\t\tg:Top\t\t^Q:Quit\t\t^F:Filter\t\t^L:Process Info"
        )
        self.actions.display()
        self.actions.editable = False

        self.window.edit()

    def while_waiting(self):
        self.update()

    def update(self):
        """
        Update the form in background, this used to be called inside the ThreadJob
        and but now is getting called automatically in while_waiting
        """
        try:
            #### Overview information ####

            row1 = "Disk Usage (/) {4}{0: <6}/{1: >6} MB{4}{2: >2} %{5}Processes{4}{3: <8}"

            row2 = "Swap Memory    {4}{0: <6}/{1: >6} MB{4}{2: >2} %{5}Threads  {4}{3: <8}"

            row3 = "Main Memory    {4}{0: <6}/{1: >6} MB{4}{2: >2} %{5}Boot Time{4}{3: <8} hours"

            row4 = "Network Speed  {2}{0: <3}↓ {1: <3}↑ MB/s"

            self.basic_stats.value = row1 + "\n" + row2 + "\n" + row3 + "\n" + row4
            # Lazy update to GUI
            self.basic_stats.update(clear=True)

            self.window.DISPLAY()
        # catch the fucking KeyError caused to c
        # cumbersome point of reading the stats data structures
        except KeyError:
            self._logger.info("Some of the stats reading failed", exc_info=True)

    def main(self):
        self.draw()


if __name__ == "__main__":

    # app wide global stop flag
    # global_stop_event = threading.Event()

    App = TradeAppGUI()
    App.run()