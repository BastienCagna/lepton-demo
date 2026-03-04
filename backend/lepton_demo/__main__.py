from pathlib import Path
from lepton.app import LeptonApp, LeptonConfig
from lepton_demo.game import MRTusIOHelper
from lepton_demo.controller import router as game_router


config = LeptonConfig(
    app_name="MRTus",
    frontend_path=Path(__file__).parent.parent / "front",
    config_dir=Path.home() / ".config/mrtus"
)
app = LeptonApp(config, MRTusIOHelper)
app.include_router(game_router, prefix="/game", tags=["game"])


if __name__ == "__main__":
    app.start_uvicorn()
