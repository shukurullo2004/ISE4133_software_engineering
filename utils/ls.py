from textual.app import App, ComposeResult
from textual.widgets import ProgressBar, Static
import requests

class LoadingScreen(Static):
    """Custom loading screen with progress tracking"""
    
    def __init__(self):
        super().__init__()
        self.progress_steps = [
            ("Checking internet connection", self.check_internet),
            ("Verifying API endpoints", self.check_apis),
            ("Validating AI models", self.check_models),
            ("Finalizing setup", self.finalize)
        ]
        self.current_step = 0

    def compose(self) -> ComposeResult:
        yield ProgressBar(total=len(self.progress_steps)*25, show_eta=False)

    def on_mount(self) -> None:
        self.run_steps = self.set_interval(0.5, self.run_next_step)

    def check_internet(self) -> bool:
        try:
            return requests.get("https://google.com", timeout=5).ok
        except:
            return False

    def check_apis(self) -> bool:
        try:
            # Add actual API ping checks here
            return all([
                requests.get("https://nominatim.openstreetmap.org", timeout=5).ok,
                requests.get("https://generativelanguage.googleapis.com", timeout=5).ok
            ])
        except:
            return False

    def check_models(self) -> bool:
        return any(
            "gemini-2.5-pro-preview-03-25" in model.name
            for model in client.models.list()
        )

    def finalize(self) -> bool:
        # Add any final initialization logic
        return True

    def run_next_step(self) -> None:
        if self.current_step >= len(self.progress_steps):
            self.run_steps.stop()
            return
            
        label, task = self.progress_steps[self.current_step]
        self.query_one(ProgressBar).update(total=100)
        success = task()
        
        if not success:
            self.notify(f"Failed at step: {label}", severity="error")
            self.app.exit()
            
        self.query_one(ProgressBar).advance(25)
        self.current_step += 1

class TravelAssistant(App):
    def compose(self) -> ComposeResult:
        yield LoadingScreen()

    def on_ready(self) -> None:
        # Transition to main UI after loading
        pass

if __name__ == "__main__":
    app = TravelAssistant()
    app.run()
