[![Tests](https://github.com/vboussange/rere/actions/workflows/runtest.yml/badge.svg)](https://github.com/vboussange/rere/actions/workflows/runtest.yml)

# A glacier melt model applied to Breithorngletscher (Zermatt, Switzerland) to learn about reproducible research practices

This an example code repository going along with the workshop https://github.com/mauro3/CORDS/tree/master/Workshop-Reproducible-Research

## Mass balance model

- The melt model is a simple temperature index melt model.
- Temperature lapses with a linear function.
- Precipitation is from measurements and a threshold temperature determines whether it is snow.

The main function is `glacier_net_balance_fn` which returns:
- the glacier net balance [m] (i.e. how much volume was gained or lost
  over the time period)
- net balance at all points [m] (i.e. how much volume was gained or
  lost at each grid cell)


## Data

- measured temperature (operated by VAW-LG in 2007) from a met-station near Breithorngletscher is used
- digital elevation model is the DHM200 of swisstopo
- mask is derived from outlines of the Swiss Glacier Inventory (however, we pretend that we digitised that outline ourselves)

Data is located at https://raw.githubusercontent.com/mauro3/CORDS/master/data/workshop-reproducible-research


## Installation
- first install `minimamba`
- `mamba env create --prefix ./.env --file environment.yml --force`
- `mamba activate ./.env`
- `pip install -e .`
- `python examples/simple.py`