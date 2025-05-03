from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Header, Footer, ProgressBar, Label, Button, Input, ContentSwitcher, Markdown, LoadingIndicator
from textual.containers import Center, Middle, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual.reactive import reactive
from asyncio import sleep
import config
from utils import get_things_done

class MainScreen(Screen):
    TITLE = "MyDirection"
    BINDINGS = [Binding("q", "quit", "Quit"), Binding("Esc", "esc_main", "Back")]
    
    def __init__(self, args):
        super().__init__()
        self.data = get_things_done(args)


    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
    #     yield LoadingIndicator(id="loading-container")

    # def on_mount(self):
    #     check_addr('texas')
    #     # Load data from APIs
    #     self.query_one('#loading-indicator', LoadingIndicator).remove()

        with Horizontal(id="buttons"):  
            yield Button("Route", id="route")  
            yield Button("Travel tips", id="travel-tips")
            yield Button("Weather📍", id="weather1")  
            yield Button("Weather🎯", id="weather2")  


        with ContentSwitcher(initial="route"):  
            with VerticalScroll(id="route"):
                yield Markdown(self.data['route'])
            with VerticalScroll(id="travel-tips"):
                yield Markdown(self.data['gemini-tips'])
            with VerticalScroll(id="weather1"):
                yield Markdown(self.data['weather-orig'])
            with VerticalScroll(id="weather2"):
                yield Markdown(self.data['weather-dest'])
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.query_one(ContentSwitcher).current = event.button.id  

    def action_esc_main(self):
        config.logger.info('escape')
        self.app.pop_screen()
        
