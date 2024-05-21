import gym
import pygame as pg
import wargaming
from deduction_config_05.ai.RL_brain import DeepQNetwork
#from pieces_manager_02 import piece
war = wargaming.Wargame()
# env.wargame_env()
# war.run()
env = war.wargame_env
# piece_ = piece.Piece()
# env.wargame.run()


# print(env.action_space)
# print(env.observation_space)
# print(env.observation_space.high)
# print(env.observation_space.low)
# print(env.rule)
# print(env.red_player)


RL = DeepQNetwork(n_actions=6,
                  n_features=3,
                  learning_rate=0.01, e_greedy=0.9,
                  replace_target_iter=100, memory_size=2000,
                  e_greedy_increment=0.001,)
# observation = env.get_piece_xyz()
total_steps = 0
for i_episode in range(100):

    #observation = war.red_player.get_piece_state()
    #observation = piece.RTank.get_piece_state()
    ep_r = 0
    while True:
        env.wargame.run()

        action = RL.choose_action(observation)

        observation_, reward, done, info = env.move_step(action)


        RL.store_transition(observation, action, reward, observation_)

        ep_r += reward
        if total_steps > 1000:
            RL.learn()

        if done:
            print('episode: ', i_episode,
                  'ep_r: ', round(ep_r, 2),
                  ' epsilon: ', round(RL.epsilon, 2))
            break

        observation = observation_
        total_steps += 1

RL.plot_cost()

