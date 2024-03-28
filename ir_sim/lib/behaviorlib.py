from ir_sim.util.util import relative_position, WrapToPi
import numpy as np


def DiffDash(state, goal, max_vel, angle_tolerance=0.1, goal_threshold=0.1):

    distance, radian = relative_position(state, goal) 

    if distance < goal_threshold:
        return np.zeros((2, 1))

    diff_radian = WrapToPi( radian - state[2, 0] )

    linear = max_vel[0, 0] * np.cos(diff_radian)

    if abs(diff_radian) < angle_tolerance:
        angular = 0
    else:
        angular = max_vel[1, 0] * np.sign(diff_radian)

    return np.array([[linear], [angular]])

def AckerDash(state, goal, max_vel, angle_tolerance, goal_threshold):

    dis, radian = relative_position(state, goal)

    steer_opt = 0.0

    diff_radian = WrapToPi( radian - state[2, 0] )
    
    if diff_radian > -angle_tolerance and diff_radian < angle_tolerance: diff_radian = 0

    if dis < goal_threshold:
        v_opt, steer_opt = 0, 0
    else:
        v_opt = max_vel[0, 0]
        steer_opt = np.clip(diff_radian, -max_vel[1, 0], max_vel[1, 0])   

    return np.array([[v_opt], [steer_opt]])



def DiffRVO():
    

    pass






# def OmniDash(state, goal, max_vel, angle_tolerance, goal_threshold):

#     dis, radian = relative_position(state, goal)

#     steer_opt = 0.0

#     diff_radian = WrapToPi( radian - state[2, 0] )
    
#     if diff_radian > -angle_tolerance and diff_radian < angle_tolerance: diff_radian = 0

#     if dis < goal_threshold:
#         v_opt, steer_opt = 0, 0
#     else:
#         v_opt = max_vel[0, 0]
#         steer_opt = np.clip(diff_radian, -max_vel[1, 0], max_vel[1, 0])   

#     return np.array([[v_opt], [steer_opt]])