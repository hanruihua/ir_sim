from ir_sim2.env import EnvBase
import time 

env = EnvBase(world_name = 'obstacle_world.yaml')

for i in range(300):
    des_vel = env.cal_des_vel()
    env.step(des_vel)
    env.render(0.03)
    
    if env.done():
        break

env.show()
