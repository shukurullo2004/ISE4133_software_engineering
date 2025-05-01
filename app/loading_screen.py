from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, Label, Button
from textual.containers import Center, Middle, Container
from textual.screen import Screen


from utils import check_connection, check_gemini, check_osm
from input_screen import InputScreen
steps = [
        "Internet connection",
        "OpenStreetMap APIs",
        "Gemini model",
    ]

class LoadingScreen(Screen):
    TITLE = "MyDirection"

    def __init__(self):
        super().__init__()
        self.gemini = ''

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        with Container(id="log-area"):
            with Center():
                with Middle():
                # I know it looks horrible but i tried a lot
                # and failed a lot, and ran out of patience
                # to make smth smart, DON'T JUDGE!!!
                    yield Label("Status:", classes='bold-label')
                    if not check_connection():
                        msg = "❌ " + steps[0] 
                        yield Label(msg)
                    else: 
                        msg = "🟢 " + steps[0]
                        yield Label(msg)

                        if not check_osm():
                            msg = "❌ " + steps[1]
                            yield Label(msg)
                        else: 
                            msg = "🟢 " + steps[1]
                            yield Label(msg)

                            gemini = check_gemini()
                            if not gemini[0]:
                                msg = "❌ " + steps[2]
                                yield Label(msg)
                                yield Button("Continue\n (without AI)", id="continue-btn", classes="minimal-button")
                                yield Button("Quit", id="quit-btn", classes="minimal-button", variant="error")
                            else: 
                                msg = f"🟢 {steps[2]}: {gemini[1]}"
                                self.gemini = gemini[1]
                                yield Label(msg)

                                # All good: Show continue button
                                yield Button("Continue", id="continue-btn", classes="minimal-button")

                # If only you knew how hard it was to get the loading screen running...
                # problem was that waiting is really tricky,  beacause it blocks some main threads
                # I swear, async/await is not possible to implement here, at least I couldn't [:verry-sad-face:]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue-btn":
            self.app.pop_screen()
            self.app.push_screen(InputScreen(self.gemini))
        if event.button.id == "quit-btn":
            self.app.exit() 

# The section below is 
# used for the ease of Dev/Debug pruposes only
class MyApp(App):
   
    TITLE = "MyDirection"
    BINDINGS = [Binding("q", "quit", "Quit")]
    CSS_PATH = 'static/app.tcss'

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen(LoadingScreen())


if __name__ == "__main__":
    app = MyApp()
    app.run()
