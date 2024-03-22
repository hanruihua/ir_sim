import numpy as np
from ir_sim.world.robots.robot_diff import RobotDiff
from ir_sim.world.robots.robot_acker import RobotAcker
from ir_sim.world import ObjectBase


class RobotFactory:

    def create_robot(self, kinematics_name, kinematics_dict=dict(), shape=dict(), **kwargs) -> ObjectBase:

        if kinematics_name == 'diff':
            return RobotDiff.create_with_shape('diff', shape, kinematics_dict=kinematics_dict, **kwargs)
        elif kinematics_name == 'acker':
            return RobotAcker.create_with_shape('acker', shape, kinematics_dict=kinematics_dict, **kwargs)
        elif kinematics_name == 'omni':
            # return RobotOmni(**kwargs)
            pass
        else:
            raise NotImplementedError(f"Robot kinematics {kinematics_name} not implemented")
        
    
    def create_robot_single(self, kinematics, shape=dict(), **kwargs):

        kinematics_name = kinematics.pop('name', 'omni')
        
        if kinematics_name == 'diff':
            return RobotDiff.create_with_shape('diff', shape, kinematics_dict=kinematics, **kwargs)
        elif kinematics_name == 'acker':
            return RobotAcker.create_with_shape('acker', shape, kinematics_dict=kinematics, **kwargs)
        elif kinematics_name == 'omni':
            # return RobotOmni(**kwargs)
            pass
        else:
            raise NotImplementedError(f"Robot kinematics {kinematics_name} not implemented")
    
    
    
            
        
    # def __init__(self, type='diff', shape='circle', **kwargs) -> None:
        

    
        
