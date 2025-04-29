from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ProgressBar, Label
from textual.containers import Center, Middle, Vertical, Container
from textual.screen import Screen
from textual.reactive import reactive
from asyncio import sleep

from utils import check_connection, check_gemini, check_osm

steps = [
        "Internet connection",
        "OpenStreetMap API",
        "Gemini model",
    ]

class LoadingScreen(Screen):
    TITLE = "MyDirection"

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Container(id="log-area"):
            with Center():
                with Middle():
                    # I know it looks horrible but i tried a lot
                    # and failed a lot, and ran out of patience
                    # to make smth smart, DON'T JUDGE!!!
                    yield Label("Loading...", classes='bold-label')
                    if check_connection():
                        msg = "🟢 " + steps[0]
                    else: 
                        msg = "❌ " + steps[0]
                    yield Label(msg)
                    if check_osm():
                        msg = "🟢 " + steps[1]
                    else: 
                        msg = "❌ " + steps[1]
                    yield Label(msg)
                    gemini = check_gemini()
                    if gemini[0]:
                        msg = f"🟢 {steps[2]}: {gemini[2]}"
                    else: 
                        msg = "❌ " + steps[2]
                    yield Label(msg)
                    # If only you knew how hard it was to get the loading screen running...
                    # problem was that waiting is really tricky,  beacause it blocks some main threads
                    # I swear, async/await is not possible to implement here, at least I couldn't [:ver-sad-face:]

    def on_ready(self):
       
        self.app.pop_screen()        



class MyApp(App):
    CSS = """
    .bold-label {
        text-style: bold;
        padding-bottom: 1;
    }
    """

    TITLE = "MyDirection"
    BINDINGS = [Binding("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen(LoadingScreen())


if __name__ == "__main__":
    app = MyApp()
    app.run()
