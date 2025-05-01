from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Label, Button, Input, Select
from textual.containers import Center, Middle, Vertical, Horizontal
from textual.screen import Screen
from textual.reactive import reactive
from asyncio import sleep

from utils import check_addr
from main_screen import MainScreen

TRANSPORT = ["car", "bike", "foot", "driving", "bicycling", "walking"]

class InputScreen(Screen):
    TITLE = "MyDirection"
    # BINDINGS = [Binding("q", "quit", "Quit")]

    def __init__(self, gemini_model):
        super().__init__()
        self.gemini = gemini_model
        self.transport = ''
        self.originAddr = ''
        self.destAddr = ''

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Center():
            with Middle():
                with Center():
                    yield Select.from_values(TRANSPORT)
                    yield Input(id='origin-input', placeholder="Enter origin")
                    yield Label('', id='origin-label', classes='margined-label')
                    yield Input(id='dest-input', placeholder="Enter destination")
                    yield Label('', id='dest-label', classes='margined-label')
                with Center():
                    yield Button('Check', classes='minimal-btn', id='check-addr')

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.transport = str(event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "check-addr":
            if self.transport == '':
                return None
            
            originAddr = self.query_one('#origin-input', Input).value
            destAddr = self.query_one('#dest-input', Input).value

            originAddr = check_addr(originAddr)
            destAddr = check_addr(destAddr)
            
            if originAddr[0] and destAddr[0]:
                self.originAddr = originAddr[1]
                self.destAddr = destAddr[1]
                self.app.push_screen(MainScreen(args={
                    'gemini': self.gemini,
                    'transport': self.transport,
                    'origin-addr': self.originAddr,
                    'dest-addr': self.destAddr
                    }))
            else:
                if not originAddr[0]:
                    self.query_one('#origin-label', Label).update("Address not found")
                if not destAddr[0]:
                    self.query_one('#dest-label', Label).update("Address not found")
                
# The section below is 
# used for the ease of Dev/Debug pruposes only
class MyApp(App):
    
    TITLE = "MyDirection"
    
    CSS_PATH = 'static/app.tcss'

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen(InputScreen(''))


if __name__ == "__main__":
    app = MyApp()
    app.run()
