from math import inf
import numpy as np
from ir_sim.global_param import world_param
from ir_sim.util.util import relative_position, WrapToPi
from ir_sim.lib.behaviorlib import DiffDash, AckerDash


class Behavior:
    def __init__(self, object_info=None, behavior_dict=None) -> None:

        self.object_info = object_info
        self.behavior_dict = behavior_dict


    def gen_vel(self, state, goal, min_vel, max_vel):


        if self.behavior_dict is None:
            return np.zeros((2, 1))

        if self.object_info.kinematics == 'diff':
            if self.behavior_dict['name'] == 'dash':

                angle_tolerance = self.behavior_dict.get('angle_tolerance', 0.1)
                goal_threshold = self.object_info.goal_threshold

                behavior_vel = DiffDash(state, goal, max_vel, angle_tolerance, goal_threshold)

            elif self.behavior_dict['name'] == 'wander':
                
                angle_tolerance = self.behavior_dict.get('angle_tolerance', 0.1)
                goal_threshold = self.object_info.goal_threshold

                behavior_vel = DiffDash(state, goal, max_vel, angle_tolerance, goal_threshold)

            
        elif self.object_info.kinematics == 'acker':

            if self.behavior_dict['name'] == 'dash':

                angle_tolerance = self.behavior_dict.get('angle_tolerance', 0.1)
                goal_threshold = self.object_info.goal_threshold

                behavior_vel = AckerDash(state, goal, max_vel, angle_tolerance, goal_threshold)

        elif self.object_info.kinematics == 'omni':
            pass
            
                
        return behavior_vel







        
        