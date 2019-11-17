import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='mnk-game-v0',
    entry_point='gym_mnk.envs:mnkEnv',
)