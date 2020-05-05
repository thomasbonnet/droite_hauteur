import pytest
from calcul_droite import *
from units import *

#TODO : case pour l'hemisphère sud

def test_calc_declinaison_for_days():
    to_be_tested = [
        # year, month, day, result
        (2020, 4, 13, (pytest.approx(179.8637*degrees), pytest.approx(9.135786*degrees))),
        (1998, 3, 4, (pytest.approx(177.0311*degrees), pytest.approx(-6.599075*degrees))),
    ]

    for row in to_be_tested:
        result = calc_sun_ephemerides(row[0], row[1], row[2])
        assert result == row[3]


def test_calc_declinaison_for_hours():
    to_be_tested = [
        # year, month, day, result
        (2020, 4, 13, 14, 44, 18, (pytest.approx(40.977315*degrees), pytest.approx(9.357577*degrees))),
        (1998, 3, 4, 15, 24, 4, (pytest.approx(48.08246*degrees), pytest.approx(-6.352139*degrees))),
        (2020, 1, 10, 14, 44, 18, (pytest.approx(39.235732*degrees), pytest.approx(-21.974566*degrees))),
       # (2020, 4, 25, 15, 49, 22, (pytest.approx(57.8781*degrees, rel=1e-3), pytest.approx(13,484444*degrees, rel=1e-3)))
    ]

    for row in to_be_tested:
        result = calc_sun_ephemerides(row[0], row[1], row[2], row[3], row[4], row[5])
        assert result == row[6]


def test_to_decimal_degrees():
    to_be_tested = [
        (math.pi, 180),
        (0, 0),
        (2*math.pi, 360),
        (-math.pi/2., -90)
    ]
    for row in to_be_tested:
        result = radian_to_decimal_degrees(row[0])
        assert result == row[1]


def test_decimal_degrees_to_degrees_min_AH():
    to_be_tested = [
        (3.5*degrees, (3, 30)),
        (50.25*degrees, (50, 15)),
        (182.75*degrees, (182, 45)),
        (179.8637*degrees,(179, 51.8)),
        (177.0311*degrees,(177, 1.9)),
        (40.977315*degrees,(40, 58.6)),
        (48.08246*degrees,(48, 4.9)),
        (39.235732*degrees,(39, 14.1)),
    ]
    for row in to_be_tested:
        result = angle_to_degrees_min(row[0], format="AH")
        assert result == row[1]


def test_decimal_degrees_to_degrees_min_Dec():
    to_be_tested = [
        (-85.5*degrees, (-85, 30)),
        (50.25*degrees, (50, 15)),
        (9.135786*degrees, (9, 8.1)),
        (-6.599075*degrees, (-6, 35.9)),
        (9.357577*degrees, (9, 21.5)),
        (-6.352139*degrees, (-6, 21.1)),
        (-21.974566*degrees,(-21, 58.5)),
    ]
    for row in to_be_tested:
        result = angle_to_degrees_min(row[0], format="Dec")
        assert result == row[1]

def test_degrees_minutes_to_decimal_degrees():
    to_be_tested = [
        ((45, 30), 45.5),
        ((50, 15), 50.25),
    ]
    for row in to_be_tested:
        result = degrees_minutes_to_decimal_degrees(*row[0])
        assert result == row[1]

def test_degrees_minutes_secondes_to_decimal_degrees():
    to_be_tested = [
        ((45, 30, 30), pytest.approx(45.50833)),
        ((50, 15, 15), pytest.approx(50.25416)),
    ]
    for row in to_be_tested:
        result = degrees_minutes_to_decimal_degrees(*row[0])
        assert result == row[1]

def test_calc_hc():
    #Declinaison:float, AHl:float, EstimatedLatitude:float
    to_be_tested = [
        (-6.353582222*degrees,45.1958022*degrees,47*degrees+29*minutes,pytest.approx(23.06262309*degrees)),
        (13*degrees+29*minutes+4*seconds,52.54477*degrees,45*degrees+51*minutes,pytest.approx(35*degrees+23*minutes, rel=1e-3)) 
    ]
    for row in to_be_tested:
        result = calc_hc(row[0],row[1],row[2])
        assert result == row[3]

def test_calc_Z():
    #Declinaison:float,AHl:float, EstimatedLatitude:float, CalculatedHeigth:float
    to_be_tested = [
       # (-6.353582222*degrees,45.1958022*degrees,47*degrees+29*minutes,23.06262309*degrees,pytest.approx(129.9669419*degrees)), 
        (13*degrees+29*minutes+4*seconds,52.54477*degrees,45*degrees+51*minutes,35*degrees+23*minutes,pytest.approx(251.26*degrees,rel=1e-3)),
        (13*degrees+20*minutes+59*seconds,262.5279*degrees, 45*degrees+51*minutes,4*degrees+26*minutes,pytest.approx(75.38*degrees, rel=1e-3))
    ]
    for row in to_be_tested:
        result = calc_Z(row[0],row[1],row[2],row[3])
        assert result == row[4]

def test_calc_AHl():
    #AHvo:float,EstimatedLongitude:float
    to_be_tested = [
        (408.0791356*degrees,-(2*degrees+53*minutes),pytest.approx(45.1958022*degrees)),
        (28*degrees+58.35*minutes,-(5*degrees+30*minutes),pytest.approx(23*degrees+28.35*minutes)),
        (57.8781*degrees,-(5*degrees+20*minutes),pytest.approx(52.54477*degrees))
        
    ]
    for row in to_be_tested:
        result = calc_AHl(row[0],row[1])
        assert result == row[2]


def test_calcul_droite():
    date = dt.datetime(2020, 4, 24, 15, 45, 30)
    Ge = (45, 30)
    Le = (-12, 56)

    calc_droite(date, Ge, Le)