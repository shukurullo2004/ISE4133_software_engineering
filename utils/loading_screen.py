from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ProgressBar, Label
from textual.color import Gradient
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.reactive import reactive
from asyncio import sleep

# Your gradient is fine
gradient = Gradient.from_colors(
    "#881177", "#aa3355", "#cc6666", "#ee9944", "#eedd00",
    "#99dd55", "#44dd88", "#22ccbb", "#00bbcc", "#0099cc",
    "#3366bb", "#663399",
)

class LoadingScreen(Screen):

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Label("Loading...", classes='bold-label')
                yield ProgressBar(total=100, show_eta=False, id="progress-bar", gradient=gradient)
                yield Label("", id="status-label")

    # async def on_mount(self) -> None:
    async def on_ready(self) -> None:
        await self.run_loading_steps()

    async def run_loading_steps(self) -> None:
        await self.update_step("Checking internet connection...", 25)
        await self.update_step("Connecting to OpenStreetMap API...", 50)
        await self.update_step("Loading AI model (Gemini)...", 75)
        await self.update_step("Ready to go!", 100)
        await sleep(1)
        # await self.app.pop_screen()

    async def update_step(self, message: str, progress: int):
        self.query_one("#status-label", Label).update(message)
        self.query_one("#progress-bar", ProgressBar).progress = progress
        self.refresh() 
        await sleep(1)


class MyApp(App):
    CSS = """
    .bold-label {
        text-style: bold;
    }
    """

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
