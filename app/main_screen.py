from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ProgressBar, Label, Button, Input, ContentSwitcher, Markdown
from textual.containers import Center, Middle, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.reactive import reactive
from asyncio import sleep

from utils import check_addr
# from main_screen import MainScreen

class MainScreen(Screen):
    TITLE = "MyDirection"
    BINDINGS = [Binding("q", "quit", "Quit"), Binding("Esc", "esc_main", "Input screen")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

        with Horizontal(id="buttons"):  
            yield Button("Route", id="route")  
            yield Button("Travel tips", id="travel-tips")
            yield Button("Weather", id="weather")  

        with ContentSwitcher(initial="route"):  
            with VerticalScroll(id="route"):
                yield Markdown("route here")
            with VerticalScroll(id="travel-tips"):
                yield Markdown("tts here")
            with VerticalScroll(id="weather"):
                yield Markdown("weather here")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id  

    def action_ecs_main(self):
        self.app.pop_screen()
        # self.app.push_screen(InputScreen())

class MyApp(App):
    
    TITLE = "MyDirection"
    
    CSS_PATH = 'static/app.tcss'

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    app = MyApp()
    app.run()
