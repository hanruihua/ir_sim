import yaml

from ir_sim.util.util import file_check
# from ir_sim.world import world, MultiRobots, MultiObstacles
from ir_sim.world import world
from .env_plot import EnvPlot
import threading
from ir_sim.global_param import world_param, env_param
import time
import sys
from ir_sim.world.robots.robot_factory import RobotFactory
from ir_sim.world.obstacles.obstacle_factory import ObstacleFactory
from matplotlib import pyplot as plt
from ir_sim.world.robots.multi_robots import MultiRobots
from ir_sim.world.obstacles.multi_obstacles import MultiObstacles
import platform
import numpy as np
from pynput import keyboard

class EnvBase:

    '''
    The base class of environment.

        parameters:
            world_name: the name of the world file, default is None
    
    
    '''

    def __init__(self, world_name=None, display=True, disable_all_plot=False, save_ani=False, full=False, **kwargs):

        world_file_path = file_check(world_name)
        
        world_kwargs, plot_kwargs, robot_kwargs_list, robots_kwargs_list, obstacle_kwargs_list, obstacles_kwargs_list  = dict(), dict(), [], [], [], []

        if world_file_path != None:
           
            with open(world_file_path) as file:
                com_list = yaml.load(file, Loader=yaml.FullLoader)
                world_kwargs = com_list.get('world', dict())
                plot_kwargs = com_list.get('plot', dict())
                keyboard_kwargs = com_list.get('keyboard', dict())
                robot_kwargs_list = com_list.get('robot', list())
                robots_kwargs_list = com_list.get('robots', list())
                obstacle_kwargs_list = com_list.get('obstacle', list())
                obstacles_kwargs_list = com_list.get('obstacles', list())

        # for python 3.10
        # world_kwargs |= kwargs.get('world', dict())
        # plot_kwargs |= kwargs.get('plot', dict())
        # robots_kwargs |= kwargs.get('robots', dict())
        # obstacles_kwargs |= kwargs.get('obstacles', dict())
        # robot_kwargs |= kwargs.get('robot', dict())

        world_kwargs.update(kwargs.get('world', dict()))
        plot_kwargs.update(kwargs.get('plot', dict()))

        [robot_kw.update(kw) for (robot_kw, kw) in zip( robot_kwargs_list, kwargs.get('robot', list()) )]
        [robots_kw.update(kw) for (robots_kw, kw) in zip( robots_kwargs_list, kwargs.get('robots', list()) )]
        [obstacle_kw.update(kw) for (obstacle_kw, kw) in zip( obstacle_kwargs_list, kwargs.get('obstacle', list()) )]
        [obstacles_kw.update(kw) for (obstacles_kw, kw) in zip( obstacles_kwargs_list, kwargs.get('obstacles', list()) )]

        # init world, robot, obstacles
        self.world = world(**world_kwargs)

        robot_factory = RobotFactory() 
        obstacle_factory = ObstacleFactory() 

        self.robot_list = [ robot_factory.create_robot_single(**robot_kw) for robot_kw in robot_kwargs_list]
        self.robots_list = [ MultiRobots(**robots_kwargs) for robots_kwargs in robots_kwargs_list ]
        self.obstacle_list = [ obstacle_factory.create_obstacle_single(**obstacle_kw) for obstacle_kw in obstacle_kwargs_list]
        self.obstacles_list = [ MultiObstacles(**obstacles_kw) for obstacles_kw in obstacles_kwargs_list ]
        
        # self.objects = self.robot_list + self.robots_list + self.obstacle_list + self.obstacles_list 
        
        robots_sum_list = [robot for robots in self.robots_list for robot in robots.robot_list]
        obstacles_sum_list = [obstacle for obstacles in self.obstacles_list for obstacle in obstacles.obstacle_list]

        self.objects = self.robot_list + robots_sum_list + self.obstacle_list + obstacles_sum_list
        

        self.env_plot = EnvPlot(self.world.grid_map, self.objects, self.world.x_range, self.world.y_range, **plot_kwargs)

        self.robot_number = len(self.robot_list + robots_sum_list)
        self.obstacle_number = len(self.obstacle_list + obstacles_sum_list)


        # set env param
        self.display = display
        self.disable_all_plot = disable_all_plot

        self.save_ani = save_ani

        env_param.objects = self.objects

        if world_param.control_mode == 'keyboard':
            self.init_keyboard(keyboard_kwargs)

        if full:
            mode = platform.system()
            if mode == 'Linux':
                # mng = plt.get_current_fig_manager()
                plt.get_current_fig_manager().full_screen_toggle()
                # mng.resize(*mng.window.maxsize())
                # mng.frame.Maximize(True)

            elif mode == 'Windows':
                # figManager = plt.get_current_fig_manager()
                # figManager.window.showMaximized()
                # figManager.resize(*figManager.window.maxsize())
                # self.env_plot.fig.canvas.manager.window.showMaximized()
                mng = plt.get_current_fig_manager()
                mng.full_screen_toggle()
        # # thread
        # self.step_thread = threading.Thread(target=self.step)
    
    # def start(self, duration=500, **kwargs):

    #     self.step_thread.start()

    #     while world_param.count < duration:
    #         print(world_param.count)
    #         self.render(world_param.step_time)

    def __del__(self):
        print('Simulated Environment End')

    def start(self, duration=500):
        pass
    
    # step
    def step(self, action=None, action_id=0, **kwargs):

        if isinstance(action, list):
            self.objects_step(action)
        else:
            if world_param.control_mode == 'keyboard': 
                self.object_step(self.key_vel, self.key_id)
            else:
                self.object_step(action, action_id)

        # if action is None:
        #     action = [None] * len(self.objects)
        self.world.step()

    def objects_step(self, action=None):
        action = action + [None] * (len(self.objects) - len(action))
        [ obj.step(action) for obj, action in zip(self.objects, action)]

    def object_step(self, action, obj_id=0):
        self.objects[obj_id].step(action)
        [ obj.step() for obj in self.objects if obj._id != obj_id]

        
    def render(self, interval=0.05, figure_kwargs=dict(), **kwargs):

        # figure_args: arguments when saving the figures for animation, see https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html for detail
        # default figure arguments

        if not self.disable_all_plot: 
            if self.world.sampling:

                if self.display: plt.pause(interval)

                if self.save_ani: self.env_plot.save_gif_figure(**figure_kwargs)

                self.env_plot.clear_components('dynamic', self.objects, **kwargs)
                self.env_plot.draw_components('dynamic', self.objects, **kwargs)
                

    def show(self):
        self.env_plot.show()

    # def clear(self):
    #     pass

    # def init_plot(self, **kwargs):
    #     pass

    def reset_plot(self):
        plt.cla()
        self.env_plot.init_plot(self.world.grid_map, self.objects)


    def init_keyboard(self, keyboard_kwargs=dict()):

        vel_max = keyboard_kwargs.get('vel_max', [3.0, 1.0])
        self.key_lv_max = keyboard_kwargs.get("key_lv_max", vel_max[0])
        self.key_ang_max = keyboard_kwargs.get("key_ang_max", vel_max[1])
        self.key_lv = keyboard_kwargs.get("key_lv", 0.0)
        self.key_ang = keyboard_kwargs.get("key_ang", 0.0)
        self.key_id = keyboard_kwargs.get("key_id", 0)
        self.alt_flag = 0

        plt.rcParams['keymap.save'].remove('s')
        plt.rcParams['keymap.quit'].remove('q')
        
        self.key_vel = np.zeros((2, 1))

        print('start to keyboard control')
        print('w: forward', 's: backforward', 'a: turn left', 'd: turn right', 
                'q: decrease linear velocity', 'e: increase linear velocity',
                'z: decrease angular velocity', 'c: increase angular velocity',
                'alt+num: change current control robot id', 'r: reset the environment')
                
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()



    def draw_trajectory(self, traj, traj_type='g-', **kwargs):
        self.env_plot.draw_trajectory(traj, traj_type, **kwargs)

    def draw_points(self, points, s=30, c='b', **kwargs):
        self.env_plot.draw_points(points, s, c, **kwargs)


    def draw_box(self, vertex, refresh=True, **kwargs):
        self.env_plot.draw_box(vertex, refresh, **kwargs)


    def end(self, ending_time=1, **kwargs):

        if self.save_ani:
            self.env_plot.save_animate(**kwargs)


        print(f'Figure will be closed within {ending_time:d} seconds.')
        plt.pause(ending_time)
        plt.close()
        

    def done(self, mode='all'):

        done_list = [ obj.done() for obj in self.objects if obj.role=='robot']

        if len(done_list) == 0:
            return False

        if mode == 'all':
            return all(done_list)
        elif mode == 'any':
            return any(done_list)
        
    def reset(self):
        self.reset_all() 

    def reset_all(self):
        [obj.reset() for obj in self.objects]
        


    def get_robot_info(self, id=0):
        return self.robot_list[id].get_info()



    #     def reset(self, mode='now', **kwargs):
    #     # mode: 
    #     #   default: reset the env now
    #     #   any: reset all the env when any robot done
    #     #   all: reset all the env when all robots done
    #     #   single: reset one robot who has done, depending on the done list
    #     if mode == 'now':
    #         self.reset_all() 
    #     else:
    #         done_list = self.done_list(**kwargs)
    #         if mode == 'any' and any(done_list): self.reset_all()
    #         elif mode == 'all' and all(done_list): self.reset_all()
    #         elif mode == 'single': 
    #             [self.reset_single(i) for i, done in enumerate(done_list) if done]

    # def end(self, ani_name='animation', fig_name='fig.png', ending_time = 3, suffix='.gif', keep_len=30, rm_fig_path=True, fig_kwargs=dict(), ani_kwargs=dict(), **kwargs):
        
    #     # fig_kwargs: arguments when saving the figures for animation, see https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html for detail
    #     # ani_kwargs: arguments for animations(gif): see https://imageio.readthedocs.io/en/v2.8.0/format_gif-pil.html#gif-pil for detail
    #     if self.control_mode == 'keyboard': self.listener.stop()
        
    #     show = kwargs.get('show', self.display)
        
    #     if not self.disable_all_plot:

    #         if self.save_ani:
    #             saved_ani_kwargs = {'subrectangles': True}
    #             saved_ani_kwargs.update(ani_kwargs) 
    #             self.save_animate(ani_name, suffix, keep_len, rm_fig_path, **saved_ani_kwargs)

    #         if self.save_fig or show:
    #             self.draw_components(self.ax, mode='dynamic', **kwargs)
            
    #         if self.save_fig: 
    #             if not self.fig_path.exists(): self.fig_path.mkdir()

    #             self.fig.savefig(str(self.fig_path) + '/' + fig_name, bbox_inches=self.bbox_inches, dpi=self.fig_dpi, **fig_kwargs)

    #         if show:
    #             plt.show(block=False)
    #             print(f'Figure will be closed within {ending_time:d} seconds.')
    #             plt.pause(ending_time)
    #             plt.close()


    @property
    def robot(self):
        robot_list = [ obj for obj in self.objects if obj.role == 'robot']

        return robot_list[0]

    @property
    def arrive(self):
        return self.robot.arrive
    
    @property
    def collision(self):
        return self.robot.collision


    def get_current_robots(self):
        return [obj for obj in self.objects if obj.role == 'robot']

    def get_robot_state(self):
        return self.robot._state
    
    def get_lidar_scan(self, id=0):
        r_list = self.get_current_robots()

        return r_list[id].get_lidar_scan()
    
    def get_lidar_points(self, id=0):

        r_list = self.get_current_robots()
        
        return r_list[id].get_lidar_points()

        


    

    # region: keyboard control
    def on_press(self, key):

        try:
            if key.char.isdigit() and self.alt_flag:

                if int(key.char) >= self.robot_number:
                    print('out of number of robots')
                    self.key_id = int(key.char)
                else:
                    print('current control id: ', int(key.char))
                    self.key_id = int(key.char)

            if key.char == 'w':
                self.key_lv = self.key_lv_max
            if key.char == 's':
                self.key_lv = - self.key_lv_max
            if key.char == 'a':
                self.key_ang = self.key_ang_max
            if key.char == 'd':
                self.key_ang = -self.key_ang_max
            
            self.key_vel = np.array([ [self.key_lv], [self.key_ang]])

        except AttributeError:
            
            try:
                if "alt" in key.name:
                    self.alt_flag = True

            except AttributeError:

                if key.char.isdigit() and self.alt_flag:

                    if int(key.char) >= self.robot_number:
                        print('out of number of robots')
                        self.key_id = int(key.char)
                    else:
                        print('current control id: ', int(key.char))
                        self.key_id = int(key.char)
        
    def on_release(self, key):
        
        try:
            if key.char == 'w':
                self.key_lv = 0
            if key.char == 's':
                self.key_lv = 0
            if key.char == 'a':
                self.key_ang = 0
            if key.char == 'd':
                self.key_ang = 0
            if key.char == 'q':
                self.key_lv_max = self.key_lv_max - 0.2
                print('current lv ', self.key_lv_max)
            if key.char == 'e':
                self.key_lv_max = self.key_lv_max + 0.2
                print('current lv ', self.key_lv_max)
            
            if key.char == 'z':
                self.key_ang_max = self.key_ang_max - 0.2
                print('current ang ', self.key_ang_max)
            if key.char == 'c':
                self.key_ang_max = self.key_ang_max + 0.2
                print('current ang ', self.key_ang_max)
            
            if key.char == 'r':
                self.reset()
            
            self.key_vel = np.array([[self.key_lv], [self.key_ang]])

        except AttributeError:
            if "alt" in key.name:
                self.alt_flag = False
    # endregion:keyboard control
    

    


