from .obstacle_base import ObstacleBase
import matplotlib as mpl
import numpy as np
from math import sin, cos

class ObstacleCircle(ObstacleBase):

    obstacle_type = 'obstacle_circle' # circle, polygon
    obstacle_shape = 'circle'  # circle, polygon
    point_dim = (2, 1) # the point dimension, x, y
    vel_dim = (2, 1) # the velocity dimension, linear and angular velocity
    goal_dim = (2, 1) # the goal dimension, x, y, theta
    convex = True
    cone_type = 'norm2' # 'Rpositive'; 'norm2' 
    
    def __init__(self, id, point=np.zeros((2, 1)), goal=np.ones((2, 1)), radius=0.2, step_time=0.1, dynamic=True, sport='wander', **kwargs):

        if isinstance(point, list): point = np.c_[point]
        if isinstance(goal, list): goal = np.c_[goal]

        self.point = point
        self.radius = radius

        assert point.shape == self.point_dim and goal.shape == self.goal_dim

        super(ObstacleCircle, self).__init__(id=id, step_time=step_time, **kwargs)

        self.goal = goal
        self.goal_threshold = kwargs.get('goal_threshold', 0.2)

        self.vel_min = kwargs.get('vel_min', np.c_[[-2, -2]])
        self.vel_max = kwargs.get('vel_max', np.c_[[2, 2]])

        if isinstance(self.vel_min, list): self.vel_min = np.c_[self.vel_min]
        if isinstance(self.vel_max, list): self.vel_max = np.c_[self.vel_max]

        self.sport_range = kwargs.get('sport_range', [0, 0, 10, 10])  # xmin ymin xmax ymax  (if sport 'wander')

        self.sport = sport  # default, wander, patrol 
        self.plot_patch_list = []
        self.dynamic = dynamic
        self.arrive_flag = False
    
    def move(self, vel, **kwargs):
        self.point = self.point + vel * self.step_time
        self.A, self.b = self.gen_inequal()
    
    def move_goal(self, **kwargs):
        des_vel = self.cal_des_vel()
        self.move(des_vel)
    
    def move_wander(self, **kwargs):
        
        if self.arrive_flag:
            temp = np.random.uniform(low=self.sport_range[0:2], high=self.sport_range[2:4])
            self.goal = np.expand_dims(temp, axis=1)
            self.arrive_flag = False

        des_vel = self.cal_des_vel()
        self.move(des_vel)

    def arrive(self):
        return np.linalg.norm(self.point - self.goal) <= self.goal_threshold

    def cal_des_vel(self):
        
        dis, radian = ObstacleCircle.relative_position(self.point, self.goal, topi=False)
        
        if dis > self.goal_threshold:
            vx = self.vel_max[0, 0] * cos(radian)
            vy = self.vel_max[1, 0] * sin(radian)
        else:
            vx = 0
            vy = 0
            self.arrive_flag = True

        return np.array([[vx], [vy]])

    def gen_inequal(self):
        A = np.array([ [1, 0], [0, 1], [0, 0] ])
        b = np.row_stack((self.point, -self.radius * np.ones((1,1))))

        return A, b

    def gen_inequal_cir(self, point, radius):
        A = np.array([ [1, 0], [0, 1], [0, 0] ])
        b = np.row_stack((point, -radius * np.ones((1,1))))
        return A, b

    def gen_matrix(self):
        pass

    def plot(self, ax, obs_cir_color='k', **kwargs): 
        obs_circle = mpl.patches.Circle(xy=(self.point[0, 0], self.point[1, 0]), radius = self.radius, color = obs_cir_color)
        obs_circle.set_zorder(2)
        ax.add_patch(obs_circle)
        self.plot_patch_list.append(obs_circle)

    def plot_clear(self):
        for patch in self.plot_patch_list:
            patch.remove()

        self.plot_patch_list = []
    

    