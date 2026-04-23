"""
Lab 15 Demo: Play FrozenLake by hand.

Interactive demo for getting a feel for FrozenLake before you implement
the agent. A pygame window shows the grid. Focus that window and press:

    Arrow keys or WASD  -- move
    r                   -- reset the episode
    q                   -- quit

Run from the repo root:
    python lab15/demo.py
"""

import gymnasium as gym
import pygame

ACTION_NAMES = {0: "Left", 1: "Down", 2: "Right", 3: "Up"}
KEY_TO_ACTION = {
    pygame.K_LEFT: 0, pygame.K_a: 0,
    pygame.K_DOWN: 1, pygame.K_s: 1,
    pygame.K_RIGHT: 2, pygame.K_d: 2,
    pygame.K_UP: 3, pygame.K_w: 3,
}


def print_status(step, action, state, reward, total_reward, terminated, truncated):
    print(
        f"step {step:>3} | action={action} ({ACTION_NAMES[action]:<5}) "
        f"| state={state:>2} | reward={reward:>4.1f} | total={total_reward:>4.1f} "
        f"| terminated={terminated} | truncated={truncated}"
    )
    if reward > 0:
        print("  " + "=" * 42)
        print(f"  *** REWARD RECEIVED: +{reward} ***")
        print("  " + "=" * 42)


def main():
    env = gym.make("FrozenLake-v1", is_slippery=False, render_mode="human")
    state, _ = env.reset()
    total_reward = 0.0
    step = 0
    episode_over = False

    print("FrozenLake-v1 (is_slippery=False). S=start, F=frozen, H=hole, G=goal.")
    print("Focus the pygame window. Arrow keys / WASD to move, r=reset, q=quit.")
    print(f"Starting state: {state}")
    pygame.display.set_caption("FrozenLake Demo -- arrows/WASD | r=reset | q=quit")

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_q:
                running = False
                break
            if event.key == pygame.K_r:
                state, _ = env.reset()
                total_reward = 0.0
                step = 0
                episode_over = False
                print(f"\nReset. Starting state: {state}")
                continue
            if episode_over or event.key not in KEY_TO_ACTION:
                continue

            action = KEY_TO_ACTION[event.key]
            state, reward, terminated, truncated, _ = env.step(action)
            reward = float(reward)
            total_reward += reward
            step += 1
            print_status(step, action, state, reward, total_reward, terminated, truncated)

            if terminated or truncated:
                outcome = "reached the goal!" if reward >= 1.0 else "fell in a hole."
                print(f"Episode over after {step} steps -- {outcome}  (press r to reset)")
                episode_over = True
        clock.tick(30)

    env.close()
    pygame.quit()


if __name__ == "__main__":
    main()
