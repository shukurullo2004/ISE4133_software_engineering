from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ProgressBar, Label
from textual.color import Gradient
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.reactive import reactive
from asyncio import sleep

from loading_screen import LoadingScreen
from input_screen import InputScreen

class MyApp(App):
    CSS_PATH = 'static/app.tcss'
    TITLE = "MyDirection"
    BINDINGS = [Binding("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    async def on_mount(self) -> None:
        await self.push_screen(LoadingScreen())
    

if __name__ == "__main__":
    app = MyApp()
    app.run()