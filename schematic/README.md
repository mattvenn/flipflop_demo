# Schematic as code using [Schemdraw](https://schemdraw.readthedocs.io/en/stable/)

## Setup

```
python3 -m venv env
env/bin/python -m pip install -r requirements.txt
```

## Edit (notebook)

```
env/bin/jupyter notebook tg_ff.ipynb
# edits are autosaved to the plain text version.
```

## Edit (plain text)

```
$EDITOR tg_ff.py
env/bin/jupytext --sync tg_ff.ipynb
# or just reload the jupyter notebook tab if opened.
```
