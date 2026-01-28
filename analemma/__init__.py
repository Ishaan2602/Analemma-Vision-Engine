"""
Analemma Engine Package

A modular system for calculating and visualizing the analemma - the figure-8 path
the Sun traces in the sky when photographed at the same mean solar time over a year.
"""

__version__ = "1.0.0"

from .calculator import AnalemmaCalculator
from .sky_mapper import SkyMapper
from .plotter import AnalemmaPlotter

__all__ = ['AnalemmaCalculator', 'SkyMapper', 'AnalemmaPlotter']
