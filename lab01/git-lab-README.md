# Git Introduction
This lab is designed to introduce you to the basics of Git. You will learn how to create a repository, commit changes, and push your changes to a remote repository.

## What is Git?
Git is a distributed version control system that allows you to keep track of your code changes and collaborate with other developers. It is a tool that is used by developers to manage their codebase and work on projects with other developers.

## Checkout these resource for learning more about Git
- https://www.youtube.com/watch?v=Ala6PHlYjmw
- https://www.youtube.com/watch?v=SWYqp7iY_Tc
- https://githubtraining.github.io/training-manual


## Git Commands
- `git init`
- `git add`
- `git commit`
- `git status`
- `git push`
- `git pull`
- `git clone`
- `git switch`
- `git remote`
- `git checkout`
- `git branch`
- `git stash`

## Submission
- Clone this repository in your local machine.
- Create your own remote repository in GitHub.
- Rename the remote from 'origin' to 'profremote', using the `git remote` command
- Link your local repository to your remote repository using `git remote add origin <your-remote-repo-link>`
- Create your first python script (`lab01.py`) to print 'Hello [your name]'.
- Commit your changes to the repository
    - Use `git add` to stage your changes
        - You can add just the file you created or add all untracked files, if you created others.
    - Use `git commit` with `-m` flag to commit your changes with a message.
        - A message is always required for a commit.
    - Verify your commit using `git log` or `git status`.
- Push your changes to your remote repository.
- Submit the link to your commit. 
  - Ensure that the link looks like the following with the hash of your commit at the end.

      `https://github.com/username/game-ai-lab/commit/7b1b9e5b72093rnd08h4rgd723923u0042h`

  __IMPORTANT__: All your lab submissions will be commit links like this one to the respective code update, except otherwise mentioned.
      
