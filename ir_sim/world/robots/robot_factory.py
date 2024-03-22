import numpy as np
from ir_sim.world.robots.robot_diff import RobotDiff
from ir_sim.world.robots.robot_acker import RobotAcker
from ir_sim.world import ObjectBase


class RobotFactory:
    def __init__(self, robot_kwargs=None, robots_kwargs=None) -> None:

        self.robot_kwargs = robot_kwargs
        self.robots_kwargs = robots_kwargs

    # def create_robot(self, kinematics_name, kinematics_dict=dict(), shape=dict(), **kwargs) -> ObjectBase:

    #     if kinematics_name == 'diff':
    #         return RobotDiff.create_with_shape('diff', shape, kinematics_dict=kinematics_dict, **kwargs)
    #     elif kinematics_name == 'acker':
    #         return RobotAcker.create_with_shape('acker', shape, kinematics_dict=kinematics_dict, **kwargs)
    #     elif kinematics_name == 'omni':
    #         # return RobotOmni(**kwargs)
    #         pass
    #     else:
    #         raise NotImplementedError(f"Robot kinematics {kinematics_name} not implemented")
        
    
    # def create_robot_single(self, kinematics, shape=dict(), **kwargs):

    #     kinematics_name = kinematics.pop('name', 'omni')
        
    #     if kinematics_name == 'diff':
    #         return RobotDiff.create_with_shape('diff', shape, kinematics_dict=kinematics, **kwargs)
    #     elif kinematics_name == 'acker':
    #         return RobotAcker.create_with_shape('acker', shape, kinematics_dict=kinematics, **kwargs)
    #     elif kinematics_name == 'omni':
    #         # return RobotOmni(**kwargs)
    #         pass
    #     else:
    #         raise NotImplementedError(f"Robot kinematics {kinematics_name} not implemented")
    
    def create_from_parse(self):
        
        if self.robot_kwargs is not None:
            self.create_robot(**self.robot_kwargs)
        

    def create_robot(self, kinematics, shape=dict(), **kwargs):

        # kinematics_name = kinematics.pop('name', 'omni')
        kinematics_name = kinematics.get('name', 'omni')
        
        if kinematics_name == 'diff':
            return RobotDiff.create_with_shape('diff', shape, kinematics_dict=kinematics, **kwargs)
        elif kinematics_name == 'acker':
            return RobotAcker.create_with_shape('acker', shape, kinematics_dict=kinematics, **kwargs)
        elif kinematics_name == 'omni':
            # return RobotOmni(**kwargs)
            pass
        else:
            raise NotImplementedError(f"Robot kinematics {kinematics_name} not implemented")

    def create_robot_single(self, kinematics, shape=dict(), **kwargs):
        pass
        
    @staticmethod
    def convert():
        pass

            
        
    
        

    
        
