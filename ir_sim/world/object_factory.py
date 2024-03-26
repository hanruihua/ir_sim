import numpy as np
from ir_sim.world.robots.robot_diff import RobotDiff
from ir_sim.world.robots.robot_acker import RobotAcker
from ir_sim.world import ObjectBase
from ir_sim.world.obstacles.obstacle_diff import ObstacleDiff
from ir_sim.world.obstacles.obstacle_static import ObstacleStatic
from ir_sim.util.util import extend_list, is_list_of_lists, is_list_not_list_of_lists
from ir_sim.global_param import env_param 
import random

class ObjectFactory:
    
    
    def create_from_parse(self, parse, obj_type='robot'):
        # create object from yaml file parse

        object_list = list()

        if isinstance(parse, list):
            object_list = [obj for sp in parse for obj in self.create_object(obj_type, **sp)]

        elif isinstance(parse, dict):
            object_list = [obj for obj in self.create_object(obj_type, **parse)]

        return object_list


    def create_object(self, obj_type='robot', number=1, distribution={'name': 'manual'}, state=[1, 1, 0], goal=[1, 9, 0], **kwargs):

        '''
        create object based on the number of objects to create, object type, distribution of states and initial state
            - obj_type: 'robot' or 'obstacle'
            - number: number of objects to create
            - distribution: distribution of states for objects
            - state: initial state for objects
            - kwargs: other parameters for object creation
        '''
        
        state_list, goal_list = self.generate_state_list(number, obj_type, distribution, state, goal)
        object_list = list()

        for i in range(number):
            obj_dict = dict()
            
            obj_dict = {k: extend_list(v, number)[i] for k, v in kwargs.items() if k is not 'sensors'}
            obj_dict['state'] = state_list[i]
            obj_dict['goal'] = goal_list[i]
            
            if 'sensors' in kwargs:
                obj_dict['sensors'] = kwargs['sensors'] if is_list_not_list_of_lists(kwargs['sensors']) else extend_list(kwargs['sensors'], number)[i]

            if obj_type == 'robot':
                object_list.append(self.create_robot(**obj_dict))
            elif obj_type == 'obstacle':
                object_list.append(self.create_obstacle(**obj_dict))

        return object_list
    
    
            

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


    def generate_state_list(self, number=1, obj_type='robot', distribution={'name': 'manual'}, state=[1, 1, 0], goal=[1, 9, 0]):

        '''
        Generate state list for robots or obstacles based on distribution and state provided in kwargs
            - number: number of objects to generate
            - obj_type: 'robot' or 'obstacle'
            - distribution: distribution dictionary of states for objects
            - state: initial state for objects
        '''
        
        if number == 1:
            return [state], [goal]

        if distribution['name'] == 'manual':

            if is_list_not_list_of_lists(state):
                env_param.logger.warning("No state list provided for manual distribution, default start state {} sequence will be used.".format(state))

                if obj_type=='robot': 
                    state_list = [ [state[0] + i, state[1], state[2]] for i in range(number)]
                    goal_list = [ [goal[0] + i, goal[1], goal[2]] for i in range(number)]

                if obj_type=='obstacle': 
                    state_list = [state] * number
                    goal_list = [goal] * number

                return state_list, goal_list
            

            if is_list_of_lists(state):

                if is_list_not_list_of_lists(goal): 
                    goal = extend_list(goal, number)
                else:
                    goal = goal[:number]


                if len(state) < number:
                    if obj_type=='robot': 
                        env_param.logger.error("Robot state list provided is less than number of robots")
                        assert False

                    elif obj_type=='obstacle':
                        env_param.logger.warning("Obstacle state list provided is less than number of obstacles, state list will be repeated")

                        if is_list_not_list_of_lists(goal): goal = [goal]

                        return extend_list(state, number), goal
    
                else:
                    return state[:number], goal


        if distribution['name'] == 'random':
            pass
            
        #     x_range = distribution.get('x_range', (0, 10))
        #     y_range = distribution.get('y_range', (0, 10))
        #     theta_range = distribution.get('theta_range', (0, 2*np.pi))

        #     state_list = []
        #     for _ in range(number):
        #         x = random.uniform(*x_range)
        #         y = random.uniform(*y_range)
        #         theta = random.uniform(*theta_range)
        #         state_list.append([x, y, theta])
                 




