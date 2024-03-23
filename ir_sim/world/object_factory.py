import numpy as np
from ir_sim.world.robots.robot_diff import RobotDiff
from ir_sim.world.robots.robot_acker import RobotAcker
from ir_sim.world import ObjectBase
from ir_sim.world.obstacles.obstacle_diff import ObstacleDiff
from ir_sim.world.obstacles.obstacle_static import ObstacleStatic

class ObjectFactory:
    
    def create_from_parse(self, single_parse, multiple_parse, obj_type='robot'):
        
        object_list1 = list()

        if isinstance(single_parse, list):
            object_list1 = [self.create_object(obj_type, **sp) for sp in single_parse]
            
        elif isinstance(single_parse, dict):
            object_list1 = [self.create_object(obj_type, **single_parse)]


        return object_list1

    def create_object(self, obj_type='robot', **kwargs):
        
        if obj_type == 'robot':
            return self.create_robot(**kwargs)
        elif obj_type == 'obstacle':
            return self.create_obstacle(**kwargs)


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


    def create_obstacle(self, kinematics=dict(), shape=dict(), **kwargs):
        
        kinematics_name = kinematics.get('name', 'omni')
  
        if kinematics_name == 'diff':
            return ObstacleDiff.create_with_shape(kinematics_name, shape, kinematics_dict=kinematics, **kwargs)
        elif kinematics_name == 'acker':
            pass
        elif kinematics_name == 'omni':
            pass
        else:
            return ObstacleStatic.create_with_shape(kinematics_name, shape, kinematics_dict=kinematics, **kwargs)


    @staticmethod
    def convert_multiple_parse():
        pass

            
        
    
        

    
        
