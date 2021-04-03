import npyscreen

# This application class serves as a wrapper for the initialization of curses
# and also manages the actual forms of the application


class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())


# This form class defines the display that will be presented to the user.


class MainForm(npyscreen.Form):
    def create(self):
        t = self.add(npyscreen.BoxTitle, name="Text:", value="Hellow World!")
        t.display()
        t.editable = False

    def afterEditing(self):
        self.parentApp.setNextForm(None)


if __name__ == "__main__":
    TA = MyTestApp()
    try:
        TA.run()
    except (KeyboardInterrupt):
        print("Application Closed")
