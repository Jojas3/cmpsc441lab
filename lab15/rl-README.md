# Lab 15: Reinforcement Learning with Monte Carlo Control

## Overview
In this lab you will implement a **Monte Carlo (MC) control** agent that learns to solve the `FrozenLake-v1` environment from Gymnasium. Unlike temporal-difference methods (Q-learning, SARSA) which update value estimates after every step, MC methods wait until an episode finishes and then update from the full trajectory. This makes MC conceptually the simplest RL algorithm: just collect episodes and average the returns.

## The Environment
`FrozenLake-v1` is a 4x4 grid (16 states, 4 actions) where the agent must walk from start to goal without falling into a hole. The scaffold uses `is_slippery=False`, so transitions are deterministic and an optimal policy reaches the goal on every episode.

- **States**: integers `0..15`.
- **Actions**: `0` Left, `1` Down, `2` Right, `3` Up.
- **Reward**: `+1` for reaching the goal, `0` otherwise.
- **Terminal states**: holes and the goal.

Docs: <https://gymnasium.farama.org/environments/toy_text/frozen_lake/>

## Files
```
lab15/
├── rl-README.md   # this file
├── demo.py        # play FrozenLake manually to get a feel for the env
└── lab15.py       # scaffold you will complete
```

## Get a Feel for the Environment First
Before writing any code, drive the agent by hand to see what the state, reward, and termination signals look like:
```bash
python lab15/demo.py
```
You pick actions one step at a time (`w`/`a`/`s`/`d` or `0`-`3`) and watch how the environment responds. This is the same interface your agent will use.

## What You Need to Implement
Open `lab15.py` and search for `TODO`. There are **two** functions to complete:

1. **`choose_action(state, action_space, epsilon)`** — epsilon-greedy action selection.
   - With probability `epsilon`, return a random action from `action_space`.
   - Otherwise return `argmax_a Q[(state, a)]`, breaking ties randomly.
   - When `epsilon == 0.0`, the function must act greedily. Measurement mode depends on this.

2. **`update_from_episode(episode)`** — first-visit Monte Carlo update.
   - `episode` is a list of `(state, action, reward)` tuples in time order.
   - Walk backwards accumulating the return `G = reward + GAMMA * G`.
   - For the **first** visit of each `(state, action)` pair in the episode, update the running average:
     ```
     returns_count[(s, a)] += 1
     Q[(s, a)] += (G - Q[(s, a)]) / returns_count[(s, a)]
     ```

That's it. Do **not** modify the environment, the training loop, or the measurement code — the grader relies on them.

## Running
From the repository root:
```bash
python lab15/lab15.py
```
This will train for `NUM_EPISODES` episodes and then run measurement mode. A correctly implemented agent trains in a few seconds.

## Measurement Mode (Success Criterion)
After training, `measure()` runs **100 greedy episodes** (`epsilon=0.0`) using fixed seeds and reports a success rate. The task is considered **solved** when the success rate is at least **90%**. Expected output on success:
```
Success rate: 100.00%  (threshold 90%)
Verdict: SOLVED
```
If you see `Verdict: NOT SOLVED`, your implementation has a bug or hyperparameters need tuning.

## Hints
- First-visit MC means: if `(s, a)` appears more than once in an episode, only update it the first time it is encountered.
- Compute returns in a single backward pass — it is easier than summing forward.
- Track visited `(state, action)` pairs in a `set` to detect first visits.
- When `Q[(state, a)]` is zero for every action (start of training), `max` ties must break **randomly**, otherwise the agent deterministically explores only one direction.
- If the agent never learns, check that exploration is actually happening: print `epsilon` during training, and verify that early episodes contain varied actions.
- The default `NUM_EPISODES = 5000` and decay schedule are sufficient. If you tune them and still cannot solve the task, the bug is almost certainly in `update_from_episode`.

## Deliverables
Commit your completed `lab15.py`. Your submission will be graded by running:
```bash
python lab15/lab15.py
```
and checking that the measurement mode prints `Verdict: SOLVED`.

## References
- Sutton & Barto, *Reinforcement Learning: An Introduction*, Chapter 5 (Monte Carlo Methods).
- Gymnasium FrozenLake docs: <https://gymnasium.farama.org/environments/toy_text/frozen_lake/>
