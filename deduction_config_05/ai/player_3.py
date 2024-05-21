# -*- coding: utf-8 -*-
# @Time : 2021/5/12 14:43
import tensorflow as tf
import os
import numpy as np
import torch as T
import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical
import random

NAME = '钟山智狼'

# np.random.seed(2)
# tf.set_random_seed(2)

class PPOMemory:
    def __init__(self, batch_size):
        self.states = []
        self.probs = []
        self.vals = []
        self.actions = []
        self.rewards = []
        self.dones = []

        self.batch_size = batch_size

    def generate_batches(self):
        n_states = len(self.states)
        batch_start = np.arange(0, n_states, self.batch_size)
        indices = np.arange(n_states, dtype=np.int64)
        np.random.shuffle(indices)
        batches = [indices[i:i + self.batch_size] for i in batch_start]
        return np.array(self.states), \
               np.array(self.actions), \
               np.array(self.probs), \
               np.array(self.vals), \
               np.array(self.rewards), \
               np.array(self.dones), \
               batches

    def store_memory(self, state, action, probs, vals, reward, done):
        self.states.append(state)
        self.actions.append(action)
        self.probs.append(probs)
        self.vals.append(vals)
        self.rewards.append(reward)
        self.dones.append(done)

    def clear_memory(self):
        self.states = []
        self.probs = []
        self.actions = []
        self.rewards = []
        self.dones = []
        self.vals = []


class ActorNetwork(nn.Module):
    def __init__(self, n_actions, input_dims, alpha=0.0003,
                 fc1_dims=256, fc2_dims=256, fc3_dims=256,
                 chkpt_dir='C:/Users/周佳炜/Desktop/陆战智能战术兵棋推演平台【先胜1号】v4.1/deduction_config_05/ai_01'):
        super(ActorNetwork, self).__init__()

        self.checkpoint_file = os.path.join(chkpt_dir, 'actor_torch_ppo')
        self.actor = nn.Sequential(
            nn.Linear(*input_dims, fc1_dims),
            nn.ReLU(),
            nn.Linear(fc1_dims, fc2_dims),
            nn.ReLU(),
            nn.Linear(fc2_dims, fc3_dims),
            nn.ReLU(),
            nn.Linear(fc3_dims, n_actions),
            nn.Softmax(dim=-1)
        )
        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self,state):
        dist = self.actor(state)
        dist = Categorical(dist)
        return dist

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpiont(self):
        self.load_state_dict(T.load(self.checkpoint_file))


class CriticNetwork(nn.Module):
    def __init__(self, input_dims, alpha=0.0003, fc1_dims=256, fc2_dims=256, fc3_dims=256,
                 chkpt_dir='C:/Users/周佳炜/Desktop/陆战智能战术兵棋推演平台【先胜1号】v4.1/deduction_config_05/ai'):
        super(CriticNetwork, self).__init__()

        self.checkpoint_file = os.path.join(chkpt_dir, 'critic_torch_ppo')
        self.critic = nn.Sequential(
            nn.Linear(*input_dims, fc1_dims),
            nn.ReLU(),
            nn.Linear(fc1_dims, fc2_dims),
            nn.ReLU(),
            nn.Linear(fc2_dims, fc3_dims),
            nn.ReLU(),
            nn.Linear(fc3_dims, 1)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        value = self.critic(state)
        return value

    def save_checkpoint(self):
        T.save(self.state_dict(), self.checkpoint_file)

    def load_checkpoint(self):
        self.load_state_dict(T.load(self.checkpoint_file))


class Agent:
    def __init__(self, n_actions, input_dims=4, gamma=0.99, alpha=0.0003, gae_lambda=0.95,
                 policy_clip=0.2, batch_size=64, n_epochs=10):
        self.gamma = gamma
        self.policy_clip = policy_clip
        self.n_epochs = n_epochs
        self.gae_lambda = gae_lambda

        self.actor = ActorNetwork(n_actions, input_dims, alpha)
        self.critic = CriticNetwork(input_dims, alpha)
        self.memory = PPOMemory(batch_size)

    def remember(self, state, action, probs, vals, reward, done):
        # 自我记忆存储
        self.memory.store_memory(state, action, probs, vals, reward, done)

    def save_models(self):
        print('... saving models ...')
        self.actor.save_checkpoint()
        self.critic.save_checkpoint()

    def load_models(self):
        print('... loading models ...')
        self.actor.load_checkpoint()
        self.critic.load_checkpoint()

    def choose_action(self, observation):
        '''
        usage: 选择可以观察到当前状态的动作
        '''
        state = T.tensor([observation], dtype=T.float).to(self.actor.device)
        dist = self.actor(state)
        value = self.critic(state)
        action = dist.sample()
        # 实际执行操作的对数概率；squeeze()数据维度压缩，去掉维数为1的维度
        probs = T.squeeze(dist.log_prob(action)).item()
        action = T.squeeze(action).item()
        value = T.squeeze(value).item()

        return action, probs, value

    def learn(self):
        for _ in range(self.n_epochs):
            state_arr, action_arr, old_prob_arr, vals_arr, \
            reward_arr, dones_arr, batches = \
                self.memory.generate_batches()

            values = vals_arr
            advantage = np.zeros(len(reward_arr), dtype=np.float32)

            for t in range(len(reward_arr) - 1):
                discount = 1
                a_t = 0
                for k in range(t, len(reward_arr) - 1):
                    a_t += discount * (reward_arr[k] + self.gamma * values[k + 1] * \
                                       (1 - int(dones_arr[k])) - values[k])
                    discount *= self.gamma * self.gae_lambda
                advantage[t] = a_t
            advantage = T.tensor(advantage).to(self.actor.device)

            values = T.tensor(values).to(self.actor.device)
            for batch in batches:
                states = T.tensor(state_arr[batch], dtype=T.float).to(self.actor.device)
                old_probs = T.tensor(old_prob_arr[batch]).to(self.actor.device)
                actions = T.tensor(action_arr[batch]).to(self.actor.device)

                dist = self.actor(states)
                # 根据状态更新到critic网络的更新值
                critic_value = self.critic(states)

                critic_value = T.squeeze(critic_value)

                new_probs = dist.log_prob(actions)
                prob_ratio = new_probs.exp() / old_probs.exp()
                # prob_ratio = (new_probs - old_probs).exp()
                # 加权概率计算由advantage[batch]乘以裁剪概率
                weighted_probs = advantage[batch] * prob_ratio
                # 计算加权裁剪概率，输入的prob_ratio夹紧到(1-self.policy_clip, 1+self.policy_clip)乘以advantage[batch]
                weighted_clipped_probs = T.clamp(prob_ratio, 1 - self.policy_clip,
                                                 1 + self.policy_clip) * advantage[batch]
                actor_loss = -T.min(weighted_probs, weighted_clipped_probs).mean()

                returns = advantage[batch] + values[batch]
                critic_loss = (returns - critic_value) ** 2
                critic_loss = critic_loss.mean()

                total_loss = actor_loss + 0.5 * critic_loss
                # 梯度归零
                self.actor.optimizer.zero_grad()
                self.critic.optimizer.zero_grad()
                total_loss.backward()
                self.actor.optimizer.step()
                self.critic.optimizer.step()

        self.memory.clear_memory()


def get_state(wargame):
    state = np.array([wargame.scenario.red_tank_1.co_x,
                     wargame.scenario.red_tank_1.co_y,
                     wargame.scenario.red_tank_1.goal[0],
                     wargame.scenario.red_tank_1.goal[1]
                        ])

    return state

def replace_action(num, wargame):
    s_x = wargame.scenario.red_tank_1.co_x
    s_y = wargame.scenario.red_tank_1.co_y
    s_x_ = wargame.scenario.red_tank_2.co_x
    s_y_ = wargame.scenario.red_tank_2.co_y
    e_x = wargame.scenario.blue_tank_1.co_x
    e_y = wargame.scenario.blue_tank_1.co_y
    e_x_ = wargame.scenario.blue_tank_2.co_x
    e_y_ = wargame.scenario.blue_tank_2.co_y

    site_neighbour_1 = wargame.game_map.get_neighbour(s_x, s_y)
    site_neighbour_2 = wargame.game_map.get_neighbour(s_x_, s_y_)
    tank1 = wargame.scenario.red_tank_1
    tank2 = wargame.scenario.red_tank_2
    enermy1 = wargame.scenario.blue_tank_1
    enermy2 = wargame.scenario.blue_tank_2

    if wargame.game_map.visibility_estimation(s_x,s_y,e_x,e_y) or wargame.game_map.visibility_estimation(s_x_,s_y_,e_x,e_y):
        tank1.direct_fire(enermy1)
        tank2.direct_fire(enermy1)
    elif wargame.game_map.visibility_estimation(s_x,s_y,e_x_,e_y_) or wargame.game_map.visibility_estimation(s_x_,s_y_,e_x_,e_y_):
        tank1.direct_fire(enermy2)
        tank2.direct_fire(enermy2)
    elif s_y >= 7 and s_y <= 17:
        tank1.move_one_step(site_neighbour_1[1][0], site_neighbour_1[1][1])
        tank2.move_one_step(site_neighbour_2[1][0], site_neighbour_2[1][1])
    elif num == 0 and 11 <= site_neighbour_1[0][0] <= 25 and 5 <= site_neighbour_1[0][1] <= 43:
        tank1.move_one_step(site_neighbour_1[0][0], site_neighbour_1[0][1])
        tank2.move_one_step(site_neighbour_2[0][0], site_neighbour_2[0][1])
    elif num == 1 and 11 <= site_neighbour_1[1][0] <= 25 and 5 <= site_neighbour_1[1][1] <= 43:
        tank1.move_one_step(site_neighbour_1[1][0], site_neighbour_1[1][1])
        tank2.move_one_step(site_neighbour_2[1][0], site_neighbour_2[1][1])
    elif num == 2 and 11 <= site_neighbour_1[2][0] <= 25 and 5 <= site_neighbour_1[2][1] <= 43:
        tank1.move_one_step(site_neighbour_1[2][0], site_neighbour_1[2][1])
        tank2.move_one_step(site_neighbour_2[2][0], site_neighbour_2[2][1])
    elif num == 3 and 11 <= site_neighbour_1[3][0] <= 25 and 5 <= site_neighbour_1[3][1] <= 43:
        tank1.move_one_step(site_neighbour_1[3][0], site_neighbour_1[3][1])
        tank2.move_one_step(site_neighbour_2[3][0], site_neighbour_2[3][1])
    elif num == 4 and 11 <= site_neighbour_1[4][0] <= 25 and 5 <= site_neighbour_1[4][1] <= 43:
        tank1.move_one_step(site_neighbour_1[4][0], site_neighbour_1[4][1])
        tank2.move_one_step(site_neighbour_2[4][0], site_neighbour_2[4][1])
    elif num == 5 and 11 <= site_neighbour_1[5][0] <= 25 and 5 <= site_neighbour_1[5][1] <= 43:
        tank1.move_one_step(site_neighbour_1[5][0], site_neighbour_1[5][1])
        tank2.move_one_step(site_neighbour_2[5][0], site_neighbour_2[5][1])

sess = tf.Session()
agent = Agent(6,)
saver = tf.train.Saver()
# saver.restore(sess, 'model/train-15000')

def red_choose_action(wargame):
    s = get_state(wargame)
    num = agent.choose_action(s)
    replace_action(num, wargame)