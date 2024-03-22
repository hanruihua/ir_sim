import numpy as np
from ir_sim.world.obstacles.obstacle_diff import ObstacleDiff
from ir_sim.world.obstacles.obstacle_static import ObstacleStatic


class ObstacleFactory:

    def create_obstacle(self, kinematics_dict, shape=dict(), **kwargs):
        
        if kinematics_dict is not None:
            kinematics_name = kinematics_dict.pop('name', 'diff')
        else:
            kinematics_name = None
        # kinematics_name, kinematics_dict=dict(),  

        if kinematics_name == 'diff':
            return ObstacleDiff.create_with_shape(kinematics_name, shape, kinematics_dict=kinematics_dict, **kwargs)
        elif kinematics_name == 'acker':
            pass
        elif kinematics_name == 'omni':
            pass
        else:
            return ObstacleStatic.create_with_shape(kinematics_name, shape, kinematics_dict=kinematics_dict, **kwargs)
             

    def create_obstacle_single(self, kinematics=None, shape=dict(), **kwargs):

        if kinematics is None:
            return ObstacleStatic.create_with_shape(None, shape, kinematics_dict=dict(), **kwargs)

        kinematics_name = kinematics.pop('name', 'omni')
        
        if kinematics_name == 'diff':
            return ObstacleDiff.create_with_shape('diff', shape, kinematics_dict=kinematics, **kwargs)
        elif kinematics_name == 'acker':
            pass
        elif kinematics_name == 'omni':
            # return RobotOmni(**kwargs)
            pass
        



    # def __init__(self, type='diff', shape='circle', **kwargs) -> None:
        

    
        
