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
        page_title="Museum of Universal Life",
        layout="wide",
        page_icon="🏛️",
        initial_sidebar_state="expanded"
    )

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
    def check_password_on_change():
        try:
            correct_pass = st.secrets["passwords"]["app_password"]
        except (KeyError, AttributeError):
            st.error("FATAL ERROR: No password found in Streamlit Secrets.")
            st.info("Please ensure you have a .streamlit/secrets.toml file with:\n\n[passwords]\napp_password = 'your_password'")
            st.session_state.password_correct = False
            return

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
    
    st.sidebar.markdown('<h1 style="text-align: center; color: #00aaff;">🏛️<br>Museum of Universal Life</h1>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    s = copy.deepcopy(st.session_state.settings)

    if st.sidebar.button("Reset Console to Defaults", width='stretch', key="reset_defaults_button"):
        st.session_state.settings.clear()
        st.toast("Curator's Console reset to defaults!", icon="⚙️")
        time.sleep(1)
        st.rerun()

    if st.sidebar.button("Decommission Museum & Restart", width='stretch', key="clear_state_button"):
        db.truncate()
        st.session_state.clear()
        st.toast("Cleared all archived data. The museum has been reset.", icon="🗑️")
        time.sleep(1)
        st.rerun()
        
    with st.sidebar.expander("🌠 Exhibit Hall Manager (Your Personal Collections)", expanded=True):
        presets = st.session_state.exhibit_presets
        preset_names = ["<Select a Collection to Load>"] + list(presets.keys())
        
        c1, c2 = st.columns(2)
        with c1:
            new_preset_name = st.text_input("New Collection Name", placeholder="e.g., 'High-Gravity Worlds'")
        with c2:
            st.write(" ") # Spacer
            if st.button("💾 Archive Current Exhibit", width='stretch'):
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
                    
                    st.toast(f"Collection '{new_preset_name}' (with results) archived!", icon="💾")
                    st.session_state.exhibit_presets = presets
                    st.rerun()
                else:
                    st.warning("Please enter a name for your collection.")

        selected_preset = st.selectbox("Load from Personal Collection", options=preset_names, index=0)
        
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
                st.toast(f"Deleted collection '{selected_preset}'.", icon="🗑️")
                st.rerun()
                    
        st.sidebar.markdown("---")
        st.sidebar.markdown("#### 💾 Load Exhibit from Archive File")
        uploaded_file = st.sidebar.file_uploader(
            "Upload your 'exhibit_archive.json' or .zip file", 
            type=["json", "zip"],
            key="checkpoint_uploader"
        )
        
        if st.sidebar.button("LOAD FROM UPLOADED FILE", width='stretch', key="load_checkpoint_button"):
            if uploaded_file is not None:
                try:
                    data = None
                    
                    if uploaded_file.name.endswith('.zip'):
                        st.toast("Unzipping archive... Please wait.", icon="📦")
                        mem_zip = io.BytesIO(uploaded_file.getvalue())
                        
                        with zipfile.ZipFile(mem_zip, 'r') as zf:
                            json_filename = None
                            for f in zf.namelist():
                                if f.endswith('.json') and not f.startswith('__MACOSX'):
                                    json_filename = f
                                    break
                            
                            if json_filename:
                                st.toast(f"Found '{json_filename}' inside zip.", icon="📄")
                                with zf.open(json_filename) as f:
                                    data = json.load(f)
                            else:
                                st.error("No .json file found inside the .zip archive.")
                    
                    elif uploaded_file.name.endswith('.json'):
                        st.toast("Loading .json file...", icon="📄")
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
                        
                        st.toast("✅ Archive Loaded! You can now 'Extend Simulation'.", icon="🎉")
                        
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
                            
                            You are ready to click **'🧬 Extend Simulation'** to proceed from Epoch {last_gen + 1}.
                            """
                        )
                        
                        st.rerun()
                    
                    elif data is None and not uploaded_file.name.endswith('.zip'):
                        st.error("File is not a .zip or .json file.")
                        
                except Exception as e:
                    st.error(f"Failed to load archive: {e}")
            else:
                st.warning("Please upload a file first.")
        
    st.sidebar.markdown("### 🌍 Gallery Physics & Astrobiology")
    with st.sidebar.expander("Fundamental Physical Constants", expanded=False):
        st.markdown("Set the fundamental, unchanging laws of this gallery.")
        s['gravity'] = st.slider("Gravity", 0.0, 20.0, s.get('gravity', 9.8), 0.1, help="Influences motility cost.")
        s['em_coupling'] = st.slider("Electromagnetic Coupling", 0.1, 2.0, s.get('em_coupling', 1.0), 0.05, help="Scales energy from light (photosynthesis).")
        s['thermo_efficiency'] = st.slider("Thermodynamic Efficiency", 0.1, 1.0, s.get('thermo_efficiency', 0.25), 0.01, help="Base energy loss from all actions (entropy).")
        s['planck_scale'] = st.slider("Computational Planck Scale", 1, 10, s.get('planck_scale', 1), 1, help="Minimum 'granularity' of computation (conceptual).")
        s['cosmic_radiation'] = st.slider("Cosmic Radiation (Mutation)", 0.0, 1.0, s.get('cosmic_radiation', 0.1), 0.01, help="Baseline environmental mutation pressure.")
        s['universe_age_factor'] = st.slider("Universe Age Factor", 0.1, 10.0, s.get('universe_age_factor', 1.0), 0.1, help="Scales how fast resources change or decay.")
        s['dark_energy_pressure'] = st.slider("Dark Energy Pressure (Grid Expansion)", -1.0, 1.0, s.get('dark_energy_pressure', 0.0), 0.01, help="Conceptual: Positive values push organisms apart.")
        s['information_density_limit'] = st.slider("Information Density Limit", 1, 100, s.get('information_density_limit', 50), 1, help="Max complexity per cell (conceptual).")
        s['fundamental_constant_drift'] = st.slider("Fundamental Constant Drift", 0.0, 0.01, s.get('fundamental_constant_drift', 0.0), 0.0001, help="Rate at which constants like 'gravity' slowly change over eons.")
        
    with st.sidebar.expander("Grid & Resource Distribution", expanded=False):
        st.markdown("Define the exhibit environment itself.")
        s['grid_width'] = st.slider("Grid Width", 50, 500, s.get('grid_width', 100), 10)
        s['grid_height'] = st.slider("Grid Height", 50, 500, s.get('grid_height', 100), 10)
        s['light_intensity'] = st.slider("Light Energy Intensity", 0.0, 5.0, s.get('light_intensity', 1.0), 0.1)
        s['mineral_richness'] = st.slider("Mineral Richness", 0.0, 5.0, s.get('mineral_richness', 1.0), 0.1)
        s['water_abundance
