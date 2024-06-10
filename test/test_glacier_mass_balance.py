import pytest
from src.glacier_mass_balance import melt, accumulate, lapse, net_balance_fn, glacier_net_balance_fn
from src.utils import make_sha_filename
import numpy as np
from pathlib import Path

# Test `melt` function
def test_melt():
    assert melt(0, 1) == 0
    assert melt(-10, 1) == 0
    assert melt(1, 1) == 1
    assert melt(4, 7) == 4 * 7
    melt_factor = 0.005
    assert melt(4, melt_factor) == 4 * melt_factor

# Test `accumulate` function
def test_accumulate():
    assert accumulate(0, 5, 4) > 0
    assert accumulate(5, 5, 4) == 0

# Test `lapse` function
def test_lapse():
    assert lapse(5, 100, 1) > 5
    assert lapse(5, -100, 1) < 5

# Test example from `simple.jl`
def test_example_smb():
    with open(Path(__file__).parent / "../examples/simple.py", "r") as file:
        loc = {}
        exec(file.read(), None, loc)    
        assert np.isclose(loc["glacier_net_balance"], -0.11063311845641427)  # Use actual expected value

# Test `make_sha_filename` function from `utils.py`
def test_make_sha_filename():
    filename = make_sha_filename("test", ".png")
    assert filename.startswith("test-")
    assert filename.endswith(".png")
