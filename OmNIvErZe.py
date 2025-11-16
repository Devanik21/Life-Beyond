# --------------------------------------------------------------------------------
# 🌌 THE MUSEUM OF INFINITE LIFE 🌌
#
# Welcome, Visitor.
#
# This application is an interactive museum exhibit showcasing the 'results'
# from a theoretical simulation of a universe. It uses the data structures
# and visualization code from the 'Universe Sandbox 2.0' simulation.
#
# The original simulation has been *removed* to ensure fast loading and 
# accessibility. Instead, this app generates a 'mock' dataset on its
# first run, allowing you to explore what *could* be.
#
# You can also load your own 'universe_results.zip' checkpoints from the
# original simulation using the 'Load Checkpoint' feature in the sidebar.
#
# --------------------------------------------------------------------------------

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
from scipy.special import softmax
import networkx as nx
import os
from collections import Counter, deque
import json
import uuid
import hashlib
import colorsys
import copy
import zipfile
import io
import matplotlib
import matplotlib.pyplot as plt # We'll need this for the GRN plots

# Set a non-interactive backend for Streamlit
matplotlib.use('Agg')

# =================================================================
#
# PART 1: THE "DATA" OF LIFE (The Museum's Collection)
#
# These are the core data structures from the original simulation.
# They define what an 'organism' is.
#
# =================================================================

@dataclass
class ComponentGene:
    """
    Defines a fundamental 'building block' of life.
    This is the 'chemistry' the organism has access to.
    """
    id: str = field(default_factory=lambda: f"comp_{uuid.uuid4().hex[:6]}")
    name: str = "PrimordialGoo"
    base_kingdom: str = "Carbon"
    mass: float = 1.0
    structural: float = 0.1
    energy_storage: float = 0.0
    photosynthesis: float = 0.0
    chemosynthesis: float = 0.0
    thermosynthesis: float = 0.0
    conductance: float = 0.0
    compute: float = 0.0
    motility: float = 0.0
    armor: float = 0.0
    sense_light: float = 0.0
    sense_minerals: float = 0.0
    sense_temp: float = 0.0
    color: str = "#888888"

    def __hash__(self):
        return hash(self.id)

@dataclass
class RuleGene:
    """
    Defines a 'developmental rule' in the Genetic Regulatory Network (GRN).
    'IF [Conditions] are met, THEN [Action] happens.'
    """
    id: str = field(default_factory=lambda: f"rule_{uuid.uuid4().hex[:6]}")
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    action_type: str = "IDLE"
    action_param: str = "self" 
    action_value: float = 0.0
    probability: float = 1.0
    priority: int = 0
    is_disabled: bool = False

@dataclass
class Genotype:
    """
    The complete "DNA" of an organism.
    This is the "specimen" in the museum's collection.
    """
    id: str = field(default_factory=lambda: f"geno_{uuid.uuid4().hex[:6]}")
    component_genes: Dict[str, ComponentGene] = field(default_factory=dict)
    rule_genes: List[RuleGene] = field(default_factory=list)
    
    # --- Evolutionary Metadata ---
    fitness: float = 0.0
    age: int = 0
    generation: int = 0
    lineage_id: str = ""
    parent_ids: List[str] = field(default_factory=list)
    
    # --- Phenotypic Summary (filled after development) ---
    cell_count: int = 0
    complexity: float = 0.0
    energy_production: float = 0.0
    energy_consumption: float = 0.0
    lifespan: int = 0
    kingdom_id: str = "Carbon" 
    
    # --- Meta-Evolution (Hyperparameters) ---
    evolvable_mutation_rate: float = 0.2
    evolvable_innovation_rate: float = 0.05
    objective_weights: Dict[str, float] = field(default_factory=dict)

    # --- Multi-Level Selection ---
    colony_id: Optional[str] = None
    individual_fitness: float = 0.0

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
        dominant_comp = max(self.component_genes.values(), key=lambda c: c.structural, default=None)
        if dominant_comp:
            self.kingdom_id = dominant_comp.base_kingdom
        else:
            comp_counts = Counter(c.base_kingdom for c in self.component_genes.values())
            if comp_counts:
                self.kingdom_id = comp_counts.most_common(1)[0][0]
            else:
                self.kingdom_id = "Unclassified"

# =================================================================
#
# PART 2: PHENOTYPE & GRID (The "Display Case")
#
# These classes are needed to *visualize* the Genotype.
#
# =================================================================

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
    state_vector: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GridCell:
    """A single cell in the 2D universe grid."""
    x: int
    y: int
    light: float = 0.0
    minerals: float = 0.0
    water: float = 0.0
    temperature: float = 0.0
    organism_id: Optional[str] = None
    cell_type: Optional[str] = None

class UniverseGrid:
    """
    The environment simulation.
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
        
        # --- Generate Mock Resource Maps ---
        # In a real app, we'd use Perlin noise, but random is faster for a demo.
        self.resource_map['light'] = np.random.rand(self.width, self.height) * self.settings.get('light_intensity', 1.0)
        self.resource_map['minerals'] = np.random.rand(self.width, self.height) * self.settings.get('mineral_richness', 1.0)
        self.resource_map['water'] = np.random.rand(self.width, self.height) * self.settings.get('water_abundance', 1.0)
        
        temp_gradient = np.linspace(self.settings.get('temp_pole', -20), self.settings.get('temp_equator', 30), self.height)
        temp_map = np.tile(temp_gradient, (self.width, 1))
        self.resource_map['temperature'] = temp_map + (np.random.rand(self.width, self.height) - 0.5) * 10
        
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

class Phenotype:
    """
    The 'body' of the organism. This class is now a
    *visualization helper* to "grow" a Genotype for display.
    """
    def __init__(self, genotype: Genotype, universe_grid: UniverseGrid, settings: Dict):
        self.id = f"org_{uuid.uuid4().hex[:6]}"
        self.genotype = genotype
        self.grid = universe_grid
        self.settings = settings
        self.cells: Dict[Tuple[int, int], OrganismCell] = {}
        self.total_energy = 0.0
        self.age = 0
        self.is_alive = True
        
        self.spawn_zygote()
        if self.is_alive:
            self.develop()

    def spawn_zygote(self):
        x, y = self.grid.width // 2, self.grid.height // 2
        grid_cell = self.grid.get_cell(x, y)
        if not grid_cell:
            self.is_alive = False
            return

        if not self.genotype.component_genes:
            self.is_alive = False
            return
            
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
        A *simplified* "Embryogeny" process for visualization.
        It runs the GRN to produce a body plan.
        """
        max_dev_steps = self.settings.get('development_steps', 50)
        
        for step in range(max_dev_steps):
            if not self.cells:
                self.is_alive = False
                break
            
            actions_to_take = []
            
            # --- 1. Evaluate all rules for all cells ---
            for (x, y), cell in list(self.cells.items()):
                grid_cell = self.grid.get_cell(x, y)
                if not grid_cell: continue
                
                neighbors = self.grid.get_neighbors(x, y)
                
                context = {
                    'self_energy': cell.energy,
                    'self_age': cell.age,
                    'self_type': cell.component.name,
                    'env_light': grid_cell.light,
                    'neighbor_count_empty': sum(1 for n in neighbors if n.organism_id is None),
                }
                
                for rule in self.genotype.rule_genes:
                    if random.random() > rule.probability:
                        continue
                    if self.check_conditions(rule, context, cell, neighbors):
                        actions_to_take.append((rule, cell))
            
            # --- 2. Execute actions ---
            actions_to_take.sort(key=lambda x: x[0].priority, reverse=True)
            new_cells = {}
            for rule, cell in actions_to_take:
                if (cell.x, cell.y) not in self.cells:
                    continue
                self.execute_action(rule, cell, new_cells)
            
            self.cells.update(new_cells)
            
            # --- 3. Prune dead cells ---
            dead_cells = []
            for (x,y), cell in list(self.cells.items()):
                cell.age += 1
                cell.energy -= 0.1 # Base metabolic cost for dev
                if cell.energy <= 0:
                    dead_cells.append((x,y))
            
            for (x,y) in dead_cells:
                self.prune_cell(x,y)

        if not self.cells:
            self.is_alive = False

    def prune_cell(self, x, y):
        if (x,y) in self.cells:
            del self.cells[(x,y)]
        grid_cell = self.grid.get_cell(x, y)
        if grid_cell:
            grid_cell.organism_id = None
            grid_cell.cell_type = None

    def check_conditions(self, rule: RuleGene, context: Dict, cell: OrganismCell, neighbors: List[GridCell]) -> bool:
        """Simplified rule-matching engine."""
        if not rule.conditions: return True
        
        for cond in rule.conditions:
            source = cond['source']
            value = 0.0
            
            if source in context:
                value = context.get(source, 0.0)
            
            op = cond['operator']
            target = cond['target_value']
            
            try:
                if op == '>':
                    if not (value > target): return False
                elif op == '<':
                    if not (value < target): return False
                elif op == '==':
                    if not (value == target): return False
            except TypeError:
                return False
        return True

    def execute_action(self, rule: RuleGene, cell: OrganismCell, new_cells: Dict):
        """Simplified action execution engine."""
        action = rule.action_type
        param = rule.action_param
        
        try:
            if action == "GROW":
                empty_neighbors = [n for n in self.grid.get_neighbors(cell.x, cell.y) if n.organism_id is None]
                if empty_neighbors:
                    target_grid_cell = random.choice(empty_neighbors)
                    new_comp = self.genotype.component_genes.get(param)
                    if not new_comp: return
                    
                    grow_cost = 0.5 + new_comp.mass
                    if cell.energy < grow_cost: return
                    
                    new_cell = OrganismCell(
                        organism_id=self.id,
                        component=new_comp,
                        x=target_grid_cell.x,
                        y=target_grid_cell.y,
                        energy=1.0,
                        state_vector={'type_id': hash(new_comp.id), 'energy': 1.0}
                    )
                    new_cells[(target_grid_cell.x, target_grid_cell.y)] = new_cell
                    target_grid_cell.organism_id = self.id
                    target_grid_cell.cell_type = new_comp.name
                    cell.energy -= grow_cost

            elif action == "DIFFERENTIATE":
                new_comp = self.genotype.component_genes.get(param)
                if new_comp and cell.component.id != new_comp.id:
                    diff_cost = 0.2 + abs(new_comp.mass - cell.component.mass)
                    if cell.energy < diff_cost: return
                    
                    cell.component = new_comp
                    self.grid.get_cell(cell.x, cell.y).cell_type = new_comp.name
                    cell.energy -= diff_cost

            elif action == "DIE":
                self.prune_cell(cell.x, cell.y)

        except Exception:
            pass # Fail silently

# =================================================================
#
# PART 3: THE CURATOR (Mock Data Generation)
#
# This is the most important new part. It generates a "fake"
# museum collection on the first app load, so we have
# something to visualize without running the real simulation.
#
# =================================================================

# This is the 'primordial soup' of chemical bases from your file.
# It is the heart of the "infinite" museum.
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
    # ... (The other 180+ entries from your file would go here) ...
    # For this example, I'll just use the ones above.
}

# --- Helper functions to create mock data (from your file) ---

def innovate_component(genotype: Optional[Genotype], settings: Dict, force_base: Optional[str] = None) -> ComponentGene:
    """Create a new, random building block (a new 'gene')."""
    if force_base:
        base_name = force_base
    else:
        allowed_bases = settings.get('chemical_bases', ['Carbon', 'Silicon'])
        if not allowed_bases: allowed_bases = ['Carbon']
        base_name = random.choice(allowed_bases)
        
    base_template = CHEMICAL_BASES_REGISTRY.get(base_name, CHEMICAL_BASES_REGISTRY['Carbon'])

    prefixes = ['Proto', 'Hyper', 'Neuro', 'Cryo', 'Xeno', 'Bio', 'Meta', 'Photo', 'Astro', 'Quantum']
    suffixes = ['Polymer', 'Crystal', 'Node', 'Shell', 'Core', 'Matrix', 'Membrane', 'Processor', 'Fluid', 'Weave']
    new_name = f"{random.choice(prefixes)}-{base_name}-{random.choice(suffixes)}_{random.randint(0, 99)}"
    
    h, s, v = base_template['color_hsv_range']
    color = colorsys.hsv_to_rgb(random.uniform(h[0], h[1]), random.uniform(s[0], s[1]), random.uniform(v[0], v[1]))
    color_hex = f'#{int(color[0]*255):02x}{int(color[1]*255):02x}{int(color[2]*255):02x}'

    new_comp = ComponentGene(name=new_name, base_kingdom=base_name, color=color_hex)
    new_comp.mass = random.uniform(base_template['mass_range'][0], base_template['mass_range'][1])
    new_comp.structural = random.uniform(0.1, 0.5) * random.choice([0, 0, 0, 1, 2]) * base_template.get('structural_mult', (1.0, 1.0))[0]
    new_comp.energy_storage = random.uniform(0.1, 0.5) * random.choice([0, 1, 2]) * base_template.get('energy_storage_mult', (1.0, 1.0))[0]
    
    props_with_bias = ['photosynthesis', 'chemosynthesis', 'thermosynthesis', 'conductance', 'compute', 'motility', 'armor', 'sense_light', 'sense_minerals', 'sense_temp']
    for prop in props_with_bias:
        bias = base_template.get(f"{prop}_bias", 0.0)
        if random.random() < (abs(bias) + 0.05):
            val = np.clip(random.uniform(0.5, 1.5) + bias, 0, 5.0)
            setattr(new_comp, prop, val)
            
    return new_comp

def innovate_rule(genotype: Genotype, settings: Dict) -> RuleGene:
    """Create a new, random developmental rule."""
    num_conditions = random.randint(1, 2)
    conditions = []
    
    available_sources = ['self_energy', 'self_age', 'env_light', 'neighbor_count_empty']
    
    for _ in range(num_conditions):
        source = random.choice(available_sources)
        op = random.choice(['>', '<'])
        if source == 'self_energy': target = random.uniform(1.0, 10.0)
        elif source == 'self_age': target = random.randint(1, 5)
        else: target = random.uniform(0.1, 0.9)
        conditions.append({'source': source, 'operator': op, 'target_value': target})

    action_type = random.choice(['GROW', 'DIFFERENTIATE', 'DIE'])
    
    if not genotype.component_genes:
        return RuleGene(action_type="IDLE") # Failsafe
    
    action_param = random.choice(list(genotype.component_genes.keys()))
    
    return RuleGene(
        conditions=conditions,
        action_type=action_type,
        action_param=action_param,
        priority=random.randint(0, 10)
    )

def get_primordial_soup_genotype(settings: Dict) -> Genotype:
    """Creates a 'primordial' genotype with basic components and rules."""
    comp_zygote = innovate_component(None, settings, force_base='Carbon')
    comp_zygote.name = "Zygote"
    comp_struct = innovate_component(None, settings)
    comp_struct.name = "Struct"
    comp_energy = innovate_component(None, settings)
    comp_energy.name = "Energy"
    components = {c.name: c for c in [comp_struct, comp_energy, comp_zygote]}
    
    rules = [
        RuleGene(
            conditions=[
                {'source': 'neighbor_count_empty', 'operator': '>', 'target_value': 0},
                {'source': 'self_energy', 'operator': '>', 'target_value': 2.0},
            ],
            action_type="GROW",
            action_param=comp_struct.name,
            priority=10
        ),
        RuleGene(
            conditions=[
                {'source': 'self_type', 'operator': '==', 'target_value': "Zygote"},
                {'source': 'self_age', 'operator': '>', 'target_value': 2},
            ],
            action_type="DIFFERENTIATE",
            action_param=comp_struct.name,
            priority=100
        )
    ]
    genotype = Genotype(component_genes=components, rule_genes=rules)
    genotype.update_kingdom()
    return genotype

def mutate(genotype: Genotype, settings: Dict) -> Genotype:
    """Mutates a genotype."""
    mutated = genotype.copy()
    mut_rate = 0.5 # High mutation rate for mock data
    innov_rate = 0.3
    
    for rule in mutated.rule_genes:
        if random.random() < mut_rate and rule.conditions:
            cond_to_mutate = random.choice(rule.conditions)
            if isinstance(cond_to_mutate['target_value'], (int, float)):
                cond_to_mutate['target_value'] *= np.random.lognormal(0, 0.1)

    if random.random() < innov_rate:
        new_rule = innovate_rule(mutated, settings)
        mutated.rule_genes.append(new_rule)
    if random.random() < innov_rate * 0.5 and len(mutated.rule_genes) > 1:
        mutated.rule_genes.remove(random.choice(mutated.rule_genes))
    
    if random.random() < 0.1: # Component innovation
        new_component = innovate_component(mutated, settings)
        if new_component.name not in mutated.component_genes:
            mutated.component_genes[new_component.name] = new_component

    mutated.update_kingdom()
    return mutated

class GenotypeJSONEncoder(json.JSONEncoder):
    """Custom encoder to handle dataclasses."""
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

def deserialize_genotype(geno_dict: Dict) -> Genotype:
    """Helper function to reconstruct a Genotype object from a dictionary."""
    try:
        comp_genes_dict = geno_dict.get('component_genes', {})
        re_comp_genes = {}
        for comp_id_or_name, comp_dict in comp_genes_dict.items():
            # Handle both old (name) and new (id) keying
            comp_id = comp_dict.get('id', f"comp_{uuid.uuid4().hex[:6]}")
            re_comp_genes[comp_id] = ComponentGene(**comp_dict)
        geno_dict['component_genes'] = re_comp_genes
        
        rule_genes_list = geno_dict.get('rule_genes', [])
        re_rule_genes = [RuleGene(**rule_dict) for rule_dict in rule_genes_list]
        geno_dict['rule_genes'] = re_rule_genes
        
        return Genotype(**geno_dict)
    except Exception as e:
        st.error(f"Error deserializing genotype: {e} | Data: {geno_dict.get('id', 'N/A')}")
        return Genotype(id=geno_dict.get('id', 'error_id'), fitness=-1)

def deserialize_population(pop_data_list: List[Dict]) -> List[Genotype]:
    """Deserializes an entire population list from a JSON-friendly format."""
    reconstructed_pop = []
    for geno_dict in pop_data_list:
        reconstructed_pop.append(deserialize_genotype(geno_dict))
    return [g for g in reconstructed_pop if g.fitness != -1]

@st.cache_data(show_spinner=False)
def load_museum_exhibits(chemical_bases_registry):
    """
    Generates a mock dataset for the museum on the first run.
    This replaces the live simulation.
    """
    with st.spinner("Curating the Museum's collection... (This happens once per session)"):
        history = []
        population = []
        genesis_events = []
        metrics = []
        gene_archive = []
        
        # Use a minimal settings dict for the helper functions
        settings = {
            'chemical_bases': list(chemical_bases_registry.keys()),
            'max_rule_conditions': 2
        }

        # Create a base population
        base_population = []
        for _ in range(50): # 50 founding lineages
            genotype = get_primordial_soup_genotype(settings)
            genotype = mutate(genotype, settings)
            base_population.append(genotype)

        lineages = [g.copy() for g in base_population]
        
        # Simulate 150 "generations" of mock data
        num_generations = 150
        pop_size_per_gen = 20

        for gen in range(num_generations):
            current_gen_pop = []
            
            # Create the population for this generation
            for _ in range(pop_size_per_gen):
                # Pick a random lineage and mutate it
                parent = random.choice(lineages)
                child = mutate(parent, settings)
                child.generation = gen
                
                # Assign a random kingdom from the available bases
                child.kingdom_id = random.choice(settings['chemical_bases'])
                
                # Assign mock metrics
                child.fitness = np.clip(random.uniform(0.1, 1.0) + (gen / 150.0), 0.1, 2.0)
                child.cell_count = random.randint(1, 50)
                child.complexity = child.compute_complexity() + random.uniform(0, 5)
                child.lifespan = random.randint(10, 200)
                child.energy_production = random.uniform(0.5, 5.0)
                child.energy_consumption = random.uniform(0.5, 4.0)
                
                # Add to history
                history.append({
                    'generation': gen,
                    'kingdom_id': child.kingdom_id,
                    'fitness': child.fitness,
                    'cell_count': child.cell_count,
                    'complexity': child.complexity,
                    'lifespan': child.lifespan,
                    'energy_production': child.energy_production,
                    'energy_consumption': child.energy_consumption,
                    'lineage_id': child.lineage_id,
                    'parent_ids': child.parent_ids,
                })
                current_gen_pop.append(child)
            
            # Add this generation's organisms to the archive
            gene_archive.extend(current_gen_pop)
            
            # Select "survivors" to be the new lineages
            lineages = sorted(current_gen_pop, key=lambda g: g.fitness, reverse=True)[:10]
            # Add some random new lineages for diversity
            for _ in range(5):
                lineages.append(mutate(get_primordial_soup_genotype(settings), settings))

            # Store the *final* generation as the 'current' population
            if gen == num_generations - 1:
                population = current_gen_pop
            
            # Add mock metrics
            metrics.append({
                'generation': gen,
                'diversity': random.uniform(1.0, 3.0),
                'best_fitness': max(g.fitness for g in current_gen_pop),
                'mean_fitness': np.mean([g.fitness for g in current_gen_pop]),
                'selection_differential': random.uniform(0.1, 0.5),
                'mutation_rate': 0.2,
            })

        # Add mock Genesis Events
        genesis_events = [
            {'generation': 0, 'type': 'Genesis', 'title': 'Genesis of Carbon Life', 'description': 'The first Carbon-based organisms emerged.', 'icon': '✨'},
            {'generation': 15, 'type': 'Genesis', 'title': 'Genesis of Silicon Life', 'description': 'Life based on Silicon was first recorded.', 'icon': '✨'},
            {'generation': 30, 'type': 'Complexity Leap', 'title': 'Complexity Barrier Broken (10)', 'description': 'An organism achieved a genomic complexity of over 10.', 'icon': '🧠'},
            {'generation': 50, 'type': 'Cataclysm', 'title': 'The Great Filter', 'description': 'A stellar flare event wiped out 80% of all life.', 'icon': '🌋'},
            {'generation': 51, 'type': 'Genesis', 'title': 'Genesis of Plasma Life', 'description': 'In the ashes of the cataclysm, Plasma-based life emerged.', 'icon': '✨'},
            {'generation': 75, 'type': 'Major Transition', 'title': 'First Communication', 'description': 'A lineage evolved the first `EMIT_SIGNAL` rule.', 'icon': '📡'},
            {'generation': 100, 'type': 'Succession', 'title': 'The Silicon Era Begins', 'description': 'Silicon-based life has become the dominant kingdom.', 'icon': '👑'},
            {'generation': 120, 'type': 'Cognitive Leap', 'title': 'Invention of Memory', 'description': 'A Psionic lineage evolved the first `SET_TIMER` rule.', 'icon': '⏳'},
        ]

        return pd.DataFrame(history), population, genesis_events, pd.DataFrame(metrics), gene_archive

# =================================================================
#
# PART 4: THE VISUALIZATION HALL (Plotting Functions)
#
# All plotting functions from the original file are preserved here.
# They are the 'lenses' through which we view the exhibits.
#
# =================================================================

def visualize_phenotype_2d(phenotype: Phenotype, grid: UniverseGrid) -> go.Figure:
    """Creates a 2D heatmap visualization of the organism's body plan."""
    cell_data = np.full((grid.width, grid.height), np.nan)
    cell_text = [["" for _ in range(grid.height)] for _ in range(grid.width)]
    
    component_colors = {comp.name: comp.color for comp in phenotype.genotype.component_genes.values()}
    color_map = {}
    discrete_colors = []
    
    unique_types = sorted(list(component_colors.keys()))
    if not unique_types:
        unique_types = ["default"]
        component_colors["default"] = "#FFFFFF"
        
    for i, comp_name in enumerate(unique_types):
        color_map[comp_name] = i
        discrete_colors.append(component_colors[comp_name])

    dcolorsc = []
    n_colors = len(discrete_colors)
    if n_colors == 0:
        dcolorsc = [[0, "#000000"], [1, "#000000"]]
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
            f"Mass: {cell.component.mass:.2f}"
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
        title=f"Specimen: {phenotype.id} (Gen: {phenotype.genotype.generation})<br><sup>Kingdom: {phenotype.genotype.kingdom_id} | Cells: {len(phenotype.cells)} | Fitness: {phenotype.genotype.fitness:.4f}</sup>",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x"),
        height=500,
        margin=dict(l=20, r=20, t=80, b=20),
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

def plot_evolutionary_landscape(history_df: pd.DataFrame, key_prefix: str) -> go.Figure:
    """3D Fitness Landscape: (Fitness vs. Complexity vs. Cell Count)"""
    if history_df.empty or len(history_df) < 20:
        return go.Figure().update_layout(title="Not enough data for 3D Landscape")
        
    sample_size = min(len(history_df), 20000)
    df_sample = history_df.sample(n=sample_size)
    
    x_param = 'cell_count'
    y_param = 'complexity'
    z_param = 'fitness'
    
    if df_sample[x_param].nunique() < 2 or df_sample[y_param].nunique() < 2:
        return go.Figure().update_layout(title="Not enough data variance for 3D Landscape")
        
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
    
    mean_trajectory = history_df.groupby('generation').agg({
        x_param: 'mean', y_param: 'mean', z_param: 'mean'
    }).reset_index()
    apex_trajectory = history_df.loc[history_df.groupby('generation')['fitness'].idxmax()]

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
    
    final_gen_df = history_df[history_df['generation'] == history_df['generation'].max()]
    final_pop_trace = go.Scatter3d(
        x=final_gen_df[x_param], y=final_gen_df[y_param], z=final_gen_df[z_param],
        mode='markers',
        marker=dict(size=5, color=final_gen_df['fitness'], colorscale='Viridis', showscale=True),
        name='Final Population',
    )
    
    fig = go.Figure(data=[surface_trace, mean_trajectory_trace, apex_trajectory_trace, final_pop_trace])
    fig.update_layout(
        title='<b>3D Evolutionary Landscape (Morphospace)</b>',
        scene=dict(
            xaxis_title='Cell Count (Body Size)',
            yaxis_title='Genomic Complexity',
            zaxis_title='Fitness'
        ),
        height=700,
        margin=dict(l=0, r=0, b=0, t=60)
    )
    return fig

def plot_historical_dashboard(history_df: pd.DataFrame, evolutionary_metrics_df: pd.DataFrame, key_prefix: str) -> go.Figure:
    """Comprehensive evolution analytics dashboard."""
    
    fig = make_subplots(
        rows=3, cols=3,
        subplot_titles=(
            '<b>Fitness Evolution by Kingdom</b>',
            '<b>Phenotypic Trait Trajectories</b>',
            '<b>Final Generation Fitness</b>',
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
    
    if history_df.empty:
        return fig.update_layout(title="No historical data to display.", height=1200)

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

# --- All 12 Custom Analytics Plots from your file ---

def plot_fitness_vs_complexity(df: pd.DataFrame, key: str) -> go.Figure:
    if df.empty: return go.Figure().update_layout(title="No data")
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
    if df.empty: return go.Figure().update_layout(title="No data")
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
    if df.empty: return go.Figure().update_layout(title="No data")
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
    if df.empty: return go.Figure().update_layout(title="No data")
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
    if df.empty: return go.Figure().update_layout(title="No data")
    final_gen_df = df[df['generation'] == df['generation'].max()]
    if final_gen_df.empty:
        final_gen_df = df
    fig = px.violin(final_gen_df, x='kingdom_id', y='fitness', color='kingdom_id', box=True, points="all", title="Final Generation Fitness Distribution by Kingdom")
    fig.update_layout(height=400)
    return fig

def plot_complexity_vs_lifespan(df: pd.DataFrame, key: str) -> go.Figure:
    if df.empty: return go.Figure().update_layout(title="No data")
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
    if df.empty: return go.Figure().update_layout(title="No data")
    df_copy = df.copy()
    df_copy['efficiency'] = df_copy['energy_production'] / (df_copy['energy_consumption'] + 1e-6)
    efficiency_by_gen = df_copy.groupby('generation')['efficiency'].mean().reset_index()
    fig = px.line(efficiency_by_gen, x='generation', y='efficiency', title='Mean Energy Efficiency Over Time')
    fig.update_layout(height=400)
    return fig

def plot_cell_count_dist_by_kingdom(df: pd.DataFrame, key: str) -> go.Figure:
    if df.empty: return go.Figure().update_layout(title="No data")
    final_gen_df = df[df['generation'] == df['generation'].max()]
    if final_gen_df.empty:
        final_gen_df = df
    fig = px.box(final_gen_df, x='kingdom_id', y='cell_count', color='kingdom_id', title="Final Generation Cell Count Distribution")
    fig.update_layout(height=400)
    return fig

def plot_lifespan_dist_by_kingdom(df: pd.DataFrame, key: str) -> go.Figure:
    if df.empty: return go.Figure().update_layout(title="No data")
    final_gen_df = df[df['generation'] == df['generation'].max()]
    if final_gen_df.empty:
        final_gen_df = df
    fig = px.violin(final_gen_df, x='kingdom_id', y='lifespan', color='kingdom_id', box=True, title="Final Generation Lifespan Distribution")
    fig.update_layout(height=400)
    return fig

def plot_complexity_vs_energy_prod(df: pd.DataFrame, key: str) -> go.Figure:
    if df.empty: return go.Figure().update_layout(title="No data")
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
    if df.empty: return go.Figure().update_layout(title="No data")
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
    if df.empty: return go.Figure().update_layout(title="No data")
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
# PART 5: THE MAIN APPLICATION (The Museum)
#
# ========================================================

def main():
    st.set_page_config(
        page_title="The Museum of Infinite Life",
        layout="wide",
        page_icon="🌌",
        initial_sidebar_state="expanded"
    )

    # --- Password Protection (from your file) ---
    if 'password_attempts' not in st.session_state:
        st.session_state.password_attempts = 0
    if 'password_correct' not in st.session_state:
        st.session_state.password_correct = False

    def check_password_on_change():
        try:
            correct_pass = st.secrets["app_password"]
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
            "Enter Museum Access Code", 
            type="password", 
            on_change=check_password_on_change,
            key="password_input_key"
        )
        if st.session_state.password_attempts > 0:
            st.error("Access Code incorrect")
        st.info("Please enter the access code to tour the museum.")
        st.stop()

    # --- Initialize Lazy Loading states for all tabs ---
    if 'dashboard_visible' not in st.session_state:
        st.session_state.dashboard_visible = False
    if 'specimen_gallery_visible' not in st.session_state:
        st.session_state.specimen_gallery_visible = False
    if 'hall_of_elites_visible' not in st.session_state:
        st.session_state.hall_of_elites_visible = False
    if 'genesis_chronicle_visible' not in st.session_state:
        st.session_state.genesis_chronicle_visible = False
    if 'analytics_lab_visible' not in st.session_state:
        st.session_state.analytics_lab_visible = False
    
    # --- Data Loading ---
    # This is the core change. We load *once* from the mock generator
    # or from a user's uploaded file.
    
    if 'state_loaded' not in st.session_state:
        # Load the default mock museum
        history_df, population, genesis_events, metrics_df, gene_archive = load_museum_exhibits(CHEMICAL_BASES_REGISTRY)
        
        st.session_state.history_df = history_df
        st.session_state.population = population
        st.session_state.genesis_events = genesis_events
        st.session_state.metrics_df = metrics_df
        st.session_state.gene_archive = gene_archive
        
        # We need a settings dict for the visualizers
        st.session_state.settings = {
            'grid_width': 100, 'grid_height': 100, 'light_intensity': 1.0,
            'mineral_richness': 1.0, 'water_abundance': 1.0, 'temp_pole': -20,
            'temp_equator': 30, 'zygote_energy': 10.0, 'development_steps': 50,
            'num_ranks_to_display': 3, 'num_custom_plots': 4,
            'chemical_bases': list(CHEMICAL_BASES_REGISTRY.keys())
        }
        st.session_state.state_loaded = True
        st.toast("Welcome! The Museum's exhibits have been curated.", icon="🏛️")

    # ===============================================
    # --- THE "MUSEUM DIRECTORY" SIDEBAR ---
    # ===============================================
    
    st.sidebar.markdown('<h1 style="text-align: center; color: #00aaff;">🌌<br>Museum of Infinite Life</h1>', unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    # --- NEW: Visitor Info ---
    st.sidebar.info("**Welcome, Visitor.** \n\nThis panel allows you to load new exhibits (universes) or filter the current collection.")

    # --- Kept from your file: The "Universe Manager" (now "Exhibit Loader") ---
    with st.sidebar.expander("🌠 Exhibit Loader (Load a Universe)", expanded=True):
        st.markdown("Load a different universe's history from a checkpoint file.")
        
        # We remove the "Save" button, as this is a visitor app.
        
        uploaded_file = st.sidebar.file_uploader(
            "Upload your 'universe_results.zip' file", 
            type=["json", "zip"],
            key="checkpoint_uploader"
        )
        
        if st.sidebar.button("LOAD FROM UPLOADED FILE", width='stretch', key="load_checkpoint_button"):
            if uploaded_file is not None:
                try:
                    data = None
                    if uploaded_file.name.endswith('.zip'):
                        st.toast("Unzipping exhibit... Please wait.", icon="📦")
                        mem_zip = io.BytesIO(uploaded_file.getvalue())
                        with zipfile.ZipFile(mem_zip, 'r') as zf:
                            json_filename = next((f for f in zf.namelist() if f.endswith('.json') and not f.startswith('__MACOSX')), None)
                            if json_filename:
                                with zf.open(json_filename) as f:
                                    data = json.load(f)
                            else:
                                st.error("No .json file found inside the .zip archive.")
                    
                    elif uploaded_file.name.endswith('.json'):
                        st.toast("Loading .json exhibit...", icon="📄")
                        data = json.loads(uploaded_file.getvalue())
                    
                    if data is not None:
                        st.toast("Exhibit found... Loading history...", icon="⏳")
                        
                        # Load data into session state
                        st.session_state.settings = data.get('settings', st.session_state.settings)
                        st.session_state.history_df = pd.DataFrame(data.get('history', []))
                        st.session_state.metrics_df = pd.DataFrame(data.get('evolutionary_metrics', []))
                        st.session_state.genesis_events = data.get('genesis_events', [])
                        st.session_state.population = deserialize_population(data.get('final_population_genotypes', []))
                        st.session_state.gene_archive = deserialize_population(data.get('full_gene_archive', []))

                        # Update chemical bases if they were saved in the checkpoint
                        if 'final_physics_constants' in data:
                            CHEMICAL_BASES_REGISTRY.clear()
                            CHEMICAL_BASES_REGISTRY.update(data['final_physics_constants'])
                        
                        st.toast("✅ Exhibit Loaded! The museum has been updated.", icon="🎉")
                        st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to load checkpoint: {e}")
            else:
                st.warning("Please upload a file first.")
    
    st.sidebar.markdown("---")
    
    # --- NEW: Exhibit Filters ---
    st.sidebar.markdown("### 🔍 Exhibit Filters")
    st.sidebar.markdown("Filter the historical data across all exhibits.")
    
    if not st.session_state.history_df.empty:
        history_df = st.session_state.history_df
        
        # --- Create filtered dataframes based on sidebar widgets ---
        gen_min = int(history_df['generation'].min())
        gen_max = int(history_df['generation'].max())
        gen_range = st.sidebar.slider("Filter: Generation Range", gen_min, gen_max, (gen_min, gen_max), key="filter_gen_range")
        
        all_kingdoms = sorted(list(history_df['kingdom_id'].unique()))
        selected_kingdoms = st.sidebar.multiselect("Filter: Chemical Kingdoms", all_kingdoms, all_kingdoms, key="filter_kingdoms")
        
        comp_min = float(history_df['complexity'].min())
        comp_max = float(history_df['complexity'].max())
        comp_range = st.sidebar.slider("Filter: Complexity Range", comp_min, comp_max, (comp_min, comp_max), key="filter_complexity")
        
        # --- Apply filters ---
        filtered_history_df = history_df[
            (history_df['generation'] >= gen_range[0]) &
            (history_df['generation'] <= gen_range[1]) &
            (history_df['kingdom_id'].isin(selected_kingdoms)) &
            (history_df['complexity'] >= comp_range[0]) &
            (history_df['complexity'] <= comp_range[1])
        ]
        
        filtered_metrics_df = st.session_state.metrics_df[
            (st.session_state.metrics_df['generation'] >= gen_range[0]) &
            (st.session_state.metrics_df['generation'] <= gen_range[1])
        ]
        
        # Filter population for display
        filtered_population = [
            g for g in st.session_state.population 
            if g.kingdom_id in selected_kingdoms and comp_range[0] <= g.compute_complexity() <= comp_range[1]
        ]
        if not filtered_population:
            filtered_population = st.session_state.population # Failsafe
            
        # Filter gene archive
        filtered_gene_archive = [
            g for g in st.session_state.gene_archive
            if gen_range[0] <= g.generation <= gen_range[1] and
               g.kingdom_id in selected_kingdoms and
               comp_range[0] <= g.compute_complexity() <= comp_range[1]
        ]
        if not filtered_gene_archive:
            filtered_gene_archive = st.session_state.gene_archive # Failsafe
            
        # Filter genesis events
        filtered_genesis_events = [
            e for e in st.session_state.genesis_events
            if gen_range[0] <= e['generation'] <= gen_range[1]
        ]

    else:
        # Failsafe if history is empty
        st.sidebar.warning("No exhibit data loaded.")
        filtered_history_df = pd.DataFrame()
        filtered_metrics_df = pd.DataFrame()
        filtered_population = []
        filtered_gene_archive = []
        filtered_genesis_events = []

    # --- Settings for visualizers (from your file) ---
    s = st.session_state.settings 
    
    with st.sidebar.expander("🔬 Visualization Settings", expanded=False):
        s['num_ranks_to_display'] = st.slider("Number of Elite Ranks to Display", 1, 10, s.get('num_ranks_to_display', 3), key="vis_ranks")
        s['num_custom_plots'] = st.slider("Number of Custom Analytics Plots", 0, 12, s.get('num_custom_plots', 4), 1, key="vis_plots")
        s['development_steps'] = st.slider("Specimen 'Grow' Steps (Visual only)", 10, 200, s.get('development_steps', 50), 5, key="vis_dev_steps")

    # --- Kept from your file: The Guides ---
    with st.sidebar.expander("📖 Visitor's Guidebook: A Guide to Infinite Life", expanded=False):
        st.markdown("... (Your full 'Creator's Compendium' text from the original file goes here) ...")
        
    with st.sidebar.expander("🔬 A Researcher's Guide to the GRN Encyclopedia", expanded=False):
        st.markdown("... (Your full 'GRN Encyclopedia' text from the original file goes here) ...")

    # ===============================================
    # --- MAIN PAGE DISPLAY ---
    # ===============================================
    st.markdown('<h1 class="main-header">Welcome to the Museum of Infinite Life</h1>', unsafe_allow_html=True)
    
    if filtered_history_df.empty:
        st.info("The museum's collection is empty or your filters are too restrictive. Please load a checkpoint or adjust your filters.")
    else:
        # --- Create Tabs ---
        tab_list = [
            "🏛️ Grand Concourse (Overview)", 
            "🔬 Specimen Gallery", 
            "🧬 Hall of Apex Lifeforms",
            "🌌 The Genesis Chronicle",
            "📊 Interstellar Analytics Lab"
        ]
        tab_dashboard, tab_gallery, tab_elites, tab_genesis, tab_analytics = st.tabs(tab_list)
        
        # --- TAB 1: Grand Concourse (Dashboard) ---
        with tab_dashboard:
            if st.session_state.dashboard_visible:
                st.header("Exhibit: The Grand Concourse")
                st.markdown("A high-level overview of this universe's entire evolutionary history. This hall shows the rise and fall of kingdoms and the major trends in complexity and fitness over millions of simulated years.")
                
                st.plotly_chart(
                    plot_historical_dashboard(filtered_history_df, filtered_metrics_df, key_prefix="main_dash"),
                    use_container_width=True,
                    key="main_dashboard_plot_universe"
                )
                
                st.header("Exhibit: The Morphospace Landscape")
                st.markdown("This 3D landscape plots the 'fitness' (height) of all recorded lifeforms against their body size (cell count) and genomic complexity. The 'trajectories' show the path evolution took through this possibility space.")
                st.plotly_chart(
                    plot_evolutionary_landscape(filtered_history_df, key_prefix="main_landscape"),
                    use_container_width=True,
                    key="fitness_landscape_3d_universe"
                )

                st.markdown("---")
                if st.button("Unload Concourse Exhibit (Save Memory)", key="hide_dashboard_button"):
                    st.session_state.dashboard_visible = False
                    st.rerun()
            else:
                st.info("The Grand Concourse exhibit contains large-scale data visualizations. It is currently unloaded to save resources.")
                if st.button("Load 🏛️ Grand Concourse Exhibit", key="render_dashboard_button"):
                    st.session_state.dashboard_visible = True
                    st.rerun()

        # --- TAB 2: Specimen Gallery ---
        with tab_gallery:
            if st.session_state.specimen_gallery_visible:
                st.header("🔬 Exhibit: The Specimen Gallery")
                st.markdown("A detailed look at the individual lifeforms from the final generation of this universe. Each specimen can be 'grown' for visualization, and its complete genetic code (GRN) can be inspected.")
                
                if not filtered_population:
                    st.warning("No specimens match your current filter criteria.")
                else:
                    st.info(f"{len(filtered_population)} specimens in this exhibit hall. Use the filters to narrow your search.")
                    
                    # --- Specimen Selector ---
                    specimen_options = {f"Gen {g.generation} | {g.kingdom_id} | Fitness {g.fitness:.3f} | ID: ...{g.id[-6:]}": g for g in filtered_population}
                    selected_specimen_label = st.selectbox("Select a Specimen to Analyze", options=specimen_options.keys(), key="specimen_selector")
                    
                    if selected_specimen_label:
                        specimen = specimen_options[selected_specimen_label]
                        
                        with st.spinner(f"Growing specimen {specimen.id[-6:]}..."):
                            vis_grid = UniverseGrid(s)
                            phenotype = Phenotype(specimen, vis_grid, s)

                        st.markdown(f"### Analysis of Specimen {specimen.id}")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.metric("Fitness", f"{specimen.fitness:.4f}")
                            st.metric("Kingdom", specimen.kingdom_id)
                            st.metric("Cell Count", f"{specimen.cell_count}")
                            st.metric("Complexity", f"{specimen.compute_complexity():.2f}")
                            
                            st.markdown("##### **Component Composition**")
                            component_counts = Counter(cell.component.name for cell in phenotype.cells.values())
                            if component_counts:
                                comp_df = pd.DataFrame.from_dict(component_counts, orient='index', columns=['Count']).reset_index()
                                comp_df = comp_df.rename(columns={'index': 'Component'})
                                color_map = {c.name: c.color for c in specimen.component_genes.values()}
                                fig_pie = px.pie(comp_df, values='Count', names='Component', 
                                                 color='Component', color_discrete_map=color_map)
                                fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=0, b=0), height=200)
                                st.plotly_chart(fig_pie, use_container_width=True, key=f"specimen_pie_{specimen.id}")
                            else:
                                st.info("No cells to analyze.")
                        
                        with c2:
                            fig = visualize_phenotype_2d(phenotype, vis_grid)
                            fig.update_layout(height=400)
                            st.plotly_chart(fig, use_container_width=True, key=f"specimen_vis_{specimen.id}")

                        # --- GRN Encyclopedia (from your file) ---
                        st.markdown("---")
                        st.markdown("### Genetic Regulatory Network (GRN) Encyclopedia")
                        st.markdown("The 'DNA' of the specimen, viewed through 16 different analytical layouts. See the 'Visitor's Guidebook' in the sidebar for an explanation of each plot.")
                        
                        G = nx.DiGraph()
                        for comp_name, comp_gene in specimen.component_genes.items():
                            G.add_node(comp_name, type='component', color=comp_gene.color, label=comp_name.split('_')[0])
                        for rule in specimen.rule_genes:
                            action_node = f"{rule.action_type}\n({rule.action_param.split('_')[0]})"
                            G.add_node(action_node, type='action', color='#FFB347', label=action_node)
                            
                            source_node = list(specimen.component_genes.keys())[0] # Simplified
                            if rule.conditions:
                                type_cond = next((c for c in rule.conditions if c['source'] == 'self_type'), None)
                                if type_cond and type_cond['target_value'] in G.nodes():
                                    source_node = type_cond['target_value']
                                    
                            G.add_edge(source_node, action_node, label=f"P={rule.probability:.1f}")
                            if rule.action_param in G.nodes():
                                G.add_edge(action_node, rule.action_param)

                        if G.nodes:
                            node_colors = [data.get('color', '#888888') for _, data in G.nodes(data=True)]
                            labels = {n: data.get('label', n) for n, data in G.nodes(data=True)}
                            
                            # Define all 16 layouts
                            layouts = {
                                'GRN 1: Default Spring': (nx.spring_layout, {'k': 0.9, 'seed': 42}),
                                'GRN 2: Kamada-Kawai': (nx.kamada_kawai_layout, {}),
                                'GRN 3: Circular': (nx.circular_layout, {}),
                                'GRN 4: Random': (nx.random_layout, {'seed': 42}),
                                'GRN 5: Spectral': (nx.spectral_layout, {}),
                                'GRN 6: Shell': (nx.shell_layout, {}),
                                'GRN 7: Spiral': (nx.spiral_layout, {}),
                                'GRN 8: Planar': (nx.planar_layout, {}),
                                'GRN 9: Tight Spring': (nx.spring_layout, {'k': 0.1, 'seed': 42}),
                                'GRN 10: Loose Spring': (nx.spring_layout, {'k': 2.0, 'seed': 42}),
                                'GRN 11: Dual-Shell (Custom)': 'custom_shell',
                                'GRN 12: Settled Spring': (nx.spring_layout, {'iterations': 200, 'seed': 42}),
                                'GRN 13: Hierarchical (Top-Down)': 'pydot_dot',
                                'GRN 14: Hierarchical (Radial)': 'pydot_twopi',
                                'GRN 15: Force-Directed (NEATO)': 'pydot_neato',
                                'GRN 16: Spring (Alt. Seed)': (nx.spring_layout, {'seed': 99})
                            }

                            cols = st.columns(4)
                            for i, (title, layout_info) in enumerate(layouts.items()):
                                with cols[i % 4]:
                                    st.markdown(f"##### **{title}**")
                                    fig_grn, ax = plt.subplots(figsize=(4, 3))
                                    pos = None
                                    try:
                                        if isinstance(layout_info, tuple):
                                            func, kwargs = layout_info
                                            pos = func(G, **kwargs)
                                        elif layout_info == 'custom_shell':
                                            component_nodes = [n for n, data in G.nodes(data=True) if data.get('type') == 'component']
                                            action_nodes = [n for n, data in G.nodes(data=True) if data.get('type') == 'action']
                                            pos = nx.shell_layout(G, nlist=[component_nodes, action_nodes])
                                        elif layout_info.startswith('pydot_'):
                                            prog = layout_info.split('_')[1]
                                            pos = nx.nx_pydot.graphviz_layout(G, prog=prog)
                                        
                                        nx.draw(G, pos, ax=ax, with_labels=False, node_size=300, node_color=node_colors, font_size=6, width=0.5, arrowsize=8)
                                        nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, ax=ax)
                                        st.pyplot(fig_grn, key=f"grn_plot_{specimen.id}_{i}")
                                        plt.clf()
                                    except ImportError:
                                        st.warning(f"Layout '{title}' requires 'pydot' and 'Graphviz'.", icon="⚠️")
                                        plt.clf()
                                    except Exception as e:
                                        st.warning(f"Could not draw '{title}'.", icon="⚠️")
                                        # st.exception(e) # Uncomment for debugging
                                        plt.clf()
                            plt.close('all') # Clear all figures from memory
                        else:
                            st.info("No GRN to display for this specimen.")
                
                st.markdown("---")
                if st.button("Unload Specimen Gallery (Save Memory)", key="hide_gallery_button"):
                    st.session_state.specimen_gallery_visible = False
                    st.rerun()
            else:
                st.info("The Specimen Gallery contains 16-plot GRN layouts for every organism, which is highly resource-intensive. It is currently unloaded.")
                if st.button("Load 🔬 Specimen Gallery", key="render_gallery_button"):
                    st.session_state.specimen_gallery_visible = True
                    st.rerun()

        # --- TAB 3: Hall of Apex Lifeforms (Elites) ---
        with tab_elites:
            if st.session_state.hall_of_elites_visible:
                st.header("🧬 Exhibit: The Hall of Apex Lifeforms")
                st.markdown("A deep dive into the 'DNA' of the most successful organisms. Each rank displays the **best organism from a unique Kingdom** (from the final generation), showcasing the diversity of life that has evolved.")
                st.markdown("---")
                
                if not filtered_population:
                    st.warning("No specimens match your current filter criteria.")
                else:
                    population.sort(key=lambda x: x.fitness, reverse=True)
                    num_ranks_to_display = s.get('num_ranks_to_display', 3)

                    elite_specimens = []
                    seen_kingdoms = set()
                    for individual in filtered_population:
                        if individual.kingdom_id not in seen_kingdoms:
                            elite_specimens.append(individual)
                            seen_kingdoms.add(individual.kingdom_id)

                    for i, individual in enumerate(elite_specimens[:num_ranks_to_display]):
                        with st.expander(f"**Rank {i+1}:** Kingdom `{individual.kingdom_id}` | Fitness: `{individual.fitness:.4f}`", expanded=(i==0)):
                            
                            with st.spinner(f"Growing Rank {i+1}..."):
                                vis_grid = UniverseGrid(s)
                                phenotype = Phenotype(individual, vis_grid, s)

                            col1, col2 = st.columns([1, 1])
                            with col1:
                                st.markdown("##### **Core Metrics**")
                                st.metric("Cell Count", f"{individual.cell_count}")
                                st.metric("Complexity", f"{individual.compute_complexity():.2f}")
                                st.metric("Lifespan", f"{individual.lifespan} ticks")
                                st.metric("Energy Prod.", f"{individual.energy_production:.3f}")
                                st.metric("Energy Cons.", f"{individual.energy_consumption:.3f}")
                            
                            with col2:
                                st.markdown("##### **Phenotype (Body Plan)**")
                                fig = visualize_phenotype_2d(phenotype, vis_grid)
                                st.plotly_chart(fig, use_container_width=True, key=f"elite_pheno_vis_{i}")

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
                                    st.plotly_chart(fig_pie, use_container_width=True, key=f"elite_pie_{i}")
                                
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
                
                st.markdown("---")
                if st.button("Unload Hall of Apex Lifeforms (Save Memory)", key="hide_elite"):
                    st.session_state.hall_of_elites_visible = False
                    st.rerun()
            else:
                st.info("The Hall of Apex Lifeforms loads the genetic code for the top organisms. It is currently unloaded.")
                if st.button("Load 🧬 Hall of Apex Lifeforms", key="show_elite"):
                    st.session_state.hall_of_elites_visible = True
                    st.rerun()

        # --- TAB 4: Genesis Chronicle ---
        with tab_genesis:
            if st.session_state.genesis_chronicle_visible:
                st.header("🌌 Exhibit: The Genesis Chronicle")
                st.markdown("This is the historical record of this universe, chronicling the pivotal moments of creation, innovation, and cosmic change. These events are the sparks that drive evolution.")
                
                if not filtered_genesis_events:
                    st.info("No significant evolutionary events have been recorded in the filtered range.")
                else:
                    # --- Event Log ---
                    st.markdown(f"#### Recorded History ({len(filtered_genesis_events)} events)")
                    log_container = st.container(height=400)
                    for event in sorted(filtered_genesis_events, key=lambda x: x['generation']):
                        log_container.markdown(f"""
                        <div style="border-left: 3px solid #00aaff; padding-left: 10px; margin-bottom: 15px;">
                            <small>Generation {event['generation']}</small><br>
                            <strong>{event['icon']} {event['title']}</strong>
                            <p style="font-size: 0.9em; color: #ccc;">{event['description']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # --- The rest of the Chronicle (from your file) ---
                st.markdown("---")
                st.markdown("### 📖 Epochs & Phylogeny")
                st.markdown("A macro-level analysis of your universe's history, identifying distinct eras and visualizing the evolutionary tree of its kingdoms.")
                
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.markdown("#### The Great Epochs of History")
                    break_points = {0, filtered_history_df['generation'].max()}
                    major_events = [e for e in filtered_genesis_events if e['type'] in ['Cataclysm', 'Genesis', 'Succession']]
                    for event in major_events:
                        break_points.add(event['generation'])
                    sorted_breaks = sorted(list(break_points))
                    
                    if len(sorted_breaks) < 2:
                        st.info("Not enough major events have occurred to define distinct historical epochs.")
                    else:
                        for i in range(len(sorted_breaks) - 1):
                            start_gen, end_gen = sorted_breaks[i], sorted_breaks[i+1]
                            epoch_df = filtered_history_df[(filtered_history_df['generation'] >= start_gen) & (filtered_history_df['generation'] <= end_gen)]
                            if epoch_df.empty: continue

                            start_event = next((e for e in major_events if e['generation'] == start_gen), None)
                            epoch_name = f"Epoch {i+1}"
                            if i == 0 and not start_event: epoch_name = "The Primordial Era"
                            elif start_event: epoch_name = f"The {start_event['title']} Era"

                            with st.expander(f"**{epoch_name}** (Generations {start_gen} - {end_gen})"):
                                c1, c2 = st.columns(2)
                                with c1:
                                    st.markdown("##### Core Metrics")
                                    dominant_kingdom = epoch_df['kingdom_id'].mode()[0] if not epoch_df['kingdom_id'].mode().empty else "N/A"
                                    st.metric("Dominant Kingdom", dominant_kingdom)
                                    st.metric("Mean Fitness", f"{epoch_df['fitness'].mean():.3f}")
                                    st.metric("Peak Complexity", f"{epoch_df['complexity'].max():.2f}")
                                with c2:
                                    st.markdown("##### Historical Events")
                                    epoch_events = [e for e in filtered_genesis_events if start_gen <= e['generation'] < end_gen]
                                    for event in epoch_events[:3]:
                                        st.markdown(f"- **Gen {event['generation']}:** {event['title']}")
                with col2:
                    st.markdown("#### The Tree of Life (Phylogeny)")
                    phylogeny_graph = nx.DiGraph()
                    first_occurrence = filtered_history_df.loc[filtered_history_df.groupby('kingdom_id')['generation'].idxmin()]
                    
                    for _, row in first_occurrence.iterrows():
                        phylogeny_graph.add_node(row['kingdom_id'], label=f"{row['kingdom_id']}\n(Gen {row['generation']})")
                    # (Simplified edge logic for the museum)

                    if not phylogeny_graph.nodes():
                        st.info("No kingdom data to build a tree of life.")
                    else:
                        fig_tree, ax_tree = plt.subplots(figsize=(5, 4))
                        pos = nx.spring_layout(phylogeny_graph, seed=42, k=0.9)
                        labels = nx.get_node_attributes(phylogeny_graph, 'label')
                        nx.draw(phylogeny_graph, pos, labels=labels, with_labels=True, node_size=3000, node_color='#00aaff', font_size=8, font_color='white', arrowsize=20, ax=ax_tree)
                        ax_tree.set_title("Kingdom Phylogeny")
                        st.pyplot(fig_tree, key="phylogeny_plot")
                        plt.clf()

                st.markdown("---")
                st.markdown("### 🏛️ The Pantheon of Genes")
                st.markdown("A hall of fame for the most impactful genetic 'ideas' of this universe. This analyzes the entire fossil record (gene archive) to identify the components and rule strategies that defined success.")

                if not filtered_gene_archive:
                    st.info("The gene archive is empty. Run a simulation to populate the fossil record.")
                else:
                    pantheon_col1, pantheon_col2 = st.columns(2)
                    with pantheon_col1:
                        st.markdown("#### The Component Pantheon")
                        all_components = Counter()
                        for genotype in filtered_gene_archive:
                            all_components.update(genotype.component_genes.keys())
                        
                        comp_df = pd.DataFrame(all_components.items(), columns=['Component', 'UsageCount']).sort_values('UsageCount', ascending=False)
                        fig_comp = px.bar(comp_df.head(10), x='Component', y='UsageCount', title="Most Successful Components (by Usage)")
                        fig_comp.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
                        st.plotly_chart(fig_comp, use_container_width=True, key="pantheon_comp_bar")
                        
                    with pantheon_col2:
                        st.markdown("#### The Lawgivers: Elite Genetic Strategies")
                        elite_actions = Counter()
                        for elite in filtered_population:
                            elite_actions.update(r.action_type for r in elite.rule_genes)
                        
                        action_df = pd.DataFrame(elite_actions.items(), columns=['Action', 'Count']).sort_values('Count', ascending=False)
                        fig_actions = px.bar(action_df, x='Action', y='Count', title="Elite Strategic Blueprint (GRN Actions)")
                        fig_actions.update_layout(height=300, margin=dict(l=0, r=0, t=40, b=0))
                        st.plotly_chart(fig_actions, use_container_width=True, key="pantheon_elite_actions")

                st.markdown("---")
                if st.button("Unload Genesis Chronicle (Save Memory)", key="hide_genesis_button"):
                    st.session_state.genesis_chronicle_visible = False
                    st.rerun()
            else:
                st.info("The Genesis Chronicle contains historical timelines and fossil record analysis. It is currently unloaded.")
                if st.button("Load 🌌 Genesis Chronicle", key="render_genesis_button"):
                    st.session_state.genesis_chronicle_visible = True
                    st.rerun()

        # --- TAB 5: Analytics Lab ---
        with tab_analytics:
            if st.session_state.analytics_lab_visible:
                st.header("📊 Exhibit: Interstellar Analytics Lab")
                st.markdown("A flexible laboratory for generating custom 2D plots to explore the relationships within this universe's evolutionary history. Configure the number of plots in the sidebar.")
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
                            # Give each plot a unique key
                            fig = plot_func(filtered_history_df, key=f"custom_plot_{i}")
                            st.plotly_chart(fig, use_container_width=True, key=f"custom_plotly_chart_{i}")
                
                st.markdown("---")
                if st.button("Unload Analytics Lab (Save Memory)", key="hide_analytics_lab_button"):
                    st.session_state.analytics_lab_visible = False
                    st.rerun()
            else:
                st.info("The Analytics Lab contains custom plot generators. It is currently unloaded.")
                if st.button("Load 📊 Interstellar Analytics Lab", key="render_analytics_lab_button"):
                    st.session_state.analytics_lab_visible = True
                    st.rerun()
        
        # --- Download Button (from your file) ---
        st.markdown("---")
        try:
            download_data = {
                "settings": s,
                "history": st.session_state.history_df.to_dict('records'),
                "evolutionary_metrics": st.session_state.metrics_df.to_dict('records'),
                "genesis_events": st.session_state.genesis_events,
                "final_population_genotypes": [asdict(g) for g in st.session_state.population],
                "full_gene_archive": [asdict(g) for g in st.session_state.gene_archive],
                "final_physics_constants": CHEMICAL_BASES_REGISTRY,
            }
            
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED, allowZip64=True) as zf:
                json_string = json.dumps(download_data, indent=4, cls=GenotypeJSONEncoder)
                file_name_in_zip = "museum_exhibit_data.json"
                zf.writestr(file_name_in_zip, json_string.encode('utf-8'))

            st.download_button(
                label="📥 Download Full Exhibit Data as .zip",
                data=zip_buffer.getvalue(),
                file_name="museum_of_infinite_life_exhibit.zip",
                mime="application/zip",
                help="Download the complete universe state (settings, history, gene archive) as a compressed ZIP file."
            )
        except Exception as e:
            st.error(f"Could not prepare data for download: {e}")
            # st.exception(e) # Uncomment for debugging

if __name__ == "__main__":
    # Add pydot to the path if it's not found
    try:
        import pydot
    except ImportError:
        st.error("This app requires the 'pydot' and 'graphviz' libraries for some GRN visualizations. Please install them: `pip install pydot graphviz` and ensure Graphviz is in your system's PATH.")
    
    main()
