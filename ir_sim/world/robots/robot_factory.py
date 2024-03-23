import numpy as np
from ir_sim.world.robots.robot_diff import RobotDiff
from ir_sim.world.robots.robot_acker import RobotAcker
from ir_sim.world import ObjectBase
from ir_sim.world.object_factory import ObjectFactory

class RobotFactory():

        
    def create_robot(self, kinematics=dict(), shape=dict(), **kwargs):

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


            
        
    
        

    
        
