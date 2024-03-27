from ir_sim.env import EnvBase

env = EnvBase('random_obstacle.yaml', save_ani=False, rm_fig_path=False, full=False)

for i in range(300):

    env.step()
    env.render(0.05, show_goal=False)
    
    if env.done():
        break

env.end(3)
