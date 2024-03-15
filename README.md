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

### The project structure

my_project/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── data_processing.py
│   │   └── helpers.py
│   └── models/
│       ├── __init__.py
│       ├── model_a.py
│       └── model_b.py
├── tests/
│   ├── __init__.py
│   ├── test_data_processing.py
│   └── test_models.py
├── data/
│   ├── raw/
│   │   └── dataset.csv
│   └── processed/
│       └── cleaned_dataset.csv
├── docs/
│   ├── README.md
│   └── api_documentation.md
├── requirements.txt
├── setup.py
└── .gitignore