import numpy as np
from ir_sim.world.robots.robot_diff import RobotDiff
from ir_sim.world.robots.robot_acker import RobotAcker
from ir_sim.world import ObjectBase


class RobotFactory:

    def create_robot(self, dynamics_name, dynamics_dict=dict(), shape=dict(), **kwargs) -> ObjectBase:

        if dynamics_name == 'diff':
            return RobotDiff.create_with_shape('diff', shape, dynamics_dict=dynamics_dict, **kwargs)
        elif dynamics_name == 'acker':
            return RobotAcker.create_with_shape('acker', shape, dynamics_dict=dynamics_dict, **kwargs)
        elif dynamics_name == 'omni':
            # return RobotOmni(**kwargs)
            pass
        else:
            raise NotImplementedError(f"Robot dynamics {dynamics_name} not implemented")
        
    
    def create_robot_single(self, dynamics, shape=dict(), **kwargs):

        dynamics_name = dynamics.pop('name', 'omni')
        
        if dynamics_name == 'diff':
            return RobotDiff.create_with_shape('diff', shape, dynamics_dict=dynamics, **kwargs)
        elif dynamics_name == 'acker':
            return RobotAcker.create_with_shape('acker', shape, dynamics_dict=dynamics, **kwargs)
        elif dynamics_name == 'omni':
            # return RobotOmni(**kwargs)
            pass
        else:
            raise NotImplementedError(f"Robot dynamics {dynamics_name} not implemented")
    
    
    
            
        
    # def __init__(self, type='diff', shape='circle', **kwargs) -> None:
        

    
        
