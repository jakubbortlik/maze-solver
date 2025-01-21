# About this repository

This repository contains the code to a simple maze creator and solver written in Python using the
`tkinter` library.

## Running the maze solver

Simply do `python main.py` and see how the maze is created with a random path from the left upper
corner to the right bottom corner, ane how it is solved.

## ModuleNotFoundError: No module named '_tkinter'

If you can't run the code due to the missing `_tkinter` module, you can install the package using
`poetry` and then you should be able to run it with `poetry run python main.py` or by first entering
the Poetry shell and then running normally:

```bash
poetry shell
python main.py
```
