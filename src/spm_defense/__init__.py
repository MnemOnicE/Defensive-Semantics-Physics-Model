"""
SPM Defense Module
"""

from .tokenization import HyperToken
from .models import SPMSignal, RhetoricalForceVector
from .agents import MonitorAgent
from .calculations import (
    estimate_semantic_mass_proxy,
    calculate_force_vector,
    calculate_ethos_coefficient,
    calculate_semantic_acceleration
)

__all__ = [
    "HyperToken",
    "SPMSignal",
    "RhetoricalForceVector",
    "MonitorAgent",
    "estimate_semantic_mass_proxy",
    "calculate_force_vector",
    "calculate_ethos_coefficient",
    "calculate_semantic_acceleration"
]
