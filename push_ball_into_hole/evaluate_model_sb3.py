import gymnasium as gym
from stable_baselines3 import PPO
import matplotlib.pyplot as plt

gym.register(
    id="PushingBall-v0",
    entry_point="push:PushingBallEnv",  
    max_episode_steps=100,
)

# Initialize the environment
env = gym.make("PushingBall-v0", render_mode="human")

# Load the trained model
model = PPO.load("ppo_pushing_ball3")

# Test the policy for multiple episodes
num_test_episodes = 100  # Number of test episodes
rewards_per_episode = []  # To store total rewards for each episode
success_per_episode = []  # To store success for each episode

for episode in range(num_test_episodes):
    obs, info = env.reset()
    done = False
    total_reward = 0
    success = False

    while not done:
        # Predict the next action using the trained model
        action, _states = model.predict(obs, deterministic=True)  
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        done = terminated or truncated

        # Check if success was achieved
        if "is_success" in info and info["is_success"]:
            success = True

    rewards_per_episode.append(total_reward)
    success_per_episode.append(1 if success else 0)  # 1 for success, 0 otherwise
    print(f"Episode {episode + 1}: Total Reward = {total_reward}, Success = {success}")

env.close()

# Visualization
# Plot rewards per episode
plt.figure(figsize=(10, 5))
plt.plot(rewards_per_episode, label="Total Reward per Episode")
plt.xlabel("Episode")
plt.ylabel("Total Reward")
plt.title("Rewards per Episode")
plt.legend()
plt.grid(True)
plt.show()

# Plot success rate
plt.figure(figsize=(10, 5))
plt.bar(range(1, num_test_episodes + 1), success_per_episode, label="Success per Episode")
plt.xlabel("Episode")
plt.ylabel("Success (1 = Yes, 0 = No)")
plt.title("Success per Episode")
plt.legend()
plt.grid(True)
plt.show()

# Print overall success rate
overall_success_rate = sum(success_per_episode) / num_test_episodes * 100
print(f"Overall Success Rate: {overall_success_rate:.2f}%")
