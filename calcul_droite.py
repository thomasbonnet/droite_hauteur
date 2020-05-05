import math
import ephem
import datetime as dt

from units import *


def nadeg(rad, fixedwidth=1):
    # changes ephem.angle (rad) to the format usually used in the nautical almanac (ddd°mm.m) and returns a string object.
	# the optional argument specifies the minimum width for degrees (only)
    theminus = ""
    if rad < 0:
    	theminus = '-'
    df = abs(math.degrees(rad))	# convert radians to degrees (float)
    di = int(df)			# degrees (integer)
    # note: round() uses "Rounding Half To Even" strategy
    mf = round((df-di)*60, 1)	# minutes (float), rounded to 1 decimal place
    mi = int(mf)			# minutes (integer)
    if mi == 60:
        mf -= 60
        di += 1
        if di == 360:
            di = 0
    if fixedwidth == 2:
        gm = "{}{:02d}$^\circ${:04.1f}".format(theminus,di,mf)
    else:
        if fixedwidth == 3:
            gm = "{}{:03d}$^\circ${:04.1f}".format(theminus,di,mf)
        else:
            gm = "{}{}$^\circ${:04.1f}".format(theminus,di,mf)
    return gm


def degrees_minutes_to_decimal_degrees(degrees:int, minutes: float, secondes: float=0) -> float:
    return degrees + minutes/60.+ secondes/3600


def radian_to_decimal_degrees(angle_radians: float) -> float:
    return math.degrees(angle_radians)


def angle_to_degrees_min(angle: float, format: str) -> (int, float):
    integer_degrees = int(angle/degrees)
    integer_minutes = round(abs(angle/degrees - integer_degrees)*60, 1)
    if format == "AH":
        integer_degrees = integer_degrees%360

    return (integer_degrees, integer_minutes)


def calc_sun_ephemerides(year, month, day, hour=0, minutes=0, seconds=0):
    date = ephem.date(dt.datetime(year, month, day, hour, minutes, seconds))
    ephem_sun = ephem.Sun()

    obs = ephem.Observer()
    obs.date = date
    
    #Sun
    ephem_sun.compute(date,epoch=date)
    AHvo = ephem.degrees(obs.sidereal_time()-ephem_sun.g_ra).norm
    Dec = ephem_sun.g_dec
    return AHvo, Dec


def calc_AHl(AHvo:float,EstimatedLongitude:float)-> float:
    AHl = AHvo+EstimatedLongitude
    while AHl>360*degrees:
        AHl = AHl-360*degrees
    while AHl<0:
        AHl = AHl+360*degrees
    return AHl


def calc_hc(Declinaison:float, AHl:float, EstimatedLatitude:float)-> float:
    return math.asin(math.sin(Declinaison/radians)*math.sin(EstimatedLatitude/radians) + 
    math.cos(Declinaison/radians)*math.cos(AHl/radians)*math.cos(EstimatedLatitude/radians))

def calc_Z(Declinaison:float,AHl:float, EstimatedLatitude:float, CalculatedHeigth:float)-> float:
    Z = math.acos((math.sin(Declinaison/radians)- math.sin(EstimatedLatitude/radians)*math.sin(CalculatedHeigth/radians)) 
    /(math.cos(EstimatedLatitude/radians)*math.cos(CalculatedHeigth/radians)))
    #Z = 180*degrees+math.atan(math.sin(AHl/radians)/
    #((math.cos(AHl)*math.sin(EstimatedLatitude/radians))-(math.tan(Declinaison/radians)*math.cos(EstimatedLatitude/radians))))
    if AHl<180*degrees:
        Z=360*degrees-Z

    return Z

def calc_droite(date: dt.datetime, Ge_deg_min: (str, int, float), Le_deg_min: (str, int, float)):
    
    signe = -1 if Ge_deg_min[1] == 'W'else 1 
    Ge = signe * (Ge_deg_min[1] * degrees + Ge_deg_min[2] * minutes)
    
    signe = -1 if Le_deg_min[1] == 'S'else 1
    Le = signe * (Le_deg_min[1] * degrees + Le_deg_min[2] * minutes)

    AHvo, Dec = calc_sun_ephemerides(date.year, date.month, date.day, 
                                     date.hour, date.minute, date.second)

    AHl = calc_AHl(AHvo, Ge)

    Hc = calc_hc(Dec, AHl, Le)
    Z = calc_Z(Dec, AHl, Le, Hc)

    return (Hc/degrees, Z/degrees)
