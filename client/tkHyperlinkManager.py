from tkinter import Text, CURRENT
# Source: https://web.archive.org/web/20200806215420/http://effbot.org/zone/tkinter-text-hyperlink.htm
# and https://stackoverflow.com/questions/49353034/python-tkinter-have-displayed-text-as-hyperlink 

class HyperlinkManager:

    def __init__(self, text:str) -> None:

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self) -> None:
        self.links = {}

    def add(self, action) -> tuple[str, str]:
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event) -> None:
        self.text.config(cursor="hand2")

    def _leave(self, event) -> None:
        self.text.config(cursor="")

    def _click(self, event) -> None:
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return