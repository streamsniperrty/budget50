import pytest
from project import assets, paycheckCalculator, longTermGoal
import pandas as pd

df = pd.read_csv('mybudget.csv')

def test_assets():
    assert(assets()) == df.to_string(index=False)

def test_paycheckCalculator():
    assert paycheckCalculator(1000) == (425.0, 255.0, 170.0)
    assert paycheckCalculator(0) == (0.0, 0.0, 0.0)
    assert paycheckCalculator(100) == (42.5, 25.5, 17.0)
    assert paycheckCalculator(10000) == (4250.0, 2550.0, 1700.0)
    assert paycheckCalculator(-1000) == (-425.0, -255.0, -170.0)

def test_longTermGoal():
    assert longTermGoal(1200, 100) == 12.0
    assert longTermGoal(1250, 100) == 12.5
    assert longTermGoal(50, 10) == 5.0
    assert longTermGoal(10000, 500) == 20.0

    assert longTermGoal(0, 100) == 0.0

    with pytest.raises(ZeroDivisionError):
        longTermGoal(1000, 0)
