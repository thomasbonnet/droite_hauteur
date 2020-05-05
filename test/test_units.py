import pytest
import math
from units import *

def test_angle_units():
    assert 180 * degrees == math.pi * radians
    assert 60 * minutes == 1 * degrees
    assert 60 * seconds == 1 * minutes
    assert 15*degrees + 30*minutes == 15.5*degrees