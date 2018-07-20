from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features
import random

import time
# Functions
_TRAIN_SCV = actions.FUNCTIONS.Train_SCV_quick.id
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id

# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SCV = 45

# Parameters
_PLAYER_SELF = 1
_NOT_QUEUED = [0]
_QUEUED = [1]

class SimpleAgent(base_agent.BaseAgent):
    base_top_left = None
    supply_depot_built = True
    scv_selected = False

    def transformLocation(self, x, x_distance, y, y_distance):
        if not self.base_top_left:
            return [x - x_distance, y - y_distance]

        return [x + x_distance, y + y_distance]



    def step(self, obs):
        super(SimpleAgent, self).step(obs)

        #time.sleep(0.5)

        if self.base_top_left is None:
            player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
            self.base_top_left = player_y.mean() <= 31




        if not self.barracks_selected:
            unit_type = obs.observation["screen"][_UNIT_TYPE]
            unit_y, unit_x = (unit_type == _TERRAN_BARRACKS).nonzero()
            if unit_y.any():
                target = [int(unit_x.mean()), int(unit_y.mean())]

                return actions.FunctionCall(_SELECT_POINT, [_NOT_QUEUED, target])

        if self.supply_depot_built:
            if not self.scv_selected:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_SCV).nonzero()

                target = [unit_x[0], unit_y[0]]

                self.scv_selected = True

                return actions.FunctionCall(_SELECT_POINT, [_QUEUED, target])

            elif _BUILD_SUPPLYDEPOT in obs.observation["available_actions"]:
                unit_type = obs.observation["screen"][_UNIT_TYPE]
                unit_y, unit_x = (unit_type == _TERRAN_COMMANDCENTER).nonzero()

                target = self.transformLocation(abs(random.randint(0, 40)),abs(random.randint(0, 40)), abs(random.randint(0, 40)), abs(random.randint(0, 40)))

                self.supply_depot_built = True

                return actions.FunctionCall(_BUILD_SUPPLYDEPOT, [_QUEUED, target])
        return actions.FunctionCall(_NOOP, [])
