from enum import Enum
from pathlib import Path
from dataclasses import field
import random
from typing import List
from lepton_common.objects import LObject, IOHelper
from pydantic import BaseModel


DEFAULT_MAX_TRIALS = 4
DEFAULT_DICT = [
    "scanner", "morphology", "anatomy", "complexity",
    "algorithm", "programming", "development", "architecture",
    "brain", "neuron", "synapse", "cognition", "intelligence",
    "machine", "learning", "artificial", "intelligence", "data",
    "epygenetics", "neuroscience", "psychology", "philosophy",
    "disease", "medicine", "health", "wellness", "fitness",
    "parkinson", "alzheimers", "dementia", "stroke", "cancer",
    "echography", "imaging", "diagnosis", "treatment", "therapy",
    "neuroplasticity", "rehabilitation", "prosthetics", "assistive",
    "statistics", "probability", "modeling", "simulation", "visualization",
]

class MRTusLetterState(Enum):
    NONE = 0
    WRONG_PLACE = 1
    CORRECT = 2

class MRTusTrial(BaseModel):
    word: str
    states: List[MRTusLetterState]

class MRTusGame(BaseModel):
    answer: str
    max_trials: int = DEFAULT_MAX_TRIALS
    trials: List[MRTusTrial] = field(default_factory=list)

    def add_trial(self, word: str) -> MRTusTrial:
        if len(self.trials) >= self.max_trials:
            raise ValueError("Maximum number of trials reached")
        
        # Compute the state of each letter in the trial
        states = []
        letter_counts = {}
        for i, s in enumerate(word):
            if s == self.answer[i]:
                state = MRTusLetterState.CORRECT
            elif s in self.answer:
                if letter_counts.get(s, 0) >= self.answer.count(s):
                    state = MRTusLetterState.NONE
                else:
                    state = MRTusLetterState.WRONG_PLACE
            else:
                state = MRTusLetterState.NONE
            letter_counts[s] = letter_counts.get(s, 0) + 1
            states.append(state)

        # Register the trial
        trial = MRTusTrial(word=word, states=states)
        self.trials.append(trial)
        return trial

class MRTusGameSet(LObject):
    dictionnary: List[str] = field(default=DEFAULT_DICT)
    games: List[MRTusGame] = field(default_factory=list)

    def new_game(self) -> MRTusGame:
        answer = None
        while answer is None or answer in [game.answer for game in self.games]:
            answer = self.dictionnary[int(len(self.dictionnary) * random.random())]
        game = MRTusGame(answer=answer)
        self.games.append(game)
        return game

def load_game_set(path: Path) -> MRTusGameSet:
    if not path.exists():
        return MRTusGameSet()
    return MRTusGameSet.parse_file(path)

def save_game_set(path: Path, snap: MRTusGameSet):
    snap.json(path, indent=4)


MRTusIOHelper = IOHelper(MRTusGameSet, load_game_set, save_game_set)