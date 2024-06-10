[![.github/workflows/runtest.yml](https://github.com/vboussange/rere/actions/workflows/runtest.yml/badge.svg)](https://github.com/vboussange/rere/actions/workflows/runtest.yml)

```
rere/
├── src/ # contains model and reusable functions
│   ├── __init__.py
│   ├── glacier_mass_balance.py
│   ├── utils.py
│   └── data.py
├── scripts/
│   └── real_glacier.py
├── examples/
│   └── simple.py
├── test/
│   └── test_glacier_mass_balance.py
├── setup.py
└── environment.yml
```

## install
- first install `minimamba`
- `mamba env create --prefix ./.env --file environment.yml --force`
- `mamba activate ./.env`
- `pip install -e .`
- `python examples/simple.py`