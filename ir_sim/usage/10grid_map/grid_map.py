from ir_sim.env import EnvBase

env = EnvBase('grid_map.yaml', save_ani=False, rm_fig_path=False, full=False)

for i in range(1000):

    env.step()
    env.render(0.05)
    
    if env.done():
        break

env.end(10)
