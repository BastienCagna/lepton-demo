from typing import List

from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.params import Depends
from lepton.session import get_session_from_token, get_token_data, ObjectStoreItem
from lepton.app import LeptonApp
from lepton.utils import get_lepton_app
from lepton.auth import TokenData

from .game import MRTusGameSet, MRTusTrial, MRTusGame

router = APIRouter()

class MRTusGameData(BaseModel):
    word_length: int
    max_trials: int
    trials: List[MRTusTrial]


def get_gameset(
    token_data: TokenData = Depends(get_token_data),
    app: LeptonApp = Depends(get_lepton_app),
) -> MRTusGameSet:
    """ Get the current game or create a new one if it doesn't exist """
    session = get_session_from_token(token_data, app)
    if len(session.items) == 0:
        gameset = MRTusGameSet()
        session.register_item(ObjectStoreItem(None, gameset))
    return session.items[0].object

def get_last_game(gameset: MRTusGameSet = Depends(get_gameset)) -> MRTusGame:
    if len(gameset.games) == 0:
        gameset.new_game()
    return gameset.games[-1]
    
@router.get("/current", response_model=MRTusGameData)
def get_current(game=Depends(get_last_game)):
    return MRTusGameData(len(game.answer), game.max_trials, game.trials)

@router.get("/new", response_model=MRTusGameData)
def get_new(gameset: MRTusGameSet = Depends(get_gameset)):
    game = gameset.new_game()
    return MRTusGameData(len(game.answer), game.max_trials, game.trials)

@router.post("/answer", response_model=MRTusTrial)
def post_anwser(answer: str, game=Depends(get_last_game)):
    return game.add_trial(answer)