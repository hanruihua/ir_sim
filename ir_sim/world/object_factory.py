import numpy as np
from ir_sim.world.robots.robot_diff import RobotDiff
from ir_sim.world.robots.robot_acker import RobotAcker
from ir_sim.world import ObjectBase
from ir_sim.world.obstacles.obstacle_diff import ObstacleDiff
from ir_sim.world.obstacles.obstacle_static import ObstacleStatic
from ir_sim.util.util import extend_list


class ObjectFactory:
    
    
    def create_from_parse(self, parse, obj_type='robot'):
        # create object from yaml file parse

        object_list = list()

        if isinstance(parse, list):
            object_list = [obj for sp in parse for obj in self.create_object(obj_type, **sp)]

        elif isinstance(parse, dict):
            object_list = [obj for obj in self.create_object(obj_type, **parse)]

        return object_list


    def create_object(self, obj_type='robot', **kwargs):
        
        number = int(kwargs.get('number', 1))
        distribution = kwargs.get('distribution', 'manual')

        if number == 0:
            return list()

        if number == 1:
            if obj_type == 'robot':
                return [self.create_robot(**kwargs)]
            elif obj_type == 'obstacle':
                return [self.create_obstacle(**kwargs)]
        
        else:
            if distribution == 'manual':
                pass
                
            elif distribution == 'random':
                pass

            else:
                raise NotImplementedError(f"Distribution {distribution} not implemented, please use 'manual', 'random'")


        
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
        
        kinematics_name = kinematics.get('name', None)
  
        if kinematics_name == 'diff':
            return ObstacleDiff.create_with_shape(kinematics_name, shape, kinematics_dict=kinematics, **kwargs)
        elif kinematics_name == 'acker':
            pass
        elif kinematics_name == 'omni':
            pass
        else:
            return ObstacleStatic.create_with_shape(kinematics_name, shape, kinematics_dict=kinematics, **kwargs)


    def generate_state_list(self, number, distribution='random', **kwargs):
        pass

            
        
    
        

    
        
