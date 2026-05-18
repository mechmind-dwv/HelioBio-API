"""Datos históricos de ciclos solares verificados"""
import pandas as pd
import math

SOLAR_CYCLES_DATA = [
    {"cycle": 1, "start": 1755, "end": 1766, "duration": 11.3, "max_ssn": 86.5, "min_ssn": 5.2},
    {"cycle": 2, "start": 1766, "end": 1775, "duration": 9.0, "max_ssn": 115.8, "min_ssn": 3.1},
    {"cycle": 3, "start": 1775, "end": 1784, "duration": 9.3, "max_ssn": 158.5, "min_ssn": 9.5},
    {"cycle": 4, "start": 1784, "end": 1798, "duration": 13.6, "max_ssn": 141.2, "min_ssn": 3.2},
    {"cycle": 5, "start": 1798, "end": 1810, "duration": 12.4, "max_ssn": 49.2, "min_ssn": 0.0},
    {"cycle": 6, "start": 1810, "end": 1823, "duration": 12.8, "max_ssn": 48.7, "min_ssn": 0.1},
    {"cycle": 7, "start": 1823, "end": 1833, "duration": 10.5, "max_ssn": 71.5, "min_ssn": 7.3},
    {"cycle": 8, "start": 1833, "end": 1843, "duration": 9.7, "max_ssn": 146.9, "min_ssn": 10.6},
    {"cycle": 9, "start": 1843, "end": 1855, "duration": 12.5, "max_ssn": 131.9, "min_ssn": 3.2},
    {"cycle": 10, "start": 1855, "end": 1867, "duration": 11.3, "max_ssn": 98.0, "min_ssn": 5.2},
    {"cycle": 11, "start": 1867, "end": 1878, "duration": 11.8, "max_ssn": 140.3, "min_ssn": 2.2},
    {"cycle": 12, "start": 1878, "end": 1890, "duration": 11.3, "max_ssn": 74.6, "min_ssn": 5.0},
    {"cycle": 13, "start": 1890, "end": 1902, "duration": 12.1, "max_ssn": 87.9, "min_ssn": 2.7},
    {"cycle": 14, "start": 1902, "end": 1913, "duration": 11.5, "max_ssn": 64.2, "min_ssn": 1.5},
    {"cycle": 15, "start": 1913, "end": 1923, "duration": 10.0, "max_ssn": 105.4, "min_ssn": 5.6},
    {"cycle": 16, "start": 1923, "end": 1933, "duration": 10.1, "max_ssn": 78.1, "min_ssn": 3.5},
    {"cycle": 17, "start": 1933, "end": 1944, "duration": 10.4, "max_ssn": 119.2, "min_ssn": 7.7},
    {"cycle": 18, "start": 1944, "end": 1954, "duration": 10.2, "max_ssn": 151.8, "min_ssn": 3.4},
    {"cycle": 19, "start": 1954, "end": 1964, "duration": 10.5, "max_ssn": 201.3, "min_ssn": 9.6},
    {"cycle": 20, "start": 1964, "end": 1976, "duration": 11.7, "max_ssn": 110.6, "min_ssn": 12.2},
    {"cycle": 21, "start": 1976, "end": 1986, "duration": 10.3, "max_ssn": 164.5, "min_ssn": 12.3},
    {"cycle": 22, "start": 1986, "end": 1996, "duration": 10.0, "max_ssn": 158.5, "min_ssn": 8.0},
    {"cycle": 23, "start": 1996, "end": 2008, "duration": 12.2, "max_ssn": 120.8, "min_ssn": 1.7},
    {"cycle": 24, "start": 2008, "end": 2019, "duration": 11.0, "max_ssn": 81.8, "min_ssn": 2.2},
    {"cycle": 25, "start": 2019, "end": 0, "duration": 0.0, "max_ssn": 125.0, "min_ssn": 0.0},
]

def get_solar_cycles_data():
    df = pd.DataFrame(SOLAR_CYCLES_DATA)
    # Reemplazar NaN/None con 0 para JSON
    df = df.fillna(0).replace([float('inf'), float('-inf')], 0)
    return df
