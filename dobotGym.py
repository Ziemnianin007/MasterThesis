
import math
import gym
from gym import spaces
import numpy as np
import coordinateOperation
import fileOperation

class dobotGym(gym.Env):
    def __init__(self):
        self.coordinateOperationInstance = coordinateOperation.coordinateOperation(plot=False, save=True)
        self.coordinateOperationInstance.recording = False

        self.coordinateOperationInstance.preparationForMoving()
        while(1):
            self.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
            self.coordinateOperationInstance.setDobotPositionToMove(X,Y,Z)
            self.coordinateOperationInstance.moveDobotToPreparedPosition()
        self.coordinateOperationInstance.endOfMoving()

        # Angle at which to fail the episode

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.

        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def step(self, action):


        x, x_dot, theta, theta_dot = self.state
        force = self.force_mag if action == 1 else -self.force_mag
        costheta = math.cos(theta)
        sintheta = math.sin(theta)

        # For the interested reader:
        # https://coneural.org/florian/papers/05_cart_pole.pdf
        temp = (force + self.polemass_length * theta_dot ** 2 * sintheta) / self.total_mass
        thetaacc = (self.gravity * sintheta - costheta * temp) / (self.length * (4.0 / 3.0 - self.masspole * costheta ** 2 / self.total_mass))
        xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

        if self.kinematics_integrator == 'euler':
            x = x + self.tau * x_dot
            x_dot = x_dot + self.tau * xacc
            theta = theta + self.tau * theta_dot
            theta_dot = theta_dot + self.tau * thetaacc
        else:  # semi-implicit euler
            x_dot = x_dot + self.tau * xacc
            x = x + self.tau * x_dot
            theta_dot = theta_dot + self.tau * thetaacc
            theta = theta + self.tau * theta_dot

        self.state = (x, x_dot, theta, theta_dot)

        done = bool(
            x < -self.x_threshold
            or x > self.x_threshold
            or theta < -self.theta_threshold_radians
            or theta > self.theta_threshold_radians
        )

        if not done:
            reward = 1.0
        elif self.steps_beyond_done is None:
            # Pole just fell!
            self.steps_beyond_done = 0
            reward = 1.0
        else:
            if self.steps_beyond_done == 0:
                pass
            self.steps_beyond_done += 1
            reward = 0.0

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_beyond_done = None
        return np.array(self.state)


    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None