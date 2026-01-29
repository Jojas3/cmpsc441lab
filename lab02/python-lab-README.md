# Python Introduction
This lab is designed to introduce you to the basics to beauty of Python. You will learn the second most important industry skill after Git, __debugging__.

Just sit back, pay attention and soak in the beauty of Python with an open mind. Don't forget to ask questions along the way.

Enjoy the ride!!

## Lab tasks

The lab02.py file will run all the tests in the `tests` folder. Complete the tasks in the other files in the folder. 

1. Try your solutions by running `lab02.py`
2. Commit and push your changes to GitHub.
3. Submit the link to the commit on Canvas.

Consider reading the code in the `tests` folder to learn about test driven development (TDD).

## Using UV for Labs

UV is a modern Python package manager that's faster than pip and handles virtual environments automatically.

**Install UV:** https://docs.astral.sh/uv/getting-started/installation/

```bash
# Initialize project (creates pyproject.toml)
uv init

# Add packages for your lab
uv add requests numpy pandas

# Run your lab code with dependencies
uv run python lab02.py

# Install all project dependencies
uv sync
```

UV ensures consistent Python versions and dependencies across all lab environments.
