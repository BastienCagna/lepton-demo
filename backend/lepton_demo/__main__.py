from pathlib import Path
from lepton.app import LeptonApp, LeptonConfig
from .game import MRTusIOHelper
from .controller import router as game_router


config = LeptonConfig(
    app_name="MRTus",
    frontend_path=Path(__file__).parent.parent / "front",
    settings_f=Path.home() / ".config/mrtus"
)
app = LeptonApp(config, MRTusIOHelper)
app.include_router(game_router, prefix="/game")


if __name__ == "__main__":
    app.start_uvicorn()
