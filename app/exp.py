from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ProgressBar, Label
from textual.color import Gradient
from textual.containers import Center, Middle
from textual.screen import Screen
from textual.reactive import reactive

gradient = Gradient.from_colors(
    "#881177", "#aa3355", "#cc6666", "#ee9944", "#eedd00",
    "#99dd55", "#44dd88", "#22ccbb", "#00bbcc", "#0099cc",
    "#3366bb", "#663399",
)

class LoadingScreen(Screen):
    progress = reactive(0)
    step = reactive(0)

    steps = [
        ("🔌 Checking internet connection...", 25),
        ("📡 Connecting to OpenStreetMap API...", 50),
        ("🤖 Loading AI model (Gemini)...", 75),
        ("✅ Ready to go!", 100),
    ]

    def compose(self) -> ComposeResult:
        with Center():
            with Middle():
                yield Label("Loading...", id="title-label")
                yield ProgressBar(total=100, show_eta=False, id="progress-bar", gradient=gradient)
                yield Label("", id="status-label")

    def on_ready(self) -> None:
        # Start updating every 1.5 seconds
        self.set_interval(1.5, self.next_step)

    def next_step(self) -> None:
        # Only proceed if there are still steps left
        if self.step < len(self.steps):
            message, progress = self.steps[self.step]
            self.query_one("#status-label", Label).update(message)
            self.query_one("#progress-bar", ProgressBar).progress = progress
            self.step += 1
        else:
            self.app.pop_screen()  # Transition after all steps

class MyApp(App):
    TITLE = "MyDirection"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()

    async def on_mount(self) -> None:
        await self.push_screen(LoadingScreen())

if __name__ == "__main__":
    app = MyApp()
    app.run()
