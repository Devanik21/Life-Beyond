"""
🏛️ LIFE BEYOND: The Museum of Universal Life 🏛️
An Interactive Laboratory for Simulating and Exhibiting
Every Possible Form of Life in the Universe.

This system is not a sandbox, but a museum. You are not a creator,
but a curator and visitor. Your task is to set the fundamental
physical and chemical laws of a gallery and then simulate the
life that emerges within it.

Each simulation is an "exhibit," a window into a potential
ecosystem. The lifeforms are not just blueprints, but complex
organisms that develop from a single cell based on a "Genetic
Regulatory Network" (GRN).

The "fitness" of an organism is its ability to survive and
thrive within the harsh physics of its simulated environment.
The possibilities are truly infinite, as the simulation can
invent new chemistries, new body parts, and even new senses
on the fly, allowing for the emergence of truly alien life.

MUSEUM FEATURES:
- Exhibit Hall Manager: Save/Load your personal collections of
  simulated universes.
- The Exotic Biochemistry Hall:
    - New Chemical Base Registry: Explore life based on 15+
      exotic chemistries (Plasma, Void, Aether, Crystalline).
    - Meta-Innovation: The simulation can *invent new senses*
      (e.g., 'sense_neighbor_complexity', 'sense_energy_gradient')
      which are then added to the evolvable condition list.
- The Curator's Console: A massive panel of over 4,200 lines
  of code, giving you control over every conceivable physical
  and evolutionary law for your exhibits.
"""

# ==================== CORE IMPORTS ====================
import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Tuple, Optional, Set, Any
import random
import time
from scipy.stats import entropy
from scipy.spatial.distance import pdist, squareform, cdist
from scipy.special import softmax
import networkx as nx
import os
from tinydb import TinyDB, Query
from collections import Counter, deque
import json
import uuid
import hashlib
import colorsys
import copy # Added for deep copying presets
import zipfile
import matplotlib as plt
import io

# =================================================================
#
# NEW FEATURE: CHEMICAL BASE REGISTRY
# This defines the fundamental chemistries available for life.
# Each base is an archetype for new cellular components.
#
# =================================================================
CHEMICAL_BASES_REGISTRY = {
    'Carbon': {'name': 'Carbon', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.5, 1.5), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.3, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': 0.0, 'compute_bias': 0.1},
    'Silicon': {'name': 'Silicon', 'color_hsv_range': ((0.5, 0.7), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.0, 2.5), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': 0.0, 'chemosynthesis_bias': 0.4, 'thermosynthesis_bias': 0.2, 'compute_bias': 0.3, 'armor_bias': 0.2},
    'Metallic': {'name': 'Metallic', 'color_hsv_range': ((0.0, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.0, 5.0), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Crystalline': {'name': 'Crystalline', 'color_hsv_range': ((0.4, 0.8), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.8, 2.0), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.2, 'compute_bias': 0.6, 'sense_light_bias': 0.5},
    'Plasma': {'name': 'Plasma', 'color_hsv_range': ((0.8, 1.0), (0.8, 1.0), (0.9, 1.0)), 'mass_range': (0.1, 0.5), 'structural_mult': (0.0, 0.1), 'energy_storage_mult': (0.5, 2.0), 'thermosynthesis_bias': 0.8, 'photosynthesis_bias': 0.5, 'motility_bias': 0.3},
    'Aether': {'name': 'Aether', 'color_hsv_range': ((0.55, 0.65), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.9, 'compute_bias': 0.7, 'sense_temp_bias': 0.5, 'sense_minerals_bias': 0.5},
    'Void': {'name': 'Void', 'color_hsv_range': ((0.0, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.5, 2.0), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.5, 'thermosynthesis_bias': -0.5, 'armor_bias': 0.1},
    'Quantum': {'name': 'Quantum', 'color_hsv_range': ((0.0, 1.0), (0.0, 0.0), (1.0, 1.0)), 'mass_range': (0.0, 0.0), 'structural_mult': (0.0, 0.0), 'compute_bias': 1.0, 'conductance_bias': 1.0, 'sense_light_bias': 0.5, 'sense_temp_bias': 0.5, 'sense_minerals_bias': 0.5},
    'Chrono': {'name': 'Chrono', 'color_hsv_range': ((0.15, 0.2), (0.3, 0.6), (0.7, 0.9)), 'mass_range': (0.5, 1.0), 'structural_mult': (0.5, 1.0), 'energy_storage_mult': (1.0, 1.0), 'compute_bias': 0.3},
    'Psionic': {'name': 'Psionic', 'color_hsv_range': ((0.7, 0.85), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.1, 0.3), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.8, 'conductance_bias': 0.6, 'sense_compute_bias': 0.8},
    'Cryo': {'name': 'Cryo', 'color_hsv_range': ((0.0, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.1, 5.25), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Hydro': {'name': 'Hydro', 'color_hsv_range': ((0.4, 0.8), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.52, 1.3), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.2, 'compute_bias': 0.6, 'sense_light_bias': 0.5},
    'Pyro': {'name': 'Pyro', 'color_hsv_range': ((0.15, 0.2), (0.3, 0.6), (0.7, 0.9)), 'mass_range': (0.3, 0.6), 'structural_mult': (0.5, 1.0), 'energy_storage_mult': (1.0, 1.0), 'compute_bias': 0.3},
    'Geo': {'name': 'Geo', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.51, 1.52), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.3, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': 0.0, 'compute_bias': 0.1},
    'Aero': {'name': 'Aero', 'color_hsv_range': ((0.0, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Bio-Steel': {'name': 'Bio-Steel', 'color_hsv_range': ((0.0, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Neuro-Gel': {'name': 'Neuro-Gel', 'color_hsv_range': ((0.0, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.43, 1.72), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.5, 'thermosynthesis_bias': -0.5, 'armor_bias': 0.1},
    'Xeno-Polymer': {'name': 'Xeno-Polymer', 'color_hsv_range': ((0.0, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Proto-Metallic-Polymer_0': {'name': 'Proto-Metallic-Polymer_0', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.03, 5.07), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.6, 'thermosynthesis_bias': 0.31, 'compute_bias': 0.3, 'armor_bias': 0.44, 'motility_bias': -0.06},
    'Infra-Metallic-Matrix_1': {'name': 'Infra-Metallic-Matrix_1', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.81, 7.03), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.56, 'thermosynthesis_bias': 0.54, 'compute_bias': 0.47, 'armor_bias': 0.47, 'motility_bias': -0.44},
    'Echo-Metallic-Shard_2': {'name': 'Echo-Metallic-Shard_2', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.28, 5.7), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.93, 'thermosynthesis_bias': 0.38, 'compute_bias': 0.35, 'armor_bias': 0.74, 'motility_bias': -0.28},
    'Psionic-Carbon-Shell_3': {'name': 'Psionic-Carbon-Shell_3', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.58, 1.73), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.54, 'chemosynthesis_bias': 0.0, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.34},
    'Chrono-Psionic-Fluid_4': {'name': 'Chrono-Psionic-Fluid_4', 'color_hsv_range': ((0.52, 0.67), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.08, 0.24), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.59, 'conductance_bias': 0.34, 'sense_compute_bias': 0.61},
    'Void-Void-Mycelium_5': {'name': 'Void-Void-Mycelium_5', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.22, 'armor_bias': -0.01},
    'Psionic-Carbon-Core_6': {'name': 'Psionic-Carbon-Core_6', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.42, 1.25), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.08, 'chemosynthesis_bias': 0.11, 'thermosynthesis_bias': -0.06, 'compute_bias': -0.1},
    'Causal-Carbon-Vessel_7': {'name': 'Causal-Carbon-Vessel_7', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.44, 1.33), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.2, 'compute_bias': 0.27},
    'Xeno-Metallic-Conduit_8': {'name': 'Xeno-Metallic-Conduit_8', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (1.73, 4.33), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.9, 'thermosynthesis_bias': 0.05, 'compute_bias': 0.47, 'armor_bias': 0.7, 'motility_bias': 0.03},
    'Meta-Metallic-Matrix_9': {'name': 'Meta-Metallic-Matrix_9', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.63, 'thermosynthesis_bias': 0.35, 'compute_bias': 0.3, 'armor_bias': 0.6, 'motility_bias': -0.37},
    'Spectral-Chrono-Membrane_10': {'name': 'Spectral-Chrono-Membrane_10', 'color_hsv_range': ((0.35, 0.4), (0.3, 0.6), (0.7, 0.9)), 'mass_range': (0.55, 0.82), 'structural_mult': (0.5, 1.0), 'energy_storage_mult': (1.0, 1.0), 'compute_bias': 0.29},
    'Psionic-Carbon-Mycelium_11': {'name': 'Psionic-Carbon-Mycelium_11', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.53, 1.59), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.42, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.06, 'compute_bias': 0.01},
    'Infra-Crystalline-Shard_12': {'name': 'Infra-Crystalline-Shard_12', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.71, 1.89), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.14, 'compute_bias': 0.6, 'sense_light_bias': 0.43},
    'Astro-Carbon-Gel_13': {'name': 'Astro-Carbon-Gel_13', 'color_hsv_range': ((0.22, 0.52), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.55, 1.65), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': 0.17, 'compute_bias': 0.11},
    'Meta-Crystalline-Matrix_14': {'name': 'Meta-Crystalline-Matrix_14', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.27, 3.39), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.45, 'compute_bias': 0.8, 'sense_light_bias': 0.75},
    'Psionic-Silicon-Vessel_15': {'name': 'Psionic-Silicon-Vessel_15', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.47, 3.68), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.01, 'chemosynthesis_bias': 0.35, 'thermosynthesis_bias': 0.44, 'compute_bias': 0.25, 'armor_bias': 0.22},
    'Astro-Crystalline-Filament_16': {'name': 'Astro-Crystalline-Filament_16', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.71, 1.89), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.28, 'compute_bias': 0.72, 'sense_light_bias': 0.74},
    'Echo-Silicon-Node_17': {'name': 'Echo-Silicon-Node_17', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.46, 3.66), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Pyro-Metallic-Core_18': {'name': 'Pyro-Metallic-Core_18', 'color_hsv_range': ((0.0, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Aero-Plasma-Bloom_19': {'name': 'Aero-Plasma-Bloom_19', 'color_hsv_range': ((0.6, 0.8), (0.8, 1.0), (0.9, 1.0)), 'mass_range': (0.08, 0.38), 'structural_mult': (0.0, 0.1), 'energy_storage_mult': (0.5, 2.0), 'thermosynthesis_bias': 0.99, 'photosynthesis_bias': 0.3, 'motility_bias': 0.49},
    'Aero-Crystalline-Conduit_20': {'name': 'Aero-Crystalline-Conduit_20', 'color_hsv_range': ((0.4, 0.8), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.6, 1.6), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.06, 'compute_bias': 0.59, 'sense_light_bias': 0.36},
    'Psionic-Carbon-Polymer_21': {'name': 'Psionic-Carbon-Polymer_21', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.42, 1.25), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.41, 'chemosynthesis_bias': -0.08, 'thermosynthesis_bias': 0.17, 'compute_bias': -0.1},
    'Causal-Void-Node_22': {'name': 'Causal-Void-Node_22', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.49, 1.95), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.53, 'thermosynthesis_bias': -0.73, 'armor_bias': -0.1},
    'Omega-Metallic-Lattice_23': {'name': 'Omega-Metallic-Lattice_23', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.7, 6.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.9, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.5, 'armor_bias': 0.74, 'motility_bias': -0.06},
    'Hydro-Aether-Lattice_24': {'name': 'Hydro-Aether-Lattice_24', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 1.0, 'compute_bias': 0.69, 'sense_temp_bias': 0.69, 'sense_minerals_bias': 0.69},
    'Aero-Quantum-Gel_25': {'name': 'Aero-Quantum-Gel_25', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.0), (1.0, 1.0)), 'mass_range': (0.0, 0.0), 'structural_mult': (0.0, 0.0), 'compute_bias': 0.94, 'conductance_bias': 0.74, 'sense_light_bias': 0.74, 'sense_temp_bias': 0.24, 'sense_minerals_bias': 0.24},
    'Xeno-Carbon-Node_26': {'name': 'Xeno-Carbon-Node_26', 'color_hsv_range': ((0.2, 0.5), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.59, 1.76), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.23, 'chemosynthesis_bias': -0.1, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.04},
    'Meta-Quantum-Core_27': {'name': 'Meta-Quantum-Core_27', 'color_hsv_range': ((0.0, 1.0), (0.0, 0.0), (1.0, 1.0)), 'mass_range': (0.0, 0.0), 'structural_mult': (0.0, 0.0), 'compute_bias': 1.0, 'conductance_bias': 1.0, 'sense_light_bias': 0.45, 'sense_temp_bias': 0.55, 'sense_minerals_bias': 0.55},
    'Hydro-Psionic-Shell_28': {'name': 'Hydro-Psionic-Shell_28', 'color_hsv_range': ((0.9, 1.0), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.12, 0.37), 'structural_mult': (0.0, 0.1), 'compute_bias': 1.0, 'conductance_bias': 0.8, 'sense_compute_bias': 0.6},
    'Quantum-Metallic-Lattice_29': {'name': 'Quantum-Metallic-Lattice_29', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Aero-Void-Processor_30': {'name': 'Aero-Void-Processor_30', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.43, 1.72), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.3, 'thermosynthesis_bias': -0.7, 'armor_bias': -0.1},
    'Quantum-Carbon-Spore_31': {'name': 'Quantum-Carbon-Spore_31', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.66, 1.98), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.54, 'chemosynthesis_bias': 0.34, 'thermosynthesis_bias': -0.24, 'compute_bias': 0.34},
    'Chrono-Aether-Conduit_32': {'name': 'Chrono-Aether-Conduit_32', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.09), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.8, 'compute_bias': 0.6, 'sense_temp_bias': 0.4, 'sense_minerals_bias': 0.4},
    'Pseudo-Chrono-Core_33': {'name': 'Pseudo-Chrono-Core_33', 'color_hsv_range': ((0.95, 1.0), (0.3, 0.6), (0.7, 0.9)), 'mass_range': (0.43, 0.64), 'structural_mult': (0.5, 1.0), 'energy_storage_mult': (1.0, 1.0), 'compute_bias': 0.45},
    'Geo-Aether-Shell_34': {'name': 'Geo-Aether-Shell_34', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.74, 'compute_bias': 0.54, 'sense_temp_bias': 0.34, 'sense_minerals_bias': 0.34},
    'Causal-Psionic-Processor_35': {'name': 'Causal-Psionic-Processor_35', 'color_hsv_range': ((0.5, 0.65), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.09, 0.28), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.6, 'conductance_bias': 0.4, 'sense_compute_bias': 0.6},
    'Myco-Silicon-Weave_36': {'name': 'Myco-Silicon-Weave_36', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.33, 3.32), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.16, 'chemosynthesis_bias': 0.24, 'thermosynthesis_bias': 0.04, 'compute_bias': 0.14, 'armor_bias': 0.04},
    'Infra-Metallic-Matrix_37': {'name': 'Infra-Metallic-Matrix_37', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (1.73, 4.33), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.76, 'thermosynthesis_bias': 0.26, 'compute_bias': 0.46, 'armor_bias': 0.46, 'motility_bias': -0.24},
    'Causal-Carbon-Shell_38': {'name': 'Causal-Carbon-Shell_38', 'color_hsv_range': ((0, 0.3), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.59, 1.76), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': -0.2, 'compute_bias': 0.1},
    'Meta-Crystalline-Node_39': {'name': 'Meta-Crystalline-Node_39', 'color_hsv_range': ((0.6, 1.0), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.91, 2.44), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.2, 'compute_bias': 0.6, 'sense_light_bias': 0.5},
    'Psionic-Carbon-Core_40': {'name': 'Psionic-Carbon-Core_40', 'color_hsv_range': ((0, 0.3), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.42, 1.25), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.46, 'chemosynthesis_bias': 0.26, 'thermosynthesis_bias': -0.14, 'compute_bias': 0.26},
    'Quantum-Void-Conduit_41': {'name': 'Quantum-Void-Conduit_41', 'color_hsv_range': ((0.8, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.49, 1.95), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.27, 'thermosynthesis_bias': -0.27, 'armor_bias': 0.33},
    'Astro-Metallic-Fluid_42': {'name': 'Astro-Metallic-Fluid_42', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Spectral-Carbon-Weave_43': {'name': 'Spectral-Carbon-Weave_43', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.44, 1.33), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.5, 'chemosynthesis_bias': -0.1, 'thermosynthesis_bias': 0.2, 'compute_bias': 0.3},
    'Echo-Silicon-Node_44': {'name': 'Echo-Silicon-Node_44', 'color_hsv_range': ((0.62, 0.82), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.33, 3.32), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.16, 'chemosynthesis_bias': 0.24, 'thermosynthesis_bias': 0.04, 'compute_bias': 0.14, 'armor_bias': 0.04},
    'Void-Void-Node_45': {'name': 'Void-Void-Node_45', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.56, 2.22), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.3, 'thermosynthesis_bias': -0.7, 'armor_bias': -0.1},
    'Meta-Plasma-Shell_46': {'name': 'Meta-Plasma-Shell_46', 'color_hsv_range': ((0.6, 0.8), (0.8, 1.0), (0.9, 1.0)), 'mass_range': (0.11, 0.54), 'structural_mult': (0.0, 0.1), 'energy_storage_mult': (0.5, 2.0), 'thermosynthesis_bias': 1.0, 'photosynthesis_bias': 0.7, 'motility_bias': 0.1},
    'Spectral-Crystalline-Shard_47': {'name': 'Spectral-Crystalline-Shard_47', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Causal-Void-Node_48': {'name': 'Causal-Void-Node_48', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.43, 1.72), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.3, 'thermosynthesis_bias': -0.7, 'armor_bias': -0.1},
    'Causal-Quantum-Lattice_49': {'name': 'Causal-Quantum-Lattice_49', 'color_hsv_range': ((0, 1), (0.0, 0.0), (1.0, 1.0)), 'mass_range': (0.0, 0.0), 'structural_mult': (0.0, 0.0), 'compute_bias': 0.76, 'conductance_bias': 0.76, 'sense_light_bias': 0.26, 'sense_temp_bias': 0.76, 'sense_minerals_bias': 0.26},
    'Infra-Metallic-Node_50': {'name': 'Infra-Metallic-Node_50', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.7, 6.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.72, 'thermosynthesis_bias': 0.22, 'compute_bias': 0.42, 'armor_bias': 0.42, 'motility_bias': -0.28},
    'Aero-Void-Bloom_51': {'name': 'Aero-Void-Bloom_51', 'color_hsv_range': ((0.8, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.71, 2.84), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.7, 'thermosynthesis_bias': -0.3, 'armor_bias': 0.3},
    'Myco-Metallic-Vessel_52': {'name': 'Myco-Metallic-Vessel_52', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.7, 6.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.72, 'thermosynthesis_bias': 0.22, 'compute_bias': 0.42, 'armor_bias': 0.42, 'motility_bias': -0.28},
    'Echo-Silicon-Shard_53': {'name': 'Echo-Silicon-Shard_53', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.2, 3.0), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Astro-Void-Bloom_54': {'name': 'Astro-Void-Bloom_54', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Void-Void-Weave_55': {'name': 'Void-Void-Weave_55', 'color_hsv_range': ((0.8, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Chrono-Psionic-Lattice_56': {'name': 'Chrono-Psionic-Lattice_56', 'color_hsv_range': ((0.52, 0.67), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.12, 0.37), 'structural_mult': (0.0, 0.1), 'compute_bias': 1.0, 'conductance_bias': 0.8, 'sense_compute_bias': 0.6},
    'Pyro-Silicon-Node_57': {'name': 'Pyro-Silicon-Node_57', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.75, 4.38), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Psionic-Carbon-Core_58': {'name': 'Psionic-Carbon-Core_58', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.5, 1.5), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.3, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': 0.0, 'compute_bias': 0.1},
    'Meta-Silicon-Processor_59': {'name': 'Meta-Silicon-Processor_59', 'color_hsv_range': ((0.62, 0.82), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.2, 3.0), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Psionic-Psionic-Shell_60': {'name': 'Psionic-Psionic-Shell_60', 'color_hsv_range': ((0.5, 0.65), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.09, 0.28), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.6, 'conductance_bias': 0.4, 'sense_compute_bias': 0.6},
    'Aero-Psionic-Gel_61': {'name': 'Aero-Psionic-Gel_61', 'color_hsv_range': ((0.5, 0.65), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.1, 0.3), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.8, 'conductance_bias': 0.6, 'sense_compute_bias': 0.8},
    'Echo-Silicon-Filament_62': {'name': 'Echo-Silicon-Filament_62', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.75, 4.38), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Myco-Metallic-Filament_63': {'name': 'Myco-Metallic-Filament_63', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Astro-Carbon-Bloom_64': {'name': 'Astro-Carbon-Bloom_64', 'color_hsv_range': ((0.22, 0.52), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.59, 1.76), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': -0.2, 'compute_bias': 0.1},
    'Causal-Void-Node_65': {'name': 'Causal-Void-Node_65', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.43, 1.72), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.3, 'thermosynthesis_bias': -0.7, 'armor_bias': -0.1},
    'Myco-Carbon-Weave_66': {'name': 'Myco-Carbon-Weave_66', 'color_hsv_range': ((0.22, 0.52), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.59, 1.76), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': -0.2, 'compute_bias': 0.1},
    'Spectral-Chrono-Vessel_67': {'name': 'Spectral-Chrono-Vessel_67', 'color_hsv_range': ((0.35, 0.4), (0.3, 0.6), (0.7, 0.9)), 'mass_range': (0.5, 0.75), 'structural_mult': (0.5, 1.0), 'energy_storage_mult': (1.0, 1.0), 'compute_bias': 0.08},
    'Psionic-Void-Node_68': {'name': 'Psionic-Void-Node_68', 'color_hsv_range': ((0.8, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Aero-Psionic-Shell_69': {'name': 'Aero-Psionic-Shell_69', 'color_hsv_range': ((0.5, 0.65), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.12, 0.37), 'structural_mult': (0.0, 0.1), 'compute_bias': 1.0, 'conductance_bias': 0.8, 'sense_compute_bias': 0.6},
    'Infra-Metallic-Matrix_70': {'name': 'Infra-Metallic-Matrix_70', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (1.73, 4.33), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.76, 'thermosynthesis_bias': 0.26, 'compute_bias': 0.46, 'armor_bias': 0.46, 'motility_bias': -0.24},
    'Spectral-Void-Vessel_71': {'name': 'Spectral-Void-Vessel_71', 'color_hsv_range': ((0.8, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.71, 2.84), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.7, 'thermosynthesis_bias': -0.3, 'armor_bias': 0.3},
    'Omega-Silicon-Bloom_72': {'name': 'Omega-Silicon-Bloom_72', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.46, 3.66), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Infra-Crystalline-Processor_73': {'name': 'Infra-Crystalline-Processor_73', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Causal-Carbon-Shard_74': {'name': 'Causal-Carbon-Shard_74', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.66, 1.98), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.54, 'chemosynthesis_bias': 0.34, 'thermosynthesis_bias': -0.24, 'compute_bias': 0.34},
    'Causal-Metallic-Filament_75': {'name': 'Causal-Metallic-Filament_75', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (1.73, 4.33), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.76, 'thermosynthesis_bias': 0.26, 'compute_bias': 0.46, 'armor_bias': 0.46, 'motility_bias': -0.24},
    'Quantum-Aether-Lattice_76': {'name': 'Quantum-Aether-Lattice_76', 'color_hsv_range': ((0.75, 0.85), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 1.14, 'compute_bias': 0.94, 'sense_temp_bias': 0.74, 'sense_minerals_bias': 0.74},
    'Pyro-Carbon-Matrix_77': {'name': 'Pyro-Carbon-Matrix_77', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.66, 1.98), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.54, 'chemosynthesis_bias': 0.34, 'thermosynthesis_bias': -0.24, 'compute_bias': 0.34},
    'Quantum-Quantum-Polymer_78': {'name': 'Quantum-Quantum-Polymer_78', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.0), (1.0, 1.0)), 'mass_range': (0.0, 0.0), 'structural_mult': (0.0, 0.0), 'compute_bias': 1.2, 'conductance_bias': 1.2, 'sense_light_bias': 0.7, 'sense_temp_bias': 0.7, 'sense_minerals_bias': 0.7},
    'Cryo-Metallic-Mycelium_79': {'name': 'Cryo-Metallic-Mycelium_79', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Void-Void-Weave_80': {'name': 'Void-Void-Weave_80', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Spectral-Metallic-Vessel_81': {'name': 'Spectral-Metallic-Vessel_81', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.7, 6.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.72, 'thermosynthesis_bias': 0.22, 'compute_bias': 0.42, 'armor_bias': 0.42, 'motility_bias': -0.28},
    'Causal-Carbon-Conduit_82': {'name': 'Causal-Carbon-Conduit_82', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.66, 1.98), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.54, 'chemosynthesis_bias': 0.34, 'thermosynthesis_bias': -0.24, 'compute_bias': 0.34},
    'Chrono-Aether-Conduit_83': {'name': 'Chrono-Aether-Conduit_83', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.09), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.8, 'compute_bias': 0.6, 'sense_temp_bias': 0.4, 'sense_minerals_bias': 0.4},
    'Quantum-Carbon-Polymer_84': {'name': 'Quantum-Carbon-Polymer_84', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Astro-Metallic-Vessel_85': {'name': 'Astro-Metallic-Vessel_85', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Aero-Crystalline-Core_86': {'name': 'Aero-Crystalline-Core_86', 'color_hsv_range': ((0.6, 1.0), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.71, 1.89), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.14, 'compute_bias': 0.6, 'sense_light_bias': 0.43},
    'Infra-Aether-Conduit_87': {'name': 'Infra-Aether-Conduit_87', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.74, 'compute_bias': 0.54, 'sense_temp_bias': 0.34, 'sense_minerals_bias': 0.34},
    'Myco-Silicon-Gel_88': {'name': 'Myco-Silicon-Gel_88', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.46, 3.66), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Astro-Void-Shard_89': {'name': 'Astro-Void-Shard_89', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Pseudo-Carbon-Shard_90': {'name': 'Pseudo-Carbon-Shard_90', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.59, 1.76), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': -0.2, 'compute_bias': 0.1},
    'Myco-Aether-Matrix_91': {'name': 'Myco-Aether-Matrix_91', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.09), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.8, 'compute_bias': 0.6, 'sense_temp_bias': 0.4, 'sense_minerals_bias': 0.4},
    'Myco-Aether-Processor_92': {'name': 'Myco-Aether-Processor_92', 'color_hsv_range': ((0.75, 0.85), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 1.14, 'compute_bias': 0.94, 'sense_temp_bias': 0.74, 'sense_minerals_bias': 0.74},
    'Causal-Carbon-Vessel_93': {'name': 'Causal-Carbon-Vessel_93', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.44, 1.33), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.2, 'compute_bias': 0.27},
    'Chrono-Metallic-Polymer_94': {'name': 'Chrono-Metallic-Polymer_94', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Psionic-Psionic-Lattice_95': {'name': 'Psionic-Psionic-Lattice_95', 'color_hsv_range': ((0.52, 0.67), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.1, 0.3), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.61, 'conductance_bias': 0.41, 'sense_compute_bias': 0.61},
    'Myco-Silicon-Vessel_96': {'name': 'Myco-Silicon-Vessel_96', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.33, 3.32), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.16, 'chemosynthesis_bias': 0.24, 'thermosynthesis_bias': 0.04, 'compute_bias': 0.14, 'armor_bias': 0.04},
    'Geo-Carbon-Shell_97': {'name': 'Geo-Carbon-Shell_97', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Void-Void-Weave_98': {'name': 'Void-Void-Weave_98', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.43, 1.72), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.3, 'thermosynthesis_bias': -0.7, 'armor_bias': -0.1},
    'Astro-Metallic-Shard_99': {'name': 'Astro-Metallic-Shard_99', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Astro-Plasma-Lattice_100': {'name': 'Astro-Plasma-Lattice_100', 'color_hsv_range': ((0.6, 0.8), (0.8, 1.0), (0.9, 1.0)), 'mass_range': (0.11, 0.54), 'structural_mult': (0.0, 0.1), 'energy_storage_mult': (0.5, 2.0), 'thermosynthesis_bias': 1.0, 'photosynthesis_bias': 0.7, 'motility_bias': 0.1},
    'Astro-Metallic-Node_101': {'name': 'Astro-Metallic-Node_101', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.28, 5.7), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.93, 'thermosynthesis_bias': 0.38, 'compute_bias': 0.35, 'armor_bias': 0.74, 'motility_bias': -0.28},
    'Xeno-Crystalline-Node_102': {'name': 'Xeno-Crystalline-Node_102', 'color_hsv_range': ((0.6, 1.0), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.91, 2.44), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.2, 'compute_bias': 0.6, 'sense_light_bias': 0.5},
    'Quantum-Carbon-Membrane_103': {'name': 'Quantum-Carbon-Membrane_103', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.59, 1.76), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': -0.2, 'compute_bias': 0.1},
    'Hydro-Silicon-Matrix_104': {'name': 'Hydro-Silicon-Matrix_104', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.33, 3.32), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.16, 'chemosynthesis_bias': 0.24, 'thermosynthesis_bias': 0.04, 'compute_bias': 0.14, 'armor_bias': 0.04},
    'Causal-Void-Core_105': {'name': 'Causal-Void-Core_105', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.71, 2.84), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.7, 'thermosynthesis_bias': -0.3, 'armor_bias': 0.3},
    'Pyro-Crystalline-Shard_106': {'name': 'Pyro-Crystalline-Shard_106', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Quantum-Carbon-Spore_107': {'name': 'Quantum-Carbon-Spore_107', 'color_hsv_range': ((0.22, 0.52), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.44, 1.33), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.2, 'compute_bias': 0.27},
    'Spectral-Silicon-Core_108': {'name': 'Spectral-Silicon-Core_108', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.75, 4.38), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Astro-Carbon-Vessel_109': {'name': 'Astro-Carbon-Vessel_109', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Spectral-Silicon-Node_110': {'name': 'Spectral-Silicon-Node_110', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.2, 3.0), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Pseudo-Carbon-Polymer_111': {'name': 'Pseudo-Carbon-Polymer_111', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Causal-Metallic-Shell_112': {'name': 'Causal-Metallic-Shell_112', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Aero-Crystalline-Core_113': {'name': 'Aero-Crystalline-Core_113', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Myco-Silicon-Shard_114': {'name': 'Myco-Silicon-Shard_114', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.47, 3.68), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.01, 'chemosynthesis_bias': 0.35, 'thermosynthesis_bias': 0.44, 'compute_bias': 0.25, 'armor_bias': 0.22},
    'Myco-Quantum-Membrane_115': {'name': 'Myco-Quantum-Membrane_115', 'color_hsv_range': ((0, 1), (0.0, 0.0), (1.0, 1.0)), 'mass_range': (0.0, 0.0), 'structural_mult': (0.0, 0.0), 'compute_bias': 1.0, 'conductance_bias': 1.0, 'sense_light_bias': 0.5, 'sense_temp_bias': 0.5, 'sense_minerals_bias': 0.5},
    'Causal-Carbon-Shard_116': {'name': 'Causal-Carbon-Shard_116', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.5, 1.5), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.3, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': 0.0, 'compute_bias': 0.1},
    'Astro-Carbon-Bloom_117': {'name': 'Astro-Carbon-Bloom_117', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.42, 1.25), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.46, 'chemosynthesis_bias': 0.26, 'thermosynthesis_bias': -0.14, 'compute_bias': 0.26},
    'Omega-Silicon-Conduit_118': {'name': 'Omega-Silicon-Conduit_118', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.2, 3.0), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Quantum-Carbon-Polymer_119': {'name': 'Quantum-Carbon-Polymer_119', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.5, 1.5), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.3, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': 0.0, 'compute_bias': 0.1},
    'Infra-Metallic-Vessel_120': {'name': 'Infra-Metallic-Vessel_120', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (1.73, 4.33), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.76, 'thermosynthesis_bias': 0.26, 'compute_bias': 0.46, 'armor_bias': 0.46, 'motility_bias': -0.24},
    'Aero-Plasma-Bloom_121': {'name': 'Aero-Plasma-Bloom_121', 'color_hsv_range': ((0.6, 0.8), (0.8, 1.0), (0.9, 1.0)), 'mass_range': (0.08, 0.38), 'structural_mult': (0.0, 0.1), 'energy_storage_mult': (0.5, 2.0), 'thermosynthesis_bias': 0.99, 'photosynthesis_bias': 0.3, 'motility_bias': 0.49},
    'Aero-Crystalline-Node_122': {'name': 'Aero-Crystalline-Node_122', 'color_hsv_range': ((0.6, 1.0), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.91, 2.44), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.2, 'compute_bias': 0.6, 'sense_light_bias': 0.5},
    'Causal-Aether-Conduit_123': {'name': 'Causal-Aether-Conduit_123', 'color_hsv_range': ((0.75, 0.85), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 1.14, 'compute_bias': 0.94, 'sense_temp_bias': 0.74, 'sense_minerals_bias': 0.74},
    'Infra-Carbon-Bloom_124': {'name': 'Infra-Carbon-Bloom_124', 'color_hsv_range': ((0.22, 0.52), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.44, 1.33), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.2, 'compute_bias': 0.27},
    'Infra-Aether-Filament_125': {'name': 'Infra-Aether-Filament_125', 'color_hsv_range': ((0.75, 0.85), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 1.14, 'compute_bias': 0.94, 'sense_temp_bias': 0.74, 'sense_minerals_bias': 0.74},
    'Myco-Metallic-Gel_126': {'name': 'Myco-Metallic-Gel_126', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Infra-Void-Gel_127': {'name': 'Infra-Void-Gel_127', 'color_hsv_range': ((0.8, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Astro-Crystalline-Gel_128': {'name': 'Astro-Crystalline-Gel_128', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Psionic-Psionic-Shard_129': {'name': 'Psionic-Psionic-Shard_129', 'color_hsv_range': ((0.52, 0.67), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.12, 0.37), 'structural_mult': (0.0, 0.1), 'compute_bias': 1.0, 'conductance_bias': 0.8, 'sense_compute_bias': 0.6},
    'Hydro-Crystalline-Core_130': {'name': 'Hydro-Crystalline-Core_130', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Geo-Metallic-Gel_131': {'name': 'Geo-Metallic-Gel_131', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (1.73, 4.33), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.76, 'thermosynthesis_bias': 0.26, 'compute_bias': 0.46, 'armor_bias': 0.46, 'motility_bias': -0.24},
    'Cryo-Crystalline-Lattice_132': {'name': 'Cryo-Crystalline-Lattice_132', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Psionic-Aether-Shard_133': {'name': 'Psionic-Aether-Shard_133', 'color_hsv_range': ((0.75, 0.85), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.09), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.8, 'compute_bias': 0.6, 'sense_temp_bias': 0.4, 'sense_minerals_bias': 0.4},
    'Quantum-Carbon-Gel_134': {'name': 'Quantum-Carbon-Gel_134', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.53, 1.59), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.42, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.06, 'compute_bias': 0.01},
    'Echo-Silicon-Spore_135': {'name': 'Echo-Silicon-Spore_135', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.33, 3.32), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.16, 'chemosynthesis_bias': 0.24, 'thermosynthesis_bias': 0.04, 'compute_bias': 0.14, 'armor_bias': 0.04},
    'Causal-Metallic-Bloom_136': {'name': 'Causal-Metallic-Bloom_136', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Pseudo-Carbon-Polymer_137': {'name': 'Pseudo-Carbon-Polymer_137', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Quantum-Carbon-Bloom_138': {'name': 'Quantum-Carbon-Bloom_138', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Xeno-Metallic-Conduit_139': {'name': 'Xeno-Metallic-Conduit_139', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.7, 6.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.72, 'thermosynthesis_bias': 0.22, 'compute_bias': 0.42, 'armor_bias': 0.42, 'motility_bias': -0.28},
    'Chrono-Aether-Processor_140': {'name': 'Chrono-Aether-Processor_140', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.09), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.8, 'compute_bias': 0.6, 'sense_temp_bias': 0.4, 'sense_minerals_bias': 0.4},
    'Chrono-Void-Mycelium_141': {'name': 'Chrono-Void-Mycelium_141', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.71, 2.84), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.7, 'thermosynthesis_bias': -0.3, 'armor_bias': 0.3},
    'Meta-Crystalline-Lattice_142': {'name': 'Meta-Crystalline-Lattice_142', 'color_hsv_range': ((0.6, 1.0), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Myco-Silicon-Weave_143': {'name': 'Myco-Silicon-Weave_143', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.47, 3.68), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.01, 'chemosynthesis_bias': 0.35, 'thermosynthesis_bias': 0.44, 'compute_bias': 0.25, 'armor_bias': 0.22},
    'Astro-Metallic-Shard_144': {'name': 'Astro-Metallic-Shard_144', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.7, 6.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.72, 'thermosynthesis_bias': 0.22, 'compute_bias': 0.42, 'armor_bias': 0.42, 'motility_bias': -0.28},
    'Echo-Silicon-Gel_145': {'name': 'Echo-Silicon-Gel_145', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.75, 4.38), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Aero-Psionic-Shell_146': {'name': 'Aero-Psionic-Shell_146', 'color_hsv_range': ((0.52, 0.67), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.1, 0.3), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.61, 'conductance_bias': 0.41, 'sense_compute_bias': 0.61},
    'Astro-Void-Shard_147': {'name': 'Astro-Void-Shard_147', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.43, 1.72), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.3, 'thermosynthesis_bias': -0.7, 'armor_bias': -0.1},
    'Spectral-Silicon-Node_148': {'name': 'Spectral-Silicon-Node_148', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.2, 3.0), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Causal-Carbon-Shard_149': {'name': 'Causal-Carbon-Shard_149', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.5, 1.5), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.3, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': 0.0, 'compute_bias': 0.1},
    'Astro-Psionic-Core_150': {'name': 'Astro-Psionic-Core_150', 'color_hsv_range': ((0.5, 0.65), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.12, 0.37), 'structural_mult': (0.0, 0.1), 'compute_bias': 1.0, 'conductance_bias': 0.8, 'sense_compute_bias': 0.6},
    'Void-Void-Weave_151': {'name': 'Void-Void-Weave_151', 'color_hsv_range': ((0.8, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Astro-Crystalline-Core_152': {'name': 'Astro-Crystalline-Core_152', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Spectral-Chrono-Vessel_153': {'name': 'Spectral-Chrono-Vessel_153', 'color_hsv_range': ((0.35, 0.4), (0.3, 0.6), (0.7, 0.9)), 'mass_range': (0.5, 0.75), 'structural_mult': (0.5, 1.0), 'energy_storage_mult': (1.0, 1.0), 'compute_bias': 0.08},
    'Myco-Aether-Conduit_154': {'name': 'Myco-Aether-Conduit_154', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.74, 'compute_bias': 0.54, 'sense_temp_bias': 0.34, 'sense_minerals_bias': 0.34},
    'Psionic-Psionic-Shell_155': {'name': 'Psionic-Psionic-Shell_155', 'color_hsv_range': ((0.5, 0.65), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.1, 0.3), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.8, 'conductance_bias': 0.6, 'sense_compute_bias': 0.8},
    'Xeno-Carbon-Membrane_156': {'name': 'Xeno-Carbon-Membrane_156', 'color_hsv_range': ((0.22, 0.52), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.44, 1.33), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.2, 'compute_bias': 0.27},
    'Myco-Aether-Processor_157': {'name': 'Myco-Aether-Processor_157', 'color_hsv_range': ((0.75, 0.85), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 1.14, 'compute_bias': 0.94, 'sense_temp_bias': 0.74, 'sense_minerals_bias': 0.74},
    'Chrono-Psionic-Node_158': {'name': 'Chrono-Psionic-Node_158', 'color_hsv_range': ((0.52, 0.67), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.1, 0.3), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.61, 'conductance_bias': 0.41, 'sense_compute_bias': 0.61},
    'Geo-Carbon-Lattice_159': {'name': 'Geo-Carbon-Lattice_159', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Myco-Metallic-Node_160': {'name': 'Myco-Metallic-Node_160', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Astro-Metallic-Spore_161': {'name': 'Astro-Metallic-Spore_161', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Causal-Void-Node_162': {'name': 'Causal-Void-Node_162', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.43, 1.72), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.3, 'thermosynthesis_bias': -0.7, 'armor_bias': -0.1},
    'Meta-Silicon-Core_163': {'name': 'Meta-Silicon-Core_163', 'color_hsv_range': ((0.62, 0.82), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.2, 3.0), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Chrono-Aether-Conduit_164': {'name': 'Chrono-Aether-Conduit_164', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.09), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.8, 'compute_bias': 0.6, 'sense_temp_bias': 0.4, 'sense_minerals_bias': 0.4},
    'Spectral-Void-Vessel_165': {'name': 'Spectral-Void-Vessel_165', 'color_hsv_range': ((0.8, 1.0), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.71, 2.84), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.7, 'thermosynthesis_bias': -0.3, 'armor_bias': 0.3},
    'Omega-Silicon-Bloom_166': {'name': 'Omega-Silicon-Bloom_166', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.46, 3.66), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Infra-Crystalline-Processor_167': {'name': 'Infra-Crystalline-Processor_167', 'color_hsv_range': ((0.2, 0.6), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (1.08, 2.87), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.4, 'compute_bias': 0.8, 'sense_light_bias': 0.7},
    'Causal-Carbon-Shard_168': {'name': 'Causal-Carbon-Shard_168', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.66, 1.98), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.54, 'chemosynthesis_bias': 0.34, 'thermosynthesis_bias': -0.24, 'compute_bias': 0.34},
    'Causal-Metallic-Filament_169': {'name': 'Causal-Metallic-Filament_169', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (1.73, 4.33), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.76, 'thermosynthesis_bias': 0.26, 'compute_bias': 0.46, 'armor_bias': 0.46, 'motility_bias': -0.24},
    'Quantum-Aether-Lattice_170': {'name': 'Quantum-Aether-Lattice_170', 'color_hsv_range': ((0.75, 0.85), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 1.14, 'compute_bias': 0.94, 'sense_temp_bias': 0.74, 'sense_minerals_bias': 0.74},
    'Pyro-Carbon-Matrix_171': {'name': 'Pyro-Carbon-Matrix_171', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.66, 1.98), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.54, 'chemosynthesis_bias': 0.34, 'thermosynthesis_bias': -0.24, 'compute_bias': 0.34},
    'Quantum-Quantum-Polymer_172': {'name': 'Quantum-Quantum-Polymer_172', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.0), (1.0, 1.0)), 'mass_range': (0.0, 0.0), 'structural_mult': (0.0, 0.0), 'compute_bias': 1.2, 'conductance_bias': 1.2, 'sense_light_bias': 0.7, 'sense_temp_bias': 0.7, 'sense_minerals_bias': 0.7},
    'Cryo-Metallic-Mycelium_173': {'name': 'Cryo-Metallic-Mycelium_173', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Void-Void-Weave_174': {'name': 'Void-Void-Weave_174', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Spectral-Metallic-Vessel_175': {'name': 'Spectral-Metallic-Vessel_175', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.7, 6.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.72, 'thermosynthesis_bias': 0.22, 'compute_bias': 0.42, 'armor_bias': 0.42, 'motility_bias': -0.28},
    'Causal-Carbon-Conduit_176': {'name': 'Causal-Carbon-Conduit_176', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.66, 1.98), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.54, 'chemosynthesis_bias': 0.34, 'thermosynthesis_bias': -0.24, 'compute_bias': 0.34},
    'Chrono-Aether-Conduit_177': {'name': 'Chrono-Aether-Conduit_177', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.09), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.8, 'compute_bias': 0.6, 'sense_temp_bias': 0.4, 'sense_minerals_bias': 0.4},
    'Quantum-Carbon-Polymer_178': {'name': 'Quantum-Carbon-Polymer_178', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Astro-Metallic-Vessel_179': {'name': 'Astro-Metallic-Vessel_179', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.3, 5.75), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.8, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.5, 'armor_bias': 0.5, 'motility_bias': -0.2},
    'Aero-Crystalline-Core_180': {'name': 'Aero-Crystalline-Core_180', 'color_hsv_range': ((0.6, 1.0), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.71, 1.89), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.14, 'compute_bias': 0.6, 'sense_light_bias': 0.43},
    'Infra-Aether-Conduit_181': {'name': 'Infra-Aether-Conduit_181', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.74, 'compute_bias': 0.54, 'sense_temp_bias': 0.34, 'sense_minerals_bias': 0.34},
    'Myco-Silicon-Gel_182': {'name': 'Myco-Silicon-Gel_182', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.46, 3.66), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.06, 'chemosynthesis_bias': 0.44, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.47, 'armor_bias': 0.14},
    'Astro-Void-Shard_183': {'name': 'Astro-Void-Shard_183', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.59, 2.37), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.73, 'thermosynthesis_bias': -0.27, 'armor_bias': -0.07},
    'Pseudo-Carbon-Shard_184': {'name': 'Pseudo-Carbon-Shard_184', 'color_hsv_range': ((0.9, 1.0), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.59, 1.76), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': -0.2, 'compute_bias': 0.1},
    'Myco-Aether-Matrix_185': {'name': 'Myco-Aether-Matrix_185', 'color_hsv_range': ((0.35, 0.45), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.09), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 0.8, 'compute_bias': 0.6, 'sense_temp_bias': 0.4, 'sense_minerals_bias': 0.4},
    'Myco-Aether-Processor_186': {'name': 'Myco-Aether-Processor_186', 'color_hsv_range': ((0.75, 0.85), (0.5, 0.8), (0.9, 1.0)), 'mass_range': (0.01, 0.1), 'structural_mult': (0.0, 0.0), 'energy_storage_mult': (1.0, 3.0), 'conductance_bias': 1.14, 'compute_bias': 0.94, 'sense_temp_bias': 0.74, 'sense_minerals_bias': 0.74},
    'Causal-Carbon-Vessel_187': {'name': 'Causal-Carbon-Vessel_187', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.44, 1.33), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.2, 'compute_bias': 0.27},
    'Chrono-Metallic-Polymer_188': {'name': 'Chrono-Metallic-Polymer_188', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Psionic-Psionic-Lattice_189': {'name': 'Psionic-Psionic-Lattice_189', 'color_hsv_range': ((0.52, 0.67), (0.6, 0.9), (0.8, 1.0)), 'mass_range': (0.1, 0.3), 'structural_mult': (0.0, 0.1), 'compute_bias': 0.61, 'conductance_bias': 0.41, 'sense_compute_bias': 0.61},
    'Myco-Silicon-Vessel_190': {'name': 'Myco-Silicon-Vessel_190', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.33, 3.32), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.16, 'chemosynthesis_bias': 0.24, 'thermosynthesis_bias': 0.04, 'compute_bias': 0.14, 'armor_bias': 0.04},
    'Geo-Carbon-Shell_191': {'name': 'Geo-Carbon-Shell_191', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.6, 1.8), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.14, 'chemosynthesis_bias': -0.06, 'thermosynthesis_bias': 0.14, 'compute_bias': 0.14},
    'Void-Void-Weave_192': {'name': 'Void-Void-Weave_192', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.43, 1.72), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.3, 'thermosynthesis_bias': -0.7, 'armor_bias': -0.1},
    'Astro-Metallic-Shard_193': {'name': 'Astro-Metallic-Shard_193', 'color_hsv_range': ((0, 1), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.12, 5.3), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.94, 'thermosynthesis_bias': 0.3, 'compute_bias': 0.38, 'armor_bias': 0.51, 'motility_bias': -0.06},
    'Astro-Plasma-Lattice_194': {'name': 'Astro-Plasma-Lattice_194', 'color_hsv_range': ((0.6, 0.8), (0.8, 1.0), (0.9, 1.0)), 'mass_range': (0.11, 0.54), 'structural_mult': (0.0, 0.1), 'energy_storage_mult': (0.5, 2.0), 'thermosynthesis_bias': 1.0, 'photosynthesis_bias': 0.7, 'motility_bias': 0.1},
    'Astro-Metallic-Node_195': {'name': 'Astro-Metallic-Node_195', 'color_hsv_range': ((0.8, 1.0), (0.0, 0.1), (0.7, 1.0)), 'mass_range': (2.28, 5.7), 'structural_mult': (2.0, 4.0), 'energy_storage_mult': (0.1, 0.5), 'conductance_bias': 0.93, 'thermosynthesis_bias': 0.38, 'compute_bias': 0.35, 'armor_bias': 0.74, 'motility_bias': -0.28},
    'Xeno-Crystalline-Node_196': {'name': 'Xeno-Crystalline-Node_196', 'color_hsv_range': ((0.6, 1.0), (0.1, 0.3), (0.9, 1.0)), 'mass_range': (0.91, 2.44), 'structural_mult': (0.5, 1.5), 'energy_storage_mult': (1.0, 2.5), 'conductance_bias': 0.2, 'compute_bias': 0.6, 'sense_light_bias': 0.5},
    'Quantum-Carbon-Membrane_197': {'name': 'Quantum-Carbon-Membrane_197', 'color_hsv_range': ((0.1, 0.4), (0.7, 1.0), (0.5, 0.9)), 'mass_range': (0.59, 1.76), 'structural_mult': (1.0, 2.0), 'energy_storage_mult': (0.5, 1.5), 'photosynthesis_bias': 0.1, 'chemosynthesis_bias': 0.1, 'thermosynthesis_bias': -0.2, 'compute_bias': 0.1},
    'Hydro-Silicon-Matrix_198': {'name': 'Hydro-Silicon-Matrix_198', 'color_hsv_range': ((0.3, 0.5), (0.3, 0.6), (0.7, 1.0)), 'mass_range': (1.33, 3.32), 'structural_mult': (1.5, 3.0), 'energy_storage_mult': (0.2, 1.0), 'photosynthesis_bias': -0.16, 'chemosynthesis_bias': 0.24, 'thermosynthesis_bias': 0.04, 'compute_bias': 0.14, 'armor_bias': 0.04},
    'Causal-Void-Core_199': {'name': 'Causal-Void-Core_199', 'color_hsv_range': ((0, 1), (0.1, 0.3), (0.05, 0.2)), 'mass_range': (0.71, 2.84), 'structural_mult': (0.1, 0.5), 'energy_storage_mult': (2.0, 5.0), 'chemosynthesis_bias': 0.7, 'thermosynthesis_bias': -0.3, 'armor_bias': 0.3},
}

# Add more bases for the "10000+ parameter" feel
for name in ['Cryo', 'Hydro', 'Pyro', 'Geo', 'Aero', 'Bio-Steel', 'Neuro-Gel', 'Xeno-Polymer']:
    base_template = random.choice(list(CHEMICAL_BASES_REGISTRY.values()))
    new_base = copy.deepcopy(base_template)
    new_base['name'] = name
    new_base['mass_range'] = (
        np.clip(base_template['mass_range'][0] * random.uniform(0.5, 1.5), 0.1, 4.0),
        np.clip(base_template['mass_range'][1] * random.uniform(0.5, 1.5), 0.5, 5.0)
    )
    CHEMICAL_BASES_REGISTRY[name] = new_base

# ========================================================
#
# PART 1: THE GENETIC CODE (THE "ATOMS" OF LIFE)
#
# ========================================================

@dataclass
class ComponentGene:
    """
    Defines a fundamental 'building block' of life.
    This is the 'chemistry' the organism has access to.
    Evolution can invent new components based on the CHEMICAL_BASES_REGISTRY.
    """
    id: str = field(default_factory=lambda: f"comp_{uuid.uuid4().hex[:6]}")
    name: str = "PrimordialGoo"
    base_kingdom: str = "Carbon" # NEW: Tracks its chemical origin
    
    # --- Core Properties ---
    mass: float = 1.0           # Metabolic cost to maintain
    structural: float = 0.1     # Contribution to physical integrity
    energy_storage: float = 0.0 # Capacity to store energy
    
    # --- Environmental Interaction Properties ---
    photosynthesis: float = 0.0 # Ability to generate energy from 'light'
    chemosynthesis: float = 0.0 # Ability to generate energy from 'minerals'
    thermosynthesis: float = 0.0 # Ability to generate energy from 'heat'
    
    # --- Specialized Functions ---
    conductance: float = 0.0    # Ability to transport energy (like a 'wire' or 'vein')
    compute: float = 0.0        # Ability to perform information processing (a 'neuron')
    motility: float = 0.0       # Ability to generate thrust/movement (a 'muscle')
    armor: float = 0.0          # Ability to resist 'damage'
    sense_light: float = 0.0    # Ability to sense 'light'
    sense_minerals: float = 0.0 # Ability to sense 'minerals'
    sense_temp: float = 0.0     # Ability to sense 'temperature'
    
    # --- Aesthetics ---
    color: str = "#888888"      # Visual representation

    def __hash__(self):
        return hash(self.id)



# --- ADD THIS NEW CLASS ---
import dataclasses # Ensure dataclasses is imported globally (it is)
import json # Ensure json is imported globally (it is)

class GenotypeJSONEncoder(json.JSONEncoder):
    """
    Custom encoder to handle dataclasses. 
    It recursively converts any dataclass object it finds into a dictionary.
    """
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)
# --- END NEW CLASS ---

@dataclass
class RuleGene:
    """
    Defines a 'developmental rule' in the Genetic Regulatory Network (GRN).
    This is the 'grammar' of life, dictating how the organism grows.
    'IF [Conditions] are met, THEN [Action] happens.'
    """
    id: str = field(default_factory=lambda: f"rule_{uuid.uuid4().hex[:6]}")
    
    # --- The 'IF' Part ---
    # List of (source, target, required_value, operator)
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    
    # --- The 'THEN' Part ---
    # The action to perform (e.g., 'GROW', 'DIFFERENTIATE', 'METABOLIZE')
    action_type: str = "IDLE"
    # The component to use/create, or the property to change
    action_param: str = "self" 
    action_value: float = 0.0
    
    probability: float = 1.0 # Chance this rule fires if conditions are met
    priority: int = 0        # Execution order (higher fires first)
    is_disabled: bool = False # <-- ADD THIS

@dataclass
class Genotype:
    """
    The complete "DNA" of an organism.
    It is a collection of available components and the rules to assemble them.
    """
    id: str = field(default_factory=lambda: f"geno_{uuid.uuid4().hex[:6]}")
    
    # The "Alphabet": List of components this organism can create.
    component_genes: Dict[str, ComponentGene] = field(default_factory=dict)
    
    # The "Grammar": The list of developmental rules.
    rule_genes: List[RuleGene] = field(default_factory=list)
    
    # --- Evolutionary Metadata (from GENEVO) ---
    fitness: float = 0.0
    age: int = 0
    generation: int = 0
    lineage_id: str = ""
    parent_ids: List[str] = field(default_factory=list)
    
    # --- Phenotypic Summary (filled after development) ---
    cell_count: int = 0
    complexity: float = 0.0 # e.g., number of rules + components
    energy_production: float = 0.0
    energy_consumption: float = 0.0
    lifespan: int = 0
    
    # --- Speciation (from GENEVO) ---
    # The 'Form ID' is now the 'Kingdom' (e.g., Carbon-based, Silicon-based)
    # This is determined by the *dominant* structural component.
    kingdom_id: str = "Carbon" 
    
    # --- Meta-Evolution (Hyperparameters) ---
    # These can be evolved if s['enable_hyperparameter_evolution'] is True
    evolvable_mutation_rate: float = 0.2
    evolvable_innovation_rate: float = 0.05
    
    # --- Autotelic Evolution (Evolvable Objectives) ---
    # These can be evolved if s['enable_objective_evolution'] is True
    objective_weights: Dict[str, float] = field(default_factory=dict)

    # --- Multi-Level Selection ---
    colony_id: Optional[str] = None
    individual_fitness: float = 0.0 # Fitness before group-level adjustments

    def __post_init__(self):
        if not self.lineage_id:
            self.lineage_id = f"L{random.randint(0, 999999):06d}"

    def copy(self):
        """Deep copy with new lineage"""
        new_genotype = Genotype(
            component_genes={cid: ComponentGene(**asdict(c)) for cid, c in self.component_genes.items()},
            rule_genes=[RuleGene(**asdict(r)) for r in self.rule_genes],
            fitness=self.fitness,
            individual_fitness=self.individual_fitness,
            age=0,
            generation=self.generation,
            parent_ids=[self.id],
            kingdom_id=self.kingdom_id,
            evolvable_mutation_rate=self.evolvable_mutation_rate,
            evolvable_innovation_rate=self.evolvable_innovation_rate,
            objective_weights=self.objective_weights.copy()
        )
        return new_genotype
    
    def compute_complexity(self) -> float:
        """Kolmogorov complexity approximation"""
        num_components = len(self.component_genes)
        num_rules = len(self.rule_genes)
        num_conditions = sum(len(r.conditions) for r in self.rule_genes)
        return (num_components * 0.4) + (num_rules * 0.3) + (num_conditions * 0.3)

    def update_kingdom(self):
        """Determine the organism's kingdom based on its dominant structural component."""
        if not self.component_genes:
            self.kingdom_id = "Unknown"
            return

        # Find the component with the highest structural value
        dominant_comp = max(self.component_genes.values(), key=lambda c: c.structural, default=None)
        
        if dominant_comp:
            self.kingdom_id = dominant_comp.base_kingdom
        else:
            # Failsafe: if no components, or all have 0 structure
            comp_counts = Counter(c.base_kingdom for c in self.component_genes.values())
            if comp_counts:
                self.kingdom_id = comp_counts.most_common(1)[0][0]
            else:
                self.kingdom_id = "Unclassified"

# ========================================================
#
# PART 2: THE ENVIRONMENT (THE "GALLERY")
#
# ========================================================

@dataclass
class GridCell:
    """A single cell in the 2D gallery grid."""
    x: int
    y: int
    
    # --- Environmental Resources ---
    light: float = 0.0
    minerals: float = 0.0
    water: float = 0.0
    temperature: float = 0.0
    
    # --- Occupancy ---
    organism_id: Optional[str] = None
    cell_type: Optional[str] = None # Stores component name

class ExhibitGrid:
    """
    The environment simulation for a gallery.
    A 2D Cellular Automaton with resources and physics.
    """
    def __init__(self, settings: Dict):
        self.width = settings.get('grid_width', 100)
        self.height = settings.get('grid_height', 100)
        self.settings = settings
        
        self.grid: List[List[GridCell]] = []
        self.resource_map: Dict[str, np.ndarray] = {}
        self.initialize_grid()

    def initialize_grid(self):
        """Creates the grid and populates it with resources."""
        self.grid = [[GridCell(x, y) for y in range(self.height)] for x in range(self.width)]
        
        # --- Generate Resource Maps using Perlin-like noise ---
        def generate_noise_map(octaves=4, persistence=0.5, lacunarity=2.0):
            noise = np.zeros((self.width, self.height))
            freq = 1.0
            amp = 1.0
            for _ in range(octaves):
                # Ensure width/height are integers for noise generation
                int_width, int_height = int(self.width), int(self.height)
                if int_width <= 0 or int_height <= 0:
                    st.error("Grid width/height must be positive.")
                    return np.zeros((self.width, self.height))
                    
                noise_slice = np.random.normal(0, 1, (int_width, int_height))
                
                # Resize if necessary (e.g., if freq > 1)
                if noise_slice.shape != (self.width, self.height):
                     # This part is tricky, simplified for now
                     pass
                
                if noise.shape == noise_slice.shape:
                    noise += amp * noise_slice
                else:
                    # Failsafe if shapes mismatch (shouldn't happen with simple freq)
                    pass

                freq *= lacunarity
                amp *= persistence
                
            # Normalize to 0-1
            if np.max(noise) - np.min(noise) > 0:
                noise = (noise - np.min(noise)) / (np.max(noise) - np.min(noise))
            else:
                noise = np.zeros((self.width, self.height))
            return noise

        # --- Populate Resources based on Settings ---
        self.resource_map['light'] = generate_noise_map() * self.settings.get('light_intensity', 1.0)
        self.resource_map['minerals'] = generate_noise_map(octaves=6) * self.settings.get('mineral_richness', 1.0)
        self.resource_map['water'] = generate_noise_map(octaves=2) * self.settings.get('water_abundance', 1.0)
        
        temp_gradient = np.linspace(
            self.settings.get('temp_pole', -20), 
            self.settings.get('temp_equator', 30), 
            self.height
        )
        temp_map = np.tile(temp_gradient, (self.width, 1))
        self.resource_map['temperature'] = temp_map + (generate_noise_map(octaves=2) - 0.5) * 10
        
        # --- Apply to grid cells ---
        for x in range(self.width):
            for y in range(self.height):
                cell = self.grid[x][y]
                cell.light = self.resource_map['light'][x, y]
                cell.minerals = self.resource_map['minerals'][x, y]
                cell.water = self.resource_map['water'][x, y]
                cell.temperature = self.resource_map['temperature'][x, y]
                
    def get_cell(self, x, y) -> Optional[GridCell]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y]
        return None

    def get_neighbors(self, x, y, radius=1) -> List[GridCell]:
        neighbors = []
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue
                cell = self.get_cell(x + dx, y + dy)
                if cell:
                    neighbors.append(cell)
        return neighbors

    def update(self):
        """Update the environment (e.g., resource diffusion)."""
        # (Simplified for this example)
        pass # In a full sim, this would diffuse resources, etc.

# ========================================================
#
# PART 3: THE ORGANISM & DEVELOPMENT (THE "PHENOTYPE")
#
# ========================================================

@dataclass
class OrganismCell:
    """A single cell of a living organism."""
    id: str = field(default_factory=lambda: f"cell_{uuid.uuid4().hex[:6]}")
    organism_id: str = ""
    component: ComponentGene = field(default_factory=ComponentGene)
    x: int = 0
    y: int = 0
    energy: float = 1.0
    age: int = 0
    # --- Internal State for GRN ---
    state_vector: Dict[str, Any] = field(default_factory=dict)

class Phenotype:
    """
    The 'body' of the organism. A collection of OrganismCells on the grid.
    This is the physical manifestation of the Genotype.
    """
    def __init__(self, genotype: Genotype, exhibit_grid: ExhibitGrid, settings: Dict):
        self.id = f"org_{uuid.uuid4().hex[:6]}"
        self.genotype = genotype
        self.grid = exhibit_grid
        self.settings = settings
        
        self.cells: Dict[Tuple[int, int], OrganismCell] = {}
        self.total_energy = 0.0
        self.age = 0
        self.is_alive = True
        self.total_energy_production = 0.0 # Initialize
        
        # --- Initialize Zygote ---
        self.spawn_zygote()
        if self.is_alive:
            self.develop()
        
        # --- After development, calculate properties ---
        if self.is_alive:
            self.update_phenotype_summary()
            self.genotype.cell_count = len(self.cells)
            self.genotype.energy_consumption = sum(c.component.mass for c in self.cells.values())
            self.genotype.energy_production = self.total_energy_production
        else:
            # Ensure genotype reflects failure
            self.genotype.cell_count = 0
            self.genotype.energy_consumption = 0
            self.genotype.energy_production = 0
            
    def spawn_zygote(self):
        """Place the first cell (zygote) in the grid."""
        x, y = self.grid.width // 2, self.grid.height // 2
        
        # Find a free spot (simple linear probe)
        for _ in range(50):
            grid_cell = self.grid.get_cell(x, y)
            if grid_cell and grid_cell.organism_id is None:
                break
            x = (x + random.randint(-5, 5)) % self.grid.width
            y = (y + random.randint(-5, 5)) % self.grid.height
        
        grid_cell = self.grid.get_cell(x, y)
        if not grid_cell or grid_cell.organism_id is not None:
            self.is_alive = False # Failed to spawn
            return

        # Find a component to be the zygote.
        # Prioritize 'Zygote' in name, then 'Primordial', then just pick one.
        zygote_comp = None
        if not self.genotype.component_genes:
            st.warning("Genotype has no components! Cannot spawn.")
            self.is_alive = False
            return
            
        for name, comp in self.genotype.component_genes.items():
            if 'zygote' in name.lower():
                zygote_comp = comp
                break
        if not zygote_comp:
            for name, comp in self.genotype.component_genes.items():
                if 'primordial' in name.lower():
                    zygote_comp = comp
                    break
        if not zygote_comp:
            zygote_comp = list(self.genotype.component_genes.values())[0]

        
        zygote = OrganismCell(
            organism_id=self.id,
            component=zygote_comp,
            x=x,
            y=y,
            energy=self.settings.get('zygote_energy', 10.0),
            state_vector={'type_id': hash(zygote_comp.id), 'energy': 1.0}
        )
        self.cells[(x, y)] = zygote
        grid_cell.organism_id = self.id
        grid_cell.cell_type = zygote_comp.name
        self.total_energy = zygote.energy

    def develop(self):
        """
        The "Embryogeny" process.
        Grows the zygote into a multicellular organism by running the GRN.
        """
        max_dev_steps = self.settings.get('development_steps', 50)
        dev_energy = self.total_energy
        
        for step in range(max_dev_steps):
            if dev_energy <= 0 or not self.cells:
                self.is_alive = False
                break
            
            signal_snapshot: Dict[Tuple[int, int], Dict[str, float]] = {}
            for (x, y), cell in list(self.cells.items()):
                signal_snapshot[(x, y)] = cell.state_vector.get('signals_out', {})
            
        # --- 1. Signal Diffusion Step (Morphogenesis) ---
        # Read the 'signals_out' from the *previous* step,
        # calculate the average, and write it to 'signals_in' for *this* step.

        # Create a snapshot of all signals currently being emitted
        
        

        # Calculate incoming signals for each cell based on the snapshot
        for (x, y), cell in list(self.cells.items()):
            cell.state_vector['signals_in'] = {} # Reset incoming signals
            neighbors = self.grid.get_neighbors(x, y)

            # Tally all signals from neighbors
            incoming_signals_tally: Dict[str, List[float]] = {}
            for n in neighbors:
                neighbor_pos = (n.x, n.y)
                # Check if neighbor is part of this organism
                if neighbor_pos in signal_snapshot:
                    for signal_name, signal_value in signal_snapshot[neighbor_pos].items():
                        if signal_name not in incoming_signals_tally:
                            incoming_signals_tally[signal_name] = []
                        incoming_signals_tally[signal_name].append(signal_value)

            # Average the tallied signals and store in 'signals_in'
            for signal_name, values in incoming_signals_tally.items():
                if values:
                    cell.state_vector['signals_in'][signal_name] = np.mean(values)
        # --- END OF SIGNAL DIFFUSION BLOCK ---
            
            actions_to_take = []
            
            # --- 1. Evaluate all rules for all cells ---
            for (x, y), cell in list(self.cells.items()):
                cell.state_vector['signals_out'] = {}
                grid_cell = self.grid.get_cell(x, y)
                if not grid_cell: continue # Cell is somehow off-grid, prune
                
                neighbors = self.grid.get_neighbors(x, y)
                
                # --- Create context for rule engine ---
                context = {
                    'self_energy': cell.energy,
                    'self_age': cell.age,
                    'self_type': cell.component.name,
                    'env_light': grid_cell.light,
                    'env_minerals': grid_cell.minerals,
                    'env_temp': grid_cell.temperature,
                    'neighbor_count_total': len(neighbors),
                    'neighbor_count_empty': sum(1 for n in neighbors if n.organism_id is None),
                    'neighbor_count_self': sum(1 for n in neighbors if n.organism_id == self.id),
                    'neighbor_count_other': sum(1 for n in neighbors if n.organism_id is not None and n.organism_id != self.id),
                }
                
                # --- NEW 2.0: Add dynamic senses to context ---
                # This is where meta-innovated senses would be populated
                # (e.g., by scanning neighbors and calculating gradient)
                if 'sense_energy_gradient_N' in st.session_state.get('evolvable_condition_sources', []):
                    # Example: check northern neighbor's energy
                    n_cell = self.grid.get_cell(x, y-1)
                    context['sense_energy_gradient_N'] = (n_cell.light + n_cell.minerals) - (grid_cell.light + grid_cell.minerals) if n_cell else 0.0
                if 'sense_neighbor_complexity' in st.session_state.get('evolvable_condition_sources', []):
                    # Example: count unique component types in neighbors
                    neighbor_types = {n.cell_type for n in neighbors if n.organism_id == self.id}
                    context['sense_neighbor_complexity'] = len(neighbor_types)

                
                for rule in self.genotype.rule_genes:
                    if rule.is_disabled:
                        continue
                    if random.random() > rule.probability:
                        continue
                        
                    if self.check_conditions(rule, context, cell, neighbors):
                        actions_to_take.append((rule, cell))
            
            # --- 2. Execute all valid actions (in priority order) ---
            actions_to_take.sort(key=lambda x: x[0].priority, reverse=True)
            
            new_cells = {}
            for rule, cell in actions_to_take:
                # Check if cell still exists (might have been killed by a higher-prio rule)
                if (cell.x, cell.y) not in self.cells:
                    continue
                cost = self.execute_action(rule, cell, new_cells)
                dev_energy -= cost
                cell.energy -= cost # Action cost comes from cell energy
                if dev_energy <= 0: break
            
            self.cells.update(new_cells)
            
            # --- 3. Prune dead cells (ran out of energy) ---
            dead_cells = []
            for (x,y), cell in list(self.cells.items()):
                cell.age += 1
                if cell.energy <= 0:
                    dead_cells.append((x,y))
            
            for (x,y) in dead_cells:
                self.prune_cell(x,y)
        
        self.total_energy = sum(c.energy for c in self.cells.values())
        if self.total_energy <= 0 or not self.cells:
            self.is_alive = False

    def prune_cell(self, x, y):
        """Removes a single cell from the organism and the grid."""
        if (x,y) in self.cells:
            del self.cells[(x,y)]
        grid_cell = self.grid.get_cell(x, y)
        if grid_cell:
            grid_cell.organism_id = None
            grid_cell.cell_type = None
            # TODO: Release cell's stored energy/minerals back to grid?

    def check_conditions(self, rule: RuleGene, context: Dict, cell: OrganismCell, neighbors: List[GridCell]) -> bool:
        """Rule-matching engine for the GRN."""
        if not rule.conditions: return True # Rules with no conditions always fire
        
        for cond in rule.conditions:
            source = cond['source']
            value = 0.0
            
            if source.startswith('self_'):
                value = context.get(source, 0.0)
            elif source.startswith('env_'):
                value = context.get(source, 0.0)
            elif source.startswith('neighbor_'):
                value = context.get(source, 0.0)
            elif source in cell.state_vector:
                value = cell.state_vector[source]
            elif source in context: # NEW 2.0: Check for dynamic senses
                value = context.get(source, 0.0)
            
            # --- ADD THIS NEW CONDITION ---
            elif source.startswith('timer_'):
                # Checks a timer. e.g., source: 'timer_grow_pulse'
                timer_name = source.replace('timer_', '', 1)
                if 'timers' in cell.state_vector:
                    value = cell.state_vector['timers'].get(timer_name, 0)
                else:
                    value = 0 # No timers exist, so timer is 0
            # --- END OF ADDITION ---
            # --- END OF ADDITION ---

            # --- ADD THIS NEW CONDITION ---
            elif source.startswith('signal_'):
                # Checks an incoming signal. e.g., source: 'signal_inhibitor'
                signal_name = source.replace('signal_', '', 1)
                if 'signals_in' in cell.state_vector:
                    value = cell.state_vector['signals_in'].get(signal_name, 0.0)
                else:
                    value = 0.0 # No signals in, so value is 0
            # --- END OF ADDITION ---
            
            
            op = cond['operator']
            target = cond['target_value']
            
            try:
                if op == '>':
                    if not (value > target): return False
                elif op == '<':
                    if not (value < target): return False
                elif op == '==':
                    if not (value == target): return False
                elif op == '!=':
                    if not (value != target): return False
            except TypeError:
                # This happens if comparing incompatible types, e.g., string and float.
                # In this case, the condition is considered not met.
                return False
        return True # All conditions passed

    def execute_action(self, rule: RuleGene, cell: OrganismCell, new_cells: Dict) -> float:
        """Executes a developmental action and returns its energy cost."""
        action = rule.action_type
        param = rule.action_param
        value = rule.action_value
        
        cost = self.settings.get('action_cost_base', 0.01)
        
        try:
            if action == "GROW":
                # Find an empty neighbor cell
                empty_neighbors = [n for n in self.grid.get_neighbors(cell.x, cell.y) if n.organism_id is None]
                if empty_neighbors:
                    target_grid_cell = random.choice(empty_neighbors)
                    
                    # 'param' is the ID of the component to grow
                    new_comp = self.genotype.component_genes.get(param)
                    if not new_comp: return 0.0 # Invalid component
                    
                    # Cost to grow is base cost + component mass
                    grow_cost = self.settings.get('action_cost_grow', 0.5) + new_comp.mass
                    if cell.energy < grow_cost: return 0.0 # Can't afford
                    
                    new_cell_energy = self.settings.get('new_cell_energy', 1.0)
                    
                    new_cell = OrganismCell(
                        organism_id=self.id,
                        component=new_comp,
                        x=target_grid_cell.x,
                        y=target_grid_cell.y,
                        energy=new_cell_energy, # Starts with base energy
                        state_vector={'type_id': hash(new_comp.id), 'energy': 1.0}
                    )
                    new_cells[(target_grid_cell.x, target_grid_cell.y)] = new_cell
                    target_grid_cell.organism_id = self.id
                    target_grid_cell.cell_type = new_comp.name
                    cost += grow_cost

            elif action == "DIFFERENTIATE":
                # 'param' is the ID of the component to change into
                new_comp = self.genotype.component_genes.get(param)
                if new_comp and cell.component.id != new_comp.id:
                    diff_cost = self.settings.get('action_cost_diff', 0.2) + abs(new_comp.mass - cell.component.mass)
                    if cell.energy < diff_cost: return 0.0 # Can't afford
                    
                    cell.component = new_comp
                    self.grid.get_cell(cell.x, cell.y).cell_type = new_comp.name
                    cell.state_vector['type_id'] = hash(new_comp.id)
                    cost += diff_cost

            # (After MODIFY_TIMER from Proposal A)
            elif action == "DISABLE_RULE":
                # 'param' is the rule.id to disable
                for rule in self.genotype.rule_genes:
                    if rule.id == param:
                        rule.is_disabled = True
                        break
                cost += self.settings.get('action_cost_compute', 0.02)

            elif action == "ENABLE_RULE":
                # 'param' is the rule.id to enable
                for rule in self.genotype.rule_genes:
                    if rule.id == param:
                        rule.is_disabled = False
                        break
                cost += self.settings.get('action_cost_compute', 0.02)
                
            
            elif action == "SET_STATE":
                # Set an internal state variable
                cell.state_vector[param] = value
                cost += self.settings.get('action_cost_compute', 0.02)

            # --- ADD THESE NEW ACTIONS ---
            elif action == "SET_TIMER":
                # 'param' = timer name (e.g., "pulse_A"), 'value' = duration in ticks
                if 'timers' not in cell.state_vector:
                    cell.state_vector['timers'] = {}
                cell.state_vector['timers'][param] = int(value)
                cost += self.settings.get('action_cost_compute', 0.02)
            
            elif action == "MODIFY_TIMER":
                # 'param' = timer name, 'value' = ticks to add/subtract
                if 'timers' in cell.state_vector and param in cell.state_vector['timers']:
                    cell.state_vector['timers'][param] += int(value)
                cost += self.settings.get('action_cost_compute', 0.02)
            # --- END OF ADDITION ---
            
            elif action == "EMIT_SIGNAL":
                if 'signals_out' not in cell.state_vector:
                    cell.state_vector['signals_out'] = {}                   
                cell.state_vector['signals_out'][param] = value
                cost += self.settings.get('action_cost_compute', 0.02)

                
            elif action == "DIE":
                cost = cell.energy # Cell expends all remaining energy to die
                self.prune_cell(cell.x, cell.y) # Cell suicide
                
            elif action == "TRANSFER_ENERGY":
                # 'param' is direction (e.g., 'N', 'S', 'E', 'W') or 'NEIGHBORS'
                # 'value' is amount
                neighbors = self.grid.get_neighbors(cell.x, cell.y)
                valid_neighbors = [c for (x,y), c in self.cells.items() if self.grid.get_cell(x,y) in neighbors]
                if valid_neighbors:
                    target_cell = random.choice(valid_neighbors)
                    amount = min(value, cell.energy * 0.5) # Don't transfer more than half
                    target_cell.energy += amount
                    cost += amount # Cost is the transferred amount

        except Exception as e:
            # st.error(f"Error in action {action}: {e}")
            pass # Fail silently
        
        return cost

    def run_timestep(self):
        """Run one 'tick' of the organism's life."""
        if not self.is_alive: return
        
        self.age += 1
        self.genotype.lifespan = self.age
        
        energy_gain = 0.0
        metabolic_cost = 0.0
        
        # --- 1. Run all cells ---
        for (x, y), cell in list(self.cells.items()):
            comp = cell.component
            grid_cell = self.grid.get_cell(x, y)
            if not grid_cell: continue # Should not happen
            
            # --- 1a. Energy Gain ---
            gain = 0
            gain += comp.photosynthesis * grid_cell.light
            gain += comp.chemosynthesis * grid_cell.minerals
            gain += comp.thermosynthesis * grid_cell.temperature
            
            # Cap gain by storage
            gain = min(gain, comp.energy_storage if comp.energy_storage > 0 else 1.0)
            cell.energy += gain
            energy_gain += gain
            
            # --- 1b. Metabolic Cost ---
            cost = 0
            cost += comp.mass # Base cost to exist
            cost += comp.compute * self.settings.get('cost_of_compute', 0.1)
            cost += comp.motility * self.settings.get('cost_of_motility', 0.2)
            cost += comp.conductance * self.settings.get('cost_of_conductance', 0.02)
            cost += comp.armor * self.settings.get('cost_of_armor', 0.05)
            
            cell.energy -= cost
            metabolic_cost += cost
            # (After metabolic cost calculation, before energy distribution)
            
            # --- 1c. Run GRN for behavior (simplified) ---
            # (A full sim would run the GRN here too for non-developmental actions)

            # --- ADD THIS TIMER LOOP ---
            # Update internal timers
            if 'timers' in cell.state_vector:
                for timer_name in list(cell.state_vector['timers'].keys()):
                    if cell.state_vector['timers'][timer_name] > 0:
                        cell.state_vector['timers'][timer_name] -= 1
                    else:
                        # Timer reached 0, remove it
                        del cell.state_vector['timers'][timer_name]
            # --- END OF ADDITION ---
            
        # --- 2. Energy Distribution (simplified) ---
            
            # --- 1c. Run GRN for behavior (simplified) ---
            # (A full sim would run the GRN here too for non-developmental actions)
            
        # --- 2. Energy Distribution (simplified) ---
        # Cells with high conductance share energy
        for (x, y), cell in list(self.cells.items()):
            if cell.component.conductance > 0.5:
                neighbors = self.grid.get_neighbors(x, y)
                self_neighbors = [self.cells.get((n.x, n.y)) for n in neighbors if self.cells.get((n.x, n.y)) is not None]
                if not self_neighbors: continue

                avg_energy = (cell.energy + sum(n.energy for n in self_neighbors)) / (len(self_neighbors) + 1)
                
                # Move towards average
                transfer_share = (avg_energy - cell.energy) * cell.component.conductance * 0.1 # Slow diffusion
                cell.energy += transfer_share
                for n in self_neighbors:
                    n.energy -= transfer_share / len(self_neighbors)

        # --- 3. Prune dead cells and check for life ---
        dead_cells = []
        for (x,y), cell in self.cells.items():
            if cell.energy <= 0:
                dead_cells.append((x,y))

        for (x,y) in dead_cells:
            self.prune_cell(x,y)
            
        self.total_energy = sum(c.energy for c in self.cells.values())
        if self.total_energy <= 0 or not self.cells:
            self.is_alive = False
            
    def update_phenotype_summary(self):
        """Calculate high-level properties of the organism."""
        self.total_energy_production = 0.0
        if not self.cells: return
        
        for (x, y), cell in list(self.cells.items()):
            comp = cell.component
            grid_cell = self.grid.get_cell(x, y)
            if not grid_cell: continue
            
            self.total_energy_production += comp.photosynthesis * grid_cell.light
            self.total_energy_production += comp.chemosynthesis * grid_cell.minerals
            self.total_energy_production += comp.thermosynthesis * grid_cell.temperature
            

# ========================================================
#
# PART 4: EVOLUTION (THE "SIMULATION ENGINE")
#
# ========================================================

def get_primordial_soup_genotype(settings: Dict) -> Genotype:
    """Creates the 'Adam/Eve' genotype with procedurally generated components."""
    
    # 1. Define primordial components by innovating from the base registry
    comp_zygote = innovate_component(None, settings, force_base='Carbon')
    comp_zygote.name = f"Zygote_{uuid.uuid4().hex[:4]}"
    comp_zygote.energy_storage *= 2.0 # Boost zygote storage
    
    comp_struct = innovate_component(None, settings)
    comp_struct.name = f"Struct_{uuid.uuid4().hex[:4]}"
    comp_struct.structural *= 1.5 # Boost structure
    
    comp_energy = innovate_component(None, settings)
    comp_energy.name = f"Energy_{uuid.uuid4().hex[:4]}"

    components = {c.name: c for c in [comp_struct, comp_energy, comp_zygote]}
    
    # 2. Define primordial rules that refer to the new components
    rules = [
        # Rule 1: If neighbor is empty and I have energy, grow a structural cell
        RuleGene(
            conditions=[
                {'source': 'neighbor_count_empty', 'operator': '>', 'target_value': 0},
                {'source': 'self_energy', 'operator': '>', 'target_value': random.uniform(1.5, 3.0)},
            ],
            action_type="GROW",
            action_param=comp_struct.name,
            priority=10
        ),
        # Rule 2: If neighbor is empty and I have lots of energy, grow an energy cell
        RuleGene(
            conditions=[
                {'source': 'neighbor_count_empty', 'operator': '>', 'target_value': 0},
                {'source': 'self_energy', 'operator': '>', 'target_value': random.uniform(4.0, 6.0)},
            ],
            action_type="GROW",
            action_param=comp_energy.name,
            priority=11
        ),
        # Rule 3: If I am a Zygote and old, differentiate into a Struct
        RuleGene(
            conditions=[
                {'source': 'self_type', 'operator': '==', 'target_value': comp_zygote.name},
                {'source': 'self_age', 'operator': '>', 'target_value': 2},
            ],
            action_type="DIFFERENTIATE",
            action_param=comp_struct.name,
            priority=100 # High priority
        )
    ]
    
    # --- Initialize Evolvable Objectives ---
    # If autotelic evolution is enabled, the organism gets its own set of goals.
    # Otherwise, the dict is empty and the global settings are used.
    objective_weights = {
        'w_lifespan': 0.4,
        'w_efficiency': 0.3,
        'w_reproduction': 0.3,
        'w_complexity_pressure': 0.0,
    }

    genotype = Genotype(
        component_genes=components,
        rule_genes=rules,
        objective_weights=objective_weights
    )
    genotype.update_kingdom() # Set initial kingdom
    return genotype

def evaluate_fitness(genotype: Genotype, grid: ExhibitGrid, settings: Dict) -> float:
    """
    Simulates the life of an organism and returns its fitness.
    Fitness = (Lifespan * EnergyEfficiency) + ComplexityBonus + ReproductionBonus
    """
    
    # --- 1. Development ---
    organism = Phenotype(genotype, grid, settings)
    
    if not organism.is_alive or organism.genotype.cell_count == 0:
        return 0.0 # Failed to develop
    
    # --- 2. Life Simulation ---
    lifespan = 0
    total_energy_gathered = 0
    max_lifespan = settings.get('max_organism_lifespan', 200)
    
    for step in range(max_lifespan):
        organism.run_timestep()
        if not organism.is_alive:
            break
        lifespan += 1
        total_energy_gathered += organism.total_energy_production
        
    organism.genotype.lifespan = lifespan
    
    # --- 3. Calculate Fitness Components ---
    
    # --- Use organism's own objectives if autotelic evolution is enabled ---
    if settings.get('enable_objective_evolution', False) and genotype.objective_weights:
        weights = genotype.objective_weights
    else:
        # Fallback to global settings
        weights = settings

    # --- Base Fitness: Energy Efficiency & Longevity ---
    total_cost = organism.genotype.energy_consumption
    if total_cost == 0: total_cost = 1.0
    
    energy_efficiency = total_energy_gathered / (total_cost * lifespan + 1.0)
    lifespan_score = lifespan / max_lifespan
    
    base_fitness = (lifespan_score * weights.get('w_lifespan', 0.4)) + (energy_efficiency * weights.get('w_efficiency', 0.3))
    
    # --- Reproduction Bonus ---
    repro_bonus = 0.0
    repro_threshold = settings.get('reproduction_energy_threshold', 50.0)
    if organism.total_energy > repro_threshold:
        repro_bonus = weights.get('w_reproduction', 0.3) * (organism.total_energy / repro_threshold)
        
    # --- Complexity Pressure (from settings) ---
    # --- Complexity Pressure (from settings) ---
    complexity = genotype.compute_complexity()
    complexity_pressure = weights.get('w_complexity_pressure', 0.0)
    complexity_score = complexity * complexity_pressure
    
    # --- Final Fitness ---
    total_fitness = base_fitness + repro_bonus + complexity_score
    
    # Apply fitness floor
    return max(1e-6, total_fitness)

# ========================================================
#
# PART 5: MUTATION (THE "INFINITE" ENGINE)
#
# ========================================================

def mutate(genotype: Genotype, settings: Dict) -> Genotype:
    """
    The core of "infinite" evolution. Mutates parameters,
    rules, and *invents new components and rules*.
    """
    mutated = genotype.copy()
    
    # --- Use evolvable hyperparameters if enabled ---
    if settings.get('enable_hyperparameter_evolution', False):
        mut_rate = mutated.evolvable_mutation_rate
        innov_rate = mutated.evolvable_innovation_rate
    else:
        mut_rate = settings.get('mutation_rate', 0.2)
        innov_rate = settings.get('innovation_rate', 0.05)
    
    # --- 1. Parameter Mutations (tweak existing rules) ---
    for rule in mutated.rule_genes:
        if random.random() < mut_rate:
            rule.probability = np.clip(rule.probability + np.random.normal(0, 0.1), 0.1, 1.0)
        if random.random() < mut_rate:
            rule.priority += random.randint(-1, 1)
        if rule.conditions and random.random() < mut_rate:
            cond_to_mutate = random.choice(rule.conditions)
            if isinstance(cond_to_mutate['target_value'], (int, float)):
                cond_to_mutate['target_value'] *= np.random.lognormal(0, 0.1)

    # --- 2. Structural Mutations (add/remove/change rules) ---
    if random.random() < innov_rate:
        # Add a new rule
        new_rule = innovate_rule(mutated, settings)
        mutated.rule_genes.append(new_rule)
    if random.random() < innov_rate * 0.5 and len(mutated.rule_genes) > 1:
        # Remove a random rule
        mutated.rule_genes.remove(random.choice(mutated.rule_genes))
    
    # --- 3. Component Innovation (THE "INFINITE" PART) ---
    if random.random() < settings.get('component_innovation_rate', 0.01):
        new_component = innovate_component(mutated, settings)
        if new_component.name not in mutated.component_genes:
            mutated.component_genes[new_component.name] = new_component
            # Pass lineage_id to the toast for chronicle logging
            st.toast(f"🔬 {new_component.base_kingdom} Innovation! New component: **{new_component.name}** lineage:{mutated.lineage_id}", icon="💡")

    # --- 4. Hyperparameter Mutation (Evolving Evolution Itself) ---
    if settings.get('enable_hyperparameter_evolution', False):
        hyper_mut_rate = settings.get('hyper_mutation_rate', 0.05)
        if random.random() < hyper_mut_rate and 'mutation_rate' in settings.get('evolvable_params', []):
            mutated.evolvable_mutation_rate = np.clip(mutated.evolvable_mutation_rate * np.random.lognormal(0, 0.1), 0.01, 0.9)
        if random.random() < hyper_mut_rate and 'innovation_rate' in settings.get('evolvable_params', []):
            mutated.evolvable_innovation_rate = np.clip(mutated.evolvable_innovation_rate * np.random.lognormal(0, 0.1), 0.01, 0.5)

    # --- 5. Objective Mutation (Evolving the Goal Itself) ---
    if settings.get('enable_objective_evolution', False):
        hyper_mut_rate = settings.get('hyper_mutation_rate', 0.05) # Reuse meta-mutation rate
        if random.random() < hyper_mut_rate:
            # Pick a random objective to mutate
            if not mutated.objective_weights: # Initialize if empty
                mutated.objective_weights = {'w_lifespan': 0.5, 'w_efficiency': 0.5}
            objective_to_change = random.choice(list(mutated.objective_weights.keys()))
            # Mutate it slightly
            current_val = mutated.objective_weights[objective_to_change]
            mutated.objective_weights[objective_to_change] = current_val + np.random.normal(0, 0.05)
            # (No clipping here to allow for negative weights, which can be interesting)

    mutated.complexity = mutated.compute_complexity()
    mutated.update_kingdom() # Update kingdom in case dominant component changed
    return mutated

def innovate_rule(genotype: Genotype, settings: Dict) -> RuleGene:
    """Create a new, random developmental rule."""
    
    # --- 1. Create Conditions ---
    num_conditions = random.randint(1, settings.get('max_rule_conditions', 3))
    conditions = []
    
    # --- Condition sources (the 'sensors' of the cell) ---
    # NEW 2.0: Use the evolvable list of sources
    available_sources = st.session_state.get('evolvable_condition_sources', [
        'self_energy', 'self_age', 'env_light', 'env_minerals', 'env_temp',
        'neighbor_count_empty', 'neighbor_count_self',
        'timer_A', 'timer_B', 'timer_C','signal_A', 'signal_B' # <-- ADD THIS
    ])
    
    for _ in range(num_conditions):
        source = random.choice(available_sources)
        op = random.choice(['>', '<'])
        
        # Set a logical target value
        if source == 'self_energy': target = random.uniform(1.0, 10.0)
        elif source == 'self_age': target = random.randint(1, 20)
        elif source.startswith('env_'): target = random.uniform(0.1, 0.9)
        elif source.startswith('neighbor_'): target = random.randint(0, 5)
        elif source.startswith('sense_'): target = random.uniform(-0.5, 0.5)
        elif source.startswith('timer_'): target = random.randint(0, 20)
        elif source.startswith('signal_'): target = random.uniform(0.1, 1.0)
        else: target = 0.0
        
        conditions.append({'source': source, 'operator': op, 'target_value': target})

    # --- 2. Create Action ---
    action_type = random.choice(['GROW', 'DIFFERENTIATE', 'SET_STATE', 'TRANSFER_ENERGY', 'DIE',
                                'SET_TIMER', 'MODIFY_TIMER','ENABLE_RULE', 'DISABLE_RULE','EMIT_SIGNAL'])
    
    # Pick a random component from the genotype's "alphabet"
    if not genotype.component_genes:
        # This should not happen, but as a failsafe:
        return RuleGene(action_type="IDLE")

    if action_type in ['ENABLE_RULE', 'DISABLE_RULE']:
        if not genotype.rule_genes: # Failsafe if no rules exist yet
             action_type = "IDLE"
             action_param = "self"
        else:
             action_param = random.choice(genotype.rule_genes).id # Target another rule
    else:
        action_param = random.choice(list(genotype.component_genes.keys())) # Target a component
    # --- END OF MODIFICATION ---
        

    action_value = random.random() * 5.0
    if action_type == "SET_STATE":
        action_param = f"state_{random.randint(0,2)}"
    elif action_type == "TRANSFER_ENERGY":
        action_param = "NEIGHBORS"
    
    elif action_type in ['SET_TIMER', 'MODIFY_TIMER']:
        action_param = random.choice(['pulse_A', 'pulse_B', 'phase_C']) # Give it some timer names
        if action_type == 'SET_TIMER':
            action_value = random.randint(5, 50) # Set timer duration
        else:
            action_value = random.choice([-1, 1, 5, -5]) # Modify by value
        # --- ADD THIS BLOCK ---
    elif action_type == 'EMIT_SIGNAL':
        action_param = random.choice(['signal_A', 'signal_B']) # Name of signal
        action_value = random.uniform(0.5, 2.0) # Strength of signal
# --- END OF ADDITION ---

    return RuleGene(
        conditions=conditions,
        action_type=action_type,
        action_param=action_param,
        action_value=action_value, # e.g., energy to transfer, value to set
        priority=random.randint(0, 10)
    )

def innovate_component(genotype: Optional[Genotype], settings: Dict, force_base: Optional[str] = None) -> ComponentGene:
    """
    Create a new, random building block (a new 'gene').
    This is how "silicon" or "plasma" life emerges.
    
    NEW 2.0: This function is completely rewritten to use the
    CHEMICAL_BASES_REGISTRY.
    """
    
    # --- 1. Select a Chemical Base ---
    if force_base:
        base_name = force_base
    else:
        # Use chemical bases allowed in settings
        allowed_bases = settings.get('chemical_bases', ['Carbon', 'Silicon'])
        if not allowed_bases: allowed_bases = ['Carbon'] # Failsafe
        base_name = random.choice(allowed_bases)
        
    base_template = CHEMICAL_BASES_REGISTRY.get(base_name, CHEMICAL_BASES_REGISTRY['Carbon'])

    # --- 2. Naming ---
    prefixes = ['Proto', 'Hyper', 'Neuro', 'Cryo', 'Xeno', 'Bio', 'Meta', 'Photo', 'Astro', 'Quantum']
    suffixes = ['Polymer', 'Crystal', 'Node', 'Shell', 'Core', 'Matrix', 'Membrane', 'Processor', 'Fluid', 'Weave']
    new_name = f"{random.choice(prefixes)}-{base_name}-{random.choice(suffixes)}_{random.randint(0, 99)}"
    
    # --- 3. Color ---
    h, s, v = base_template['color_hsv_range']
    color = colorsys.hsv_to_rgb(
        random.uniform(h[0], h[1]),
        random.uniform(s[0], s[1]),
        random.uniform(v[0], v[1])
    )
    color_hex = f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

    # --- 4. Properties (randomly assigned based on template) ---
    new_comp = ComponentGene(
        name=new_name,
        base_kingdom=base_name,
        color=color_hex
    )
    
    # --- Base properties from template ---
    new_comp.mass = random.uniform(base_template['mass_range'][0], base_template['mass_range'][1])
    new_comp.structural = random.uniform(0.1, 0.5) * random.choice([0, 0, 0, 1, 2]) * base_template.get('structural_mult', (1.0, 1.0))[0]
    new_comp.energy_storage = random.uniform(0.1, 0.5) * random.choice([0, 1, 2]) * base_template.get('energy_storage_mult', (1.0, 1.0))[0]
    
    # --- Biased properties ---
    props_with_bias = [
        'photosynthesis', 'chemosynthesis', 'thermosynthesis', 'conductance',
        'compute', 'motility', 'armor', 'sense_light', 'sense_minerals', 'sense_temp'
    ]
    
    for prop in props_with_bias:
        bias = base_template.get(f"{prop}_bias", 0.0)
        
        # Chance to gain this property is proportional to bias (min 5%)
        if random.random() < (abs(bias) + 0.05):
            base_val = random.uniform(0.5, 1.5)
            # Apply bias (e.g., bias of 0.8 means value is likely 0.8-1.5, bias of -0.2 means 0.0-0.8)
            val = np.clip(base_val + bias, 0, 5.0)
            setattr(new_comp, prop, val)

    # --- Final cleanup ---
    new_comp.mass = np.clip(new_comp.mass, 0.1, 5.0)
    
    return new_comp

def meta_innovate_condition_source(settings: Dict):
    """
    "Truly Infinite" Part 2: Inventing new senses.
    This function has a small chance to create a new, random
    sensory condition and add it to the global list.
    """
    if random.random() < settings.get('meta_innovation_rate', 0.005):
        sense_types = ['gradient', 'count', 'average', 'presence']
        sense_targets = ['energy', 'complexity', 'age', 'type']
        sense_scopes = ['N', 'S', 'E', 'W', 'Neighbors_R1', 'Neighbors_R2', 'Colony']
        
        new_sense = f"sense_{random.choice(sense_targets)}_{random.choice(sense_types)}_{random.choice(sense_scopes)}"
        
        if new_sense not in st.session_state.evolvable_condition_sources:
            st.session_state.evolvable_condition_sources.append(new_sense)
            st.toast(f"🧠 Meta-Innovation! Life has evolved a new sense: **{new_sense}**", icon="🧬")



def apply_physics_drift(settings: Dict):
    """
    "Truly Infinite" Part 3: Co-evolving the Gallery's Physics.
    
    This function has a very small chance to "mutate" the fundamental
    archetypes in the CHEMICAL_BASES_REGISTRY. This makes the
    very "physics" of what life *can* be co-evolve with the life itself.
    """
    if random.random() < settings.get('physics_drift_rate', 0.001):
        
        # Pick a random base to mutate
        try:
            base_name, base_template = random.choice(list(CHEMICAL_BASES_REGISTRY.items()))
        except IndexError:
            return # Registry is empty, shouldn't happen
            
        # Pick a random property to mutate
        prop_to_mutate = random.choice(list(base_template.keys()))
        
        drift_magnitude = np.random.normal(0, 0.05) # Small drift
        
        if prop_to_mutate.endswith('_range'):
            # Mutate a range tuple, e.g., 'mass_range': (0.5, 1.5)
            # We'll just drift the midpoint and keep the interval
            try:
                min_val, max_val = base_template[prop_to_mutate]
                mid_point = (min_val + max_val) / 2
                interval = (max_val - min_val)
                
                # Apply drift relative to the midpoint
                new_mid_point = mid_point + (drift_magnitude * mid_point)
                new_min = max(0.01, new_mid_point - interval/2) # Don't go below zero
                new_max = new_min + interval
                
                base_template[prop_to_mutate] = (new_min, new_max)
            except Exception:
                pass # Fail silently if it's not a (min, max) tuple
                
        elif prop_to_mutate.endswith('_bias'):
            # Mutate a bias float, e.g., 'photosynthesis_bias': 0.3
            try:
                current_bias = base_template[prop_to_mutate]
                new_bias = current_bias + drift_magnitude
                base_template[prop_to_mutate] = new_bias
            except Exception:
                pass # Fail silently if not a float
        
        if drift_magnitude != 0:
            st.toast(f"🌌 Physics Drift! Archetype '{base_name}' property '{prop_to_mutate}' has mutated.", icon="🌀")

            # --- NEW: Log this event to the Genesis Chronicle ---
            event_desc = f"The fundamental physical properties of the '{base_name}' chemical archetype have mutated. The property '{prop_to_mutate}' drifted, subtly altering the rules of chemistry and biology for all life based on it."
            st.session_state.genesis_events.append({
                'generation': st.session_state.history[-1]['generation'] if st.session_state.history else 0,
                'type': 'Physics Drift',
                'title': f"Physics Drift in '{base_name}'",
                'description': event_desc,
                'icon': '🌀'
            })

# ========================================================
#
# PART 6: VISUALIZATION (THE "EXHIBIT DISPLAY")
#
# ========================================================

def visualize_phenotype_2d(phenotype: Phenotype, grid: ExhibitGrid) -> go.Figure:
    """
    Creates a 2D heatmap visualization of the organism's body plan.
    """
    cell_data = np.full((grid.width, grid.height), np.nan)
    cell_text = [["" for _ in range(grid.height)] for _ in range(grid.width)]
    
    # Map component names to colors
    component_colors = {comp.name: comp.color for comp in phenotype.genotype.component_genes.values()}
    color_map = {}
    discrete_colors = []
    
    # Create a discrete colorscale
    unique_types = sorted(list(component_colors.keys()))
    if not unique_types:
        unique_types = ["default"]
        component_colors["default"] = "#FFFFFF"
        
    for i, comp_name in enumerate(unique_types):
        color_map[comp_name] = i
        discrete_colors.append(component_colors[comp_name])

    # Create a Plotly discrete colorscale
    dcolorsc = []
    n_colors = len(discrete_colors)
    if n_colors == 0:
        dcolorsc = [[0, "#000000"], [1, "#000000"]] # Failsafe
    elif n_colors == 1:
        dcolorsc = [[0, discrete_colors[0]], [1, discrete_colors[0]]]
    else:
        for i, color in enumerate(discrete_colors):
            val = i / (n_colors - 1)
            dcolorsc.append([val, color])

    for (x, y), cell in phenotype.cells.items():
        cell_data[x, y] = color_map.get(cell.component.name, 0)
        cell_text[x][y] = (
            f"<b>{cell.component.name}</b> (Base: {cell.component.base_kingdom})<br>"
            f"Energy: {cell.energy:.2f}<br>"
            f"Age: {cell.age}<br>"
            f"Mass: {cell.component.mass:.2f}<br>"
            f"Photosynthesis: {cell.component.photosynthesis:.2f}"
        )

    fig = go.Figure(data=go.Heatmap(
        z=cell_data,
        text=cell_text,
        hoverinfo="text",
        colorscale=dcolorsc,
        showscale=True,
        zmin=0,
        zmax=max(0, len(discrete_colors) - 1),
        colorbar=dict(
            tickvals=list(range(len(unique_types))),
            ticktext=unique_types
        )
    ))
    
    fig.update_layout(
        title=f"Phenotype: {phenotype.id} (Gen: {phenotype.genotype.generation})<br><sup>Kingdom: {phenotype.genotype.kingdom_id} | Cells: {len(phenotype.cells)} | Fitness: {phenotype.genotype.fitness:.4f}</sup>",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x"),
        height=500,
        margin=dict(l=20, r=20, t=80, b=20),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def visualize_fitness_landscape(history_df: pd.DataFrame):
    if history_df.empty or len(history_df) < 20:
        st.warning("Not enough data to render fitness landscape.")
        return
        
    st.markdown("### 3D Fitness Landscape: (Fitness vs. Complexity vs. Cell Count)")
    sample_size = min(len(history_df), 20000)
    df_sample = history_df.sample(n=sample_size)
    
    x_param = 'cell_count'
    y_param = 'complexity'
    z_param = 'fitness'
    
    # --- 1. Create the Fitness Surface ---
    if df_sample[x_param].nunique() < 2 or df_sample[y_param].nunique() < 2:
        st.warning("Not enough variance in population to create 3D landscape.")
        return
        
    x_bins = np.linspace(df_sample[x_param].min(), df_sample[x_param].max(), 30)
    y_bins = np.linspace(df_sample[y_param].min(), df_sample[y_param].max(), 30)

    df_sample['x_bin'] = pd.cut(df_sample[x_param], bins=x_bins, labels=False, include_lowest=True)
    df_sample['y_bin'] = pd.cut(df_sample[y_param], bins=y_bins, labels=False, include_lowest=True)
    grid = df_sample.groupby(['x_bin', 'y_bin'])[z_param].mean().unstack(level='x_bin')
    
    x_coords = (x_bins[:-1] + x_bins[1:]) / 2
    y_coords = (y_bins[:-1] + y_bins[1:]) / 2
    z_surface = grid.values

    surface_trace = go.Surface(
        x=x_coords, y=y_coords, z=z_surface,
        colorscale='cividis', opacity=0.6,
        name='Estimated Fitness Landscape',
    )

    # --- 2. Calculate Evolutionary Trajectories ---
    mean_trajectory = history_df.groupby('generation').agg({
        x_param: 'mean', y_param: 'mean', z_param: 'mean'
    }).reset_index()
    apex_trajectory = history_df.loc[history_df.groupby('generation')['fitness'].idxmax()]

    # --- 3. Create Trajectory Traces ---
    mean_trajectory_trace = go.Scatter3d(
        x=mean_trajectory[x_param], y=mean_trajectory[y_param], z=mean_trajectory[z_param],
        mode='lines', line=dict(color='red', width=8),
        name='Population Mean Trajectory'
    )
    apex_trajectory_trace = go.Scatter3d(
        x=apex_trajectory[x_param], y=apex_trajectory[y_param], z=apex_trajectory[z_param],
        mode='lines+markers', line=dict(color='cyan', width=4),
        name='Apex (Best) Trajectory'
    )

    # --- 4. Create Final Population Scatter ---
    final_gen_df = history_df[history_df['generation'] == history_df['generation'].max()]
    final_pop_trace = go.Scatter3d(
        x=final_gen_df[x_param], y=final_gen_df[y_param], z=final_gen_df[z_param],
        mode='markers',
        marker=dict(size=5, color=final_gen_df['fitness'], colorscale='Viridis', showscale=True),
        name='Final Population',
    )

    # --- 5. Assemble Figure ---
    fig = go.Figure(data=[surface_trace, mean_trajectory_trace, apex_trajectory_trace, final_pop_trace])
    fig.update_layout(
        title='<b>3D Fitness Landscape with Multi-Trajectory Analysis</b>',
        scene=dict(
            xaxis_title='Cell Count',
            yaxis_title='Genomic Complexity',
            zaxis_title='Fitness'
        ),
        height=700,
        margin=dict(l=0, r=0, b=0, t=60)
    )
    st.plotly_chart(fig, width='stretch', key="fitness_landscape_3d_museum")

def create_simulation_dashboard(history_df: pd.DataFrame, evolutionary_metrics_df: pd.DataFrame) -> go.Figure:
    """Comprehensive evolution analytics dashboard."""
    
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=(
            '<b>Fitness Evolution by Kingdom</b>',
            '<b>Phenotypic Trait Trajectories</b>',
            '<b>Final Population Fitness</b>',
            '<b>Kingdom Dominance Over Time</b>',
            '<b>Genetic Diversity (H)</b>',
            '<b>Phenotypic Divergence (σ)</b>',
            '<b>Selection Pressure (Δ) & Mutation Rate (μ)</b>',
            '<b>Complexity & Cell Count Growth</b>',
            '<b>Mean Organism Lifespan</b>'
        ),
        specs=[
            [{}, {}, {}],
            [{}, {}, {}],
            [{'secondary_y': True}, {'secondary_y': True}, {}]
        ],
        vertical_spacing=0.15,
        horizontal_spacing=0.1
    )
    
    # --- Plot 1: Fitness Evolution by Kingdom ---
    unique_kingdoms = history_df['kingdom_id'].unique()
    for i, kingdom in enumerate(unique_kingdoms):
        kingdom_data = history_df[history_df['kingdom_id'] == kingdom]
        mean_fitness = kingdom_data.groupby('generation')['fitness'].mean()
        plot_color = px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
        fig.add_trace(go.Scatter(x=mean_fitness.index, y=mean_fitness.values, mode='lines', name=kingdom, legendgroup=kingdom, line=dict(color=plot_color)), row=1, col=1)
    
    # --- Plot 2: Phenotypic Trait Trajectories ---
    mean_energy_prod = history_df.groupby('generation')['energy_production'].mean()
    mean_energy_cons = history_df.groupby('generation')['energy_consumption'].mean()
    fig.add_trace(go.Scatter(x=mean_energy_prod.index, y=mean_energy_prod.values, name='Mean Energy Prod.', line=dict(color='green')), row=1, col=2)
    fig.add_trace(go.Scatter(x=mean_energy_cons.index, y=mean_energy_cons.values, name='Mean Energy Cons.', line=dict(color='red')), row=1, col=2)

    # --- Plot 3: Final Population Fitness ---
    final_gen_df = history_df[history_df['generation'] == history_df['generation'].max()]
    if not final_gen_df.empty:
        fig.add_trace(go.Histogram(x=final_gen_df['fitness'], name='Fitness', marker_color='blue'), row=1, col=3)

    # --- Plot 4: Kingdom Dominance ---
    kingdom_counts = history_df.groupby(['generation', 'kingdom_id']).size().unstack(fill_value=0)
    kingdom_percentages = kingdom_counts.apply(lambda x: x / x.sum(), axis=1)
    for kingdom in kingdom_percentages.columns:
        fig.add_trace(go.Scatter(
            x=kingdom_percentages.index, y=kingdom_percentages[kingdom],
            mode='lines', name=kingdom,
            stackgroup='one', groupnorm='percent',
            showlegend=False, legendgroup=kingdom
        ), row=2, col=1)

    # --- Plot 5: Genetic Diversity ---
    if not evolutionary_metrics_df.empty:
        fig.add_trace(go.Scatter(
            x=evolutionary_metrics_df['generation'], y=evolutionary_metrics_df['diversity'],
            name='Diversity (H)', line=dict(color='purple')
        ), row=2, col=2)

    # --- Plot 6: Phenotypic Divergence ---
    pheno_divergence = history_df.groupby('generation')[['cell_count', 'complexity']].std().reset_index()
    fig.add_trace(go.Scatter(x=pheno_divergence['generation'], y=pheno_divergence['cell_count'], name='σ (Cell Count)'), row=2, col=3)
    fig.add_trace(go.Scatter(x=pheno_divergence['generation'], y=pheno_divergence['complexity'], name='σ (Complexity)'), row=2, col=3)

    # --- Plot 7: Selection Pressure & Mutation Rate ---
    if not evolutionary_metrics_df.empty:
        fig.add_trace(go.Scatter(x=evolutionary_metrics_df['generation'], y=evolutionary_metrics_df['selection_differential'], name='Selection Δ', line=dict(color='red')), secondary_y=False, row=3, col=1)
        fig.add_trace(go.Scatter(x=evolutionary_metrics_df['generation'], y=evolutionary_metrics_df['mutation_rate'], name='Mutation Rate μ', line=dict(color='orange', dash='dash')), secondary_y=True, row=3, col=1)

    # --- Plot 8: Complexity & Cell Count Growth ---
    arch_stats = history_df.groupby('generation')[['complexity', 'cell_count']].mean().reset_index()
    fig.add_trace(go.Scatter(x=arch_stats['generation'], y=arch_stats['complexity'], name='Mean Complexity', line=dict(color='cyan')), secondary_y=False, row=3, col=2)
    fig.add_trace(go.Scatter(x=arch_stats['generation'], y=arch_stats['cell_count'], name='Mean Cell Count', line=dict(color='magenta', dash='dash')), secondary_y=True, row=3, col=2)

    # --- Plot 9: Mean Organism Lifespan ---
    mean_lifespan = history_df.groupby('generation')['lifespan'].mean().reset_index()
    fig.add_trace(go.Scatter(x=mean_lifespan['generation'], y=mean_lifespan['lifespan'], name='Mean Lifespan', line=dict(color='gold')), row=3, col=3)

    # --- Layout and Axis Updates ---
    fig.update_layout(
        height=1200, showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_yaxes(title_text="Fitness", row=1, col=1)
    fig.update_yaxes(title_text="Mean Energy", row=1, col=2)
    fig.update_yaxes(title_text="Count", row=1, col=3)
    fig.update_yaxes(title_text="Population %", row=2, col=1)
    fig.update_yaxes(title_text="Diversity (H)", row=2, col=2)
    fig.update_yaxes(title_text="Std. Dev (σ)", row=2, col=3)
    fig.update_yaxes(title_text="Selection Δ", secondary_y=False, row=3, col=1)
    fig.update_yaxes(title_text="Mutation Rate μ", secondary_y=True, row=3, col=1)
    fig.update_yaxes(title_text="Complexity", secondary_y=False, row=3, col=2)
    fig.update_yaxes(title_text="Cell Count", secondary_y=True, row=3, col=2)
    fig.update_yaxes(title_text="Generations", row=3, col=3)
    
    return fig

def plot_fitness_vs_complexity(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot of fitness vs. complexity, colored by kingdom."""
    fig = px.scatter(
        df.sample(min(len(df), 5000)), 
        x='complexity', 
        y='fitness', 
        color='kingdom_id',
        title='Fitness vs. Complexity',
        hover_data=['generation', 'cell_count']
    )
    fig.update_layout(height=400)
    return fig

def plot_lifespan_vs_cell_count(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot of lifespan vs. cell count, colored by fitness."""
    fig = px.scatter(
        df.sample(min(len(df), 5000)),
        x='cell_count',
        y='lifespan',
        color='fitness',
        color_continuous_scale='Viridis',
        title='Lifespan vs. Cell Count',
        hover_data=['generation', 'complexity']
    )
    fig.update_layout(height=400)
    return fig

def plot_energy_dynamics(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot of energy production vs. consumption."""
    fig = px.scatter(
        df.sample(min(len(df), 5000)),
        x='energy_consumption',
        y='energy_production',
        color='fitness',
        color_continuous_scale='Plasma',
        title='Energy Production vs. Consumption',
        hover_data=['generation', 'lifespan']
    )
    fig.update_layout(height=400)
    return fig

def plot_complexity_density(df: pd.DataFrame, key: str) -> go.Figure:
    """2D histogram showing the density of organisms in the complexity/cell_count space."""
    fig = px.density_heatmap(
        df,
        x='complexity',
        y='cell_count',
        nbinsx=50, nbinsy=50,
        title='Density of Morphological Space'
    )
    fig.update_layout(height=400)
    return fig

def plot_fitness_violin_by_kingdom(df: pd.DataFrame, key: str) -> go.Figure:
    """Violin plot showing fitness distribution for each kingdom."""
    final_gen_df = df[df['generation'] == df['generation'].max()]
    if final_gen_df.empty:
        final_gen_df = df
    fig = px.violin(final_gen_df, x='kingdom_id', y='fitness', color='kingdom_id', box=True, points="all", title="Final Generation Fitness Distribution by Kingdom")
    fig.update_layout(height=400)
    return fig

def plot_complexity_vs_lifespan(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot of complexity vs. lifespan, colored by fitness."""
    fig = px.scatter(
        df.sample(min(len(df), 5000)),
        x='complexity',
        y='lifespan',
        color='fitness',
        color_continuous_scale='Inferno',
        title='Complexity vs. Lifespan',
        hover_data=['generation', 'cell_count']
    )
    fig.update_layout(height=400)
    return fig

def plot_energy_efficiency_over_time(df: pd.DataFrame, key: str) -> go.Figure:
    """Line plot of energy efficiency over generations."""
    df_copy = df.copy()
    df_copy['efficiency'] = df_copy['energy_production'] / (df_copy['energy_consumption'] + 1e-6)
    efficiency_by_gen = df_copy.groupby('generation')['efficiency'].mean().reset_index()
    fig = px.line(efficiency_by_gen, x='generation', y='efficiency', title='Mean Energy Efficiency Over Time')
    fig.update_layout(height=400)
    return fig

def plot_cell_count_dist_by_kingdom(df: pd.DataFrame, key: str) -> go.Figure:
    """Box plot of cell count distribution for each kingdom in the final generation."""
    final_gen_df = df[df['generation'] == df['generation'].max()]
    if final_gen_df.empty:
        final_gen_df = df
    fig = px.box(final_gen_df, x='kingdom_id', y='cell_count', color='kingdom_id', title="Final Generation Cell Count Distribution")
    fig.update_layout(height=400)
    return fig

def plot_lifespan_dist_by_kingdom(df: pd.DataFrame, key: str) -> go.Figure:
    """Violin plot of lifespan distribution for each kingdom in the final generation."""
    final_gen_df = df[df['generation'] == df['generation'].max()]
    if final_gen_df.empty:
        final_gen_df = df
    fig = px.violin(final_gen_df, x='kingdom_id', y='lifespan', color='kingdom_id', box=True, title="Final Generation Lifespan Distribution")
    fig.update_layout(height=400)
    return fig

def plot_complexity_vs_energy_prod(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot of complexity vs. energy production."""
    fig = px.scatter(
        df.sample(min(len(df), 5000)),
        x='complexity',
        y='energy_production',
        color='fitness',
        color_continuous_scale='Cividis',
        title='Complexity vs. Energy Production',
        hover_data=['generation', 'lifespan']
    )
    fig.update_layout(height=400)
    return fig

def plot_fitness_scatter_over_time(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot showing all organisms' fitness over generations."""
    fig = px.scatter(
        df.sample(min(len(df), 10000)),
        x='generation',
        y='fitness',
        color='kingdom_id',
        title='Population Fitness Landscape Over Time',
        hover_data=['cell_count', 'complexity']
    )
    fig.update_layout(height=400)
    return fig

def plot_elite_parallel_coords(df: pd.DataFrame, key: str) -> go.Figure:
    """Parallel coordinates plot for the top elite organisms of the final generation."""
    final_gen_df = df[df['generation'] == df['generation'].max()]
    if final_gen_df.empty:
        final_gen_df = df
    
    elites = final_gen_df.nlargest(min(len(final_gen_df), 100), 'fitness')
    if elites.empty:
        return go.Figure().update_layout(title="Not enough data for Parallel Coordinates Plot", height=400)

    fig = px.parallel_coordinates(
        elites,
        color="fitness",
        dimensions=['fitness', 'complexity', 'cell_count', 'lifespan', 'energy_production', 'energy_consumption'],
        color_continuous_scale=px.colors.sequential.Inferno,
        title="Trait Relationships of Elite Organisms"
    )
    fig.update_layout(height=400)
    return fig

# ========================================================
#
# PART 7.5: CUSTOM ANALYTICS PLOTS (NEW)
#
# ========================================================

def plot_fitness_vs_complexity(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot of fitness vs. complexity, colored by kingdom."""
    fig = px.scatter(
        df.sample(min(len(df), 5000)), 
        x='complexity', 
        y='fitness', 
        color='kingdom_id',
        title='Fitness vs. Complexity',
        hover_data=['generation', 'cell_count']
    )
    fig.update_layout(height=400)
    return fig

def plot_lifespan_vs_cell_count(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot of lifespan vs. cell count, colored by fitness."""
    fig = px.scatter(
        df.sample(min(len(df), 5000)),
        x='cell_count',
        y='lifespan',
        color='fitness',
        color_continuous_scale='Viridis',
        title='Lifespan vs. Cell Count',
        hover_data=['generation', 'complexity']
    )
    fig.update_layout(height=400)
    return fig

def plot_energy_dynamics(df: pd.DataFrame, key: str) -> go.Figure:
    """Scatter plot of energy production vs. consumption."""
    fig = px.scatter(
        df.sample(min(len(df), 5000)),
        x='energy_consumption',
        y='energy_production',
        color='fitness',
        color_continuous_scale='Plasma',
        title='Energy Production vs. Consumption',
        hover_data=['generation', 'lifespan']
    )
    fig.update_layout(height=400)
    return fig

def plot_complexity_density(df: pd.DataFrame, key: str) -> go.Figure:
    """2D histogram showing the density of organisms in the complexity/cell_count space."""
    fig = px.density_heatmap(
        df,
        x='complexity',
        y='cell_count',
        nbinsx=50, nbinsy=50,
        title='Density of Morphological Space'
    )
    fig.update_layout(height=400)
    return fig

def plot_fitness_violin_by_kingdom(df: pd.DataFrame, key: str) -> go.Figure:
    """Violin plot showing fitness distribution for each kingdom."""
    final_gen_df = df[df['generation'] == df['generation'].max()]
    if final_gen_df.empty:
        final_gen_df = df
    fig = px.violin(final_gen_df, x='kingdom_id', y='fitness', color='kingdom_id', box=True, points="all", title="Final Generation Fitness Distribution by Kingdom")
    fig.update_layout(height=400)
    return fig



def deserialize_genotype(geno_dict: Dict) -> Genotype:
    """Helper function to reconstruct a Genotype object from a dictionary."""
    try:
        # Reconstruct ComponentGene dict
        comp_genes_dict = geno_dict.get('component_genes', {})
        re_comp_genes = {}
        for comp_id, comp_dict in comp_genes_dict.items():
            # Use comp_id as the key, not comp_dict['name']
            re_comp_genes[comp_id] = ComponentGene(**comp_dict)
        geno_dict['component_genes'] = re_comp_genes
        
        # Reconstruct RuleGene list
        rule_genes_list = geno_dict.get('rule_genes', [])
        re_rule_genes = [RuleGene(**rule_dict) for rule_dict in rule_genes_list]
        geno_dict['rule_genes'] = re_rule_genes
        
        # Create the main Genotype object
        return Genotype(**geno_dict)
    except Exception as e:
        st.error(f"Error deserializing genotype: {e} | Data: {geno_dict.get('id', 'N/A')}")
        # Return a "dead" genotype
        return Genotype(id=geno_dict.get('id', 'error_id'), fitness=-1)

def deserialize_population(pop_data_list: List[Dict]) -> List[Genotype]:
    """Deserializes an entire population list from a JSON-friendly format."""
    reconstructed_pop = []
    for geno_dict in pop_data_list:
        reconstructed_pop.append(deserialize_genotype(geno_dict))
    return [g for g in reconstructed_pop if g.fitness != -1] # Filter out any broken ones

# ========================================================
#
# PART 7: THE STREAMLIT APP (THE "CURATOR'S CONSOLE")
#
# ========================================================

@dataclass
class RedQueenParasite:
    """A simple co-evolving digital parasite for the Red Queen dynamic."""
    target_kingdom_id: str = "Carbon"

def main():
    st.set_page_config(
        page_title="LIFE BEYOND II: The Museum of Alien Life",
        layout="wide",
        page_icon="🪐",
        initial_sidebar_state="expanded"
    )

    # --- DARK GREEN/BROWN/WHITE "TERRA" THEME ---
    st.markdown("""
        <style>
            /* --- Core App Styling --- */
            .stApp {
                background-color: #0D1117; /* Near-black */
                background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='%231A202C' fill-opacity='0.4'%3E%3Cpath d='M0 38.59l2.83-2.83 1.41 1.41L1.41 40H0v-1.41zM0 1.4l2.83 2.83 1.41-1.41L1.41 0H0v1.41zM38.59 40l-2.83-2.83 1.41-1.41L40 38.59V40h-1.41zM40 1.41l-2.83 2.83-1.41-1.41L38.59 0H40v1.41zM20 18.6l2.83-2.83 1.41 1.41L21.41 20l2.83 2.83-1.41 1.41L20 21.41l-2.83 2.83-1.41-1.41L18.59 20l-2.83-2.83 1.41-1.41L20 18.59z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
                background-size: cover;
                background-attachment: fixed;
            }

            /* --- Glassmorphism Containers --- */
            .block-container, [data-testid="stSidebar"], [data-testid="stExpander"], [data-testid="stTabs"] {
                background: rgba(15, 25, 15, 0.65); /* Dark green-black tint */
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border-radius: 15px;
                border: 1px solid rgba(67, 83, 52, 0.25); /* Subtle dark green/brown border */
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            }

            [data-testid="stSidebar"] {
                border-right: 1px solid rgba(67, 83, 52, 0.35);
            }

            [data-testid="stExpander"] {
                margin-bottom: 10px;
                border-color: rgba(67, 83, 52, 0.2);
            }

            /* --- Text & Titles --- */
            h1, h2, h3, h4, h5, h6 {
                background: -webkit-linear-gradient(45deg, #435334, #9E7676, #FAF3E3); /* Dark Green -> Brown -> Off-White */
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                text-shadow: 0 0 8px rgba(250, 243, 227, 0.1);
            }

            p, div, span, li, label, .st-emotion-cache-16idsys p {
                color: #E2E8F0 !important; /* Light gray text for readability */
                text-shadow: 0 0 3px rgba(0, 0, 0, 0.5);
            }
            
            /* --- Interactive Elements --- */
            .stButton>button {
                border-radius: 10px;
                border: 1px solid rgba(67, 83, 52, 0.7);
                background-color: rgba(67, 83, 52, 0.2);
                color: #9EB384; /* Muted green accent */
                transition: all 0.3s ease;
            }
            .stButton>button:hover {
                background-color: rgba(67, 83, 52, 0.4);
                border-color: #9EB384;
                box-shadow: 0 0 15px rgba(158, 179, 132, 0.3);
            }

        </style>
    """, unsafe_allow_html=True)

    if 'password_attempts' not in st.session_state:
        st.session_state.password_attempts = 0
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False
    # --- ADD THIS BLOCK ---
    # Initialize state for lazy-loading tabs
    if 'show_specimen_viewer' not in st.session_state:
        st.session_state.show_specimen_viewer = False
    if 'show_elite_analysis' not in st.session_state:
        st.session_state.show_elite_analysis = False
    if 'show_genesis_chronicle' not in st.session_state:
        st.session_state.show_genesis_chronicle = False
    if 'dashboard_visible' not in st.session_state:
        st.session_state.dashboard_visible = False
    if 'analytics_lab_visible' not in st.session_state:
        st.session_state.analytics_lab_visible = False
    
    # --- Password Protection ---
    # --- Password Protection (Updated) ---
    def check_password_on_change():
        # 1. Try to fetch the password safely
        correct_pass = None
        try:
            # Check for nested format [passwords] -> app_password
            if "passwords" in st.secrets and "app_password" in st.secrets["passwords"]:
                correct_pass = st.secrets["passwords"]["app_password"]
            # Check for top-level format -> app_password
            elif "app_password" in st.secrets:
                correct_pass = st.secrets["app_password"]
        except (KeyError, AttributeError, FileNotFoundError):
            pass # correct_pass remains None

        # 2. Handle missing password configuration
        if correct_pass is None:
            st.warning("⚠️ Debug Mode: No 'app_password' found in secrets. Access allowed for testing.")
            # Uncomment the line below to enforce a hard crash if you prefer:
            # st.error("FATAL ERROR: Please add 'app_password' to .streamlit/secrets.toml"); st.stop()
            st.session_state.password_correct = True
            return

        # 3. Validate Input
        if st.session_state.password_input_key == correct_pass:
            st.session_state.password_correct = True
            st.session_state.password_attempts = 0
        else:
            st.session_state.password_correct = False
            if st.session_state.password_input_key: 
                st.session_state.password_attempts += 1
    
    if st.session_state.password_attempts >= 3:
        st.error("Maximum login attempts exceeded. The application is locked.")
        st.stop()
        
    if not st.session_state.password_correct:
        # If we are already logged in via Debug Mode, skip this
        if not st.session_state.get('password_correct', False):
            st.text_input(
                "Password", 
                type="password", 
                on_change=check_password_on_change,
                key="password_input_key"
            )
            
            if st.session_state.password_attempts > 0:
                st.error("Password incorrect")

            st.info("Enter password to access the Museum of Universal Life.")
            st.stop()

    # --- Database Setup ---
    db = TinyDB('museum_of_life_db.json', indent=4)
    settings_table = db.table('settings')
    results_table = db.table('results')
    exhibit_presets_table = db.table('exhibit_presets')

    # --- Load previous state ---
    if 'state_loaded' not in st.session_state:
        st.session_state.settings = settings_table.get(doc_id=1) or {}
        
        saved_results = results_table.get(doc_id=1)
        if saved_results:
            st.session_state.history = saved_results.get('history', [])
            st.session_state.evolutionary_metrics = saved_results.get('evolutionary_metrics', [])
            st.toast("Loaded previous session data.", icon="💾")
        else:
            st.session_state.history = []
            st.session_state.evolutionary_metrics = []
            
        st.session_state.current_population = None
        st.session_state.exhibit_presets = {doc['name']: doc for doc in exhibit_presets_table.all()}
        
        st.session_state.evolvable_condition_sources = [
            'self_energy', 'self_age', 'env_light', 'env_minerals', 'env_temp',
            'neighbor_count_empty', 'neighbor_count_self', 'neighbor_count_other',
            'self_type'
        ]
        
        if 'genesis_events' not in st.session_state:
            st.session_state.genesis_events = []
            
        st.session_state.state_loaded = True

    # --- Robustness checks for all required keys on *every* run ---
    if 'settings' not in st.session_state: st.session_state.settings = settings_table.get(doc_id=1) or {}
    if 'history' not in st.session_state: st.session_state.history = []
    if 'evolutionary_metrics' not in st.session_state: st.session_state.evolutionary_metrics = []
    if 'current_population' not in st.session_state: st.session_state.current_population = None
    if 'exhibit_presets' not in st.session_state: st.session_state.exhibit_presets = {doc['name']: doc for doc in exhibit_presets_table.all()}
    if 'evolvable_condition_sources' not in st.session_state:
        st.session_state.evolvable_condition_sources = [
            'self_energy', 'self_age', 'env_light', 'env_minerals', 'env_temp',
            'neighbor_count_empty', 'neighbor_count_self', 'neighbor_count_other',
            'self_type'
        ]
    if 'genesis_events' not in st.session_state: st.session_state.genesis_events = []


    # ===============================================
    # --- THE "CURATOR'S CONSOLE" SIDEBAR ---
    # ===============================================
    
    st.sidebar.markdown('<h1 style="text-align: center;">🌌<br>LIFE BEYOND II</h1>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    s = copy.deepcopy(st.session_state.settings)

    if st.sidebar.button("Reset Curator's Console to Defaults", width='stretch', key="reset_defaults_button"):
        st.session_state.settings.clear()
        st.toast("Curator's Console reset to defaults!", icon="📡")
        time.sleep(1)
        st.rerun()

    if st.sidebar.button("Decommission Exhibit & Restart", width='stretch', key="clear_state_button"):
        db.truncate()
        st.session_state.clear()
        st.toast("Cleared all archived data. The exhibit has been reset.", icon="💥")
        time.sleep(1)
        st.rerun()
        
    with st.sidebar.expander("🔭 Exhibit Hall Manager (Your Curated Collections)", expanded=True):
        presets = st.session_state.exhibit_presets
        preset_names = ["<Select a Collection to Load>"] + list(presets.keys())
        
        c1, c2 = st.columns(2)
        with c1:
            new_preset_name = st.text_input("New Collection Name", placeholder="e.g., 'Titan Methane Seas'")
        with c2:
            st.write(" ") # Spacer
            if st.button("📦 Archive Current Exhibit", width='stretch'):
                if new_preset_name:
                    current_settings_snapshot = s 
                    current_history = st.session_state.get('history', [])
                    current_metrics = st.session_state.get('evolutionary_metrics', [])
                    
                    current_pop_data = []
                    if st.session_state.get('current_population'):
                        try:
                            current_pop_data = [asdict(g) for g in st.session_state.current_population]
                        except Exception as e:
                            st.warning(f"Could not serialize population: {e}")

                    preset_data_to_save = {
                        'name': new_preset_name,
                        'settings': current_settings_snapshot,
                        'history': current_history,
                        'evolutionary_metrics': current_metrics,
                        'genesis_events': st.session_state.get('genesis_events', []),
                        'final_population_genotypes': current_pop_data
                    }
                    
                    presets[new_preset_name] = preset_data_to_save
                    exhibit_presets_table.upsert(preset_data_to_save, Query().name == new_preset_name)
                    
                    st.toast(f"Collection '{new_preset_name}' (with results) archived!", icon="📦")
                    st.session_state.exhibit_presets = presets
                    st.rerun()
                else:
                    st.warning("Please enter a name for your collection.")

        selected_preset = st.selectbox("Load from Curated Collection", options=preset_names, index=0)
        
        if selected_preset != "<Select a Collection to Load>":
            c1, c2 = st.columns(2)
            if c1.button("LOAD COLLECTION", width='stretch', type="primary"):
                preset_to_load = presets[selected_preset]
                
                loaded_settings = copy.deepcopy(preset_to_load['settings'])
                st.session_state.settings = loaded_settings
                
                if settings_table.get(doc_id=1):
                    settings_table.update(loaded_settings, doc_ids=[1])
                else:
                    settings_table.insert(loaded_settings)
                    
                st.session_state.history = preset_to_load.get('history', [])
                st.session_state.evolutionary_metrics = preset_to_load.get('evolutionary_metrics', [])
                st.session_state.genesis_events = preset_to_load.get('genesis_events', [])
                
                pop_data = preset_to_load.get('final_population_genotypes', [])
                loaded_population = []
                if pop_data:
                    try:
                        for geno_dict in pop_data:
                            comp_genes_dict = geno_dict.get('component_genes', {})
                            re_comp_genes = {}
                            for comp_id, comp_dict in comp_genes_dict.items():
                                re_comp_genes[comp_id] = ComponentGene(**comp_dict)
                            geno_dict['component_genes'] = re_comp_genes
                            
                            rule_genes_list = geno_dict.get('rule_genes', [])
                            re_rule_genes = [RuleGene(**rule_dict) for rule_dict in rule_genes_list]
                            geno_dict['rule_genes'] = re_rule_genes
                            
                            loaded_population.append(Genotype(**geno_dict))
                    except Exception as e:
                        st.error(f"Error de-serializing population: {e}")
                        
                st.session_state.current_population = loaded_population
                
                results_to_save = {
                    'history': st.session_state.history,
                    'evolutionary_metrics': st.session_state.evolutionary_metrics,
                }
                if results_table.get(doc_id=1):
                    results_table.update(results_to_save, doc_ids=[1])
                else:
                    results_table.insert(results_to_save)

                st.toast(f"Loaded collection '{selected_preset}' (with results)!", icon="🌠")
                st.rerun()
            if c2.button("DELETE", width='stretch'):
                del presets[selected_preset] 
                exhibit_presets_table.remove(Query().name == selected_preset)
                st.session_state.exhibit_presets = presets
                st.toast(f"Deleted collection '{selected_preset}'.", icon="🔥")
                st.rerun()
                    
        st.sidebar.markdown("---")
        st.sidebar.markdown("#### 📥 Load Exhibit from Archive")
        uploaded_file = st.sidebar.file_uploader(
            "Upload your 'exhibit_archive.zip' file",
            type=["json", "zip"],
            key="checkpoint_uploader"
        )
        
        if st.sidebar.button("LOAD FROM UPLOADED FILE", width='stretch', key="load_checkpoint_button"):
            if uploaded_file is not None:
                try:
                    data = None
                    
                    if uploaded_file.name.endswith('.zip'):
                        st.toast("Unzipping archive... Please wait.", icon="🗜️")
                        mem_zip = io.BytesIO(uploaded_file.getvalue())
                        
                        with zipfile.ZipFile(mem_zip, 'r') as zf:
                            json_filename = None
                            for f in zf.namelist():
                                if f.endswith('.json') and not f.startswith('__MACOSX'):
                                    json_filename = f
                                    break
                            
                            if json_filename:
                                st.toast(f"Found '{json_filename}' inside zip.", icon="📑")
                                with zf.open(json_filename) as f:
                                    data = json.load(f)
                            else:
                                st.error("No .json file found inside the .zip archive.")
                    
                    elif uploaded_file.name.endswith('.json'):
                        st.toast("Loading .json file...", icon="📑")
                        data = json.loads(uploaded_file.getvalue())
                    
                    if data is not None:
                        st.toast("Archive found... Loading state...", icon="⏳")
                        
                        loaded_settings = data.get('settings', {})
                        st.session_state.settings = loaded_settings
                        if settings_table.get(doc_id=1):
                            settings_table.update(loaded_settings, doc_ids=[1])
                        else:
                            settings_table.insert(loaded_settings)
                        
                        st.session_state.history = data.get('history', [])
                        st.session_state.evolutionary_metrics = data.get('evolutionary_metrics', [])
                        st.session_state.genesis_events = data.get('genesis_events', [])
                        st.session_state.current_population = deserialize_population(data.get('final_population_genotypes', []))
                        st.session_state.gene_archive = deserialize_population(data.get('full_gene_archive', []))
                        
                        if 'final_physics_constants' in data:
                            CHEMICAL_BASES_REGISTRY.clear()
                            CHEMICAL_BASES_REGISTRY.update(data['final_physics_constants'])
                        
                        if 'final_evolved_senses' in data:
                            st.session_state.evolvable_condition_sources = data['final_evolved_senses']

                        st.session_state.seen_kingdoms = set(h['kingdom_id'] for h in st.session_state.history)
                        st.session_state.crossed_complexity_thresholds = set(
                            int(t) for e in st.session_state.genesis_events 
                            if e['type'] == 'Complexity Leap' 
                            for t in [10, 25, 50, 100, 200, 500] 
                            if str(t) in e['title']
                        )
                        st.session_state.last_dominant_kingdom = st.session_state.history[-1]['kingdom_id'] if st.session_state.history else None
                        st.session_state.has_logged_colonial_emergence = any(e['type'] == 'Major Transition' and 'Colonial Life' in e['title'] for e in st.session_state.genesis_events)
                        st.session_state.has_logged_philosophy_divergence = any(e['type'] == 'Cognitive Leap' and 'Philosophical Divergence' in e['title'] for e in st.session_state.genesis_events)
                        st.session_state.has_logged_computation_dawn = any(e['type'] == 'Complexity Leap' and 'Computation' in e['title'] for e in st.session_state.genesis_events)
                        st.session_state.has_logged_first_communication = any(e['type'] == 'Major Transition' and 'Communication' in e['title'] for e in st.session_state.genesis_events)
                        st.session_state.has_logged_memory_invention = any(e['type'] == 'Cognitive Leap' and 'Memory' in e['title'] for e in st.session_state.genesis_events)

                        results_to_save = {
                            'history': st.session_state.history,
                            'evolutionary_metrics': st.session_state.evolutionary_metrics,
                        }
                        if results_table.get(doc_id=1):
                            results_table.update(results_to_save, doc_ids=[1])
                        else:
                            results_table.insert(results_to_save)
                        
                        st.toast("✅ Archive Loaded! You can now 'Extend Simulation'.", icon="🛰️")
                        
                        last_gen = 0
                        if st.session_state.history:
                            last_gen = st.session_state.history[-1]['generation']
                        
                        st.sidebar.success(f"**Archive Loaded Successfully!**")
                        st.sidebar.info(
                            f"""
                            - **Last Epoch:** {last_gen}
                            - **Final Population:** {len(st.session_state.current_population)} organisms
                            - **Fossil Record:** {len(st.session_state.gene_archive)} genotypes
                            - **Evolved Senses:** {len(st.session_state.evolvable_condition_sources)}
                            <br><br>You are ready to click **'🧬 Extend Exhibit Simulation'** to proceed from Epoch {last_gen + 1}.
                            """
                        )
                        
                        st.rerun()
                    
                    elif data is None and not uploaded_file.name.endswith('.zip'):
                        st.error("File is not a .zip or .json file.")
                        
                except Exception as e:
                    st.error(f"Failed to load archive: {e}")
            else:
                st.warning("Please upload a file first.")
        
    st.sidebar.markdown("### 🪐 Wing 3: The Sculpting Hand of Environment")
    with st.sidebar.expander("Fundamental Physical Laws", expanded=False):
        st.markdown("Set the fundamental, unchanging laws of this exhibit's environment.")
        s['gravity'] = st.slider("Gravity", 0.0, 20.0, s.get('gravity', 9.8), 0.1, help="Influences motility cost.")
        s['em_coupling'] = st.slider("Electromagnetic Coupling", 0.1, 2.0, s.get('em_coupling', 1.0), 0.05, help="Scales energy from light (photosynthesis).")
        s['thermo_efficiency'] = st.slider("Thermodynamic Efficiency", 0.1, 1.0, s.get('thermo_efficiency', 0.25), 0.01, help="Base energy loss from all actions (entropy).")
        s['planck_scale'] = st.slider("Computational Planck Scale", 1, 10, s.get('planck_scale', 1), 1, help="Minimum 'granularity' of computation (conceptual).")
        s['cosmic_radiation'] = st.slider("Cosmic Radiation (Mutation)", 0.0, 1.0, s.get('cosmic_radiation', 0.1), 0.01, help="Baseline environmental mutation pressure.")
        s['universe_age_factor'] = st.slider("Environmental Age Factor", 0.1, 10.0, s.get('universe_age_factor', 1.0), 0.1, help="Scales how fast resources change or decay.")
        s['dark_energy_pressure'] = st.slider("Dark Energy Pressure (Grid Expansion)", -1.0, 1.0, s.get('dark_energy_pressure', 0.0), 0.01, help="Conceptual: Positive values push organisms apart.")
        s['information_density_limit'] = st.slider("Information Density Limit", 1, 100, s.get('information_density_limit', 50), 1, help="Max complexity per cell (conceptual).")
        s['fundamental_constant_drift'] = st.slider("Fundamental Constant Drift", 0.0, 0.01, s.get('fundamental_constant_drift', 0.0), 0.0001, help="Rate at which constants like 'gravity' slowly change over eons.")
        
    with st.sidebar.expander("Exhibit Environment & Resources", expanded=False):
        st.markdown("Define the exhibit environment itself.")
        s['grid_width'] = st.slider("Grid Width", 50, 500, s.get('grid_width', 100), 10)
        s['grid_height'] = st.slider("Grid Height", 50, 500, s.get('grid_height', 100), 10)
        s['light_intensity'] = st.slider("Light Energy Intensity", 0.0, 5.0, s.get('light_intensity', 1.0), 0.1)
        s['mineral_richness'] = st.slider("Mineral Richness", 0.0, 5.0, s.get('mineral_richness', 1.0), 0.1)
        s['water_abundance'] = st.slider("Water Abundance", 0.0, 5.0, s.get('water_abundance', 1.0), 0.1)
        s['temp_equator'] = st.slider("Equator Temperature (°C)", -100, 200, s.get('temp_equator', 30), 1)
        s['temp_pole'] = st.slider("Pole Temperature (°C)", -200, 100, s.get('temp_pole', -20), 1)
        s['resource_diffusion_rate'] = st.slider("Resource Diffusion Rate", 0.0, 0.5, s.get('resource_diffusion_rate', 0.01), 0.005)
        
    st.sidebar.markdown("### 🌱 Wing 1: The Carbon Gallery (Seeding)")
    with st.sidebar.expander("The Primordial Soup", expanded=False):
        s['initial_population'] = st.slider("Initial Population Size", 10, 500, s.get('initial_population', 50), 10)
        s['zygote_energy'] = st.slider("Initial Zygote Energy", 1.0, 100.0, s.get('zygote_energy', 10.0), 1.0)
        s['new_cell_energy'] = st.slider("New Cell Energy", 0.1, 5.0, s.get('new_cell_energy', 1.0), 0.1, help="Energy given to a newly grown cell.")
        s['development_steps'] = st.slider("Development Steps (Embryogeny)", 10, 200, s.get('development_steps', 50), 5)
        s['max_organism_lifespan'] = st.slider("Max Organism Lifespan (Epochs)", 50, 1000, s.get('max_organism_lifespan', 200), 10)
        all_bases = list(CHEMICAL_BASES_REGISTRY.keys())
        saved_bases = s.get('chemical_bases')

        if not saved_bases or len(saved_bases) < 20:
            default_selection = all_bases
        else:
            default_selection = saved_bases

        s['chemical_bases'] = st.multiselect("Allowed Chemistries (Kingdoms)", 
                                             all_bases, 
                                             default_selection)

    
    st.sidebar.markdown("### ⚖️ Fundamental Pressures of Life")
    with st.sidebar.expander("Defining 'Fitness' for this Exhibit", expanded=False):
        st.markdown("Define what 'success' means for an exhibit. (Normalized)")
        s['w_lifespan'] = st.slider("Weight: Longevity", 0.0, 1.0, s.get('w_lifespan', 0.4), 0.01)
        s['w_efficiency'] = st.slider("Weight: Energy Efficiency", 0.0, 1.0, s.get('w_efficiency', 0.3), 0.01)
        s['w_reproduction'] = st.slider("Weight: Reproduction", 0.0, 1.0, s.get('w_reproduction', 0.3), 0.01)
        s['w_complexity_pressure'] = st.slider("Pressure: Complexity", -3.0, 3.0, s.get('w_complexity_pressure', 0.0), 0.01, help="Push for/against complexity.")
        s['w_motility_pressure'] = st.slider("Pressure: Motility", 0.0, 1.0, s.get('w_motility_pressure', 0.0), 0.01, help="Reward for evolving movement.")
        s['w_compute_pressure'] = st.slider("Pressure: Intelligence", 0.0, 1.0, s.get('w_compute_pressure', 0.0), 0.01, help="Reward for evolving 'compute' genes.")
        s['reproduction_energy_threshold'] = st.slider("Reproduction Energy Threshold", 10.0, 200.0, s.get('reproduction_energy_threshold', 50.0))
        s['reproduction_bonus'] = st.slider("Reproduction Bonus", 0.0, 2.0, s.get('reproduction_bonus', 0.5))

    st.sidebar.markdown("### 🧬 The Rules of Evolution")
    with st.sidebar.expander("Genetic Operators", expanded=True):
        st.number_input(
                "Epochs to Simulate",
                min_value=10,
                max_value=50000,
                step=10,
                value=s.get('num_generations', 200),
                key="generation_simulator_sync_key",
            )
            
        s['num_generations'] = st.session_state.generation_simulator_sync_key
        s['selection_pressure'] = st.slider("Selection Pressure", 0.1, 0.9, s.get('selection_pressure', 0.4), 0.05)
        s['mutation_rate'] = st.slider("Base Mutation Rate (μ)", 0.01, 0.9, s.get('mutation_rate', 0.2), 0.01)
        s['crossover_rate'] = st.slider("Crossover Rate", 0.0, 1.0, s.get('crossover_rate', 0.7), 0.05)
        s['innovation_rate'] = st.slider("Rule Innovation Rate (σ)", 0.01, 0.5, s.get('innovation_rate', 0.05), 0.01, help="Rate of creating new GRN rules.")
        s['component_innovation_rate'] = st.slider("Component Innovation Rate (α)", 0.0, 0.1, s.get('component_innovation_rate', 0.01), 0.001, help="Rate of inventing new chemical components.")
        s['meta_innovation_rate'] = st.slider("Meta-Innovation Rate (Sensor)", 0.0, 0.01, s.get('meta_innovation_rate', 0.005), 0.0001, help="Rate of inventing new *types* of senses.")
        s['max_rule_conditions'] = st.slider("Max Rule Conditions", 1, 5, s.get('max_rule_conditions', 3), 1)

    with st.sidebar.expander("Ecosystem & Speciation Dynamics", expanded=False):
        s['enable_speciation'] = st.checkbox("Enable Speciation", s.get('enable_speciation', True), help="Group similar organisms into 'species' to protect innovation.")
        s['compatibility_threshold'] = st.slider("Compatibility Threshold", 1.0, 50.0, s.get('compatibility_threshold', 10.0), 0.5, help="Genomic distance to be in the same species.")
        s['niche_competition_factor'] = st.slider("Niche Competition", 0.0, 5.0, s.get('niche_competition_factor', 1.5), 0.1, help="How strongly members of the same species compete (fitness sharing).")
        s['gene_flow_rate'] = st.slider("Gene Flow (Hybridization)", 0.0, 0.2, s.get('gene_flow_rate', 0.01), 0.005, help="Chance for crossover between different species.")
        s['reintroduction_rate'] = st.slider("Fossil Record Reintroduction", 0.0, 0.5, s.get('reintroduction_rate', 0.05), 0.01, help="Chance to reintroduce an ancient genotype from the archive.")
        s['max_archive_size'] = st.slider("Max Gene Archive Size", 1000, 1000000, s.get('max_archive_size', 100000), 5000)
    
    with st.sidebar.expander("Advanced Biological Principles", expanded=False):
        s['enable_baldwin'] = st.checkbox("Enable Baldwin Effect (Learning)", s.get('enable_baldwin', True), help="Organisms can 'learn' (e.g., adapt to local temp) in their lifetime. Favors adaptable genotypes.")
        s['enable_epigenetics'] = st.checkbox("Enable Epigenetic Inheritance", s.get('enable_epigenetics', True), help="Learned adaptations are partially passed to offspring (Lamarckian).")
        s['enable_endosymbiosis'] = st.checkbox("Enable Endosymbiosis (Merging)", s.get('enable_endosymbiosis', True), help="Rare event where one organism absorbs another, merging their genomes.")
        s['endosymbiosis_rate'] = st.slider("Endosymbiosis Rate", 0.0, 0.1, s.get('endosymbiosis_rate', 0.005), 0.001)

    with st.sidebar.expander("☄️ Environmental Events & Cataclysms", expanded=False):
        s['enable_cataclysms'] = st.checkbox("Enable Cataclysms", s.get('enable_cataclysms', True), help="Enable rare, random mass extinction events.")
        s['cataclysm_probability'] = st.slider("Cataclysm Probability", 0.0, 0.5, s.get('cataclysm_probability', 0.01), 0.005, help="Per-epoch chance of a cataclysm.")
        s['cataclysm_extinction_severity'] = st.slider("Extinction Severity", 0.1, 1.0, s.get('cataclysm_extinction_severity', 0.9), 0.05, help="Percentage of population wiped out.")
        s['cataclysm_landscape_shift_magnitude'] = st.slider("Landscape Shift Magnitude", 0.0, 1.0, s.get('cataclysm_landscape_shift_magnitude', 0.5), 0.05, help="How drastically resource maps change.")
        s['post_cataclysm_hypermutation_multiplier'] = st.slider("Hypermutation Multiplier", 1.0, 10.0, s.get('post_cataclysm_hypermutation_multiplier', 2.0), 0.5, help="Mutation spike after cataclysm (adaptive radiation).")
        s['post_cataclysm_hypermutation_duration'] = st.slider("Hypermutation Duration (Epochs)", 0, 50, s.get('post_cataclysm_hypermutation_duration', 10), 1, help="Number of epochs the mutation spike lasts.")
        s['enable_red_queen'] = st.checkbox("Enable Red Queen (Co-evolution)", s.get('enable_red_queen', True), help="A co-evolving 'parasite' targets the most common organism type, forcing an arms race.")
        s['red_queen_virulence'] = st.slider("Parasite Virulence", 0.0, 1.0, s.get('red_queen_virulence', 0.15), 0.05, help="Fitness penalty inflicted by the parasite.")
        s['red_queen_adaptation_speed'] = st.slider("Parasite Adaptation Speed", 0.0, 1.0, s.get('red_queen_adaptation_speed', 0.2), 0.05)
        
    with st.sidebar.expander("🔬 Meta-Evolution & Self-Configuration (ADVANCED)", expanded=False):
        st.markdown("**DANGER:** Evolve the laws of evolution itself.")
        s['enable_hyperparameter_evolution'] = st.checkbox("Enable Hyperparameter Co-evolution", s.get('enable_hyperparameter_evolution', False))
        s['evolvable_params'] = st.multiselect("Evolvable Parameters", 
            ['mutation_rate', 'crossover_rate', 'innovation_rate', 'niche_competition_factor', 'selection_pressure', 'meta_innovation_rate'], 
            s.get('evolvable_params', ['mutation_rate']))
        s['hyper_mutation_rate'] = st.slider("Meta-Mutation Rate", 0.0, 0.2, s.get('hyper_mutation_rate', 0.05), 0.01)
        s['enable_genetic_code_evolution'] = st.checkbox("Enable Genetic Code Evolution", s.get('enable_genetic_code_evolution', False), help="Allow invention of new *types* of rules and conditions.")
        s['enable_objective_evolution'] = st.checkbox("Enable Objective Evolution (Autotelic)", s.get('enable_objective_evolution', False), help="Allow organisms to evolve their *own* fitness goals.")
        st.markdown("---")
        st.markdown("**THE TRUE INFINITE:** Evolve the laws of physics.")
        s['enable_physics_drift'] = st.checkbox("Enable Physics Co-evolution", s.get('enable_physics_drift', False), help="Allow the archetypes in the CHEMICAL_BASES_REGISTRY to 'mutate' over time.")
        s['physics_drift_rate'] = st.slider("Physics Drift Rate", 0.0, 0.01, s.get('physics_drift_rate', 0.001), 0.0001, help="Per-epoch chance of a random physical archetype mutating.")

    with st.sidebar.expander("🌠 Deep Evolutionary Physics & Information Dynamics (EXPANDED)", expanded=False):
        st.markdown("**THEORETICAL APEX:** Model deep physical and informational principles.")
        s['enable_deep_physics'] = st.checkbox("Enable Deep Physics Engine", s.get('enable_deep_physics', False))
        
        st.markdown("##### 1. Information-Theoretic Dynamics")
        s['kolmogorov_pressure'] = st.slider("Kolmogorov Pressure (Simplicity)", 0.0, 1.0, s.get('kolmogorov_pressure', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['pred_info_bottleneck'] = st.slider("Predictive Info Bottleneck", 0.0, 1.0, s.get('pred_info_bottleneck', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['causal_emergence_factor'] = st.slider("Causal Emergence Factor", 0.0, 1.0, s.get('causal_emergence_factor', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['phi_target'] = st.slider("Integrated Information (Φ) Target", 0.0, 1.0, s.get('phi_target', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['fep_gradient'] = st.slider("Free Energy Principle (FEP) Gradient", 0.0, 1.0, s.get('fep_gradient', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['self_modelling_capacity_bonus'] = st.slider("Self-Modelling Capacity Bonus", 0.0, 1.0, s.get('self_modelling_capacity_bonus', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['epistemic_uncertainty_drive'] = st.slider("Epistemic Uncertainty Drive", 0.0, 1.0, s.get('epistemic_uncertainty_drive', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        
        st.markdown("##### 2. Thermodynamics of Life")
        s['landauer_efficiency'] = st.slider("Landauer Limit Efficiency", 0.0, 1.0, s.get('landauer_efficiency', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['metabolic_power_law'] = st.slider("Metabolic Power Law (Exponent)", 0.5, 1.5, s.get('metabolic_power_law', 0.75), 0.01, disabled=not s['enable_deep_physics'])
        s['heat_dissipation_constraint'] = st.slider("Heat Dissipation Constraint", 0.0, 1.0, s.get('heat_dissipation_constraint', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['homeostatic_pressure'] = st.slider("Homeostatic Regulation Pressure", 0.0, 1.0, s.get('homeostatic_pressure', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['structural_decay_rate'] = st.slider("Structural Integrity Decay Rate", 0.0, 0.1, s.get('structural_decay_rate', 0.0), 0.001, disabled=not s['enable_deep_physics'])
        s['jarzynski_equality_deviation'] = st.slider("Jarzynski Equality Deviation", 0.0, 1.0, s.get('jarzynski_equality_deviation', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['negentropy_import_cost'] = st.slider("Negentropy Import Cost", 0.0, 1.0, s.get('negentropy_import_cost', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        
        st.markdown("##### 3. Quantum & Field-Theoretic Effects")
        s['quantum_annealing_fluctuation'] = st.slider("Quantum Tunneling Fluctuation", 0.0, 1.0, s.get('quantum_annealing_fluctuation', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['holographic_constraint'] = st.slider("Holographic Principle Constraint", 0.0, 1.0, s.get('holographic_constraint', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['symmetry_breaking_pressure'] = st.slider("Symmetry Breaking Pressure", 0.0, 1.0, s.get('symmetry_breaking_pressure', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['wave_function_coherence_bonus'] = st.slider("Wave Function Coherence Bonus", 0.0, 1.0, s.get('wave_function_coherence_bonus', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['zpf_extraction_rate'] = st.slider("Zero-Point Field Extraction Rate", 0.0, 1.0, s.get('zpf_extraction_rate', 0.0), 0.01, disabled=not s['enable_deep_physics'])

        st.markdown("##### 4. Topological & Geometric Constraints")
        s['manifold_adherence'] = st.slider("Manifold Hypothesis Adherence", 0.0, 1.0, s.get('manifold_adherence', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['homological_scaffold_stability'] = st.slider("Homological Scaffold Stability", 0.0, 1.0, s.get('homological_scaffold_stability', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['fractal_dimension_target'] = st.slider("Fractal Dimension Target", 1.0, 3.0, s.get('fractal_dimension_target', 1.0), 0.05, disabled=not s['enable_deep_physics'])
        s['hyperbolic_embedding_factor'] = st.slider("Hyperbolic Embedding Factor", 0.0, 1.0, s.get('hyperbolic_embedding_factor', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['small_world_bias'] = st.slider("Small-World Network Bias", 0.0, 1.0, s.get('small_world_bias', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['scale_free_exponent'] = st.slider("Scale-Free Network Exponent", 2.0, 4.0, s.get('scale_free_exponent', 2.0), 0.05, disabled=not s['enable_deep_physics'])
        s['brane_leakage_rate'] = st.slider("Brane Leakage Rate (Hyper-Dim)", 0.0, 1.0, s.get('brane_leakage_rate', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        
        st.markdown("##### 5. Cognitive & Agency Pressures")
        s['curiosity_drive'] = st.slider("Curiosity Drive (Information Gap)", 0.0, 1.0, s.get('curiosity_drive', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['world_model_accuracy'] = st.slider("World Model Accuracy Pressure", 0.0, 1.0, s.get('world_model_accuracy', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['tom_emergence_pressure'] = st.slider("Theory of Mind (ToM) Pressure", 0.0, 1.0, s.get('tom_emergence_pressure', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['cognitive_dissonance_penalty'] = st.slider("Cognitive Dissonance Penalty", 0.0, 1.0, s.get('cognitive_dissonance_penalty', 0.0), 0.01, disabled=not s['enable_deep_physics'])
        s['prospect_theory_bias'] = st.slider("Prospect Theory Bias (Risk)", -1.0, 1.0, s.get('prospect_theory_bias', 0.0), 0.05, disabled=not s['enable_deep_physics'])
        s['symbol_grounding_constraint'] = st.slider("Symbol Grounding Constraint", 0.0, 1.0, s.get('symbol_grounding_constraint', 0.0), 0.01, disabled=not s['enable_deep_physics'])

    with st.sidebar.expander("🌌 Advanced Algorithmic Frameworks (EXPANDED)", expanded=False):
        s['enable_advanced_frameworks'] = st.checkbox("Enable Advanced Frameworks Engine", s.get('enable_advanced_frameworks', False), help="DANGER: Apply priors from abstract math and logic.")
        st.markdown("##### 1. Computational Logic & Metamathematics")
        s['chaitin_omega_bias'] = st.slider("Chaitin's Omega Bias", 0.0, 1.0, s.get('chaitin_omega_bias', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['godel_incompleteness_penalty'] = st.slider("Gödelian Incompleteness Penalty", 0.0, 1.0, s.get('godel_incompleteness_penalty', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['turing_completeness_bonus'] = st.slider("Turing Completeness Bonus", 0.0, 1.0, s.get('turing_completeness_bonus', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['lambda_calculus_isomorphism'] = st.slider("Lambda Calculus Isomorphism", 0.0, 1.0, s.get('lambda_calculus_isomorphism', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['busy_beaver_limitation'] = st.slider("Busy Beaver Limitation", 0.0, 1.0, s.get('busy_beaver_limitation', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])

        st.markdown("##### 2. Advanced Statistical Learning Theory")
        s['pac_bayes_bound_minimization'] = st.slider("PAC-Bayes Bound Minimization", 0.0, 1.0, s.get('pac_bayes_bound_minimization', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['vc_dimension_constraint'] = st.slider("VC Dimension Constraint", 0.0, 1.0, s.get('vc_dimension_constraint', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['rademacher_complexity_penalty'] = st.slider("Rademacher Complexity Penalty", 0.0, 1.0, s.get('rademacher_complexity_penalty', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['causal_inference_engine_bonus'] = st.slider("Causal Inference Engine Bonus", 0.0, 1.0, s.get('causal_inference_engine_bonus', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])

        st.markdown("##### 3. Morphogenetic Engineering (Artificial Embryogeny)")
        s['reaction_diffusion_activator_rate'] = st.slider("Reaction-Diffusion Activator", 0.0, 1.0, s.get('reaction_diffusion_activator_rate', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['reaction_diffusion_inhibitor_rate'] = st.slider("Reaction-Diffusion Inhibitor", 0.0, 1.0, s.get('reaction_diffusion_inhibitor_rate', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['morphogen_gradient_decay'] = st.slider("Morphogen Gradient Decay", 0.0, 1.0, s.get('morphogen_gradient_decay', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['cell_adhesion_factor'] = st.slider("Cell Adhesion Factor", 0.0, 1.0, s.get('cell_adhesion_factor', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['hox_gene_expression_control'] = st.slider("Hox Gene Expression Control", 0.0, 1.0, s.get('hox_gene_expression_control', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['gastrulation_topology_target'] = st.slider("Gastrulation Topology Target", 0.0, 1.0, s.get('gastrulation_topology_target', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])

        st.markdown("##### 4. Collective Intelligence & Socio-Cultural Dynamics")
        s['stigmergy_potential_factor'] = st.slider("Stigmergy Potential (Indirect Comm.)", 0.0, 1.0, s.get('stigmergy_potential_factor', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['quorum_sensing_threshold'] = st.slider("Quorum Sensing Threshold", 0.0, 1.0, s.get('quorum_sensing_threshold', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['cultural_transmission_rate'] = st.slider("Cultural Transmission (Memetics)", 0.0, 1.0, s.get('cultural_transmission_rate', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['division_of_labor_incentive'] = st.slider("Division of Labor Incentive", 0.0, 1.0, s.get('division_of_labor_incentive', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['memetic_virulence_factor'] = st.slider("Memetic Virulence Factor", 0.0, 1.0, s.get('memetic_virulence_factor', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['groupthink_penalty'] = st.slider("Groupthink Penalty", 0.0, 1.0, s.get('groupthink_penalty', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])

        st.markdown("##### 5. Advanced Game Theory & Economic Models")
        s['hawk_dove_strategy_ratio'] = st.slider("Hawk-Dove Strategy Ratio", 0.0, 1.0, s.get('hawk_dove_strategy_ratio', 0.5), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['ultimatum_game_fairness_pressure'] = st.slider("Ultimatum Game Fairness Pressure", 0.0, 1.0, s.get('ultimatum_game_fairness_pressure', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['principal_agent_alignment_bonus'] = st.slider("Principal-Agent Alignment Bonus", 0.0, 1.0, s.get('principal_agent_alignment_bonus', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['tragedy_of_commons_penalty'] = st.slider("Tragedy of Commons Penalty", 0.0, 1.0, s.get('tragedy_of_commons_penalty', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        
        st.markdown("##### 6. Advanced Neuromodulation (Conceptual)")
        s['dopamine_reward_prediction_error'] = st.slider("Dopaminergic RPE Modulation", 0.0, 1.0, s.get('dopamine_reward_prediction_error', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['serotonin_uncertainty_signal'] = st.slider("Serotonergic Uncertainty Signal", 0.0, 1.0, s.get('serotonin_uncertainty_signal', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['acetylcholine_attentional_gain'] = st.slider("Cholinergic Attentional Gain", 0.0, 1.0, s.get('acetylcholine_attentional_gain', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['qualia_binding_efficiency'] = st.slider("Qualia Binding Efficiency", 0.0, 1.0, s.get('qualia_binding_efficiency', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        
        st.markdown("##### 7. Abstract Algebra & Category Theory Priors")
        s['group_theory_symmetry_bonus'] = st.slider("Group Theory Symmetry Bonus", 0.0, 1.0, s.get('group_theory_symmetry_bonus', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['category_theory_functorial_bonus'] = st.slider("Category Theory Functorial Bonus", 0.0, 1.0, s.get('category_theory_functorial_bonus', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['monad_structure_bonus'] = st.slider("Monad Structure Bonus", 0.0, 1.0, s.get('monad_structure_bonus', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])
        s['sheaf_computation_consistency'] = st.slider("Sheaf Computation Consistency", 0.0, 1.0, s.get('sheaf_computation_consistency', 0.0), 0.01, disabled=not s['enable_advanced_frameworks'])

    with st.sidebar.expander("✨ Alternate Deep Physics & Info-Dynamics (EXPERIMENTAL)", expanded=False):
        st.markdown("**THEORETICAL APEX 2:** Model alternate deep physical principles.")
        s['enable_deep_physics_alt'] = st.checkbox("Enable Alternate Deep Physics", s.get('enable_deep_physics_alt', False))
        
        st.markdown("##### 1. Alternate Info-Theoretic Dynamics")
        s['alt_kolmogorov_pressure'] = st.slider("Alt. Kolmogorov Pressure", 0.0, 1.0, s.get('alt_kolmogorov_pressure', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_pred_info_bottleneck'] = st.slider("Alt. Predictive Info Bottleneck", 0.0, 1.0, s.get('alt_pred_info_bottleneck', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_causal_emergence_factor'] = st.slider("Alt. Causal Emergence Factor", 0.0, 1.0, s.get('alt_causal_emergence_factor', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_phi_target'] = st.slider("Alt. Integrated Information (Φ) Target", 0.0, 1.0, s.get('alt_phi_target', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_fep_gradient'] = st.slider("Alt. Free Energy Principle (FEP) Gradient", 0.0, 1.0, s.get('alt_fep_gradient', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_self_modelling_capacity_bonus'] = st.slider("Alt. Self-Modelling Capacity Bonus", 0.0, 1.0, s.get('alt_self_modelling_capacity_bonus', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_epistemic_uncertainty_drive'] = st.slider("Alt. Epistemic Uncertainty Drive", 0.0, 1.0, s.get('alt_epistemic_uncertainty_drive', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        
        st.markdown("##### 2. Alternate Thermodynamics of Life")
        s['alt_landauer_efficiency'] = st.slider("Alt. Landauer Limit Efficiency", 0.0, 1.0, s.get('alt_landauer_efficiency', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_metabolic_power_law'] = st.slider("Alt. Metabolic Power Law (Exponent)", 0.5, 1.5, s.get('alt_metabolic_power_law', 0.75), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_heat_dissipation_constraint'] = st.slider("Alt. Heat Dissipation Constraint", 0.0, 1.0, s.get('alt_heat_dissipation_constraint', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_homeostatic_pressure'] = st.slider("Alt. Homeostatic Regulation Pressure", 0.0, 1.0, s.get('alt_homeostatic_pressure', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_structural_decay_rate'] = st.slider("Alt. Structural Integrity Decay Rate", 0.0, 0.1, s.get('alt_structural_decay_rate', 0.0), 0.001, disabled=not s['enable_deep_physics_alt'])
        s['alt_jarzynski_equality_deviation'] = st.slider("Alt. Jarzynski Equality Deviation", 0.0, 1.0, s.get('alt_jarzynski_equality_deviation', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_negentropy_import_cost'] = st.slider("Alt. Negentropy Import Cost", 0.0, 1.0, s.get('alt_negentropy_import_cost', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        
        st.markdown("##### 3. Alternate Quantum & Field-Theoretic Effects")
        s['alt_quantum_annealing_fluctuation'] = st.slider("Alt. Quantum Tunneling Fluctuation", 0.0, 1.0, s.get('alt_quantum_annealing_fluctuation', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_holographic_constraint'] = st.slider("Alt. Holographic Principle Constraint", 0.0, 1.0, s.get('alt_holographic_constraint', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_symmetry_breaking_pressure'] = st.slider("Alt. Symmetry Breaking Pressure", 0.0, 1.0, s.get('alt_symmetry_breaking_pressure', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_wave_function_coherence_bonus'] = st.slider("Alt. Wave Function Coherence Bonus", 0.0, 1.0, s.get('alt_wave_function_coherence_bonus', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])
        s['alt_zpf_extraction_rate'] = st.slider("Alt. Zero-Point Field Extraction Rate", 0.0, 1.0, s.get('alt_zpf_extraction_rate', 0.0), 0.01, disabled=not s['enable_deep_physics_alt'])

    with st.sidebar.expander("👽 Co-evolution & Embodiment Dynamics", expanded=False):
        st.markdown("Simulate arms races and the evolution of 'bodies'.")
        s['enable_adversarial_coevolution'] = st.checkbox("Enable Adversarial Critic Population", s.get('enable_adversarial_coevolution', False))
        s['critic_population_size'] = st.slider("Critic Population Size", 5, 100, s.get('critic_population_size', 10), 5)
        s['adversarial_fitness_weight'] = st.slider("Adversarial Fitness Weight", 0.0, 1.0, s.get('adversarial_fitness_weight', 0.2), 0.05)
        s['enable_morphological_coevolution'] = st.checkbox("Enable Morphological Co-evolution", s.get('enable_morphological_coevolution', False))
        s['cost_per_module'] = st.slider("Metabolic Cost per Cell", 0.0, 0.1, s.get('cost_per_module', 0.01), 0.001)
        s['bilateral_symmetry_bonus'] = st.slider("Bilateral Symmetry Bonus", 0.0, 0.5, s.get('bilateral_symmetry_bonus', 0.0), 0.01)
        s['segmentation_bonus'] = st.slider("Segmentation Bonus", 0.0, 0.5, s.get('segmentation_bonus', 0.0), 0.01)

    with st.sidebar.expander("✨ Multi-Level Selection (Major Transitions)", expanded=False):
        st.markdown("Evolve colonies and 'superorganisms'.")
        s['enable_multi_level_selection'] = st.checkbox("Enable Multi-Level Selection (MLS)", s.get('enable_multi_level_selection', False))
        s['colony_size'] = st.slider("Colony Size", 5, 50, s.get('colony_size', 10), 5)
        s['group_fitness_weight'] = st.slider("Group Fitness Weight (Altruism)", 0.0, 1.0, s.get('group_fitness_weight', 0.3), 0.05)
        s['selfishness_suppression_cost'] = st.slider("Selfishness Suppression Cost", 0.0, 0.2, s.get('selfishness_suppression_cost', 0.05), 0.01)
        s['caste_specialization_bonus'] = st.slider("Caste Specialization Bonus", 0.0, 0.5, s.get('caste_specialization_bonus', 0.1), 0.01)

    with st.sidebar.expander("🗄️ Curation & Archive Management", expanded=False):
        s['experiment_name'] = st.text_input("Exhibit Name", s.get('experiment_name', 'Primordial Run'))
        s['random_seed'] = st.number_input("Random Seed", -1, value=s.get('random_seed', 42), help="-1 for random.")
        s['enable_early_stopping'] = st.checkbox("Enable Early Stopping", s.get('enable_early_stopping', True))
        s['early_stopping_patience'] = st.slider("Early Stopping Patience", 5, 100, s.get('early_stopping_patience', 25))
        s['num_ranks_to_display'] = st.slider("Number of Elite Ranks to Display", 1, 10, s.get('num_ranks_to_display', 3))

    with st.sidebar.expander("📊 Custom Analytics Lab", expanded=False):
        st.markdown("Configure the custom analytics laboratory.")
        s['num_custom_plots'] = st.slider("Number of Custom Plots", 0, 12, s.get('num_custom_plots', 1), 1)
        
    st.sidebar.markdown("---")

    with st.sidebar.expander("📖 The Curator's Compendium: A Guide to Infinite Life", expanded=False):
        
        st.markdown(
            """
            ### **PART I: A BEGINNER'S GUIDE TO CURATION**
            
            Welcome, Curator. You have been given a "Curator's Console"—a set of dials that define the fundamental laws of a new exhibit. Your goal is to bring life into this void and nurture it from a simple, primordial soup into a complex, diverse ecosystem for display.
            
            This guide will walk you through handling your first exhibit and then mastering the advanced principles of "infinite" evolution.
            
            ---
            
            #### **Section 1.1: Your First "Genesis Event"**
            
            The core loop of this museum is simple: **Tweak, Simulate, Observe.**
            
            1.  **Do Nothing.** For your very first exhibit, the best choice is to change nothing at all. The default settings are a good starting point.
            2.  **Simulate:** Find the **"🚀 BEGIN SIMULATION"** button at the top of the sidebar. This will begin the simulation.
            3.  **Observe:** As the simulation runs, you will see the **"📈 Simulation Dashboard"** on the main page come to life. This is the "book of life" for your exhibit, showing you the average fitness, complexity, and population of your new creatures.
            4.  **Meet Your Creatures:** When the run is complete, click the **"🔬 Specimen Viewer"** tab. Here you will see the "phenotypes" (the body plans) of the organisms that evolved. They are the first lifeforms in your new reality.
            
            You have just completed your first act of curation.
            
            ---
            
            #### **Section 1.2: Reading the Book of Life**
            
            The main screen gives you three critical views:
            
            * **📈 Simulation Dashboard:** This is your high-level overview. The most important chart is **"Kingdom Dominance Over Time."** You will often see one color (e.g., 'Carbon') completely take over. This is called **convergence,** and it's the enemy of diversity. The **"3D Fitness Landscape"** shows you the "peaks" that evolution is trying to climb.
            
            * **🔬 Specimen Viewer:** This is your microscope. It shows you the physical bodies of your most successful organisms. You can see their **"Component Composition"** (what they're made of) and their **"Genetic Regulatory Network (GRN)"** (the "code" or "DNA" that built them).
            
            * **🧬 Elite Lineage Analysis:** This is your "Hall of Fame." It shows you the *best* organism from each **Kingdom** (e.g., the best 'Carbon' life, the best 'Silicon' life, etc.). This is the best place to find and analyze the most interesting and diverse creatures that emerged.
            
            ---
            
            #### **Section 1.3: Playing Curator (Your First Experiment)**
            
            Now you are ready for your first true experiment.
            
            1.  Go to the sidebar and open the **"Grid & Resource Distribution"** expander.
            2.  Find the **"Light Energy Intensity"** slider and move it all the way to the maximum.
            3.  Find the **"Mineral Richness"** slider and move it all the way to the *minimum*.
            
            You have just created an exhibit that is *drowning* in light but *starving* for minerals.
            
            Hit **"🚀 BEGIN SIMULATION"** again.
            
            Now, go to the **"🔬 Specimen Viewer."** Your new organisms will look completely different. They will have evolved to have massive `photosynthesis` values and almost zero `chemosynthesis`. Their body plans will be different. Their GRNs will be different.
            
            You have just performed your first act of *curation* by shaping the evolutionary pressures of your exhibit.
            
            ---
            
            ### **PART II: THE PATH TO INFINITY (A TREATISE ON EMERGENT COMPLEXITY)**
            
            You will soon discover a problem. After a few runs, all your creatures look the same. You'll get simple, 10-cell blobs. Every. Single. Time.
            
            This is the **"Convergence Trap."** Evolution is lazy. It will *always* find the simplest, "good enough" solution and stop.
            
            Your goal as a Curator is to *fight convergence* and *force novelty.* You must create an exhibit that *rewards* complexity and *punishes* boredom. This is how you achieve "truly infinite" forms.
            
            ---
            
            #### **Section 2.1: The Engine of Creation (Mastering Innovation)**
            
            You must give your organisms the "building blocks" of complexity.
            
            * **The "Words" (`component_innovation_rate`):** This is the rate at which life *invents new body parts.* If this is zero, your organisms will *never* evolve beyond the basic "Struct" and "Energy" cells. Increasing this allows them to invent `Neuro-Gel` (brains), `Bio-Steel` (armor), or `Cryo-Fluid` (heat processors) from the chemical bases you allow.
            
            * **The "Senses" (`meta_innovation_rate`):** This is the most "infinite" tool you have. It's the rate at which life *invents new senses.* Life cannot evolve eyes if it has not first "invented" the concept of `sense_light`. Life cannot evolve brains if it has not invented `sense_neighbor_complexity`. This dial creates entirely new logical pathways for the GRN, enabling true, unpredicted evolution.
            
            * **The "Elements" (`chemical_bases`):** Why stick to 'Carbon'? Enable **'Silicon', 'Plasma', 'Void', and 'Psionic'**. This allows for the emergence of entirely alien kingdoms. You cannot get silicon-based life if you do not add silicon to the primordial soup.
            
            ---
            
            #### **Section 2.2: The "Why" of Life (Rewarding Complexity)**
            
            Giving life building blocks is not enough. You must give it a *reason* to use them.
            
            * **The Prime Directive (`w_complexity_pressure`):** This is your **most important dial.** By default, it's at `0.0`. This means evolution *does not care* about complexity. A 5-cell blob that survives is just as "fit" as a 500-cell brain-creature.
            * **Set this to a positive value (e.g., `0.2`).** You are now *explicitly telling your exhibit* that complexity is a goal. You are adding a direct fitness bonus to any organism that evolves a more complex GRN and body plan. This is how you pay your organisms to evolve brains.
            
            * **The "Time" (`development_steps`):** A complex, 500-cell creature cannot grow in 50 steps. If this value is too low, you are *artificially selecting for simple blobs* because they are the only things that can finish "growing" before the simulation stops them. **Increase this to 100 or 150** to give complex embryos time to gestate.
            
            ---
            
            #### **Section 2.3: The "Shakedown" (Waging War on Boredom)**
            
            Your exhibit is now primed for complexity. But the "Convergence Trap" is strong. You must actively *destabilize* your exhibit to force it out of its rut.
            
            * **Tool 1: The "Parasite" (`enable_red_queen`):** This is your **#1 weapon against boredom.** When enabled, a digital "parasite" emerges that *constantly adapts to hunt the most common, dominant lifeform.*
            * Suddenly, being a simple, common blob is a death sentence. It creates a "Red Queen's Race" where life must *constantly* evolve new forms just to survive. This is the single fastest way to create a 'Cambrian Explosion' of diversity.
            
            * **Tool 2: The "Asteroid" (`enable_cataclysms`):** This enables random, periodic mass extinction events. A "boring" exhibit, dominated by one blob, will be wiped out. This allows the few, weird, experimental survivors to "inherit the earth" and repopulate the empty world. This is called "adaptive radiation" and it's how you get explosive new growth.
            
            * **Tool 3: The "Sanctuary" (`enable_speciation`):** This is a *protective* tool. It groups similar organisms into "species." This is crucial because it *protects* a brand-new, "weird" lifeform (e.g., the first creature with a 'Psionic' sense) from having to compete with the 10,000 hyper-optimized "Carbon" blobs. It gives innovation a safe harbor to develop.
            
            ---
            
            #### **Section 2.4: The "Curator-Mode" Levers (Evolving Evolution Itself)**
            
            These are the most advanced, dangerous, and powerful dials you possess. Here, you stop just *guiding* evolution and start *evolving the laws of evolution itself.*
            
            * **`enable_objective_evolution`:** This lets organisms *evolve their own fitness goals.* You are no longer the one defining "success." You might get a "philosopher" species that evolves to value `w_complexity_pressure` above all else, creating complex, beautiful, useless forms. You might get a "berserker" species that evolves to value only reproduction. This creates radical diversity in *strategy*.
            
            * **`enable_hyperparameter_evolution`:** This lets organisms *evolve their own mutation rates.* You will see organisms in stable environments evolve *low* mutation rates to protect their success, while organisms in chaotic, Red Queen-driven environments will evolve *high* mutation rates to adapt faster.
            
            * **`enable_physics_drift`:** This is the ultimate "infinite" tool. When enabled, the very *laws of physics* will slowly mutate over eons. The `CHEMICAL_BASES_REGISTRY` itself will change. The "mass_range" of 'Carbon' might increase. The "thermosynthesis_bias" of 'Plasma' might invert.
            * This means life can *never* find one single, perfect solution. The very ground beneath its feet is shifting. It is forced to adapt, innovate, and evolve... truly, infinitely.

            
            ---
            ---

            ### **PART III: THE NEW CODES OF LIFE (MASTERING BIZARRE GENETICS)**

            You have successfully upgraded the very "language" of genetics in your exhibit. Your organisms are no longer limited to simple, reactive logic. You have given them the tools for true computation.

            But what did you *actually* do?

            #### **Section 3.1: You Gave Life MEMORY (Proposal A: Timers)**

            * **The Old Limit:** Your cells had no concept of time. They were "goldfish" with no memory, only reacting to the present moment. They couldn't run a sequence of events, like "first grow a stem, *then* grow a leaf."
            * **The New Power (Temporal Logic):** By adding `SET_TIMER` and `timer_` conditions, you've given cells an **internal clock**.
            * **What It Unlocks (Oscillators & Sequences):** A GRN can now evolve logic like:
                * `IF timer_pulse == 0 THEN GROW("Struct") AND SET_TIMER("pulse", 10)`
                * This creates an **oscillator**. The organism will grow in 10-tick "bursts," creating segmented body plans (like a worm or a tree ring) instead of a simple blob.
                * It also allows **developmental stages**: `IF self_age < 3 THEN SET_TIMER("phase_B", 5)`... `IF timer_phase_B == 1 THEN DIFFERENTIATE("Neuro-Gel")`. This cell *waits* 5 ticks, then becomes a brain.

            #### **Section 3.2: You Gave Life LOGIC (Proposal B: Cascades)**

            * **The Old Limit:** Your GRN was a "flat list." Every rule was checked on every tick. It was a simple checklist, not a program.
            * **The New Power (Genetic Cascades):** By adding `ENABLE_RULE` and `DISABLE_RULE`, you've turned your flat list into a **computational network**. Rules can now *trigger other rules*.
            * **What It Unlocks (Genetic Switches & Programs):** This is the core of real genetics. You can now evolve:
                * **A "Genetic Switch":** `IF self_age < 5 THEN GROW("Struct") AND DISABLE_RULE("this_rule") AND ENABLE_RULE("adult_rule")`
                * This is a one-way path. The "embryo" rule runs, builds the foundation, then *permanently switches itself off* and "wakes up" the "adult" logic.
                * You can now evolve feedback loops, logic gates, and complex programs where one gene (rule) controls the expression of 10 others.

            #### **Section 3.3: You Gave Life SENSES (Proposal C: Signaling)**

            * **The Old Limit:** Your cells were "deaf and blind" to each other. A cell knew its *neighbor* existed, but it had no idea what that neighbor was *thinking* or *doing*. They couldn't coordinate to build a pattern.
            * **The New Power (Morphogenesis):** By adding `EMIT_SIGNAL` and `signal_` conditions, you've given cells a way to **talk to each other**. This is **morphogenesis**: the creation of shape.
            * **What It Unlocks (Reaction-Diffusion & Patterns):** You've unlocked the logic behind spots, stripes, and organs. A GRN can now evolve:
                * `Rule 1: IF self_type == "Core" THEN EMIT_SIGNAL("inhibitor", 1.0)`
                * `Rule 2: IF signal_inhibitor > 0.5 THEN DIFFERENTIATE("Shell")`
                * This simple logic creates a "Shell" cell *around* every "Core" cell, forming a boundary. This is how you get layers, skins, and self-organizing structures. You've given your cells the power to create **Turing Patterns**.

            ### **FINAL COMMANDMENT: USE YOUR NEW POWER**

            This new, complex "language" of life is powerful, but it's also *expensive* for evolution to use. It will be "lazy" and *avoid* using these tools unless you force it.

            You **must** use your Curator's Console to create evolutionary pressure.
            * **Turn ON `enable_red_queen`:** This punishes simple, common GRNs.
            * **Turn UP `w_complexity_pressure`:** This *rewards* organisms for evolving complex, bizarre GRNs.

            Combine your new code with these settings, and you will finally force life to evolve the truly alien and intelligent forms you've been looking for. Now go, and curate.
            """
        )

    with st.sidebar.expander("🔬 A Researcher's Guide to the GRN Encyclopedia", expanded=False):
        st.markdown(
            """
            This guide explains the meaning and scientific significance of each of the 16 unique
            GRN plots. Each plot is a different mathematical 'lens' to view the same 
            genetic network, and each lens reveals different, hidden truths about the 
            organism's underlying logic.
            
            ---
            
            ### Part I: The Force-Directed (Physics) Layouts 🕸️
            
            **Overall Significance:** These plots reveal the 'natural' clusters and communities
            within the network. They treat nodes like magnets repelling each other and
            edges like springs pulling them together. They are the best views for
            answering: **"Which genes and rules naturally work together?"**
            
            * **GRN 1: Default Spring (`nx.spring_layout`)**
                * **What it is:** The standard physics simulation. It's a "baseline" view of the graph's natural clustering.
                * **Significance:** This is your first look. It quickly shows you the main, obvious clusters of genes and rules. If the graph looks like a "hairball," it means the network is very dense.
            
            * **GRN 2: Kamada-Kawai (`nx.kamada_kawai_layout`)**
                * **What it is:** A different physics model that tries to make the visual distance between nodes proportional to their "path distance" (how many steps it takes to get from one to the other).
                * **Significance:** This layout is often much cleaner and more symmetrical than the default. It is *excellent* for revealing the core **backbone and symmetry** of a network.
            
            * **GRN 9: Tight Spring (`k=0.1`)**
                * **What it is:** A `spring_layout` where the "repulsion" force is very high (low `k`).
                * **Significance:** This layout smashes clusters tightly together. It's the perfect tool for seeing **how dense** a cluster is and identifying its "core" nodes, which will be packed into the very center.
            
            * **GRN 10: Loose Spring (`k=2.0`)**
                * **What it is:** A `spring_layout` where "repulsion" is very low (high `k`).
                * **Significance:** This layout spreads the entire graph out. It's fantastic for untangling complex "hairballs" and clearly seeing **long-range connections** between distant clusters that would otherwise overlap.
            
            * **GRN 12: Settled Spring (`iterations=200`)**
                * **What it is:** A `spring_layout` that runs the physics simulation for 200 iterations instead of the default 50.
                * **Significance:** This shows a more "final" and stable version of GRN 1. It's less random and often produces a more reliable structure, as the nodes have had more time to "settle" into their optimal positions.
            
            * **GRN 15: Graphviz NEATO (`prog='neato'`)**
                * **What it is:** This uses the powerful, external Graphviz engine to run a "spring" physics model.
                * **Significance:** This is a "second opinion" from a different physics engine. `neato` is often superior to the `networkx` layouts for large, messy, "real-world" graphs, producing a very clean and readable result.
            
            * **GRN 16: Alternate Seed (`seed=99`)**
                * **What it is:** The same as GRN 1, but with a different random starting position.
                * **Significance:** This is a crucial **sanity check**. If this plot looks *completely different* from GRN 1, it tells you the network is complex and has many different "stable" layouts. If it looks similar, it means the structure is very strong and robust.

            ---

            ### Part II: The Structural (Geometric) Layouts 🏗️
            
            **Overall Significance:** These plots *ignore* natural physics and instead
            force the nodes into specific, pre-defined shapes. This is a powerful
            technique for revealing patterns that physics-based layouts hide. They answer:
            **"Are there non-obvious patterns or long-range connections?"**
            
            * **GRN 3: Circular Layout (`nx.circular_layout`)**
                * **What it is:** Arranges all nodes in a perfect circle.
                * **Significance:** This is the *ultimate* plot for seeing **"cross-cutting" connections**. A gene (edge) that cuts directly across the center of the circle is a very important, non-obvious link connecting two parts of the network that *seem* unrelated.
            
            * **GRN 4: Random Layout (`nx.random_layout`)**
                * **What it is:** Pure chaos. It places all nodes in a random scatter-plot.
                * **Significance:** This seems useless, but it's a vital scientific control! This is your "null hypothesis"—it shows what the network looks like with *zero* intelligent organization. It makes the beautiful structures in the other 15 plots even more meaningful.
            
            * **GRN 6: Shell Layout (`nx.shell_layout`)**
                * **What it is:** Arranges nodes in concentric circles (shells).
                * **Significance:** This can be used to visualize "ranks" or "classes" of genes, though GRN 11 does this more intelligently.
            
            * **GRN 7: Spiral Layout (`nx.spiral_layout`)**
                * **What it is:** Arranges all nodes in a single, continuous spiral.
                * **Significance:** This is a unique layout that can be surprisingly good at showing a single, long **"chain of command"** or a developmental sequence, which might naturally follow the path of the spiral.
            
            * **GRN 8: Planar Layout (`nx.planar_layout`)**
                * **What it is:** A fascinating layout that *tries* to draw the graph with **zero edges crossing**.
                * **Significance:** This is a deep analytical test. If this layout *succeeds*, it proves your GRN is "simple" (mathematically planar). If it *fails* (and falls back to a random layout), it proves your GRN is "complex" (non-planar).
            
            * **GRN 11: Dual-Shell (Custom Logic)**
                * **What it is:** This is your *custom* layout. It programmatically puts all **Components (genes)** in the outer shell and all **Actions (rules)** in the inner shell.
                * **Significance:** This is one of the most useful plots for understanding the *logic* of the GRN. It clearly separates the "what" (the available body parts) from the "how" (the rules that assemble them), letting you see which genes are targets for many rules.

            ---
            
            ### Part III: The Hierarchical (Graphviz) Layouts ιε
            
            **Overall Significance:** These are the most powerful plots for
            understanding a *regulatory* network. They are designed to show
            **hierarchy, control, and the flow of information**. They answer:
            **"What gene controls what?"**
            
            * **GRN 13: Hierarchical (Top-Down) (`prog='dot'`)**
                * **What it is:** The "classic" flowchart layout. It uses a powerful algorithm to figure out the "flow" of the graph and arranges it from top to bottom.
                * **Significance:** This is the **most important plot for understanding control**. The nodes at the very *top* of the chart are the **"master regulators"**—the genes and rules that control everything else. The nodes at the bottom are the final "worker" genes.
            
            * **GRN 14: Hierarchical (Radial) (`prog='twopi'`)**
                * **What it is:** It picks a "root" node (often the graph's center) and draws all other nodes in concentric circles around it, based on their distance from the root.
                * **Significance:** This shows the "blast wave" of gene influence. It's perfect for seeing how "far" a gene's control signal can spread through the network. A gene in the center with 5 rings around it is a very powerful regulator.

            ---
            
            ### Part IV: The Mathematical (Spectral) Layout 📈
            
            **Overall Significance:** This plot is a true "X-Ray" of your network's
            deepest structure, based on advanced linear algebra. It's often
            hard to interpret but mathematically the "most true" view.
            
            * **GRN 5: Spectral Layout (`nx.spectral_layout`)**
                * **What it is:** It uses the *eigenvectors* of the graph's matrix (the "Laplacian") to position the nodes.
                * **Significance:** This is the **most mathematically profound** layout. It is the absolute best way to identify the *most fundamental, tightly-knit, and separate clusters* of genes. If two nodes are close in this layout, they are *deeply* related on a mathematical level, even if they look far apart in other plots.
            """
        )

    st.sidebar.markdown("---")

    if s != st.session_state.settings:
        st.session_state.settings = copy.deepcopy(s)
        if settings_table.get(doc_id=1):
            settings_table.update(s, doc_ids=[1])
        else:
            settings_table.insert(s)
        st.toast("Exhibit constants saved.", icon="⚙️")

    if st.session_state.history:
        last_gen = st.session_state.history[-1]['generation']
        st.sidebar.info(f"**Status:** Loaded archive at **Epoch {last_gen}**. Ready to extend exhibit simulation.", icon="⏳")
    else:
        st.sidebar.info("**Status:** Ready to curate a new exhibit.", icon="✨")

    col1, col2 = st.sidebar.columns(2)
    
    if col1.button("🚀 Curate New Exhibit", type="primary", width='stretch', key="initiate_evolution_button"):
        st.session_state.history = []
        st.session_state.evolutionary_metrics = []
        st.session_state.genesis_events = []
        
        st.session_state.seen_kingdoms = set()
        st.session_state.crossed_complexity_thresholds = set()
        st.session_state.last_dominant_kingdom = None
        st.session_state.has_logged_colonial_emergence = False # type: ignore
        st.session_state.has_logged_philosophy_divergence = False
        st.session_state.has_logged_computation_dawn = False
        st.session_state.has_logged_first_communication = False
        st.session_state.has_logged_memory_invention = False

        st.session_state.gene_archive = []
        
        if s.get('random_seed', 42) != -1:
            random.seed(s.get('random_seed', 42))
            np.random.seed(s.get('random_seed', 42))
            st.toast(f"Using fixed random seed: {s.get('random_seed', 42)}", icon="🔢")
            
        population = []
        for _ in range(s.get('initial_population', 50)):
            genotype = get_primordial_soup_genotype(s)
            genotype = mutate(genotype, s)
            genotype = mutate(genotype, s)
            population.append(genotype)
        
        if not population:
            st.error("Failed to create initial population! Check settings.")
            st.stop()
            
        st.session_state.gene_archive = [g.copy() for g in population]

        exhibit_grid = ExhibitGrid(s)
        
        progress_container = st.empty()
        metrics_container = st.empty()
        status_text = st.empty()
        
        last_best_fitness = -1
        early_stop_counter = 0
        current_mutation_rate = s.get('mutation_rate', 0.2)
        hypermutation_duration = 0
        
        red_queen = RedQueenParasite()
        
        if 'seen_kingdoms' not in st.session_state: st.session_state.seen_kingdoms = set()
        if 'crossed_complexity_thresholds' not in st.session_state: st.session_state.crossed_complexity_thresholds = set()
        if 'last_dominant_kingdom' not in st.session_state: st.session_state.last_dominant_kingdom = None
        if 'has_logged_colonial_emergence' not in st.session_state: st.session_state.has_logged_colonial_emergence = False
        if 'has_logged_philosophy_divergence' not in st.session_state: st.session_state.has_logged_philosophy_divergence = False
        if 'has_logged_computation_dawn' not in st.session_state: st.session_state.has_logged_computation_dawn = False
        if 'has_logged_first_communication' not in st.session_state: st.session_state.has_logged_first_communication = False
        if 'has_logged_memory_invention' not in st.session_state: st.session_state.has_logged_memory_invention = False

        complexity_thresholds_to_log = [10, 25, 50, 100, 200, 500]

        for gen in range(s.get('num_generations', 200)):
            status_text.markdown(f"### ⏳ Simulating Epoch {gen + 1}/{s.get('num_generations', 200)}")
            
            fitness_scores = []
            for genotype in population:
                organism_grid = ExhibitGrid(s) 
                individual_fitness = evaluate_fitness(genotype, organism_grid, s)
                genotype.individual_fitness = individual_fitness
                genotype.fitness = individual_fitness
                genotype.generation = gen
                genotype.age += 1
            
            if s.get('enable_red_queen', True):
                if population:
                    kingdom_counts = Counter(g.kingdom_id for g in population)
                    most_common_kingdom, _ = kingdom_counts.most_common(1)[0]
                    
                    if random.random() < s.get('red_queen_adaptation_speed', 0.2):
                        red_queen.target_kingdom_id = most_common_kingdom
                        st.toast(f"👑 Red Queen Adapts! Parasite now targets **{most_common_kingdom}**.", icon="🎯")
                        event_desc = f"A co-evolving parasite has adapted, now specifically targeting the dominant **{most_common_kingdom}** kingdom. This forces an evolutionary arms race."
                        st.session_state.genesis_events.append({
                            'generation': gen,
                            'type': 'Red Queen',
                            'title': f"Parasite Adapts to {most_common_kingdom}",
                            'description': event_desc,
                            'icon': '🎯'
                        })

                for genotype in population:
                    if genotype.kingdom_id == red_queen.target_kingdom_id:
                        penalty = genotype.fitness * s.get('red_queen_virulence', 0.15)
                        genotype.fitness = max(1e-6, genotype.fitness - penalty)

            if s.get('enable_multi_level_selection', False):
                colonies: Dict[str, List[Genotype]] = {}
                sorted_pop = sorted(population, key=lambda g: g.lineage_id)
                colony_size = s.get('colony_size', 10)
                num_colonies = (len(sorted_pop) + colony_size - 1) // colony_size

                for i in range(num_colonies):
                    colony_id = f"col_{gen}_{i}"
                    colony_members = sorted_pop[i*colony_size:(i+1)*colony_size]
                    colonies[colony_id] = []
                    for member in colony_members:
                        member.colony_id = colony_id
                        colonies[colony_id].append(member)

                group_fitness_scores: Dict[str, float] = {}
                for colony_id, members in colonies.items():
                    if not members: continue
                    
                    mean_individual_fitness = np.mean([m.individual_fitness for m in members])
                    
                    all_components = set()
                    for member in members:
                        all_components.update(member.component_genes.keys())
                    specialization_bonus = len(all_components) * s.get('caste_specialization_bonus', 0.1)

                    group_fitness = mean_individual_fitness + specialization_bonus
                    group_fitness_scores[colony_id] = group_fitness

                group_weight = s.get('group_fitness_weight', 0.3)
                for genotype in population:
                    if genotype.colony_id in group_fitness_scores:
                        group_fitness = group_fitness_scores[genotype.colony_id]
                        genotype.fitness = (genotype.individual_fitness * (1 - group_weight)) + (group_fitness * group_weight)

                if not st.session_state.get('has_logged_colonial_emergence', False):
                    pop_mean_fitness = np.mean([g.individual_fitness for g in population])
                    if any(gf > pop_mean_fitness * 1.2 for gf in group_fitness_scores.values()):
                        event_desc = "For the first time, individual organisms have aggregated into a cooperative colony whose group success surpasses that of average individuals. This marks a major transition towards higher-level superorganisms."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Major Transition', 'title': 'Emergence of Colonial Life',
                            'description': event_desc, 'icon': '🤝'
                        })
                        st.session_state.has_logged_colonial_emergence = True
                        st.toast("🤝 Major Transition! Colonial life has emerged!", icon="🚀")

            if hypermutation_duration > 0:
                current_mutation_rate = s.get('mutation_rate', 0.2) * s.get('post_cataclysm_hypermutation_multiplier', 2.0)
                hypermutation_duration -= 1
                if hypermutation_duration == 0:
                    st.toast("Hypermutation period has ended. Mutation rates returning to normal.", icon="🧬")
            else:
                current_mutation_rate = s.get('mutation_rate', 0.2)

            if s.get('enable_cataclysms', True) and random.random() < s.get('cataclysm_probability', 0.01):
                st.warning(f"🌋 **CATACLYSM!** A gallery-shaking event has occurred in Epoch {gen+1}!", icon="💥")
                event_desc = f"A random environmental event has caused a mass extinction, wiping out **{s.get('cataclysm_extinction_severity', 0.9)*100:.0f}%** of all life and radically altering the exhibit's resource maps."
                st.session_state.genesis_events.append({
                    'generation': gen,
                    'type': 'Cataclysm',
                    'title': 'Mass Extinction Event',
                    'description': event_desc,
                    'icon': '☄️'
                })
                
                extinction_severity = s.get('cataclysm_extinction_severity', 0.9)
                survivors_after_cataclysm = int(len(population) * (1.0 - extinction_severity))
                population.sort(key=lambda x: x.fitness, reverse=True)
                population = population[:survivors_after_cataclysm]
                st.toast(f"Mass extinction! {extinction_severity*100:.0f}% of life has been wiped out.", icon="💥")

                exhibit_grid = ExhibitGrid(s)
                st.toast("The environment has been radically altered! Resource maps have shifted.", icon="🌍")

                hypermutation_duration = s.get('post_cataclysm_hypermutation_duration', 10)
                st.toast(f"Adaptive radiation begins! Hypermutation enabled for {hypermutation_duration} epochs.", icon="⚡")

                while len(population) < s.get('initial_population', 50) and population:
                    parent = random.choice(population)
                    child = mutate(parent, s)
                    population.append(child)

            fitness_scores = [g.fitness for g in population]
            
            if not fitness_scores:
                st.error("EXTINCTION EVENT. All life has perished.")
                break
                
            fitness_array = np.array(fitness_scores)
            
            current_kingdoms = set(g.kingdom_id for g in population)
            
            newly_emerged_kingdoms = current_kingdoms - st.session_state.seen_kingdoms
            for kingdom in newly_emerged_kingdoms:
                if kingdom != "Unknown" and kingdom != "Unclassified":
                    event_desc = f"For the first time in this exhibit's history, life based on the **{kingdom}** chemical archetype has emerged from the primordial soup, opening a new evolutionary frontier."
                    st.session_state.genesis_events.append({
                        'generation': gen, 'type': 'Genesis', 'title': f"Genesis of {kingdom} Life",
                        'description': event_desc, 'icon': '✨'
                    })
                    st.session_state.seen_kingdoms.add(kingdom)

            kingdom_counts = Counter(g.kingdom_id for g in population)
            if kingdom_counts:
                current_dominant_kingdom, _ = kingdom_counts.most_common(1)[0]
                if st.session_state.last_dominant_kingdom and current_dominant_kingdom != st.session_state.last_dominant_kingdom:
                    event_desc = f"A major ecological shift has occurred. Life based on **{current_dominant_kingdom}** has overthrown the previous era's dominant **{st.session_state.last_dominant_kingdom}**-based lifeforms."
                    st.session_state.genesis_events.append({
                        'generation': gen, 'type': 'Succession', 'title': f"The {current_dominant_kingdom} Era Begins",
                        'description': event_desc, 'icon': '👑'
                    })
                st.session_state.last_dominant_kingdom = current_dominant_kingdom

            max_complexity_in_gen = 0
            if population:
                max_complexity_in_gen = max(p.compute_complexity() for p in population)
            
            for threshold in complexity_thresholds_to_log:
                if max_complexity_in_gen >= threshold and threshold not in st.session_state.crossed_complexity_thresholds:
                    fittest_organism = max(population, key=lambda p: p.fitness)
                    event_desc = f"A new era of biological organization has been reached. An organism from the **{fittest_organism.kingdom_id}** kingdom has achieved a genomic complexity of over **{threshold}**, enabling far more sophisticated body plans and behaviors."
                    st.session_state.genesis_events.append({
                        'generation': gen, 'type': 'Complexity Leap', 'title': f"Complexity Barrier Broken ({threshold})",
                        'description': event_desc, 'icon': '🧠'
                    })
                    st.session_state.crossed_complexity_thresholds.add(threshold)

            st.session_state.seen_kingdoms.update(current_kingdoms)
            
            for org in population:
                if s.get('enable_objective_evolution', False) and not st.session_state.get('has_logged_philosophy_divergence', False):
                    default_weights = np.array([s.get('w_lifespan', 0.4), s.get('w_efficiency', 0.3), s.get('w_reproduction', 0.3)])
                    org_weights_dict = org.objective_weights
                    org_weights = np.array([org_weights_dict.get('w_lifespan', 0), org_weights_dict.get('w_efficiency', 0), org_weights_dict.get('w_reproduction', 0)])
                    distance = np.linalg.norm(default_weights - org_weights)
                    if distance > 0.5:
                        top_objective = max(org_weights_dict, key=org_weights_dict.get)
                        event_desc = f"A lineage has evolved its own 'philosophy of life,' radically altering its fitness objectives. Instead of pursuing the exhibit's default goals, it now prioritizes '{top_objective}', marking the dawn of autotelic (self-directed) evolution."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Cognitive Leap', 'title': 'Philosophical Divergence',
                            'description': event_desc, 'icon': '📜'
                        })
                        st.session_state.has_logged_philosophy_divergence = True
                        st.toast("📜 Cognitive Leap! An organism evolved its own goals!", icon="🚀")
                        break

                if not st.session_state.get('has_logged_computation_dawn', False):
                    if any(rule.action_type in ["ENABLE_RULE", "DISABLE_RULE"] for rule in org.rule_genes):
                        event_desc = "A genetic regulatory network has evolved a 'genetic switch,' where one rule can enable or disable another. This allows for complex, stateful developmental programs, a primitive form of biological computation."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Complexity Leap', 'title': 'Dawn of Computation',
                            'description': event_desc, 'icon': '⚙️'
                        })
                        st.session_state.has_logged_computation_dawn = True
                        st.toast("⚙️ Complexity Leap! Life evolved a genetic switch!", icon="🚀")
                        break

                if not st.session_state.get('has_logged_first_communication', False):
                    if any(rule.action_type == "EMIT_SIGNAL" for rule in org.rule_genes):
                        event_desc = "An organism has evolved the ability for its cells to emit chemical signals. This is the first step towards intercellular communication, allowing for coordinated growth and the formation of complex patterns (morphogenesis)."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Major Transition', 'title': 'First Communication',
                            'description': event_desc, 'icon': '📡'
                        })
                        st.session_state.has_logged_first_communication = True
                        st.toast("📡 Major Transition! Cells have learned to communicate!", icon="🚀")
                        break

                if not st.session_state.get('has_logged_memory_invention', False):
                    if any(rule.action_type in ["SET_TIMER", "MODIFY_TIMER"] for rule in org.rule_genes):
                        event_desc = "For the first time, an organism's genetic code includes instructions for an internal timer. This gives its cells a rudimentary memory and a sense of time, enabling sequential developmental programs and biological rhythms."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Cognitive Leap', 'title': 'Invention of Memory',
                            'description': event_desc, 'icon': '⏳'
                        })
                        st.session_state.has_logged_memory_invention = True
                        st.toast("⏳ Cognitive Leap! An organism evolved internal timers!", icon="🚀")
                        break

            for individual in population:
                st.session_state.history.append({
                    'generation': gen,
                    'kingdom_id': individual.kingdom_id,
                    'fitness': individual.fitness,
                    'cell_count': individual.cell_count,
                    'complexity': individual.compute_complexity(),
                    'lifespan': individual.lifespan,
                    'energy_production': individual.energy_production,
                    'energy_consumption': individual.energy_consumption,
                    'lineage_id': individual.lineage_id,
                    'parent_ids': getattr(individual, 'parent_ids', []),
                })
            
            diversity = entropy(np.histogram(fitness_array, bins=10)[0])
            selection_differential = 0.0
            
            st.session_state.evolutionary_metrics.append({
                'generation': gen,
                'diversity': diversity,
                'best_fitness': fitness_array.max(),
                'mean_fitness': fitness_array.mean(),
                'selection_differential': selection_differential,
                'mutation_rate': current_mutation_rate,
            })
            
            with metrics_container.container():
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Best Fitness", f"{fitness_array.max():.4f}")
                c2.metric("Mean Fitness", f"{fitness_array.mean():.4f}")
                c3.metric("Diversity (H)", f"{diversity:.3f}")
                c4.metric("Mutation Rate (μ)", f"{current_mutation_rate:.3f}")

            population.sort(key=lambda x: x.fitness, reverse=True)
            
            if s.get('enable_multi_level_selection', False) and 'colonies' in locals() and colonies:
                num_surviving_colonies = max(1, int(len(colonies) * (1 - s.get('selection_pressure', 0.4))))
                sorted_colonies = sorted(colonies.items(), key=lambda item: group_fitness_scores[item[0]], reverse=True)
                
                survivors = []
                for colony_id, members in sorted_colonies[:num_surviving_colonies]:
                    survivors.extend(members)
                
                if not survivors:
                    num_survivors = max(2, int(len(population) * (1 - s.get('selection_pressure', 0.4))))
                    survivors = population[:num_survivors]
            else:
                num_survivors = max(2, int(len(population) * (1 - s.get('selection_pressure', 0.4))))
                survivors = population[:num_survivors]
            
            offspring = []
            pop_size = s.get('initial_population', 50)
            
            if not survivors:
                st.error("EXTINCTION EVENT. No survivors to reproduce.")
                break
                
            while len(survivors) + len(offspring) < pop_size:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)

                if s.get('enable_endosymbiosis', True) and random.random() < s.get('endosymbiosis_rate', 0.005):
                    host = parent1.copy()
                    symbiote = parent2.copy()

                    for comp_name, comp_gene in symbiote.component_genes.items():
                        if comp_name not in host.component_genes:
                            host.component_genes[comp_name] = comp_gene
                    
                    num_rules_to_take = int(len(symbiote.rule_genes) * random.uniform(0.2, 0.5))
                    if symbiote.rule_genes:
                        rules_to_take = random.sample(symbiote.rule_genes, num_rules_to_take)
                        host.rule_genes.extend(rules_to_take)

                    host.parent_ids.extend(symbiote.parent_ids)
                    host.update_kingdom()
                    host.generation = gen + 1
                    
                    child = mutate(host, s)
                    offspring.append(child)
                    st.toast(f"🤝 ENDOSYMBIOSIS! Organisms merged into a new lifeform!", icon="🧬")
                    
                    event_desc = f"Two distinct organisms from lineages `{parent1.lineage_id}` and `{parent2.lineage_id}` have merged into a single, more complex entity, combining their genetic material."
                    st.session_state.genesis_events.append({
                        'generation': gen,
                        'type': 'Endosymbiosis',
                        'title': 'Genomes Merged',
                        'description': event_desc,
                        'icon': '🧬'
                    })

                else:
                    child = parent1.copy()
                    child = mutate(child, s)
                    child.generation = gen + 1
                    offspring.append(child)
            
            population = survivors + offspring
            st.session_state.gene_archive.extend([c.copy() for c in offspring])

            meta_innovate_condition_source(s)

            if s.get('enable_physics_drift', False):
                apply_physics_drift(s)
                
            max_archive = s.get('max_archive_size', 10000)
            if len(st.session_state.gene_archive) > max_archive:
                st.session_state.gene_archive = random.sample(st.session_state.gene_archive, max_archive)
                
            current_best = fitness_array.max()
            if current_best > last_best_fitness:
                last_best_fitness = current_best
                early_stop_counter = 0
            else:
                early_stop_counter += 1
                
            if s.get('enable_early_stopping', True) and early_stop_counter > s.get('early_stopping_patience', 25):
                st.success(f"**EARLY STOPPING:** Exhibit simulation converged after {gen + 1} epochs.")
                break
                
            progress_container.progress((gen + 1) / s.get('num_generations', 200))
        
        st.session_state.current_population = population
        status_text.markdown("### ✅ Exhibit Simulation Complete! Results archived.")
        
        results_to_save = {
            'history': st.session_state.history,
            'evolutionary_metrics': st.session_state.evolutionary_metrics,
        }
        if results_table.get(doc_id=1):
            results_table.update(results_to_save, doc_ids=[1])
        else:
            results_table.insert(results_to_save)

    if col2.button("🧬 Extend Exhibit Simulation", width='stretch', key="continue_evolution_button"):
        if not st.session_state.current_population:
            st.error("Cannot continue: No population found. Load an archive or 'Curate' a new exhibit first.")
            st.stop()
        
        population = st.session_state.current_population
        s = st.session_state.settings
        
        start_gen = 0
        if st.session_state.history:
            start_gen = st.session_state.history[-1]['generation'] + 1
        
        num_generations_to_run = s.get('num_generations', 200)
        end_gen = start_gen + num_generations_to_run

        st.toast(f"Extending exhibit simulation from Epoch {start_gen} to {end_gen}...")

        if s.get('random_seed', 42) != -1:
            random.seed(s.get('random_seed', 42))
            np.random.seed(s.get('random_seed', 42))
            st.toast(f"Using fixed random seed: {s.get('random_seed', 42)}", icon="🔢")
            
        exhibit_grid = ExhibitGrid(s)
        
        progress_container = st.empty()
        metrics_container = st.empty()
        status_text = st.empty()
        
        last_best_fitness = -1
        if st.session_state.evolutionary_metrics:
            last_best_fitness = st.session_state.evolutionary_metrics[-1]['best_fitness']
        early_stop_counter = 0
        current_mutation_rate = s.get('mutation_rate', 0.2)
        hypermutation_duration = 0

        red_queen = RedQueenParasite()
        if s.get('enable_red_queen', True) and st.session_state.history:
            last_gen_df = pd.DataFrame(st.session_state.history)
            last_gen_df = last_gen_df[last_gen_df['generation'] == last_gen_df['generation'].max()]
            if not last_gen_df.empty:
                kingdom_counts = Counter(last_gen_df['kingdom_id'])
                if kingdom_counts:
                    red_queen.target_kingdom_id = kingdom_counts.most_common(1)[0][0]
        
        for gen in range(start_gen, end_gen):
            status_text.markdown(f"### ⏳ Simulating Epoch {gen + 1}/{end_gen}")
            
            fitness_scores = []
            for genotype in population:
                organism_grid = ExhibitGrid(s) 
                individual_fitness = evaluate_fitness(genotype, organism_grid, s)
                genotype.individual_fitness = individual_fitness
                genotype.fitness = individual_fitness
                genotype.generation = gen
                genotype.age += 1
            
            if s.get('enable_red_queen', True):
                if population:
                    kingdom_counts = Counter(g.kingdom_id for g in population)
                    most_common_kingdom, _ = kingdom_counts.most_common(1)[0]
                    
                    if random.random() < s.get('red_queen_adaptation_speed', 0.2):
                        red_queen.target_kingdom_id = most_common_kingdom
                        st.toast(f"👑 Red Queen Adapts! Parasite now targets **{most_common_kingdom}**.", icon="🎯")
                        event_desc = f"A co-evolving parasite has adapted, now specifically targeting the dominant **{most_common_kingdom}** kingdom. This forces an evolutionary arms race."
                        st.session_state.genesis_events.append({
                            'generation': gen,
                            'type': 'Red Queen',
                            'title': f"Parasite Adapts to {most_common_kingdom}",
                            'description': event_desc,
                            'icon': '🎯'
                        })

                for genotype in population:
                    if genotype.kingdom_id == red_queen.target_kingdom_id:
                        penalty = genotype.fitness * s.get('red_queen_virulence', 0.15)
                        genotype.fitness = max(1e-6, genotype.fitness - penalty)

            if s.get('enable_multi_level_selection', False):
                colonies: Dict[str, List[Genotype]] = {}
                sorted_pop = sorted(population, key=lambda g: g.lineage_id)
                colony_size = s.get('colony_size', 10)
                num_colonies = (len(sorted_pop) + colony_size - 1) // colony_size

                for i in range(num_colonies):
                    colony_id = f"col_{gen}_{i}"
                    colony_members = sorted_pop[i*colony_size:(i+1)*colony_size]
                    colonies[colony_id] = []
                    for member in colony_members:
                        member.colony_id = colony_id
                        colonies[colony_id].append(member)

                group_fitness_scores: Dict[str, float] = {}
                for colony_id, members in colonies.items():
                    if not members: continue
                    
                    mean_individual_fitness = np.mean([m.individual_fitness for m in members])
                    
                    all_components = set()
                    for member in members:
                        all_components.update(member.component_genes.keys())
                    specialization_bonus = len(all_components) * s.get('caste_specialization_bonus', 0.1)

                    group_fitness = mean_individual_fitness + specialization_bonus
                    group_fitness_scores[colony_id] = group_fitness

                group_weight = s.get('group_fitness_weight', 0.3)
                for genotype in population:
                    if genotype.colony_id in group_fitness_scores:
                        group_fitness = group_fitness_scores[genotype.colony_id]
                        genotype.fitness = (genotype.individual_fitness * (1 - group_weight)) + (group_fitness * group_weight)

                if not st.session_state.get('has_logged_colonial_emergence', False):
                    pop_mean_fitness = np.mean([g.individual_fitness for g in population])
                    if any(gf > pop_mean_fitness * 1.2 for gf in group_fitness_scores.values()):
                        event_desc = "For the first time, individual organisms have aggregated into a cooperative colony whose group success surpasses that of average individuals. This marks a major transition towards higher-level superorganisms."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Major Transition', 'title': 'Emergence of Colonial Life',
                            'description': event_desc, 'icon': '🤝'
                        })
                        st.session_state.has_logged_colonial_emergence = True
                        st.toast("🤝 Major Transition! Colonial life has emerged!", icon="🚀")

            if hypermutation_duration > 0:
                current_mutation_rate = s.get('mutation_rate', 0.2) * s.get('post_cataclysm_hypermutation_multiplier', 2.0)
                hypermutation_duration -= 1
                if hypermutation_duration == 0:
                    st.toast("Hypermutation period has ended. Mutation rates returning to normal.", icon="🧬")
            else:
                current_mutation_rate = s.get('mutation_rate', 0.2)

            if s.get('enable_cataclysms', True) and random.random() < s.get('cataclysm_probability', 0.01):
                st.warning(f"🌋 **CATACLYSM!** A gallery-shaking event has occurred in Epoch {gen+1}!", icon="💥")
                event_desc = f"A random environmental event has caused a mass extinction, wiping out **{s.get('cataclysm_extinction_severity', 0.9)*100:.0f}%** of all life and radically altering the exhibit's resource maps."
                st.session_state.genesis_events.append({
                    'generation': gen,
                    'type': 'Cataclysm',
                    'title': 'Mass Extinction Event',
                    'description': event_desc,
                    'icon': '☄️'
                })
                
                extinction_severity = s.get('cataclysm_extinction_severity', 0.9)
                survivors_after_cataclysm = int(len(population) * (1.0 - extinction_severity))
                population.sort(key=lambda x: x.fitness, reverse=True)
                population = population[:survivors_after_cataclysm]
                st.toast(f"Mass extinction! {extinction_severity*100:.0f}% of life has been wiped out.", icon="💥")

                exhibit_grid = ExhibitGrid(s)
                st.toast("The environment has been radically altered! Resource maps have shifted.", icon="🌍")

                hypermutation_duration = s.get('post_cataclysm_hypermutation_duration', 10)
                st.toast(f"Adaptive radiation begins! Hypermutation enabled for {hypermutation_duration} epochs.", icon="⚡")

                while len(population) < s.get('initial_population', 50) and population:
                    parent = random.choice(population)
                    child = mutate(parent, s)
                    population.append(child)

            fitness_scores = [g.fitness for g in population]
            
            if not fitness_scores:
                st.error("EXTINCTION EVENT. All life has perished.")
                break
                
            fitness_array = np.array(fitness_scores)
            
            current_kingdoms = set(g.kingdom_id for g in population)
            
            newly_emerged_kingdoms = current_kingdoms - st.session_state.seen_kingdoms
            for kingdom in newly_emerged_kingdoms:
                if kingdom != "Unknown" and kingdom != "Unclassified":
                    event_desc = f"For the first time in this exhibit's history, life based on the **{kingdom}** chemical archetype has emerged from the primordial soup, opening a new evolutionary frontier."
                    st.session_state.genesis_events.append({
                        'generation': gen, 'type': 'Genesis', 'title': f"Genesis of {kingdom} Life",
                        'description': event_desc, 'icon': '✨'
                    })
                    st.session_state.seen_kingdoms.add(kingdom)

            kingdom_counts = Counter(g.kingdom_id for g in population)
            if kingdom_counts:
                current_dominant_kingdom, _ = kingdom_counts.most_common(1)[0]
                if st.session_state.last_dominant_kingdom and current_dominant_kingdom != st.session_state.last_dominant_kingdom:
                    event_desc = f"A major ecological shift has occurred. Life based on **{current_dominant_kingdom}** has overthrown the previous era's dominant **{st.session_state.last_dominant_kingdom}**-based lifeforms."
                    st.session_state.genesis_events.append({
                        'generation': gen, 'type': 'Succession', 'title': f"The {current_dominant_kingdom} Era Begins",
                        'description': event_desc, 'icon': '👑'
                    })
                st.session_state.last_dominant_kingdom = current_dominant_kingdom

            max_complexity_in_gen = 0
            if population:
                max_complexity_in_gen = max(p.compute_complexity() for p in population)
            
            complexity_thresholds_to_log = [10, 25, 50, 100, 200, 500]
            for threshold in complexity_thresholds_to_log:
                if max_complexity_in_gen >= threshold and threshold not in st.session_state.crossed_complexity_thresholds:
                    fittest_organism = max(population, key=lambda p: p.fitness)
                    event_desc = f"A new era of biological organization has been reached. An organism from the **{fittest_organism.kingdom_id}** kingdom has achieved a genomic complexity of over **{threshold}**, enabling far more sophisticated body plans and behaviors."
                    st.session_state.genesis_events.append({
                        'generation': gen, 'type': 'Complexity Leap', 'title': f"Complexity Barrier Broken ({threshold})",
                        'description': event_desc, 'icon': '🧠'
                    })
                    st.session_state.crossed_complexity_thresholds.add(threshold)

            st.session_state.seen_kingdoms.update(current_kingdoms)
            
            for org in population:
                if s.get('enable_objective_evolution', False) and not st.session_state.get('has_logged_philosophy_divergence', False):
                    default_weights = np.array([s.get('w_lifespan', 0.4), s.get('w_efficiency', 0.3), s.get('w_reproduction', 0.3)])
                    org_weights_dict = org.objective_weights
                    org_weights = np.array([org_weights_dict.get('w_lifespan', 0), org_weights_dict.get('w_efficiency', 0), org_weights_dict.get('w_reproduction', 0)])
                    distance = np.linalg.norm(default_weights - org_weights)
                    if distance > 0.5:
                        top_objective = max(org_weights_dict, key=org_weights_dict.get)
                        event_desc = f"A lineage has evolved its own 'philosophy of life,' radically altering its fitness objectives. Instead of pursuing the exhibit's default goals, it now prioritizes '{top_objective}', marking the dawn of autotelic (self-directed) evolution."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Cognitive Leap', 'title': 'Philosophical Divergence',
                            'description': event_desc, 'icon': '📜'
                        })
                        st.session_state.has_logged_philosophy_divergence = True
                        st.toast("📜 Cognitive Leap! An organism evolved its own goals!", icon="🚀")
                        break

                if not st.session_state.get('has_logged_computation_dawn', False):
                    if any(rule.action_type in ["ENABLE_RULE", "DISABLE_RULE"] for rule in org.rule_genes):
                        event_desc = "A genetic regulatory network has evolved a 'genetic switch,' where one rule can enable or disable another. This allows for complex, stateful developmental programs, a primitive form of biological computation."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Complexity Leap', 'title': 'Dawn of Computation',
                            'description': event_desc, 'icon': '⚙️'
                        })
                        st.session_state.has_logged_computation_dawn = True
                        st.toast("⚙️ Complexity Leap! Life evolved a genetic switch!", icon="🚀")
                        break

                if not st.session_state.get('has_logged_first_communication', False):
                    if any(rule.action_type == "EMIT_SIGNAL" for rule in org.rule_genes):
                        event_desc = "An organism has evolved the ability for its cells to emit chemical signals. This is the first step towards intercellular communication, allowing for coordinated growth and the formation of complex patterns (morphogenesis)."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Major Transition', 'title': 'First Communication',
                            'description': event_desc, 'icon': '📡'
                        })
                        st.session_state.has_logged_first_communication = True
                        st.toast("📡 Major Transition! Cells have learned to communicate!", icon="🚀")
                        break

                if not st.session_state.get('has_logged_memory_invention', False):
                    if any(rule.action_type in ["SET_TIMER", "MODIFY_TIMER"] for rule in org.rule_genes):
                        event_desc = "For the first time, an organism's genetic code includes instructions for an internal timer. This gives its cells a rudimentary memory and a sense of time, enabling sequential developmental programs and biological rhythms."
                        st.session_state.genesis_events.append({
                            'generation': gen, 'type': 'Cognitive Leap', 'title': 'Invention of Memory',
                            'description': event_desc, 'icon': '⏳'
                        })
                        st.session_state.has_logged_memory_invention = True
                        st.toast("⏳ Cognitive Leap! An organism evolved internal timers!", icon="🚀")
                        break

            for individual in population:
                st.session_state.history.append({
                    'generation': gen,
                    'kingdom_id': individual.kingdom_id,
                    'fitness': individual.fitness,
                    'cell_count': individual.cell_count,
                    'complexity': individual.compute_complexity(),
                    'lifespan': individual.lifespan,
                    'energy_production': individual.energy_production,
                    'energy_consumption': individual.energy_consumption,
                    'lineage_id': individual.lineage_id,
                    'parent_ids': getattr(individual, 'parent_ids', []),
                })
            
            diversity = entropy(np.histogram(fitness_array, bins=10)[0])
            selection_differential = 0.0
            
            st.session_state.evolutionary_metrics.append({
                'generation': gen,
                'diversity': diversity,
                'best_fitness': fitness_array.max(),
                'mean_fitness': fitness_array.mean(),
                'selection_differential': selection_differential,
                'mutation_rate': current_mutation_rate,
            })
            
            with metrics_container.container():
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Best Fitness", f"{fitness_array.max():.4f}")
                c2.metric("Mean Fitness", f"{fitness_array.mean():.4f}")
                c3.metric("Diversity (H)", f"{diversity:.3f}")
                c4.metric("Mutation Rate (μ)", f"{current_mutation_rate:.3f}")

            population.sort(key=lambda x: x.fitness, reverse=True)
            
            if s.get('enable_multi_level_selection', False) and 'colonies' in locals():
                num_surviving_colonies = max(1, int(len(colonies) * (1 - s.get('selection_pressure', 0.4))))
                sorted_colonies = sorted(colonies.items(), key=lambda item: group_fitness_scores.get(item[0], 0), reverse=True)
                
                survivors = []
                for colony_id, members in sorted_colonies[:num_surviving_colonies]:
                    survivors.extend(members)
                
                if not survivors:
                    num_survivors = max(2, int(len(population) * (1 - s.get('selection_pressure', 0.4))))
                    survivors = population[:num_survivors]
            else:
                num_survivors = max(2, int(len(population) * (1 - s.get('selection_pressure', 0.4))))
                survivors = population[:num_survivors]
            
            offspring = []
            pop_size = s.get('initial_population', 50)
            
            if not survivors:
                st.error("EXTINCTION EVENT. No survivors to reproduce.")
                break
                
            while len(survivors) + len(offspring) < pop_size:
                parent1 = random.choice(survivors)
                parent2 = random.choice(survivors)

                if s.get('enable_endosymbiosis', True) and random.random() < s.get('endosymbiosis_rate', 0.005):
                    host = parent1.copy()
                    symbiote = parent2.copy()

                    for comp_name, comp_gene in symbiote.component_genes.items():
                        if comp_name not in host.component_genes:
                            host.component_genes[comp_name] = comp_gene
                    
                    num_rules_to_take = int(len(symbiote.rule_genes) * random.uniform(0.2, 0.5))
                    if symbiote.rule_genes:
                        rules_to_take = random.sample(symbiote.rule_genes, num_rules_to_take)
                        host.rule_genes.extend(rules_to_take)

                    host.parent_ids.extend(symbiote.parent_ids)
                    host.update_kingdom()
                    host.generation = gen + 1
                    
                    child = mutate(host, s)
                    offspring.append(child)
                    st.toast(f"🤝 ENDOSYMBIOSIS! Organisms merged into a new lifeform!", icon="🧬")
                    
                    event_desc = f"Two distinct organisms from lineages `{parent1.lineage_id}` and `{parent2.lineage_id}` have merged into a single, more complex entity, combining their genetic material."
                    st.session_state.genesis_events.append({
                        'generation': gen,
                        'type': 'Endosymbiosis',
                        'title': 'Genomes Merged',
                        'description': event_desc,
                        'icon': '🧬'
                    })

                else:
                    child = parent1.copy()
                    child = mutate(child, s)
                    child.generation = gen + 1
                    offspring.append(child)
            
            population = survivors + offspring
            st.session_state.gene_archive.extend([c.copy() for c in offspring])

            meta_innovate_condition_source(s)

            if s.get('enable_physics_drift', False):
                apply_physics_drift(s)
                
            max_archive = s.get('max_archive_size', 10000)
            if len(st.session_state.gene_archive) > max_archive:
                st.session_state.gene_archive = random.sample(st.session_state.gene_archive, max_archive)
                
            current_best = fitness_array.max()
            if current_best > last_best_fitness:
                last_best_fitness = current_best
                early_stop_counter = 0
            else:
                early_stop_counter += 1
                
            if s.get('enable_early_stopping', True) and early_stop_counter > s.get('early_stopping_patience', 25):
                st.success(f"**EARLY STOPPING:** Exhibit simulation converged after {gen + 1} epochs.")
                break
            
            progress_container.progress((gen - start_gen + 1) / num_generations_to_run)
        
        st.session_state.current_population = population
        status_text.markdown("### ✅ Exhibit Simulation Complete! Results archived.")
        
        results_to_save = {
            'history': st.session_state.history,
            'evolutionary_metrics': st.session_state.evolutionary_metrics,
        }
        if results_table.get(doc_id=1):
            results_table.update(results_to_save, doc_ids=[1])
        else:
            results_table.insert(results_to_save)

    st.markdown('<h1>🔭 Exhibit Hall: Simulation Results</h1>', unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.info("This exhibit hall is empty. Adjust the physical laws in the Curator's Console and press '🚀 Curate New Exhibit' to populate it with life.")
        st.markdown("""
            <div style="border-left: 3px solid #9E7676; padding-left: 15px; margin-top: 20px; border-radius: 3px;">
            ### The Museum of Universal Life: An Essay

            The universe is a vast, dark ocean of possibility, and the desire to explore it is boundless. This is the conceptual blueprint for an imaginary institution equal to that vastness: a museum dedicated to showcasing every potential form of life. Such a museum would not be a simple collection of curiosities but a profound study of how the universal laws of physics and chemistry sculpt biology in staggeringly different ways. This museum would be divided into two fundamental wings: "Life As We Know It" and the far more speculative, "Life As We Don't Know It."

            #### Wing 1: Life As We Know It (The Carbon Gallery)
            The first wing of the museum is dedicated to life built on the same foundation as our own. The central exhibit here is carbon, the "centerpiece in the molecular machinery of life."

            **The Carbon-Based Standard:** This exhibit shows why carbon is so special. It is common throughout the universe and possesses a rare ability to form four-way bonds, linking to itself in long, stable chains. This versatility allows for the "huge complex molecules" necessary for biology. Even here, the diversity would be immense; scientists have identified over a million possible carbon-based alternatives to our own DNA.

            **The Hall of Convergent Evolution:** This gallery explores a fascinating idea: even carbon-based life on other "Earth-like" planets might look familiar. It explains the concept of convergent evolution, where similar environmental pressures cause similar features to evolve independently. Exhibits show how features like eyesight and flight have appeared multiple times on Earth, suggesting that the "greatest hits of evolution" could be on repeat across the cosmos.

            #### Wing 2: Life As We Don't Know It (The Exotic Biochemistry Hall)
            This is where the museum truly expands our concept of life itself. This wing houses beings that challenge our carbon-centric biases, built from exotic chemistries thriving in environments we would consider hellish.

            **The Silicon Contender:** The most prominent exhibit here is silicon-based life. At first glance, silicon seems a perfect alternative, as it also forms four-way bonds. However, the exhibit details its flaws: its bonds are weaker, and, crucially, in the presence of oxygen, it binds into solid rock.

            A diorama here might show the frigid world of Saturn's moon Titan. In this oxygen-free environment, with vast lakes of liquid methane, silicon-based beings could theoretically exist, perhaps with ultra-slow metabolisms and lifecycles lasting millions of years.

            **The "Extreme" Exhibits:** Deeper in this wing, the truly bizarre possibilities are displayed. Speculations include lifeforms living inside molten silicate rock, self-organizing plasma crystals in cosmic dust that "resemble dna," and even theoretical "macronuclei" life evolving in the dense particle sea on the surface of a neutron star.

            #### Wing 3: The Sculpting Hand of Environment
            The final, and perhaps most dramatic, wing of the museum demonstrates how alien environments act as cosmic sculptors, shaping the bodies of both carbon-based and exotic life.

            **The Gravity Gallery:** This exhibit directly illustrates gravity's immense power.

            *   **High-Gravity Worlds:** One diorama, based on "super earths," would show a landscape of stunted plant life. The land animals here would be short, dense, and powerful, built with "large bones and muscle mass" and robust circulatory systems just to survive the crushing force.

            *   **Low-Gravity Worlds:** The neighboring diorama would be a stunning contrast. On a low-gravity planet, plants could grow to "towering heights." The animals would be slender and graceful, with "body types that boggle the mind," free from the need for bulky skeletons.

            **The Hall of Senses:** Here, an exhibit shows how life adapts to the light of its star. Life on dimly lit planets would evolve "huge eyes to suck in extra light," much like our own nocturnal mammals.

            **The "Alien Garden":** This final exhibit is a visually stunning display of alien botany, based on star color. Our plants are green because they reflect the green light from our yellow sun. This garden showcases the bizarre alternatives:

            *   Around dim red dwarf stars, the vegetation would appear "black," adapted to absorb every possible wavelength of faint light.

            *   Around hotter, bluer stars, plants "could appear redder," using different pigments for their own unique photosynthesis.

            A special display might feature a purple landscape. Earth itself may have once appeared purple due to a simpler pigment called retinol, leading to the speculation that purple, not green, "may be life's favorite color."

            Ultimately, this museum is a monument to imagination grounded in science. It teaches us that while the laws of physics are universal, the forms that life can take within those laws are limited only by the number of worlds on which it can arise.

            <br><br>
            *<p style="font-size: 0.8em; text-align: right; color: #aaa;">Inspired by Melodysheep's "LIFE BEYOND II"</p>*
            </div>
        """, unsafe_allow_html=True)
    else:
        history_df = pd.DataFrame(st.session_state.history)
        metrics_df = pd.DataFrame(st.session_state.evolutionary_metrics)
        population = st.session_state.current_population
        
        tab_list = [
            "📈 Simulation Dashboard", 
            "🔬 Specimen Gallery", 
            "🧬 Elite Lineage Analysis",
            "📜 The Genesis Chronicle",
            "📊 Custom Analytics Lab"
        ]
        tab_dashboard, tab_viewer, tab_elites, tab_genesis, tab_analytics_lab = st.tabs(tab_list)
        
        with tab_dashboard:
            if st.session_state.dashboard_visible:
                st.header("Exhibit Trajectory Dashboard")
                st.plotly_chart(
                    create_simulation_dashboard(history_df, metrics_df), # This function name is fine
                    width='stretch',
                    key="main_dashboard_plot_museum"
                )
                visualize_fitness_landscape(history_df)

                st.markdown("---")
                if st.button("Clear & Hide Dashboard", key="hide_dashboard_button"):
                    st.session_state.dashboard_visible = False
                    st.rerun()
            
            else:
                st.info("This tab renders the main dashboard with large plots. It is paused to save memory.")
                if st.button("📈 Render Exhibit Dashboard", key="render_dashboard_button"):
                    st.session_state.dashboard_visible = True
                    st.rerun()

        with tab_viewer:
            st.header("🔬 Specimen Gallery")
            st.markdown("Observe the phenotypes (body plans) of the organisms that evolved. This is the **shape of life** your exhibit created.")
            
            if population:
                gen_to_view = st.slider("Select Epoch to View", 0, history_df['generation'].max(), history_df['generation'].max())
                
                gen_pop_df = history_df[history_df['generation'] == gen_to_view]
                if gen_pop_df.empty:
                    st.warning(f"No data for epoch {gen_to_view}. Showing final epoch.")
                    gen_pop_df = history_df[history_df['generation'] == history_df['generation'].max()]
                    
                gen_pop_df = gen_pop_df.sort_values('fitness', ascending=False)
                
                num_to_display = s.get('num_ranks_to_display', 3)
                
                final_pop_sorted = sorted(population, key=lambda x: x.fitness, reverse=True)
                top_specimens = final_pop_sorted[:num_to_display]
                st.info(f"Showing top {num_to_display} specimens from the *final* population (Epoch {population[0].generation}).")
                
                cols = st.columns(len(top_specimens))
                for i, specimen in enumerate(top_specimens):
                    with cols[i], st.spinner(f"Growing specimen {i+1}..."):
                        vis_grid = ExhibitGrid(s)
                        phenotype = Phenotype(specimen, vis_grid, s)

                        st.markdown(f"**Rank {i+1} (Epoch {specimen.generation})**")
                        st.metric("Fitness", f"{specimen.fitness:.4f}")
                        st.metric("Cell Count", f"{specimen.cell_count}")

                        fig = visualize_phenotype_2d(phenotype, vis_grid)
                        st.plotly_chart(fig, width='stretch', key=f"pheno_vis_{i}")

                        st.markdown("##### **Component Composition**")
                        component_counts = Counter(cell.component.name for cell in phenotype.cells.values())
                        if component_counts:
                            comp_df = pd.DataFrame.from_dict(component_counts, orient='index', columns=['Count']).reset_index()
                            comp_df = comp_df.rename(columns={'index': 'Component'})
                            color_map = {c.name: c.color for c in specimen.component_genes.values()}
                            fig_pie = px.pie(comp_df, values='Count', names='Component', 
                                             color='Component', color_discrete_map=color_map)
                            fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=200)
                            st.plotly_chart(fig_pie, width='stretch', key=f"pheno_pie_{i}")
                        else:
                            st.info("No cells to analyze.")

                        st.markdown("##### **Evolved Objectives**")
                        if specimen.objective_weights:
                            obj_df = pd.DataFrame.from_dict(specimen.objective_weights, orient='index', columns=['Weight']).reset_index()
                            obj_df = obj_df.rename(columns={'index': 'Objective'})
                            fig_bar = px.bar(obj_df, x='Objective', y='Weight', color='Objective')
                            fig_bar.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=200)
                            st.plotly_chart(fig_bar, width='stretch', key=f"pheno_bar_{i}")
                        else:
                            st.info("Global objectives are in use.")

                        st.markdown("##### **Genetic Regulatory Network (GRN)**")
                        G = nx.DiGraph()
                        for comp_name, comp_gene in specimen.component_genes.items():
                            G.add_node(comp_name, type='component', color=comp_gene.color)
                        for rule in specimen.rule_genes:
                            action_node = f"{rule.action_type}\n({rule.action_param})"
                            G.add_node(action_node, type='action', color='#FFB347')
                            
                            source_node = list(specimen.component_genes.keys())[0]
                            if rule.conditions:
                                type_cond = next((c for c in rule.conditions if c['source'] == 'self_type'), None)
                                if type_cond and type_cond['target_value'] in G.nodes():
                                    source_node = type_cond['target_value']
                                    
                            G.add_edge(source_node, action_node, label=f"P={rule.probability:.1f}")
                            if rule.action_param in G.nodes():
                                G.add_edge(action_node, rule.action_param)

                        if G.nodes:
                            try:
                                fig_grn, ax = plt.subplots(figsize=(4, 3))
                                pos = nx.spring_layout(G, k=0.9, seed=42)
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos, ax=ax, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
                                st.pyplot(fig_grn)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 2**")
                        if G.nodes:
                            try:
                                fig_grn_2, ax_2 = plt.subplots(figsize=(4, 3))
                                pos_2 = nx.kamada_kawai_layout(G)
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_2, ax=ax_2, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_2, labels=labels, font_size=7, ax=ax_2)
                                st.pyplot(fig_grn_2)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 2: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 3**")
                        if G.nodes:
                            try:
                                fig_grn_3, ax_3 = plt.subplots(figsize=(4, 3))
                                pos_3 = nx.circular_layout(G)
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_3, ax=ax_3, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_3, labels=labels, font_size=7, ax=ax_3)
                                st.pyplot(fig_grn_3)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 3: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 4**")
                        if G.nodes:
                            try:
                                fig_grn_4, ax_4 = plt.subplots(figsize=(4, 3))
                                pos_4 = nx.random_layout(G, seed=42) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_4, ax=ax_4, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_4, labels=labels, font_size=7, ax=ax_4)
                                st.pyplot(fig_grn_4)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 4: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 5**")
                        if G.nodes:
                            try:
                                fig_grn_5, ax_5 = plt.subplots(figsize=(4, 3))
                                pos_5 = nx.spectral_layout(G) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_5, ax=ax_5, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_5, labels=labels, font_size=7, ax=ax_5)
                                st.pyplot(fig_grn_5)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 5: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 6**")
                        if G.nodes:
                            try:
                                fig_grn_6, ax_6 = plt.subplots(figsize=(4, 3))
                                pos_6 = nx.shell_layout(G) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_6, ax=ax_6, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_6, labels=labels, font_size=7, ax=ax_6)
                                st.pyplot(fig_grn_6)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 6: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 7**")
                        if G.nodes:
                            try:
                                fig_grn_7, ax_7 = plt.subplots(figsize=(4, 3))
                                pos_7 = nx.spiral_layout(G) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_7, ax=ax_7, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_7, labels=labels, font_size=7, ax=ax_7)
                                st.pyplot(fig_grn_7)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 7: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 8**")
                        if G.nodes:
                            try:
                                fig_grn_8, ax_8 = plt.subplots(figsize=(4, 3))
                                try:
                                    pos_8 = nx.planar_layout(G)
                                except nx.NetworkXException:
                                    st.caption("GRN 8: Not planar, falling back to random.")
                                    pos_8 = nx.random_layout(G, seed=43)
                                
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_8, ax=ax_8, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_8, labels=labels, font_size=7, ax=ax_8)
                                st.pyplot(fig_grn_8)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 8: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 9**")
                        if G.nodes:
                            try:
                                fig_grn_9, ax_9 = plt.subplots(figsize=(4, 3))
                                pos_9 = nx.spring_layout(G, k=0.1, seed=42) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_9, ax=ax_9, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_9, labels=labels, font_size=7, ax=ax_9)
                                st.pyplot(fig_grn_9)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 9: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 10**")
                        if G.nodes:
                            try:
                                fig_grn_10, ax_10 = plt.subplots(figsize=(4, 3))
                                pos_10 = nx.spring_layout(G, k=2.0, seed=42) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_10, ax=ax_10, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_10, labels=labels, font_size=7, ax=ax_10)
                                st.pyplot(fig_grn_10)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 10: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 11**")
                        if G.nodes:
                            try:
                                fig_grn_11, ax_11 = plt.subplots(figsize=(4, 3))
                                component_nodes = [n for n, data in G.nodes(data=True) if data.get('type') == 'component']
                                action_nodes = [n for n, data in G.nodes(data=True) if data.get('type') == 'action']
                                shell_list = [component_nodes, action_nodes]
                                
                                pos_11 = nx.shell_layout(G, nlist=shell_list) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_11, ax=ax_11, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_11, labels=labels, font_size=7, ax=ax_11)
                                st.pyplot(fig_grn_11)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 11: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 12**")
                        if G.nodes:
                            try:
                                fig_grn_12, ax_12 = plt.subplots(figsize=(4, 3))
                                pos_12 = nx.spring_layout(G, iterations=200, seed=42) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_12, ax=ax_12, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_12, labels=labels, font_size=7, ax=ax_12)
                                st.pyplot(fig_grn_12)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 12: {e}")
                        else:
                            st.info("No GRN to display.")
                            
                        st.markdown("##### **Genetic Regulatory Network (GRN) 13: Hierarchical (Top-Down)**")
                        if G.nodes:
                            try:
                                fig_grn_13, ax_13 = plt.subplots(figsize=(4, 3))
                                pos_13 = nx.nx_pydot.graphviz_layout(G, prog='dot') 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_13, ax=ax_13, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_13, labels=labels, font_size=7, ax=ax_13)
                                st.pyplot(fig_grn_13)
                                plt.clf()
                            except ImportError:
                                st.warning("GRN 13 Error: This layout requires 'pydot' (and Graphviz) to be installed. Falling back to 'spring'.")
                                try:
                                    fig_grn_13, ax_13 = plt.subplots(figsize=(4, 3))
                                    pos_13_fallback = nx.spring_layout(G, seed=13)
                                    node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                    nx.draw(G, pos_13_fallback, ax=ax_13, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                    labels = {n: n.split('\n')[0] for n in G.nodes()}
                                    nx.draw_networkx_labels(G, pos_13_fallback, labels=labels, font_size=7, ax=ax_13)
                                    st.pyplot(fig_grn_13)
                                    plt.clf()
                                except Exception as e:
                                    st.warning(f"Could not draw GRN 13 fallback: {e}")
                            except Exception as e:
                                st.warning(f"Could not draw GRN 13: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 14: Hierarchical (Radial)**")
                        if G.nodes:
                            try:
                                fig_grn_14, ax_14 = plt.subplots(figsize=(4, 3))
                                pos_14 = nx.nx_pydot.graphviz_layout(G, prog='twopi') 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_14, ax=ax_14, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_14, labels=labels, font_size=7, ax=ax_14)
                                st.pyplot(fig_grn_14)
                                plt.clf()
                            except ImportError:
                                st.warning("GRN 14 Error: This layout requires 'pydot' (and Graphviz) to be installed. Skipping.")
                            except Exception as e:
                                st.warning(f"Could not draw GRN 14: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 15: Force-Directed (NEATO)**")
                        if G.nodes:
                            try:
                                fig_grn_15, ax_15 = plt.subplots(figsize=(4, 3))
                                pos_15 = nx.nx_pydot.graphviz_layout(G, prog='neato') 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_15, ax=ax_15, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_15, labels=labels, font_size=7, ax=ax_15)
                                st.pyplot(fig_grn_15)
                                plt.clf()
                            except ImportError:
                                st.warning("GRN 15 Error: This layout requires 'pydot' (and Graphviz) to be installed. Skipping.")
                            except Exception as e:
                                st.warning(f"Could not draw GRN 15: {e}")
                        else:
                            st.info("No GRN to display.")

                        st.markdown("##### **Genetic Regulatory Network (GRN) 16: Spring Layout (Alternate Seed)**")
                        if G.nodes:
                            try:
                                fig_grn_16, ax_16 = plt.subplots(figsize=(4, 3))
                                pos_16 = nx.spring_layout(G, seed=99) 
                                node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                                nx.draw(G, pos_16, ax=ax_16, with_labels=False, node_size=500, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                labels = {n: n.split('\n')[0] for n in G.nodes()}
                                nx.draw_networkx_labels(G, pos_16, labels=labels, font_size=7, ax=ax_16)
                                st.pyplot(fig_grn_16)
                                plt.clf()
                            except Exception as e:
                                st.warning(f"Could not draw GRN 16: {e}")
                        else:
                            st.info("No GRN to display.")

            else: # This is the case where `if population:` is false
                st.warning("No population data available to view specimens. Run a simulation.")

        with tab_elites:
            st.header("🧬 Elite Lineage Analysis")
            st.markdown("A deep dive into the 'DNA' of the most successful organisms. Each rank displays the best organism from a unique Kingdom, showcasing the diversity of life that has evolved.")
            st.markdown("---")

            if st.session_state.show_elite_analysis:
                
                if population:
                    population.sort(key=lambda x: x.fitness, reverse=True)
                    num_ranks_to_display = s.get('num_ranks_to_display', 3)

                    elite_specimens = []
                    seen_kingdoms = set()
                    for individual in population:
                        if individual.kingdom_id not in seen_kingdoms:
                            elite_specimens.append(individual)
                            seen_kingdoms.add(individual.kingdom_id)

                    for i, individual in enumerate(elite_specimens[:num_ranks_to_display]):
                        with st.expander(f"**Rank {i+1}:** Kingdom `{individual.kingdom_id}` | Fitness: `{individual.fitness:.4f}`", expanded=(i==0)):
                            
                            with st.spinner(f"Growing Rank {i+1}..."):
                                vis_grid = ExhibitGrid(s)
                                phenotype = Phenotype(individual, vis_grid, s)

                            col1, col2 = st.columns([1, 1])
                            with col1:
                                st.markdown("##### **Core Metrics**")
                                st.metric("Cell Count", f"{individual.cell_count}")
                                st.metric("Complexity", f"{individual.compute_complexity():.2f}")
                                st.metric("Lifespan", f"{individual.lifespan} epochs")
                                st.metric("Energy Prod.", f"{individual.energy_production:.3f}")
                                st.metric("Energy Cons.", f"{individual.energy_consumption:.3f}")
                            
                            with col2:
                                st.markdown("##### **Phenotype (Body Plan)**")
                                fig = visualize_phenotype_2d(phenotype, vis_grid)
                                st.plotly_chart(fig, width='stretch', key=f"elite_pheno_vis_{i}")

                            st.markdown("---")
                            
                            col3, col4 = st.columns(2)

                            with col3:
                                st.markdown("##### **Component Composition**")
                                component_counts = Counter(cell.component.name for cell in phenotype.cells.values())
                                if component_counts:
                                    comp_df = pd.DataFrame.from_dict(component_counts, orient='index', columns=['Count']).reset_index()
                                    comp_df = comp_df.rename(columns={'index': 'Component'})
                                    color_map = {c.name: c.color for c in individual.component_genes.values()}
                                    fig_pie = px.pie(comp_df, values='Count', names='Component', 
                                                     color='Component', color_discrete_map=color_map, title="Cell Type Distribution")
                                    fig_pie.update_layout(showlegend=True, margin=dict(l=0, r=0, t=30, b=0), height=300)
                                    st.plotly_chart(fig_pie, width='stretch', key=f"elite_pie_{i}")
                                else:
                                    st.info("No cells to analyze.")
                                    
                                st.markdown("##### **Component Genes (The 'Alphabet')**")
                                for comp_name, comp_gene in individual.component_genes.items():
                                    st.code(f"[{comp_gene.color}] {comp_name} (Mass: {comp_gene.mass:.2f}, Struct: {comp_gene.structural:.2f})", language="text")

                            with col4:
                                st.markdown("##### **Genetic Regulatory Network (GRN Rules)**")
                                if individual.rule_genes:
                                    for rule in individual.rule_genes:
                                        cond_parts = []
                                        for c in rule.conditions:
                                            target_val = c['target_value']
                                            val_str = f"{target_val:.1f}" if isinstance(target_val, (int, float)) else f"'{target_val}'"
                                            cond_parts.append(f"{c['source']} {c['operator']} {val_str}")
                                        cond_str = " AND ".join(cond_parts) if cond_parts else "ALWAYS"
                                        st.code(f"IF {cond_str}\nTHEN {rule.action_type}({rule.action_param}) [P={rule.probability:.2f}, Pri={rule.priority}]", language='sql')
                                else:
                                    st.info("No GRN rules.")
                else:
                    st.warning("No population data available to analyze.")
                
                st.markdown("---")
                if st.button("Clear & Hide Elite Analysis", key="hide_elite"):
                    st.session_state.show_elite_analysis = False
                    st.rerun()

            else:
                st.info("This tab renders detailed organism data. It is paused to save memory.")
                if st.button("🧬 Render Elite Analysis", key="show_elite"):
                    st.session_state.show_elite_analysis = True
                    st.rerun()

        with tab_genesis:
            st.header("📜 The Chronicle of Genesis")
            st.markdown("This is the historical record of your exhibit, chronicling the pivotal moments of creation, innovation, and environmental change. These events are the sparks that drive 'truly infinite' evolution.")

            events = st.session_state.get('genesis_events', [])
            if not events:
                st.info("No significant evolutionary events have been recorded yet. Run a simulation with innovation and cataclysms enabled.")
            else:
                st.markdown("---")
                event_types = sorted(list(set(e['type'] for e in events)))
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("#### Filter Events")
                    gen_range = st.slider(
                        "Filter by Epoch",
                        min_value=0,
                        max_value=history_df['generation'].max(),
                        value=(0, history_df['generation'].max())
                    )
                    selected_types = st.multiselect(
                        "Filter by Event Type",
                        options=event_types,
                        default=event_types
                    )

                filtered_events = [
                    e for e in events 
                    if gen_range[0] <= e['generation'] <= gen_range[1] and e['type'] in selected_types
                ]

                with col2:
                    st.markdown(f"#### Recorded History ({len(filtered_events)} events)")
                    log_container = st.container(height=400)
                    for event in sorted(filtered_events, key=lambda x: x['generation']):
                        log_container.markdown(f"""
                        <div style="border-left: 3px solid #9E7676; padding-left: 10px; margin-bottom: 15px; border-radius: 3px;">
                            <small>Epoch {event['generation']}</small><br>
                            <strong>{event['icon']} {event['title']}</strong>
                            <p style="font-size: 0.9em; color: #ccc;">{event['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("---")
                st.markdown("### 💡 Hall of Innovation")
                st.markdown("A showcase of the most novel organisms that emerged directly after key evolutionary leaps.")

                innovation_events = [e for e in filtered_events if e['type'] in ['Component Innovation', 'Sense Innovation', 'Endosymbiosis', 'Genesis', 'Complexity Leap', 'Major Transition', 'Cognitive Leap']]
                if not innovation_events:
                    st.info("No innovation events found in the selected range.")
                else:
                    gallery_specimens = []
                    generations_to_check = sorted(list(set(e['generation'] + 1 for e in innovation_events)))
                    
                    lineage_lookup = {p.lineage_id: p for p in population}

                    for event in innovation_events:
                        next_gen = event['generation'] + 1
                        next_gen_df = history_df[history_df['generation'] == next_gen]
                        if not next_gen_df.empty:
                            best_in_gen_idx = next_gen_df['fitness'].idxmax()
                            best_organism_info = next_gen_df.loc[best_in_gen_idx]
                            best_lineage_id = best_organism_info['lineage_id']
                            
                            specimen = lineage_lookup.get(best_lineage_id)
                            
                            if specimen and not any(s['specimen'].id == specimen.id for s in gallery_specimens):
                                gallery_specimens.append({
                                    'specimen': specimen,
                                    'innovation_title': event['title'],
                                    'innovation_gen': next_gen 
                                })
                    
                    if not gallery_specimens:
                        st.warning("Could not find representative specimens for the selected innovations.")
                    else:
                        for i, item in enumerate(gallery_specimens[:3]):
                            specimen = item['specimen']
                            st.markdown(f"#### 🏅 Specimen from Epoch {item['innovation_gen']} (Post-'*{item['innovation_title']}*')")
                            
                            with st.spinner(f"Growing and analyzing specimen {i+1}..."):
                                    vis_grid = ExhibitGrid(s)
                                    phenotype = Phenotype(specimen, vis_grid, s)

                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.markdown("**Phenotype (Body Plan)**")
                                fig_pheno = visualize_phenotype_2d(phenotype, vis_grid)
                                fig_pheno.update_layout(height=250, title=None, margin=dict(l=0, r=0, t=0, b=0))
                                st.plotly_chart(fig_pheno, width='stretch', key=f"gallery_pheno_{i}")
                                
                                st.markdown("**Component Composition**")
                                component_counts = Counter(cell.component.name for cell in phenotype.cells.values())
                                if component_counts:
                                    comp_df = pd.DataFrame.from_dict(component_counts, orient='index', columns=['Count']).reset_index()
                                    comp_df = comp_df.rename(columns={'index': 'Component'})
                                    color_map = {c.name: c.color for c in specimen.component_genes.values()}
                                    fig_pie = px.pie(comp_df, values='Count', names='Component', 
                                                     color='Component', color_discrete_map=color_map)
                                    fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=200)
                                    st.plotly_chart(fig_pie, width='stretch', key=f"gallery_pyie_{i}")
                            with col2:
                                st.markdown("**Internal Energy Distribution**")
                                energy_data = np.full((vis_grid.width, vis_grid.height), np.nan)
                                for (x, y), cell in phenotype.cells.items():
                                    energy_data[x, y] = cell.energy
                                fig_energy = px.imshow(energy_data, color_continuous_scale='viridis', aspect='equal')
                                fig_energy.update_layout(height=250, title=None, margin=dict(l=0, r=0, t=0, b=0), coloraxis_showscale=False)
                                fig_energy.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
                                st.plotly_chart(fig_energy, width='stretch', key=f"gallery_energye_{i}")

                            with col3:
                                st.markdown("**Cellular Age Map**")
                                age_data = np.full((vis_grid.width, vis_grid.height), np.nan)
                                for (x, y), cell in phenotype.cells.items():
                                    age_data[x, y] = cell.age
                                fig_age = px.imshow(age_data, color_continuous_scale='plasma', aspect='equal')
                                fig_age.update_layout(height=250, title=None, margin=dict(l=0, r=0, t=0, b=0), coloraxis_showscale=False)
                                fig_age.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
                                st.plotly_chart(fig_age, width='stretch', key=f"galleriey_age_{i}")
                            st.markdown("---")
                
                # --- NEW: Epochs & Phylogeny Section ---
                st.markdown("---") # Separator
                st.markdown("### ⏳ Epochs & Phylogeny")
                st.markdown("A macro-level analysis of your exhibit's history, identifying distinct eras and visualizing the evolutionary tree of its kingdoms.")

                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("#### The Great Epochs of History")
                    # Identify break points for epochs
                    break_points = {0, history_df['generation'].max()}
                    major_events = [e for e in events if e['type'] in ['Cataclysm', 'Genesis', 'Succession']]
                    for event in major_events:
                        break_points.add(event['generation'])
                    
                    sorted_breaks = sorted(list(break_points))
                    
                    if len(sorted_breaks) < 2:
                        st.info("Not enough major events have occurred to define distinct historical epochs.")
                    else:
                        for i in range(len(sorted_breaks) - 1):
                            start_gen = sorted_breaks[i]
                            end_gen = sorted_breaks[i+1]
                            
                            epoch_df = history_df[(history_df['generation'] >= start_gen) & (history_df['generation'] <= end_gen)]
                            if epoch_df.empty: continue

                            # Determine epoch name from the event that started it
                            start_event = next((e for e in major_events if e['generation'] == start_gen), None)
                            epoch_name = f"Epoch {i+1}"
                            if i == 0 and not start_event: epoch_name = "The Primordial Era"
                            elif start_event: epoch_name = f"The {start_event['title']} Era"

                            with st.expander(f"**{epoch_name}** (Epochs {start_gen} - {end_gen})"):
                                # --- NEW: More complex and shocking details ---
                                c1, c2, c3 = st.columns(3)
                                
                                # 1. Core Metrics
                                with c1:
                                    st.markdown("##### Core Metrics")
                                    dominant_kingdom = epoch_df['kingdom_id'].mode()[0] if not epoch_df['kingdom_id'].mode().empty else "N/A"
                                    mean_fitness = epoch_df['fitness'].mean()
                                    peak_complexity = epoch_df['complexity'].max()
                                    st.metric("Dominant Kingdom", dominant_kingdom)
                                    st.metric("Mean Fitness", f"{mean_fitness:.3f}")
                                    st.metric("Peak Complexity", f"{peak_complexity:.2f}")

                                # 2. Evolutionary Dynamics
                                with c2:
                                    st.markdown("##### Dynamics")
                                    start_fitness = history_df[history_df['generation'] == start_gen]['fitness'].mean()
                                    end_fitness = history_df[history_df['generation'] == end_gen]['fitness'].mean()
                                    velocity = (end_fitness - start_fitness) / max(1, end_gen - start_gen)
                                    st.metric("Evolutionary Velocity", f"{velocity*100:.2f} ΔF/100epochs")

                                    apex_organism_idx = epoch_df['fitness'].idxmax()
                                    apex_organism = epoch_df.loc[apex_organism_idx]
                                    st.markdown(f"**Apex Predator:** A `{apex_organism['kingdom_id']}` organism reached a peak fitness of **{apex_organism['fitness']:.3f}** with complexity **{apex_organism['complexity']:.1f}**.")

                                # 3. Innovations and Extinctions
                                with c3:
                                    st.markdown("##### Historical Events")
                                    epoch_events = [e for e in events if start_gen <= e['generation'] < end_gen]
                                    innovations = [e['title'] for e in epoch_events if 'Innovation' in e['type']]
                                    if innovations:
                                        st.markdown("**Key Innovations:**")
                                        for innov in innovations[:3]:
                                            st.markdown(f"- `{innov.replace('New Component: ', '').replace('New Sense: ', '')}`")
                                    
                                    kingdoms_at_start = set(history_df[history_df['generation'] == start_gen]['kingdom_id'].unique())
                                    kingdoms_at_end = set(history_df[history_df['generation'] == end_gen]['kingdom_id'].unique())
                                    extinct_kingdoms = kingdoms_at_start - kingdoms_at_end
                                    if extinct_kingdoms:
                                        st.markdown("**Extinctions:**")
                                        for kingdom in extinct_kingdoms:
                                            st.markdown(f"- The **{kingdom}** kingdom perished.")

                with col2:
                    st.markdown("#### The Tree of Life (Phylogeny)")
                    phylogeny_graph = nx.DiGraph()
                    # Find the first occurrence of each kingdom
                    first_occurrence = history_df.loc[history_df.groupby('kingdom_id')['generation'].idxmin()]
                    
                    for _, row in first_occurrence.iterrows():
                        kingdom = row['kingdom_id']
                        gen = row['generation']
                        phylogeny_graph.add_node(kingdom, label=f"{kingdom}\n(Epoch {gen})")

                        # Find parent lineage
                        parent_ids_list = history_df.loc[history_df['lineage_id'] == row['lineage_id'], 'parent_ids'].iloc[0]
                        
                        if isinstance(parent_ids_list, list) and len(parent_ids_list) > 0:
                            first_parent_id = parent_ids_list[0]
                            parent_df = history_df[history_df['lineage_id'] == first_parent_id]
                            
                            if not parent_df.empty:
                                parent_kingdom = parent_df.iloc[0]['kingdom_id']
                                if parent_kingdom != kingdom and parent_kingdom in phylogeny_graph.nodes():
                                    phylogeny_graph.add_edge(parent_kingdom, kingdom)

                    if not phylogeny_graph.nodes():
                        st.info("No kingdom data to build a tree of life.")
                    else:
                        fig_tree, ax_tree = plt.subplots(figsize=(5, 4))
                        pos = nx.spring_layout(phylogeny_graph, seed=42, k=0.9)
                        labels = nx.get_node_attributes(phylogeny_graph, 'label')
                        nx.draw(phylogeny_graph, pos, labels=labels, with_labels=True, node_size=3000, node_color='#9E7676', font_size=8, font_color='white', arrowsize=20, ax=ax_tree)
                        ax_tree.set_title("Phylogeny of Kingdoms")
                        st.pyplot(fig_tree)
                        plt.clf()
                
                # --- NEW: Dynastic Histories Section ---
                st.markdown("---")
                st.markdown("### 👑 Dynastic Histories")
                st.markdown("Trace the complete story of the most influential lineages in your exhibit. Select a dynasty to view its rise, its peak, and its eventual fate.")

                # Identify major lineages from apex predators of each epoch
                major_lineages = {}
                if len(sorted_breaks) > 1:
                    for i in range(len(sorted_breaks) - 1):
                        start_gen, end_gen = sorted_breaks[i], sorted_breaks[i+1]
                        epoch_df = history_df[(history_df['generation'] >= start_gen) & (history_df['generation'] <= end_gen)]
                        if not epoch_df.empty:
                            apex_organism_idx = epoch_df['fitness'].idxmax()
                            apex_organism = epoch_df.loc[apex_organism_idx]
                            lineage_id = apex_organism['lineage_id']
                            if lineage_id not in major_lineages:
                                major_lineages[lineage_id] = f"Apex of Epoch {i+1} (Epoch {apex_organism['generation']})"

                if not major_lineages:
                    st.info("No major dynasties have been identified yet. Run a longer simulation to establish dominant lineages.")
                else:
                    lineage_options = list(major_lineages.keys())
                    selected_lineage_id = st.selectbox(
                        "Select a Dynasty to Investigate",
                        options=lineage_options,
                        format_func=lambda x: f"Lineage {x} ({major_lineages[x]})"
                    )

                    if selected_lineage_id:
                        lineage_df = history_df[history_df['lineage_id'] == selected_lineage_id].sort_values('generation')
                        universe_avg_df = history_df.groupby('generation')[['fitness', 'complexity']].mean().reset_index()

                        # --- 1. Summary Stats ---
                        founder = lineage_df.iloc[0]
                        peak = lineage_df.loc[lineage_df['fitness'].idxmax()]
                        survived_gens = lineage_df['generation'].nunique()

                        c1, c2, c3, c4 = st.columns(4)
                        c1.metric("Founded in Epoch", f"{founder['generation']}")
                        c2.metric("Founder's Kingdom", founder['kingdom_id'])
                        c3.metric("Peak Fitness", f"{peak['fitness']:.3f}")
                        c4.metric("Epochs of Dominance", f"{survived_gens}")

                        # --- 2. Performance Chart ---
                        fig_lineage = go.Figure()
                        fig_lineage.add_trace(go.Scatter(x=lineage_df['generation'], y=lineage_df['fitness'], mode='lines', name=f'Lineage {selected_lineage_id} Fitness', line=dict(color='cyan', width=3)))
                        fig_lineage.add_trace(go.Scatter(x=universe_avg_df['generation'], y=universe_avg_df['fitness'], mode='lines', name='Exhibit Avg. Fitness', line=dict(color='gray', dash='dot')))
                        fig_lineage.update_layout(title=f"Fitness Trajectory of Dynasty {selected_lineage_id}", height=300, margin=dict(l=0, r=0, t=40, b=0))
                        st.plotly_chart(fig_lineage, width='stretch', key=f"dynasty_perf_{selected_lineage_id}")

                        # --- NEW: More Complex Details ---
                        sub_col1, sub_col2 = st.columns(2)

                        with sub_col1:
                            # --- Dynastic Event Log ---
                            st.markdown("##### Dynastic Event Log")
                            dynasty_events = [e for e in events if founder['generation'] <= e['generation'] <= lineage_df.iloc[-1]['generation']]
                            if not dynasty_events:
                                st.info("This dynasty's lifespan was uneventful.")
                            else:
                                event_log_container = st.container(height=200)
                                for event in sorted(dynasty_events, key=lambda x: x['generation']):
                                    event_log_container.markdown(f"**Epoch {event['generation']}:** {event['icon']} {event['title']}")

                            # --- Legacy of Innovation ---
                            st.markdown("##### Legacy of Innovation")
                            innovations = [e for e in dynasty_events if 'Innovation' in e['type'] and e.get('lineage_id') == selected_lineage_id]
                            if not innovations:
                                st.info("This dynasty was a follower, not an innovator.")
                            else:
                                for innov in innovations:
                                    st.markdown(f"💡 Invented **{innov['title'].split(': ')[1]}** in Epoch {innov['generation']}.")

                        with sub_col2:
                            # --- Evolved Strategy Profile ---
                            st.markdown("##### Apex Strategy Profile (GRN Analysis)")
                            apex_specimen = max((g for g in st.session_state.get('gene_archive', []) if g.lineage_id == peak['lineage_id']), key=lambda g: g.fitness, default=None)
                            if apex_specimen:
                                rule_actions = Counter(r.action_type for r in apex_specimen.rule_genes)
                                action_df = pd.DataFrame.from_dict(rule_actions, orient='index', columns=['Count']).reset_index()
                                fig_strategy = px.bar(action_df, x='index', y='Count', title="GRN Action Type Frequency", labels={'index': 'Action Type'})
                                fig_strategy.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
                                st.plotly_chart(fig_strategy, width='stretch', key=f"dynasty_strat_{selected_lineage_id}")

                        # --- 3. Gallery of Ancestors ---
                        st.markdown("##### Gallery of Ancestors")
                        
                        last_known_member = lineage_df.iloc[-1]
                        ancestors_to_find = {
                            'Founder': (founder['generation'], founder['lineage_id']),
                            'Apex': (peak['generation'], peak['lineage_id']),
                            'Last Known': (last_known_member['generation'], last_known_member['lineage_id'])
                        }
                        
                        ancestor_specimens = {}
                        gene_archive = st.session_state.get('gene_archive', [])
                        for role, (gen, l_id) in ancestors_to_find.items():
                            candidate = max(
                                (g for g in gene_archive if g.generation == gen and g.lineage_id == l_id),
                                key=lambda g: g.fitness, default=None)
                            if candidate:
                                ancestor_specimens[role] = candidate

                        if not ancestor_specimens:
                            st.warning("Could not retrieve ancestor data from the gene archive for this dynasty.")
                        else:
                            cols = st.columns(len(ancestor_specimens))
                            for i, (role, specimen) in enumerate(ancestor_specimens.items()):
                                with cols[i]:
                                    st.markdown(f"**The {role}** (Epoch {specimen.generation})")
                                    st.metric("Fitness", f"{specimen.fitness:.4f}")
                                    with st.spinner(f"Growing {role}..."):
                                        vis_grid = ExhibitGrid(s)
                                        phenotype = Phenotype(specimen, vis_grid, s)
                                        fig = visualize_phenotype_2d(phenotype, vis_grid)
                                        fig.update_layout(height=250, title=None, margin=dict(l=0, r=0, t=0, b=0))
                                        st.plotly_chart(fig, width='stretch', key=f"dynasty_vis_{selected_lineage_id}_{i}")
                
                # --- NEW: Pantheon of Genes Section ---
                st.markdown("---")
                st.markdown("### 🔬 The Pantheon of Life")
                st.markdown("A hall of fame for the most impactful genetic 'ideas' of your exhibit. This analyzes the entire fossil record to identify the components and rule strategies that defined success.")

                gene_archive = st.session_state.get('gene_archive', [])
                if not gene_archive:
                    st.info("The gene archive is empty. Run a simulation to populate the fossil record.")
                else:
                    pantheon_col1, pantheon_col2 = st.columns(2)

                    with pantheon_col1:
                        st.markdown("#### The Pantheon of Components")
                        
                        # --- Analysis ---
                        all_components = {}
                        for genotype in gene_archive:
                            for comp_name, comp_gene in genotype.component_genes.items():
                                if comp_name not in all_components:
                                    all_components[comp_name] = {
                                        'gene': comp_gene,
                                        'first_gen': genotype.generation,
                                        'inventor_lineage': genotype.lineage_id,
                                        'fitness_sum': 0,
                                        'usage_count': 0,
                                        'prevalence_history': Counter()
                                    }
                                all_components[comp_name]['fitness_sum'] += genotype.fitness
                                all_components[comp_name]['usage_count'] += 1
                                all_components[comp_name]['prevalence_history'][genotype.generation] += 1

                        # Calculate scores
                        scored_components = []
                        for name, data in all_components.items():
                            avg_fitness = data['fitness_sum'] / data['usage_count'] if data['usage_count'] > 0 else 0
                            longevity = history_df['generation'].max() - data['first_gen']
                            final_prevalence = sum(1 for g in population if name in g.component_genes) if population else 0
                            
                            score = (avg_fitness * 100) + (longevity * 0.1) + (final_prevalence * 1)
                            data['score'] = score
                            scored_components.append(data)

                        # Display top components
                        for i, comp_data in enumerate(sorted(scored_components, key=lambda x: x['score'], reverse=True)[:5]):
                            comp_gene = comp_data['gene']
                            with st.expander(f"**{i+1}. {comp_gene.name}** (Score: {comp_data['score']:.0f})", expanded=(i<2)):
                                st.markdown(f"Invented in **Epoch {comp_data['first_gen']}** by Dynasty `{comp_data['inventor_lineage']}`")
                                st.code(f"[{comp_gene.color}] Base: {comp_gene.base_kingdom}, Mass: {comp_gene.mass:.2f}, Struct: {comp_gene.structural:.2f}, E.Store: {comp_gene.energy_storage:.2f}", language="text")
                                
                                # Prevalence Plot
                                history = comp_data['prevalence_history']
                                prevalence_df = pd.DataFrame(list(history.items()), columns=['generation', 'count']).sort_values('generation')
                                fig_prevalence = px.area(prevalence_df, x='generation', y='count', title="Prevalence Over Time")
                                fig_prevalence.update_layout(height=200, margin=dict(l=0, r=0, t=30, b=0))
                                st.plotly_chart(fig_prevalence, width='stretch', key=f"pantheon_prevalence_{comp_gene.id}")

                    with pantheon_col2:
                        st.markdown("#### The Lawgivers: Elite Genetic Strategies")
                        
                        # Find elite specimens
                        elites = []
                        if population:
                            sorted_pop = sorted(population, key=lambda x: x.fitness, reverse=True)
                            seen_kingdoms = set()
                            for org in sorted_pop:
                                if org.kingdom_id not in seen_kingdoms:
                                    elites.append(org)
                                    seen_kingdoms.add(org.kingdom_id)
                        
                        if not elites:
                            st.info("No elite organisms found to analyze.")
                        else:
                            # Analyze rule actions and conditions
                            elite_actions = Counter()
                            elite_conditions = Counter()
                            for elite in elites:
                                elite_actions.update(r.action_type for r in elite.rule_genes)
                                for r in elite.rule_genes:
                                    elite_conditions.update(c['source'] for c in r.conditions)

                            action_df = pd.DataFrame(elite_actions.items(), columns=['Action', 'Count']).sort_values('Count', ascending=False)
                            cond_df = pd.DataFrame(elite_conditions.items(), columns=['Condition', 'Count']).sort_values('Count', ascending=False)

                            fig_actions = px.bar(action_df, x='Action', y='Count', title="Elite Strategic Blueprint (GRN Actions)")
                            fig_actions.update_layout(height=250, margin=dict(l=0, r=0, t=40, b=0))
                            st.plotly_chart(fig_actions, width='stretch', key="pantheon_elite_actions")

                            fig_conds = px.bar(cond_df, x='Condition', y='Count', title="Elite Sensory Profile (GRN Conditions)")
                            fig_conds.update_layout(height=250, margin=dict(l=0, r=0, t=40, b=0))
                            st.plotly_chart(fig_conds, width='stretch', key="pantheon_elite_conditions")


        with tab_analytics_lab:
            if st.session_state.analytics_lab_visible:
                st.header("📊 Custom Analytics Lab")
                st.markdown("A flexible laboratory for generating custom 2D plots to explore relationships within your exhibit's history. Configure the number of plots in the Curator's Console.")
                st.markdown("---")

                num_plots = s.get('num_custom_plots', 4)
                
                plot_functions = [
                    plot_fitness_vs_complexity,
                    plot_lifespan_vs_cell_count,
                    plot_energy_dynamics,
                    plot_complexity_density,
                    plot_fitness_violin_by_kingdom,
                    plot_complexity_vs_lifespan,
                    plot_energy_efficiency_over_time,
                    plot_cell_count_dist_by_kingdom,
                    plot_lifespan_dist_by_kingdom,
                    plot_complexity_vs_energy_prod,
                    plot_fitness_scatter_over_time,
                    plot_elite_parallel_coords
                ]

                cols = st.columns(2)
                for i in range(num_plots):
                    with cols[i % 2]:
                        if i < len(plot_functions):
                            plot_func = plot_functions[i]
                            fig = plot_func(history_df, key=f"custom_plot_{i}")
                            st.plotly_chart(fig, width='stretch', key=f"custom_plotly_chart_{i}")
                
                st.markdown("---")
                if st.button("Clear & Hide Analytics Lab", key="hide_analytics_lab_button"):
                    st.session_state.analytics_lab_visible = False
                    st.rerun()

            else:
                st.info("This tab renders custom plots. It is paused to save memory.")
                if st.button("📊 Render Custom Analytics Lab", key="render_analytics_lab_button"):
                    st.session_state.analytics_lab_visible = True
                    st.rerun()
        
        
        
        st.markdown("---")
        
        try:
            final_grid_state = {}
            if 'exhibit_grid' in st.session_state and st.session_state.exhibit_grid is not None:
                final_grid_state = {name: arr.tolist() for name, arr in st.session_state.exhibit_grid.resource_map.items()}

            download_data = {
                "settings": st.session_state.settings,
                "history": st.session_state.history,
                "evolutionary_metrics": st.session_state.evolutionary_metrics,
                "genesis_events": st.session_state.get('genesis_events', []),
                "final_population_genotypes": [asdict(g) for g in population] if population else [],
                "full_gene_archive": [asdict(g) for g in st.session_state.get('gene_archive', [])],
                "final_physics_constants": CHEMICAL_BASES_REGISTRY,
                "final_evolved_senses": st.session_state.get('evolvable_condition_sources', []),
                "final_grid_state": final_grid_state
            }
            
            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
                json_string = json.dumps(download_data, indent=4, cls=GenotypeJSONEncoder)
                
                file_name_in_zip = f"exhibit_archive_{s.get('experiment_name', 'run').replace(' ', '_')}.json"
                zf.writestr(file_name_in_zip, json_string.encode('utf-8'))

            st.download_button(
                label="📥 Download Exhibit Archive (.zip)",
                data=zip_buffer.getvalue(),
                file_name=f"exhibit_archive_{s.get('experiment_name', 'run').replace(' ', '_')}.zip",
                mime="application/zip", # Correct MIME type for zip
                help="Download the complete exhibit state (settings, history, gene archive) as a compressed ZIP file."
            )
            
        except Exception as e:
            st.error(f"Could not prepare data for download: {e}")
            st.exception(e)
        

if __name__ == "__main__":
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    original_toast = st.toast
    def chronicle_toast(body, icon=None):
        if "New component" in body:
            lineage_id = None
            if "lineage:" in body:
                parts = body.split(" lineage:")
                body = parts[0]
                lineage_id = parts[1]
            st.session_state.genesis_events.append({
                'generation': st.session_state.history[-1]['generation'] if st.session_state.history else 0,
                'type': 'Component Innovation', 'title': f"New Component: {body.split('**')[1]}",
                'description': f"A new cellular component, '{body.split('**')[1]}', was invented, expanding the chemical and functional possibilities for life.", 'icon': '✨',
                'lineage_id': lineage_id
            })
        if "new sense" in body:
            st.session_state.genesis_events.append({
                'generation': st.session_state.history[-1]['generation'] if st.session_state.history else 0,
                'type': 'Sense Innovation', 'title': f"New Sense: {body.split('**')[1]}",
                'description': f"Life has evolved a new way to perceive its environment: '{body.split('**')[1]}'. This opens up entirely new evolutionary pathways.", 'icon': '👁️'
            })
        original_toast(body, icon=icon)
    st.toast = chronicle_toast
    main()
              
