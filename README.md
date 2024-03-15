# cascadef

## Developer Setup

### Installing and using PDM:

PDM is a package manager for python and it builds a virtual environment so
we can all use the same python packages.

```bash
pip install pdm
```

Then in the root of this project run

```bash
pdm install
```

An option in vscode should pop up to add an environment. Click that and choose the one with
".venv". If it does not show up try restarting vscode 

It gives us useful stuff like

```bash
pdm add matplotlib
```

And it will automatically add matplotlib to the teams environment, at least after the git changes are uploaded.

### Testing

If pdm was installed correctly you should be able to run

```bash
pytest
```

which will run all of the tests in the tests/ directory