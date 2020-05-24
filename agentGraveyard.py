def NAFAgent(self, nb_states, nb_actions):
    # Get the environment and extract the number of actions.

    # Build all necessary models: V, mu, and L networks.
    V_model = Sequential()
    V_model.add(Flatten(input_shape=(1, nb_states)))
    V_model.add(Dense(16))
    V_model.add(Activation('relu'))
    V_model.add(Dense(16))
    V_model.add(Activation('relu'))
    V_model.add(Dense(16))
    V_model.add(Activation('relu'))
    V_model.add(Dense(1))
    V_model.add(Activation('linear'))
    print(V_model.summary())

    mu_model = Sequential()
    mu_model.add(Flatten(input_shape=(1, nb_states)))
    mu_model.add(Dense(16))
    mu_model.add(Activation('relu'))
    mu_model.add(Dense(16))
    mu_model.add(Activation('relu'))
    mu_model.add(Dense(16))
    mu_model.add(Activation('relu'))
    mu_model.add(Dense(nb_actions))
    mu_model.add(Activation('linear'))
    print(mu_model.summary())

    action_input = Input(shape=(1, nb_actions,), name='action_input')
    observation_input = Input(shape=(1, nb_states), name='observation_input')
    x = Concatenate()([Flatten()(action_input), Flatten()(observation_input)])
    x = Dense(32)(x)
    x = Activation('relu')(x)
    x = Dense(32)(x)
    x = Activation('relu')(x)
    x = Dense(32)(x)
    x = Activation('relu')(x)
    # x = Dense((1))(x)
    x = Dense(((nb_actions * nb_actions + nb_actions) // 2))(x)
    x = Activation('linear')(x)
    L_model = Model(inputs=[action_input, observation_input], outputs=x)
    print(L_model.summary())

    # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
    # even the metrics!
    self.model = V_model
    processor = PendulumProcessor()
    memory = SequentialMemory(limit=100000, window_length=1)
    random_process = OrnsteinUhlenbeckProcess(theta=.15, mu=0., sigma=.3, size=nb_actions)
    agent = NAFAgent(nb_actions=nb_actions, V_model=self.model, L_model=L_model, mu_model=mu_model,
                     memory=memory, nb_steps_warmup=100, random_process=random_process,
                     gamma=.99, target_model_update=1e-3, processor=processor)
    return agent
    # agent.compile(Adam(lr=.001, clipnorm=1.), metrics=['mae'])


def agentDDP(self, nb_states, nb_actions):
    # Next, we build a very simple model.
    actor = Sequential()
    actor.add(Dense(16, activation='relu', input_shape=(1, nb_states)))
    actor.add(Dense(16, activation='relu'))
    actor.add(Dense(16, activation='relu'))
    actor.add(Dense(16, activation='relu'))
    actor.add(Dense(nb_actions, activation='linear'))
    print(actor.summary())

    action_input = Input(shape=(nb_actions,), name='action_input')
    observation_input = Input(shape=(nb_states,), name='observation_input')

    x1 = keras.layers.Dense(8)(action_input)
    x2 = keras.layers.Dense(8)(observation_input)
    # flattened_observation = Flatten()(observation_input)
    x = Concatenate()([x1, x2])
    x = Dense(32)(x)
    x = Activation('relu')(x)
    x = Dense(32)(x)
    x = Activation('relu')(x)
    x = Dense(32)(x)
    x = Activation('relu')(x)
    x = Dense(1)(x)
    x = Activation('linear')(x)
    critic = Model(inputs=[action_input, observation_input], outputs=x)
    print(critic.summary())

    # Finally, we configure and compile our agent. You can use every built-in Keras optimizer and
    # even the metrics!
    memory = SequentialMemory(limit=100000, window_length=1)
    random_process = OrnsteinUhlenbeckProcess(size=nb_actions, theta=.15, mu=0., sigma=.3)
    self.model = actor
    agent = DDPGAgent(nb_actions=nb_actions, actor=self.model, critic=critic, critic_action_input=action_input,
                      memory=memory, nb_steps_warmup_critic=100, nb_steps_warmup_actor=100,
                      random_process=random_process, gamma=.99, target_model_update=1e-3)
    agent.compile(Adam(lr=.001, clipnorm=1.), metrics=['mae'])
    return agent
    # Okay, now it's time to learn something! We visualize the training here for show, but this
    # slows down training quite a lot. You can always safely abort the training prematurely using
    # Ctrl + C.
    # agent.fit(env, nb_steps=50000, visualize=True, verbose=1, nb_max_episode_steps=200)
    #
    # # After training is done, we save the final weights.
    # agent.save_weights('ddpg_{}_weights.h5f'.format(ENV_NAME), overwrite=True)
    #
    # # Finally, evaluate our algorithm for 5 episodes.
    # agent.test(env, nb_episodes=5, visualize=True, nb_max_episode_steps=200)



import math
import gym
from gym import spaces
import numpy as np
import coordinateOperation
import fileOperation

class dobotGym(gym.Env):
    def __init__(self, plot = False, save= True, emulateOculus = True, episodeLength = 15):
        self.coordinateOperationInstance = coordinateOperation.coordinateOperation(plot = plot, save = save,emulateOculus = emulateOculus)
        self.coordinateOperationInstance.recording = False

        # Angle at which to fail the episode

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        maxStep = 150
        #self.action_space = spaces.Box(low=np.array([-maxStep, -maxStep, -maxStep]), high=np.array([maxStep, maxStep, maxStep]),dtype=np.float32)

        self.action_space = spaces.Box(np.array([self.coordinateOperationInstance.minX,self.coordinateOperationInstance.minY,self.coordinateOperationInstance.minZ]),
                                       np.array([self.coordinateOperationInstance.maxX,self.coordinateOperationInstance.maxY,self.coordinateOperationInstance.maxZ])
                                            ,dtype=np.float32)

        self.observation_space = spaces.Box(np.array([self.coordinateOperationInstance.minX,self.coordinateOperationInstance.minY,self.coordinateOperationInstance.minZ]),
                                       np.array([self.coordinateOperationInstance.maxX,self.coordinateOperationInstance.maxY,self.coordinateOperationInstance.maxZ])
                                            ,dtype=np.float32)

        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

        self.episodeLength = episodeLength -2
        self.episodeStep = 0

    def step(self, action):
        print("Action", action, self.action_space.low, self.action_space.high)
        action = np.clip(action, self.action_space.low, self.action_space.high)
        print(action)
        self.coordinateOperationInstance.coordinateFromOculusToDobotTranslation() #translating coordinates from oculus to dobot system
        self.coordinateOperationInstance.setDiffPositionToMove(action[0],action[1],action[2])
        self.state = self.coordinateOperationInstance.moveDobotToPreparedPosition()

        reward = 1/(self.coordinateOperationInstance.actualDiffXYZ+1)
        if self.coordinateOperationInstance.grip is True:
            done = False
        else:
            done = True

        if (self.episodeStep > self.episodeLength):
            done = True

        info = {
            'Diff': self.coordinateOperationInstance.actualDiffXYZ,
        }
        self.episodeStep += 1
        return np.array(self.state), reward, done, info

    def reset(self):
        self.coordinateOperationInstance.endOfMoving()
        self.episodeStep = 0
        self.coordinateOperationInstance.preparationForMoving()
        self.state = np.array([self.coordinateOperationInstance.rightXLastDobot,self.coordinateOperationInstance.rightYLastDobot,self.coordinateOperationInstance.rightZLastDobot])
        while(self.coordinateOperationInstance.grip is False):
            pass
        self.coordinateOperationInstance.startRecording()
        return np.array(self.state)


    def close(self):
        self.coordinateOperationInstance.endOfMoving()