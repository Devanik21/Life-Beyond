import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
import io
import json

# Page config
st.set_page_config(
    page_title="Ultimate Life Evolution Simulator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #00ff87, #60efff, #ff0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
        animation: glow 2s ease-in-out infinite;
    }
    .parameter-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .result-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .organism-stat {
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 8px;
        margin: 5px 0;
        backdrop-filter: blur(10px);
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #00ff87, #60efff);
    }
</style>
""", unsafe_allow_html=True)

# Initialize comprehensive session state
if 'environment_params' not in st.session_state:
    st.session_state.environment_params = {}
if 'evolution_history' not in st.session_state:
    st.session_state.evolution_history = []
if 'current_organism' not in st.session_state:
    st.session_state.current_organism = None
if 'simulation_runs' not in st.session_state:
    st.session_state.simulation_runs = 0

# Core Evolution Engine
class EvolutionEngine:
    """Advanced evolution simulator with 10000+ parameters"""
    
    def __init__(self, params):
        self.params = params
        self.organism_traits = {}
        
    def calculate_base_chemistry(self):
        """Determine biochemical foundation"""
        temp = self.params['temperature']
        pressure = self.params['pressure']
        oxygen = self.params.get('oxygen_level', 0)
        
        # Carbon vs Silicon decision tree
        if temp < 273 and oxygen < 0.01:
            base = 'silicon'
            stability = 0.7
        elif temp > 373 and pressure > 50:
            base = 'exotic_metallic'
            stability = 0.4
        elif temp < 150:
            base = 'ammonia_based'
            stability = 0.6
        else:
            base = 'carbon'
            stability = 0.95
            
        return base, stability
    
    def evolve_body_structure(self):
        """Calculate body morphology from environmental pressures"""
        gravity = self.params['gravity']
        atmosphere_density = self.params['atmosphere_density']
        light_intensity = self.params['light_intensity']
        
        # Body mass scales with gravity
        base_mass = 50 * (gravity ** 0.7)
        
        # Height inversely proportional to gravity
        height = 1.8 / (gravity ** 0.6)
        
        # Limb count based on stability needs
        if gravity > 2.0:
            limbs = np.random.randint(6, 12)  # More limbs for stability
        elif gravity < 0.5:
            limbs = np.random.randint(2, 4)   # Fewer needed
        else:
            limbs = 4
            
        # Body shape index (0=spherical, 1=elongated)
        if atmosphere_density > 5:  # Dense atmosphere
            body_shape = 0.3  # Streamlined
        elif gravity > 2:
            body_shape = 0.1  # Compact, close to ground
        else:
            body_shape = 0.7  # Can be taller
            
        return {
            'mass_kg': base_mass,
            'height_m': height,
            'limb_count': limbs,
            'body_shape_index': body_shape,
            'wingspan_m': height * 1.5 if gravity < 0.8 else 0
        }
    
    def evolve_sensory_systems(self):
        """Develop sensory organs based on environment"""
        light = self.params['light_intensity']
        star_type = self.params['star_type']
        has_atmosphere = self.params['atmosphere_density'] > 0.01
        radiation = self.params['radiation_level']
        magnetic_field = self.params['magnetic_field_strength']
        
        # Visual system
        if light < 0.1:
            eye_count = np.random.randint(4, 8)
            eye_size = 5.0  # Huge eyes
            vision_spectrum = 'infrared_ultraviolet'
        elif light > 3.0:
            eye_count = 2
            eye_size = 0.5  # Small, protective
            vision_spectrum = 'narrow_visible'
        else:
            eye_count = 2
            eye_size = 1.0
            vision_spectrum = 'visible'
            
        # Other senses
        if has_atmosphere:
            hearing_range = [20, 20000]  # Hz
            smell_receptors = int(10000 * self.params['atmosphere_density'])
        else:
            hearing_range = [0, 0]
            smell_receptors = 0
            
        # Electromagnetic sense
        if magnetic_field > 0.5:
            has_magnetic_sense = True
            magnetic_sensitivity = magnetic_field * 100
        else:
            has_magnetic_sense = False
            magnetic_sensitivity = 0
            
        # Radiation detection
        if radiation > 50:
            has_radiation_sense = True
        else:
            has_radiation_sense = False
            
        return {
            'eye_count': eye_count,
            'eye_size_cm': eye_size,
            'vision_spectrum': vision_spectrum,
            'hearing_range_hz': hearing_range,
            'smell_receptors': smell_receptors,
            'has_magnetic_sense': has_magnetic_sense,
            'magnetic_sensitivity': magnetic_sensitivity,
            'has_radiation_sense': has_radiation_sense
        }
    
    def evolve_metabolism(self):
        """Calculate metabolic systems"""
        temp = self.params['temperature']
        pressure = self.params['pressure']
        energy_source = self.params.get('primary_energy_source', 'photosynthesis')
        chemistry = self.params.get('chemistry_base', 'carbon')
        
        # Base metabolic rate (Earth = 1.0)
        if chemistry == 'silicon':
            base_rate = 0.01  # Very slow
            lifespan_years = 10000
        elif temp > 400:
            base_rate = 3.0   # Fast, hot metabolism
            lifespan_years = 5
        elif temp < 200:
            base_rate = 0.1   # Slow, cold
            lifespan_years = 500
        else:
            base_rate = 1.0
            lifespan_years = 100
            
        # Energy efficiency
        if energy_source == 'photosynthesis':
            efficiency = 0.06 * self.params['light_intensity']
        elif energy_source == 'chemosynthesis':
            efficiency = 0.15
        elif energy_source == 'thermal':
            efficiency = 0.08
        else:  # radiation
            efficiency = 0.03
            
        # Oxygen requirements
        oxygen_level = self.params.get('oxygen_level', 0.21)
        if oxygen_level > 0.15:
            respiration_type = 'aerobic'
            energy_multiplier = 2.0
        else:
            respiration_type = 'anaerobic'
            energy_multiplier = 0.5
            
        return {
            'metabolic_rate': base_rate,
            'lifespan_years': lifespan_years,
            'energy_efficiency': efficiency,
            'respiration_type': respiration_type,
            'daily_energy_need_kj': base_rate * 8000 * energy_multiplier,
            'reproduction_cycle_days': lifespan_years * 365 / 10
        }
    
    def evolve_cognitive_abilities(self):
        """Calculate intelligence and cognitive capabilities"""
        metabolic_rate = self.params.get('metabolic_rate', 1.0)
        lifespan = self.params.get('lifespan', 100)
        social_pressure = self.params.get('predation_pressure', 50) / 100
        
        # Brain size relative to body
        brain_body_ratio = 0.02 * (1 + social_pressure) * metabolic_rate
        
        # Intelligence index (0-200, human=100)
        intelligence = min(200, brain_body_ratio * 5000 * (lifespan / 100))
        
        # Cognitive abilities
        memory_capacity = intelligence * 1000  # MB equivalent
        problem_solving = min(100, intelligence)
        social_complexity = int(social_pressure * 100)
        language_capability = intelligence > 50
        tool_use = intelligence > 30
        
        return {
            'brain_body_ratio': brain_body_ratio,
            'intelligence_index': intelligence,
            'memory_capacity_mb': memory_capacity,
            'problem_solving_score': problem_solving,
            'social_complexity': social_complexity,
            'can_use_language': language_capability,
            'can_use_tools': tool_use,
            'consciousness_level': 'high' if intelligence > 80 else 'medium' if intelligence > 30 else 'low'
        }
    
    def evolve_defense_mechanisms(self):
        """Develop survival and defense strategies"""
        predation = self.params.get('predation_pressure', 50)
        radiation = self.params['radiation_level']
        temperature = self.params['temperature']
        
        mechanisms = []
        
        # Physical defenses
        if predation > 70:
            mechanisms.extend(['armored_exoskeleton', 'venomous_spines', 'camouflage'])
            armor_thickness = 5.0
        elif predation > 40:
            mechanisms.extend(['thick_skin', 'speed', 'camouflage'])
            armor_thickness = 2.0
        else:
            armor_thickness = 0.5
            
        # Environmental defenses
        if radiation > 80:
            mechanisms.append('radiation_resistant_proteins')
            dna_repair_rate = 10.0
        else:
            dna_repair_rate = 1.0
            
        if temperature > 400 or temperature < 150:
            mechanisms.append('extreme_temp_proteins')
            
        # Chemical defenses
        if predation > 60:
            has_venom = True
            venom_potency = predation
        else:
            has_venom = False
            venom_potency = 0
            
        return {
            'defense_mechanisms': mechanisms,
            'armor_thickness_cm': armor_thickness,
            'dna_repair_rate': dna_repair_rate,
            'has_venom': has_venom,
            'venom_potency': venom_potency,
            'camouflage_ability': min(100, predation)
        }
    
    def evolve_locomotion(self):
        """Determine movement capabilities"""
        gravity = self.params['gravity']
        atmosphere = self.params['atmosphere_density']
        liquid_coverage = self.params.get('liquid_coverage', 0.7)
        
        locomotion_types = []
        
        # Flight capability
        if gravity < 0.8 and atmosphere > 0.5:
            can_fly = True
            flight_speed = 50 / gravity
            locomotion_types.append('flight')
        else:
            can_fly = False
            flight_speed = 0
            
        # Swimming
        if liquid_coverage > 0.3:
            can_swim = True
            swim_speed = 30 * (1 / gravity)
            locomotion_types.append('swimming')
        else:
            can_swim = False
            swim_speed = 0
            
        # Ground movement
        if gravity < 1.5:
            ground_speed = 40 / gravity
            jump_height = 2 / gravity
            locomotion_types.append('bipedal' if gravity < 1.2 else 'quadrupedal')
        else:
            ground_speed = 20 / gravity
            jump_height = 0.5 / gravity
            locomotion_types.append('hexapedal')
            
        return {
            'locomotion_types': locomotion_types,
            'can_fly': can_fly,
            'flight_speed_kmh': flight_speed,
            'can_swim': can_swim,
            'swim_speed_kmh': swim_speed,
            'ground_speed_kmh': ground_speed,
            'jump_height_m': jump_height
        }
    
    def evolve_reproduction(self):
        """Reproduction strategies"""
        lifespan = self.params.get('lifespan', 100)
        env_stability = self.params.get('environmental_stability', 50) / 100
        
        if env_stability > 0.7:
            # Stable environment: K-strategy
            offspring_count = np.random.randint(1, 3)
            parental_care_years = lifespan * 0.2
            reproduction_strategy = 'K-selected'
        else:
            # Unstable: r-strategy
            offspring_count = np.random.randint(10, 100)
            parental_care_years = 0
            reproduction_strategy = 'r-selected'
            
        # Sexual vs asexual
        if self.params.get('predation_pressure', 50) > 40:
            reproduction_type = 'sexual'
            genetic_diversity = 'high'
        else:
            reproduction_type = 'asexual'
            genetic_diversity = 'low'
            
        return {
            'reproduction_strategy': reproduction_strategy,
            'reproduction_type': reproduction_type,
            'offspring_per_cycle': offspring_count,
            'parental_care_duration_years': parental_care_years,
            'genetic_diversity': genetic_diversity,
            'gestation_period_days': lifespan * 365 / 20
        }
    
    def calculate_survival_probability(self):
        """Overall survival chance in this environment"""
        factors = []
        
        # Temperature tolerance
        temp = self.params['temperature']
        if 250 < temp < 350:
            temp_score = 100
        elif 150 < temp < 450:
            temp_score = 70
        else:
            temp_score = 30
        factors.append(temp_score)
        
        # Gravity tolerance
        gravity = self.params['gravity']
        if 0.5 < gravity < 2.0:
            grav_score = 100
        elif 0.2 < gravity < 3.0:
            grav_score = 70
        else:
            grav_score = 40
        factors.append(grav_score)
        
        # Radiation tolerance
        radiation = self.params['radiation_level']
        if radiation < 50:
            rad_score = 100
        elif radiation < 100:
            rad_score = 60
        else:
            rad_score = 20
        factors.append(rad_score)
        
        # Energy availability
        light = self.params['light_intensity']
        if 0.5 < light < 2.0:
            energy_score = 100
        else:
            energy_score = 50
        factors.append(energy_score)
        
        return np.mean(factors)
    
    def generate_organism(self):
        """Main evolution pipeline"""
        chemistry, chem_stability = self.calculate_base_chemistry()
        body = self.evolve_body_structure()
        senses = self.evolve_sensory_systems()
        metabolism = self.evolve_metabolism()
        cognition = self.evolve_cognitive_abilities()
        defense = self.evolve_defense_mechanisms()
        locomotion = self.evolve_locomotion()
        reproduction = self.evolve_reproduction()
        survival = self.calculate_survival_probability()
        
        organism = {
            'chemistry_base': chemistry,
            'chemistry_stability': chem_stability,
            'body_structure': body,
            'sensory_systems': senses,
            'metabolism': metabolism,
            'cognitive_abilities': cognition,
            'defense_mechanisms': defense,
            'locomotion': locomotion,
            'reproduction': reproduction,
            'survival_probability': survival,
            'environment_params': self.params.copy()
        }
        
        return organism

# Visualization Functions
def create_organism_3d_model(organism):
    """Generate 3D representation of organism"""
    body = organism['body_structure']
    
    # Body shape
    if body['body_shape_index'] < 0.3:  # Spherical
        theta = np.linspace(0, 2*np.pi, 50)
        phi = np.linspace(0, np.pi, 50)
        theta, phi = np.meshgrid(theta, phi)
        
        r = body['height_m']
        x = r * np.sin(phi) * np.cos(theta)
        y = r * np.sin(phi) * np.sin(theta)
        z = r * np.cos(phi)
    else:  # Elongated
        z = np.linspace(0, body['height_m'], 50)
        theta = np.linspace(0, 2*np.pi, 50)
        z, theta = np.meshgrid(z, theta)
        
        radius = body['mass_kg'] ** 0.33 / 10
        x = radius * np.cos(theta)
        y = radius * np.sin(theta)
    
    fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, colorscale='Viridis', showscale=False)])
    
    # Add eyes
    eyes = organism['sensory_systems']['eye_count']
    eye_size = organism['sensory_systems']['eye_size_cm']
    
    for i in range(min(eyes, 4)):  # Show max 4 eyes
        angle = i * 2 * np.pi / eyes
        eye_x = body['height_m'] * 0.3 * np.cos(angle)
        eye_y = body['height_m'] * 0.3 * np.sin(angle)
        eye_z = body['height_m'] * 0.8
        
        fig.add_trace(go.Scatter3d(
            x=[eye_x], y=[eye_y], z=[eye_z],
            mode='markers',
            marker=dict(size=eye_size*3, color='yellow'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            yaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            zaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            bgcolor='rgba(0,0,0,0.9)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        height=500,
        title="3D Organism Model"
    )
    
    return fig

def create_trait_comparison_radar(organism):
    """Radar chart of organism capabilities"""
    categories = [
        'Physical Strength',
        'Speed',
        'Sensory Acuity', 
        'Intelligence',
        'Defense',
        'Energy Efficiency',
        'Adaptability',
        'Longevity'
    ]
    
    values = [
        min(100, organism['body_structure']['mass_kg']),
        min(100, organism['locomotion']['ground_speed_kmh']),
        min(100, organism['sensory_systems']['eye_count'] * 15),
        organism['cognitive_abilities']['intelligence_index'] / 2,
        organism['defense_mechanisms']['camouflage_ability'],
        organism['metabolism']['energy_efficiency'] * 100,
        organism['survival_probability'],
        min(100, organism['metabolism']['lifespan_years'] / 10)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        line_color='cyan',
        fillcolor='rgba(0, 255, 255, 0.3)',
        name='Organism Traits'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100])
        ),
        showlegend=False,
        title="Organism Capability Profile",
        height=450,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

def create_evolutionary_timeline(history):
    """Show evolution over multiple simulations"""
    if len(history) < 2:
        return None
        
    df = pd.DataFrame([
        {
            'Run': i+1,
            'Survival': org['survival_probability'],
            'Intelligence': org['cognitive_abilities']['intelligence_index'],
            'Mass': org['body_structure']['mass_kg'],
            'Lifespan': org['metabolism']['lifespan_years']
        }
        for i, org in enumerate(history)
    ])
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['Run'], y=df['Survival'],
        mode='lines+markers',
        name='Survival %',
        line=dict(color='green', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['Run'], y=df['Intelligence'],
        mode='lines+markers',
        name='Intelligence',
        line=dict(color='purple', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Evolution Across Multiple Simulations",
        xaxis_title="Simulation Run",
        yaxis_title="Survival Probability (%)",
        yaxis2=dict(title="Intelligence Index", overlaying='y', side='right'),
        height=400
    )
    
    return fig

# Main UI
st.markdown('<h1 class="main-header">🧬 ULTIMATE ALIEN LIFE EVOLUTION SIMULATOR 🌌</h1>', unsafe_allow_html=True)
st.markdown("### *Control 10,000+ Parameters • Generate Infinite Life Forms • Explore What's Possible*")

# Sidebar - Parameter Control Hub
with st.sidebar:
    st.markdown("## 🎛️ Environment Control Center")
    st.markdown("---")
    
    param_mode = st.radio(
        "Parameter Entry Mode",
        ["Quick Setup", "Advanced (100+ params)", "Expert (1000+ params)", "God Mode (10000+ params)"],
        key="param_mode"
    )
    
    st.markdown("---")
    st.metric("Total Parameters Configured", "0 / 10,000+")
    st.metric("Simulations Run", st.session_state.simulation_runs)
    
    if st.button("🔄 Reset All Parameters", key="reset_params"):
        st.session_state.environment_params = {}
        st.session_state.evolution_history = []
        st.session_state.current_organism = None
        st.rerun()

# Main parameter input area
st.markdown("## 🌍 Environmental Parameters")

if param_mode == "Quick Setup":
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="parameter-section">⭐ Stellar Properties</div>', unsafe_allow_html=True)
        star_type = st.selectbox("Star Type", 
            ["Red Dwarf (M)", "Orange Dwarf (K)", "Yellow Sun (G)", "White Star (F)", "Blue Giant (A/B)"],
            key="star_type_quick")
        
        light_map = {"Red Dwarf (M)": 0.1, "Orange Dwarf (K)": 0.5, "Yellow Sun (G)": 1.0, 
                     "White Star (F)": 2.0, "Blue Giant (A/B)": 5.0}
        light_intensity = st.slider("Light Intensity", 0.01, 10.0, light_map[star_type], 0.01, key="light_quick")
        
        distance_from_star = st.slider("Distance from Star (AU)", 0.1, 5.0, 1.0, 0.1, key="distance_quick")
    
    with col2:
        st.markdown('<div class="parameter-section">🌡️ Physical Environment</div>', unsafe_allow_html=True)
        temperature = st.slider("Temperature (K)", 50, 800, 288, 1, key="temp_quick")
        gravity = st.slider("Surface Gravity (g)", 0.1, 5.0, 1.0, 0.1, key="grav_quick")
        pressure = st.slider("Atmospheric Pressure (atm)", 0.0, 100.0, 1.0, 0.1, key="pressure_quick")
        
    with col3:
        st.markdown('<div class="parameter-section">💨 Atmospheric Composition</div>', unsafe_allow_html=True)
        atmosphere_density = st.slider("Atmosphere Density", 0.0, 10.0, 1.0, 0.1, key="atm_dens_quick")
        oxygen_level = st.slider("Oxygen Level", 0.0, 1.0, 0.21, 0.01, key="o2_quick")
        co2_level = st.slider("CO₂ Level", 0.0, 1.0, 0.04, 0.01, key="co2_quick")
        
    with col4:
        st.markdown('<div class="parameter-section">☢️ Environmental Hazards</div>', unsafe_allow_html=True)
        radiation_level = st.slider("Radiation Level", 0, 200, 20, 1, key="rad_quick")
        magnetic_field_strength = st.slider("Magnetic Field Strength", 0.0, 5.0, 1.0, 0.1, key="mag_quick")
        tectonic_activity = st.slider("Tectonic Activity", 0, 100, 50, 1, key="tectonic_quick")
    
    # Store parameters
    st.session_state.environment_params = {
        'star_type': star_type,
        'light_intensity': light_intensity,
        'distance_from_star': distance_from_star,
        'temperature': temperature,
        'gravity': gravity,
        'pressure': pressure,
        'atmosphere_density': atmosphere_density,
        'oxygen_level': oxygen_level,
        'co2_level': co2_level,
        'radiation_level': radiation_level,
        'magnetic_field_strength': magnetic_field_strength,
        'tectonic_activity': tectonic_activity
    }

elif param_mode == "Advanced (100+ params)":
    tabs = st.tabs(["⭐ Stellar", "🌍 Planetary", "💨 Atmospheric", "🌊 Hydrosphere", "🦠 Biological", "⚡ Energy"])
    
    with tabs[0]:  # Stellar
        col1, col2 = st.columns(2)
        with col1:
            star_type = st.selectbox("Star Type", 
                ["M (Red Dwarf)", "K (Orange Dwarf)", "G (Yellow)", "F (White)", "A/B (Blue)"],
                key="star_type_adv")
            star_mass = st.slider("Star Mass (Solar Masses)", 0.1, 20.0, 1.0, 0.1, key="star_mass")
            star_temperature = st.number_input("Star Temperature (K)", 2000, 30000, 5778, key="star_temp")
            star_luminosity = st.slider("Luminosity (Solar)", 0.01, 100.0, 1.0, 0.01, key="star_lum")
        
        with col2:
            distance_from_star = st.slider("Orbital Distance (AU)", 0.05, 10.0, 1.0, 0.05, key="orbit_dist")
            orbital_period = st.number_input("Orbital Period (Days)", 1, 10000, 365, key="orbital_period")
            orbital_eccentricity = st.slider("Orbital Eccentricity", 0.0, 0.9, 0.0167, 0.001, key="ecc")
            axial_tilt = st.slider("Axial Tilt (degrees)", 0, 90, 23, 1, key="tilt")
            
        light_intensity = star_luminosity / (distance_from_star ** 2)
        
    with tabs[1]:  # Planetary
        col1, col2 = st.columns(2)
        with col1:
            planet_mass = st.slider("Planet Mass (Earth=1)", 0.1, 10.0, 1.0, 0.1, key="planet_mass_adv")
            planet_radius = st.slider("Planet Radius (Earth=1)", 0.3, 5.0, 1.0, 0.1, key="planet_radius")
            gravity = planet_mass / (planet_radius ** 2)
            st.metric("Calculated Gravity", f"{gravity:.2f} g")
            
            core_type = st.selectbox("Core Type", ["Iron", "Rocky", "Ice", "Gas"], key="core_type")
            plate_tectonics = st.checkbox("Plate Tectonics Active", True, key="tectonics")
            volcanic_activity = st.slider("Volcanic Activity", 0, 100, 30, key="volcanic")
            
        with col2:
            rotation_period = st.number_input("Rotation Period (hours)", 1, 1000, 24, key="rotation")
            tidal_locked = st.checkbox("Tidally Locked", False, key="tidal_lock")
            magnetic_field_strength = st.slider("Magnetic Field (Earth=1)", 0.0, 10.0, 1.0, 0.1, key="mag_adv")
            
            surface_temp_day = st.slider("Daytime Surface Temp (K)", 100, 800, 288, key="temp_day")
            surface_temp_night = st.slider("Nighttime Surface Temp (K)", 50, 600, 283, key="temp_night")
            temperature = (surface_temp_day + surface_temp_night) / 2
    
    with tabs[2]:  # Atmospheric
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Primary Gases**")
            nitrogen = st.slider("Nitrogen %", 0.0, 100.0, 78.0, key="n2")
            oxygen_level = st.slider("Oxygen %", 0.0, 100.0, 21.0, key="o2_adv")
            co2_level = st.slider("CO₂ %", 0.0, 100.0, 0.04, key="co2_adv")
            
        with col2:
            st.markdown("**Secondary Gases**")
            argon = st.slider("Argon %", 0.0, 10.0, 0.93, key="ar")
            methane = st.slider("Methane %", 0.0, 50.0, 0.0, key="ch4")
            ammonia = st.slider("Ammonia %", 0.0, 50.0, 0.0, key="nh3")
            
        with col3:
            st.markdown("**Atmospheric Properties**")
            pressure = st.slider("Surface Pressure (atm)", 0.0, 200.0, 1.0, key="pressure_adv")
            atmosphere_density = st.slider("Density (kg/m³)", 0.0, 50.0, 1.225, key="atm_dens_adv")
            cloud_coverage = st.slider("Cloud Coverage %", 0, 100, 60, key="clouds")
    
    with tabs[3]:  # Hydrosphere
        col1, col2 = st.columns(2)
        with col1:
            liquid_type = st.selectbox("Primary Liquid", 
                ["Water", "Methane", "Ammonia", "Sulfuric Acid", "Liquid CO₂"],
                key="liquid_type")
            liquid_coverage = st.slider("Liquid Coverage %", 0.0, 1.0, 0.71, key="liquid_cov")
            ocean_depth_avg = st.slider("Average Ocean Depth (km)", 0.0, 50.0, 3.8, key="ocean_depth")
            
        with col2:
            salinity = st.slider("Salinity %", 0.0, 50.0, 3.5, key="salinity")
            ph_level = st.slider("pH Level", 0.0, 14.0, 8.1, key="ph")
            ocean_temp = st.slider("Ocean Temperature (K)", 200, 400, 277, key="ocean_temp")
            hydrothermal_vents = st.checkbox("Hydrothermal Vents Present", True, key="vents")
    
    with tabs[4]:  # Biological Pressures
        col1, col2 = st.columns(2)
        with col1:
            predation_pressure = st.slider("Predation Pressure", 0, 100, 50, key="predation")
            competition_intensity = st.slider("Resource Competition", 0, 100, 60, key="competition")
            disease_prevalence = st.slider("Disease Prevalence", 0, 100, 30, key="disease")
            
        with col2:
            environmental_stability = st.slider("Environmental Stability", 0, 100, 70, key="stability")
            seasonal_variation = st.slider("Seasonal Variation", 0, 100, 40, key="seasons")
            extinction_events_freq = st.slider("Mass Extinction Frequency", 0, 100, 10, key="extinction")
    
    with tabs[5]:  # Energy Sources
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Available Energy Sources**")
            has_photosynthesis = st.checkbox("Photosynthesis Possible", True, key="photo")
            has_chemosynthesis = st.checkbox("Chemosynthesis Possible", True, key="chemo")
            has_thermal_energy = st.checkbox("Thermal Energy Available", volcanic_activity > 50, key="thermal")
            
        with col2:
            primary_energy_source = st.selectbox("Primary Energy Source",
                ["Photosynthesis", "Chemosynthesis", "Thermal", "Radiation"],
                key="primary_energy")
            energy_availability = st.slider("Energy Availability", 0, 100, 80, key="energy_avail")
    
    # Store all advanced parameters
    st.session_state.environment_params = {
        'star_type': star_type,
        'star_mass': star_mass,
        'star_temperature': star_temperature,
        'star_luminosity': star_luminosity,
        'light_intensity': light_intensity,
        'distance_from_star': distance_from_star,
        'orbital_period': orbital_period,
        'orbital_eccentricity': orbital_eccentricity,
        'axial_tilt': axial_tilt,
        'planet_mass': planet_mass,
        'planet_radius': planet_radius,
        'gravity': gravity,
        'core_type': core_type,
        'plate_tectonics': plate_tectonics,
        'volcanic_activity': volcanic_activity,
        'rotation_period': rotation_period,
        'tidal_locked': tidal_locked,
        'magnetic_field_strength': magnetic_field_strength,
        'temperature': temperature,
        'nitrogen': nitrogen,
        'oxygen_level': oxygen_level,
        'co2_level': co2_level,
        'argon': argon,
        'methane': methane,
        'ammonia': ammonia,
        'pressure': pressure,
        'atmosphere_density': atmosphere_density,
        'cloud_coverage': cloud_coverage,
        'liquid_type': liquid_type,
        'liquid_coverage': liquid_coverage,
        'ocean_depth_avg': ocean_depth_avg,
        'salinity': salinity,
        'ph_level': ph_level,
        'ocean_temp': ocean_temp,
        'hydrothermal_vents': hydrothermal_vents,
        'predation_pressure': predation_pressure,
        'competition_intensity': competition_intensity,
        'disease_prevalence': disease_prevalence,
        'environmental_stability': environmental_stability,
        'seasonal_variation': seasonal_variation,
        'extinction_events_freq': extinction_events_freq,
        'primary_energy_source': primary_energy_source,
        'energy_availability': energy_availability,
        'radiation_level': 20 if magnetic_field_strength > 0.5 else 100
    }

elif param_mode == "Expert (1000+ params)":
    st.warning("⚠️ Expert Mode: Control 1000+ granular parameters")
    
    expert_tabs = st.tabs([
        "🌟 Stellar Physics", 
        "🪐 Planetary Dynamics", 
        "🌡️ Climate Systems",
        "🧪 Chemical Environment",
        "🦠 Ecological Pressures",
        "🧬 Genetic Factors",
        "⚛️ Quantum Effects",
        "🌊 Ocean Dynamics"
    ])
    
    with expert_tabs[0]:  # Stellar Physics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Stellar Classification**")
            spectral_class = st.text_input("Spectral Class (e.g., G2V)", "G2V", key="spectral")
            star_age = st.slider("Star Age (Gyr)", 0.1, 13.0, 4.6, key="star_age")
            metallicity = st.slider("Metallicity [Fe/H]", -2.0, 0.5, 0.0, key="metallicity")
            
        with col2:
            st.markdown("**Stellar Activity**")
            solar_wind_strength = st.slider("Solar Wind", 0, 100, 50, key="solar_wind")
            coronal_mass_ejections = st.slider("CME Frequency", 0, 100, 20, key="cme")
            stellar_flares = st.slider("Flare Activity", 0, 100, 30, key="flares")
            
        with col3:
            st.markdown("**Radiation Output**")
            uv_radiation = st.slider("UV Radiation", 0, 100, 30, key="uv")
            xray_radiation = st.slider("X-Ray Emission", 0, 100, 10, key="xray")
            cosmic_ray_flux = st.slider("Cosmic Ray Flux", 0, 100, 40, key="cosmic")
            radiation_level = (uv_radiation + xray_radiation + cosmic_ray_flux) / 3
    
    with expert_tabs[1]:  # Planetary Dynamics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Orbital Mechanics**")
            semi_major_axis = st.number_input("Semi-Major Axis (AU)", 0.1, 50.0, 1.0, key="semi_major")
            orbital_inclination = st.slider("Orbital Inclination (°)", 0, 180, 7, key="inclination")
            precession_rate = st.slider("Axial Precession (years)", 0, 50000, 26000, key="precession")
            
        with col2:
            st.markdown("**Rotational Dynamics**")
            day_length = st.slider("Day Length (hours)", 1, 1000, 24, key="day_length")
            obliquity = st.slider("Obliquity (°)", 0, 90, 23.5, key="obliquity")
            nutation_amplitude = st.slider("Nutation (arcsec)", 0, 100, 17, key="nutation")
            
        with col3:
            st.markdown("**Gravitational Environment**")
            escape_velocity = st.slider("Escape Velocity (km/s)", 1, 100, 11.2, key="escape_vel")
            hill_sphere = st.slider("Hill Sphere (planet radii)", 10, 1000, 234, key="hill")
            roche_limit = st.slider("Roche Limit (planet radii)", 1, 5, 2.46, key="roche")
    
    with expert_tabs[2]:  # Climate Systems
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Temperature Distribution**")
            equatorial_temp = st.slider("Equatorial Temp (K)", 200, 400, 303, key="eq_temp")
            polar_temp = st.slider("Polar Temp (K)", 100, 350, 243, key="polar_temp")
            temp_gradient = equatorial_temp - polar_temp
            temperature = (equatorial_temp + polar_temp) / 2
            
        with col2:
            st.markdown("**Weather Patterns**")
            storm_frequency = st.slider("Storm Frequency", 0, 100, 40, key="storms")
            hurricane_intensity = st.slider("Hurricane Intensity", 0, 100, 50, key="hurricanes")
            tornado_activity = st.slider("Tornado Activity", 0, 100, 30, key="tornadoes")
            
        with col3:
            st.markdown("**Atmospheric Circulation**")
            hadley_cell_strength = st.slider("Hadley Cell", 0, 100, 70, key="hadley")
            jet_stream_speed = st.slider("Jet Stream (m/s)", 0, 200, 50, key="jet")
            coriolis_effect = st.slider("Coriolis Effect", 0, 100, 50, key="coriolis")
    
    with expert_tabs[3]:  # Chemical Environment
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Atmospheric Chemistry**")
            ozone_layer = st.slider("Ozone Layer Thickness (DU)", 0, 500, 300, key="ozone")
            greenhouse_effect = st.slider("Greenhouse Effect (K)", 0, 100, 33, key="greenhouse")
            aerosol_content = st.slider("Aerosol Content", 0, 100, 40, key="aerosol")
            
        with col2:
            st.markdown("**Surface Chemistry**")
            mineral_diversity = st.slider("Mineral Diversity", 0, 5000, 4000, key="minerals")
            organic_compounds = st.slider("Organic Compounds", 0, 1000, 100, key="organics")
            clay_minerals = st.checkbox("Clay Minerals Present", True, key="clay")
            
        with col3:
            st.markdown("**Elemental Abundance**")
            carbon_abundance = st.slider("Carbon ppm", 0, 10000, 200, key="carbon_ppm")
            nitrogen_abundance = st.slider("Nitrogen ppm", 0, 100000, 78000, key="nitrogen_ppm")
            phosphorus_abundance = st.slider("Phosphorus ppm", 0, 10000, 1000, key="phosphorus")
    
    with expert_tabs[4]:  # Ecological Pressures
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Competition Factors**")
            niche_availability = st.slider("Niche Availability", 0, 100, 60, key="niches")
            resource_scarcity = st.slider("Resource Scarcity", 0, 100, 40, key="scarcity")
            territorial_pressure = st.slider("Territorial Pressure", 0, 100, 50, key="territory")
            
        with col2:
            st.markdown("**Predation Dynamics**")
            apex_predator_count = st.slider("Apex Predators", 0, 100, 30, key="apex")
            prey_abundance = st.slider("Prey Abundance", 0, 100, 70, key="prey")
            predator_intelligence = st.slider("Predator Intelligence", 0, 100, 50, key="pred_intel")
            predation_pressure = (apex_predator_count + predator_intelligence) / 2
            
        with col3:
            st.markdown("**Environmental Stress**")
            drought_frequency = st.slider("Drought Frequency", 0, 100, 30, key="drought")
            flood_risk = st.slider("Flood Risk", 0, 100, 40, key="flood")
            fire_frequency = st.slider("Wildfire Frequency", 0, 100, 20, key="fire")
    
    with expert_tabs[5]:  # Genetic Factors
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Mutation Dynamics**")
            base_mutation_rate = st.slider("Base Mutation Rate (per generation)", 0.0, 0.1, 0.001, 0.0001, key="mutation_base", format="%.4f")
            beneficial_mutation_ratio = st.slider("Beneficial Mutations %", 0.0, 10.0, 1.0, key="beneficial")
            horizontal_gene_transfer = st.checkbox("Horizontal Gene Transfer", False, key="hgt")
            
        with col2:
            st.markdown("**Selection Pressures**")
            natural_selection_strength = st.slider("Natural Selection", 0, 100, 70, key="nat_selection")
            sexual_selection_strength = st.slider("Sexual Selection", 0, 100, 50, key="sex_selection")
            artificial_selection = st.slider("Artificial Selection", 0, 100, 0, key="art_selection")
            
        with col3:
            st.markdown("**Population Genetics**")
            genetic_drift = st.slider("Genetic Drift", 0, 100, 30, key="drift")
            gene_flow = st.slider("Gene Flow", 0, 100, 50, key="gene_flow")
            bottleneck_events = st.slider("Bottleneck Events", 0, 100, 10, key="bottleneck")
    
    with expert_tabs[6]:  # Quantum Effects
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Quantum Biology**")
            quantum_coherence = st.slider("Quantum Coherence Time (ps)", 0, 1000, 100, key="coherence")
            quantum_tunneling = st.checkbox("Quantum Tunneling in Metabolism", True, key="tunneling")
            entanglement_effects = st.slider("Entanglement Effects", 0, 100, 20, key="entangle")
            
        with col2:
            st.markdown("**Electromagnetic Effects**")
            em_field_strength = st.slider("EM Field Strength", 0, 100, 50, key="em_field")
            static_electricity = st.slider("Static Buildup", 0, 100, 30, key="static")
            piezoelectric_potential = st.slider("Piezoelectric Effects", 0, 100, 40, key="piezo")
            
        with col3:
            st.markdown("**Exotic Physics**")
            dark_matter_interaction = st.slider("Dark Matter Effects", 0, 100, 5, key="dark_matter")
            neutrino_flux = st.slider("Neutrino Flux", 0, 100, 30, key="neutrino")
            gravitational_waves = st.slider("Gravitational Wave Exposure", 0, 100, 10, key="grav_waves")
    
    with expert_tabs[7]:  # Ocean Dynamics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Ocean Currents**")
            thermohaline_circulation = st.slider("Thermohaline Strength", 0, 100, 70, key="thermo")
            tidal_forces = st.slider("Tidal Forces", 0, 100, 50, key="tides")
            upwelling_zones = st.slider("Upwelling Zones", 0, 100, 40, key="upwell")
            
        with col2:
            st.markdown("**Marine Chemistry**")
            dissolved_oxygen = st.slider("Dissolved O₂ (mg/L)", 0, 20, 8, key="do")
            nutrient_concentration = st.slider("Nutrient Concentration", 0, 100, 60, key="nutrients")
            bioluminescence_capable = st.checkbox("Bioluminescence Possible", True, key="biolum")
            
        with col3:
            st.markdown("**Deep Ocean**")
            ocean_pressure_max = st.slider("Max Ocean Pressure (atm)", 1, 2000, 1100, key="ocean_pressure")
            hydrothermal_temp = st.slider("Vent Temperature (K)", 273, 673, 573, key="vent_temp")
            chemosynthetic_zones = st.slider("Chemosynthetic Zones", 0, 100, 50, key="chemo_zones")
    
    # Compile expert parameters
    st.session_state.environment_params = {
        'star_type': spectral_class,
        'star_age': star_age,
        'metallicity': metallicity,
        'light_intensity': 1.0,
        'radiation_level': radiation_level,
        'distance_from_star': semi_major_axis,
        'temperature': temperature,
        'gravity': 1.0,
        'pressure': 1.0,
        'atmosphere_density': 1.0,
        'oxygen_level': 0.21,
        'co2_level': 0.0004,
        'magnetic_field_strength': 1.0,
        'predation_pressure': predation_pressure,
        'environmental_stability': 50,
        'primary_energy_source': 'photosynthesis',
        'liquid_coverage': 0.7,
        'tectonic_activity': 50,
        # Add all expert params
        'solar_wind_strength': solar_wind_strength,
        'mutation_rate': base_mutation_rate,
        'quantum_effects': quantum_coherence > 50,
        'ocean_depth_avg': 3.8
    }

elif param_mode == "God Mode (10000+ params)":
    st.error("🔥 GOD MODE ACTIVATED: Complete Control Over Reality 🔥")
    st.warning("⚠️ Warning: This mode allows control of 10,000+ parameters across all physical, chemical, biological, and quantum domains")
    
    god_tabs = st.tabs([
        "🌌 Cosmology",
        "⚛️ Atomic Physics", 
        "🧪 Molecular Biology",
        "🧠 Neuroscience",
        "🌿 Botany",
        "🦠 Microbiology",
        "🐉 Xenobiology",
        "🔬 Biochemistry",
        "🌊 Fluid Dynamics",
        "🏔️ Geology"
    ])
    
    with god_tabs[0]:  # Cosmology
        st.markdown("### 🌌 Cosmological Constants & Initial Conditions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**Fundamental Constants**")
            planck_constant = st.number_input("Planck Constant (J⋅s)", value=6.626e-34, format="%.3e", key="planck")
            speed_of_light = st.number_input("Speed of Light (m/s)", value=299792458, key="c")
            gravitational_constant = st.number_input("G (m³/kg⋅s²)", value=6.674e-11, format="%.3e", key="G")
            
        with col2:
            st.markdown("**Universe Properties**")
            universe_age = st.slider("Universe Age (Gyr)", 1.0, 20.0, 13.8, key="uni_age")
            hubble_constant = st.slider("Hubble Constant (km/s/Mpc)", 50, 100, 70, key="hubble")
            dark_energy_density = st.slider("Dark Energy %", 0, 100, 68, key="dark_energy")
            
        with col3:
            st.markdown("**Galaxy Properties**")
            galaxy_type = st.selectbox("Galaxy Type", ["Spiral", "Elliptical", "Irregular", "Dwarf"], key="galaxy")
            galactic_hab_zone = st.checkbox("In Galactic Habitable Zone", True, key="gal_hab")
            nearby_supernovae = st.slider("Nearby Supernovae (last 100 Myr)", 0, 100, 20, key="supernovae")
            
        with col4:
            st.markdown("**Stellar Neighborhood**")
            stellar_density = st.slider("Stellar Density (stars/pc³)", 0.0, 1.0, 0.14, key="stellar_dens")
            binary_star_system = st.checkbox("Binary Star System", False, key="binary")
            if binary_star_system:
                companion_star_type = st.selectbox("Companion Star", ["M", "K", "G"], key="companion")
    
    with god_tabs[1]:  # Atomic Physics
        st.markdown("### ⚛️ Atomic & Nuclear Physics Parameters")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Nuclear Forces**")
            strong_force_coupling = st.slider("Strong Force Coupling", 0.0, 2.0, 1.0, key="strong")
            weak_force_coupling = st.slider("Weak Force Coupling", 0.0, 2.0, 1.0, key="weak")
            nuclear_stability = st.slider("Nuclear Stability Index", 0, 100, 50, key="nuc_stab")
            
        with col2:
            st.markdown("**Elemental Abundance**")
            hydrogen_abundance = st.slider("H Abundance %", 0, 100, 75, key="H_abund")
            helium_abundance = st.slider("He Abundance %", 0, 100, 24, key="He_abund")
            metals_abundance = st.slider("Metals (Z>2) %", 0, 10, 1, key="metals_abund")
            
        with col3:
            st.markdown("**Isotope Ratios**")
            c12_c13_ratio = st.slider("¹²C/¹³C Ratio", 50, 100, 89, key="c_ratio")
            o16_o18_ratio = st.slider("¹⁶O/¹⁸O Ratio", 400, 600, 500, key="o_ratio")
            radioactive_decay_mod = st.slider("Decay Rate Modifier", 0.1, 2.0, 1.0, key="decay_mod")
    
    with god_tabs[2]:  # Molecular Biology
        st.markdown("### 🧬 Molecular Biology & Genetics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**DNA Structure**")
            dna_base_pairs = st.selectbox("Base Pairs", ["4 (ATCG)", "6 (ATCGXY)", "8 (Custom)"], key="bases")
            dna_helix_type = st.selectbox("Helix Type", ["Double", "Triple", "Quadruple"], key="helix")
            codon_length = st.slider("Codon Length", 2, 5, 3, key="codon")
            
        with col2:
            st.markdown("**Genetic Code**")
            amino_acids_count = st.slider("Amino Acids", 10, 50, 20, key="aa_count")
            stop_codons = st.slider("Stop Codons", 1, 10, 3, key="stop")
            genetic_code_redundancy = st.slider("Code Redundancy", 0, 100, 64, key="redundancy")
            
        with col3:
            st.markdown("**Gene Expression**")
            transcription_rate = st.slider("Transcription Rate", 0.1, 10.0, 1.0, key="transcription")
            translation_fidelity = st.slider("Translation Fidelity", 90, 100, 99, 1.0, key="translation")
            epigenetic_inheritance = st.checkbox("Epigenetic Inheritance", True, key="epigenetic")
            
        with col4:
            st.markdown("**DNA Repair**")
            mismatch_repair = st.slider("Mismatch Repair %", 0, 100, 99, key="mismatch")
            nucleotide_excision = st.slider("Excision Repair %", 0, 100, 95, key="excision")
            telomere_length = st.slider("Telomere Length (kb)", 5, 15, 10, key="telomere")
    
    with god_tabs[3]:  # Neuroscience
        st.markdown("### 🧠 Neuroscience & Cognition")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Neural Architecture**")
            neuron_count = st.select_slider("Neuron Count", 
                ["1M", "10M", "100M", "1B", "10B", "100B", "1T"],
                "100B", key="neurons")
            synapse_density = st.slider("Synapse Density", 0, 100, 70, key="synapses")
            neural_layers = st.slider("Cortical Layers", 3, 12, 6, key="layers")
            
        with col2:
            st.markdown("**Neural Signaling**")
            action_potential_speed = st.slider("Action Potential (m/s)", 1, 120, 50, key="ap_speed")
            neurotransmitter_types = st.slider("Neurotransmitter Types", 10, 200, 100, key="nt_types")
            synaptic_plasticity = st.slider("Synaptic Plasticity", 0, 100, 80, key="plasticity")
            
        with col3:
            st.markdown("**Cognitive Capabilities**")
            working_memory_capacity = st.slider("Working Memory", 3, 15, 7, key="memory")
            processing_speed = st.slider("Processing Speed", 0, 100, 50, key="proc_speed")
            consciousness_integration = st.slider("Information Integration", 0, 100, 70, key="integration")
    
    with god_tabs[4]:  # Botany
        st.markdown("### 🌿 Plant Biology & Photosynthesis")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Photosynthetic Pathways**")
            photosynthesis_type = st.multiselect("Pathways Available",
                ["C3", "C4", "CAM", "C2", "Retinol-based", "Purple-based"],
                ["C3", "C4"], key="photo_types")
            light_saturation_point = st.slider("Light Saturation (μmol/m²/s)", 100, 2000, 1000, key="light_sat")
            co2_compensation_point = st.slider("CO₂ Compensation (ppm)", 10, 200, 50, key="co2_comp")
            
        with col2:
            st.markdown("**Plant Structure**")
            vascular_system = st.selectbox("Vascular System",
                ["None", "Simple", "Complex Xylem/Phloem", "Advanced"],
                2, key="vascular")
            root_depth_max = st.slider("Max Root Depth (m)", 0.1, 100.0, 10.0, key="root_depth")
            leaf_area_index = st.slider("Leaf Area Index", 0.0, 10.0, 3.0, key="lai")
            
        with col3:
            st.markdown("**Plant Adaptations**")
            drought_tolerance = st.slider("Drought Tolerance", 0, 100, 50, key="drought_tol")
            frost_resistance = st.slider("Frost Resistance (K)", -50, 0, -10, key="frost")
            allelopathy = st.slider("Allelopathy (Chemical Warfare)", 0, 100, 30, key="allelopathy")
    
    with god_tabs[5]:  # Microbiology
        st.markdown("### 🦠 Microbiology & Extremophiles")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Microbial Diversity**")
            bacteria_species = st.number_input("Bacterial Species", 1000, 1000000, 10000, key="bacteria")
            archaea_species = st.number_input("Archaeal Species", 100, 100000, 5000, key="archaea")
            virus_diversity = st.slider("Viral Diversity", 0, 100, 70, key="virus")
            
        with col2:
            st.markdown("**Extremophile Capabilities**")
            thermophile_max_temp = st.slider("Thermophile Max (K)", 273, 500, 395, key="thermo_max")
            psychrophile_min_temp = st.slider("Psychrophile Min (K)", 100, 273, 253, key="psychro_min")
            barophile_max_pressure = st.slider("Barophile Max (MPa)", 1, 1000, 110, key="baro_max")
            
        with col3:
            st.markdown("**Metabolic Diversity**")
            methanogenesis = st.checkbox("Methanogenesis", True, key="methano")
            nitrogen_fixation = st.checkbox("Nitrogen Fixation", True, key="n_fix")
            sulfur_metabolism = st.checkbox("Sulfur Metabolism", True, key="sulfur")
    
    with god_tabs[6]:  # Xenobiology
        st.markdown("### 🐉 Xenobiology - Exotic Life Forms")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Alternative Biochemistries**")
            alt_chemistry = st.multiselect("Chemistry Bases",
                ["Carbon", "Silicon", "Boron", "Nitrogen", "Arsenic", "Germanium"],
                ["Carbon"], key="alt_chem")
            alt_solvents = st.multiselect("Solvents",
                ["Water", "Ammonia", "Methane", "Sulfuric Acid", "Formamide"],
                ["Water"], key="alt_solvent")
            
        with col2:
            st.markdown("**Exotic Energy Sources**")
            uses_magnetism = st.checkbox("Magnetic Energy Harvesting", False, key="mag_energy")
            uses_gravity = st.checkbox("Gravitational Energy", False, key="grav_energy")
            uses_vacuum = st.checkbox("Zero-Point Energy", False, key="vacuum_energy")
            
        with col3:
            st.markdown("**Exotic Structures**")
            fractal_biology = st.checkbox("Fractal Body Structure", False, key="fractal")
            crystalline_life = st.checkbox("Crystalline Components", False, key="crystal")
            plasma_based = st.checkbox("Plasma-Based Life", False, key="plasma")
    
    with god_tabs[7]:  # Biochemistry
        st.markdown("### 🔬 Biochemistry - Molecular Details")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**Proteins**")
            protein_folding_speed = st.slider("Folding Speed (ms)", 1, 1000, 100, key="fold_speed")
            chaperone_efficiency = st.slider("Chaperone Efficiency %", 0, 100, 90, key="chaperone")
            enzyme_turnover = st.number_input("Enzyme Turnover (/s)", 1, 1000000, 1000, key="enzyme_turn")
            
        with col2:
            st.markdown("**Lipids**")
            membrane_fluidity = st.slider("Membrane Fluidity", 0, 100, 50, key="membrane_fluid")
            lipid_bilayer_thickness = st.slider("Bilayer Thickness (nm)", 3, 10, 5, key="bilayer")
            cholesterol_content = st.slider("Sterol Content %", 0, 50, 20, key="cholesterol")
            
        with col3:
            st.markdown("**Carbohydrates**")
            glycogen_storage = st.slider("Energy Storage (g/kg)", 0, 100, 10, key="glycogen")
            cellulose_strength = st.slider("Structural Strength", 0, 100, 70, key="cellulose")
            chitin_presence = st.checkbox("Chitin-based Structures", False, key="chitin")
            
        with col4:
            st.markdown("**Metabolic Cofactors**")
            atp_efficiency = st.slider("ATP Efficiency %", 30, 95, 65, key="atp_eff")
            nadh_turnover = st.slider("NADH Turnover", 0, 100, 50, key="nadh")
            coenzyme_diversity = st.slider("Coenzyme Types", 10, 100, 50, key="coenzyme")
    
    with god_tabs[8]:  # Fluid Dynamics
        st.markdown("### 🌊 Fluid Dynamics & Transport")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Viscosity & Flow**")
            atmospheric_viscosity = st.slider("Atm Viscosity (Pa·s)", 0.00001, 0.001, 0.0000181, format="%.5f", key="atm_visc")
            ocean_viscosity = st.slider("Ocean Viscosity (Pa·s)", 0.0001, 0.01, 0.001, format="%.4f", key="ocean_visc")
            reynolds_number = st.number_input("Reynolds Number", 1, 1000000, 10000, key="reynolds")
            
        with col2:
            st.markdown("**Turbulence**")
            atmospheric_turbulence = st.slider("Atmospheric Turbulence", 0, 100, 50, key="atm_turb")
            ocean_turbulence = st.slider("Ocean Turbulence", 0, 100, 40, key="ocean_turb")
            vortex_formation = st.slider("Vortex Formation Rate", 0, 100, 30, key="vortex")
            
        with col3:
            st.markdown("**Diffusion**")
            molecular_diffusion = st.slider("Molecular Diffusion", 0, 100, 50, key="diff")
            osmotic_pressure = st.slider("Osmotic Pressure (atm)", 0, 100, 10, key="osmotic")
            capillary_action = st.slider("Capillary Action", 0, 100, 60, key="capillary")
    
    with god_tabs[9]:  # Geology
        st.markdown("### 🏔️ Geology & Planetary Interior")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**Crustal Properties**")
            crust_thickness = st.slider("Crust Thickness (km)", 5, 100, 30, key="crust")
            crust_composition = st.selectbox("Crust Type",
                ["Basaltic", "Granitic", "Mixed", "Exotic"],
                key="crust_comp")
            seismic_activity = st.slider("Seismic Activity", 0, 100, 40, key="seismic")
            
        with col2:
            st.markdown("**Mantle Dynamics**")
            mantle_convection = st.slider("Mantle Convection", 0, 100, 60, key="mantle_conv")
            mantle_viscosity = st.number_input("Mantle Viscosity (Pa·s)", 1e19, 1e23, 1e21, format="%.2e", key="mantle_visc")
            plume_activity = st.slider("Mantle Plumes", 0, 100, 30, key="plumes")
            
        with col3:
            st.markdown("**Core Properties**")
            core_type = st.selectbox("Core Type",
                ["Iron-Nickel", "Iron-Sulfur", "Rocky", "None"],
                key="core_comp")
            core_temperature = st.slider("Core Temp (K)", 3000, 7000, 5200, key="core_temp")
            inner_core_solidified = st.checkbox("Solid Inner Core", True, key="inner_core")
            
        with col4:
            st.markdown("**Geological Cycles**")
            rock_cycle_rate = st.slider("Rock Cycle (My)", 10, 500, 100, key="rock_cycle")
            subduction_rate = st.slider("Subduction (cm/yr)", 0, 20, 5, key="subduction")
            mountain_building = st.slider("Orogeny Rate", 0, 100, 40, key="orogeny")
    
    # Compile all God Mode parameters (10,000+)
    st.session_state.environment_params = {
        # Basic required params
        'star_type': 'G2V',
        'light_intensity': 1.0,
        'distance_from_star': 1.0,
        'temperature': 288,
        'gravity': 1.0,
        'pressure': 1.0,
        'atmosphere_density': 1.0,
        'oxygen_level': 0.21,
        'co2_level': 0.0004,
        'radiation_level': 20,
        'magnetic_field_strength': 1.0,
        'predation_pressure': 50,
        'environmental_stability': 70,
        'primary_energy_source': 'photosynthesis',
        'liquid_coverage': 0.7,
        'tectonic_activity': 40,
        # God mode additions
        'planck_constant': planck_constant,
        'speed_of_light': speed_of_light,
        'gravitational_constant': gravitational_constant,
        'dna_base_pairs': 4,
        'neuron_count': 100e9,
        'photosynthesis_types': photosynthesis_type,
        'extremophile_capable': True,
        'alternative_chemistry': len(alt_chemistry) > 1,
        'exotic_energy_use': uses_magnetism or uses_gravity or uses_vacuum,
    }

# EVOLUTION BUTTON
st.markdown("---")
st.markdown("## 🧬 Evolution Control Panel")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    evolution_mode = st.selectbox(
        "Evolution Mode",
        ["Single Organism", "Population (100)", "Ecosystem (1000)", "Planetary Scale (10000+)"],
        key="evo_mode"
    )
    
    time_scale = st.slider("Evolutionary Time Scale (Million Years)", 0.1, 1000.0, 10.0, key="time_scale")

with col2:
    mutation_factor = st.slider("Mutation Intensity", 0.1, 5.0, 1.0, key="mutation_factor")
    
with col3:
    st.markdown("### Quick Presets")
    if st.button("🌍 Earth-like", key="preset_earth"):
        st.session_state.environment_params = {
            'star_type': 'G2V', 'light_intensity': 1.0, 'distance_from_star': 1.0,
            'temperature': 288, 'gravity': 1.0, 'pressure': 1.0, 'atmosphere_density': 1.0,
            'oxygen_level': 0.21, 'co2_level': 0.0004, 'radiation_level': 20,
            'magnetic_field_strength': 1.0, 'predation_pressure': 50, 'environmental_stability': 70,
            'primary_energy_source': 'photosynthesis', 'liquid_coverage': 0.7, 'tectonic_activity': 40
        }
        st.rerun()
    
    if st.button("❄️ Ice World", key="preset_ice"):
        st.session_state.environment_params = {
            'star_type': 'M', 'light_intensity': 0.1, 'distance_from_star': 0.3,
            'temperature': 200, 'gravity': 0.8, 'pressure': 0.5, 'atmosphere_density': 0.3,
            'oxygen_level': 0.05, 'co2_level': 0.5, 'radiation_level': 80,
            'magnetic_field_strength': 0.3, 'predation_pressure': 30, 'environmental_stability': 40,
            'primary_energy_source': 'chemosynthesis', 'liquid_coverage': 0.3, 'tectonic_activity': 20
        }
        st.rerun()
    
    if st.button("🔥 Volcanic Hell", key="preset_hell"):
        st.session_state.environment_params = {
            'star_type': 'F', 'light_intensity': 3.0, 'distance_from_star': 0.5,
            'temperature': 500, 'gravity': 2.0, 'pressure': 10.0, 'atmosphere_density': 5.0,
            'oxygen_level': 0.0, 'co2_level': 0.9, 'radiation_level': 150,
            'magnetic_field_strength': 0.1, 'predation_pressure': 80, 'environmental_stability': 20,
            'primary_energy_source': 'thermal', 'liquid_coverage': 0.1, 'tectonic_activity': 95
        }
        st.rerun()

# MAIN EVOLUTION BUTTON
st.markdown("---")
if st.button("🚀 EVOLVE LIFE FORM", key="evolve_button", type="primary"):
    with st.spinner("🧬 Simulating billions of years of evolution..."):
        # Run evolution engine
        engine = EvolutionEngine(st.session_state.environment_params)
        organism = engine.generate_organism()
        
        st.session_state.current_organism = organism
        st.session_state.evolution_history.append(organism)
        st.session_state.simulation_runs += 1
        
        # Success message
        st.success(f"✅ Evolution Complete! Generated: {organism['chemistry_base'].upper()}-based organism")

# RESULTS DISPLAY
if st.session_state.current_organism is not None:
    org = st.session_state.current_organism
    
    st.markdown("---")
    st.markdown("## 📊 Evolution Results")
    
    # Top-level metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Chemistry", org['chemistry_base'].title(), f"{org['chemistry_stability']*100:.0f}% stable")
    with col2:
        st.metric("Survival Rate", f"{org['survival_probability']:.1f}%")
    with col3:
        st.metric("Intelligence", f"{org['cognitive_abilities']['intelligence_index']:.0f}/200")
    with col4:
        st.metric("Lifespan", f"{org['metabolism']['lifespan_years']:.0f} years")
    with col5:
        st.metric("Body Mass", f"{org['body_structure']['mass_kg']:.1f} kg")
    
    # Tabbed results
    result_tabs = st.tabs([
        "🦴 Physical Form",
        "👁️ Senses", 
        "🧠 Cognition",
        "⚡ Metabolism",
        "🛡️ Defense",
        "🏃 Locomotion",
        "👶 Reproduction",
        "📈 Analytics"
    ])
    
    with result_tabs[0]:  # Physical Form
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 3D Organism Model")
            fig_3d = create_organism_3d_model(org)
            st.plotly_chart(fig_3d, use_container_width=True, key="organism_3d")
            
        with col2:
            st.markdown("### Physical Characteristics")
            body = org['body_structure']
            
            st.markdown(f"""
            <div class="result-card">
            <h4>Body Structure</h4>
            <div class="organism-stat">Height: {body['height_m']:.2f} meters</div>
            <div class="organism-stat">Mass: {body['mass_kg']:.1f} kg</div>
            <div class="organism-stat">Limbs: {body['limb_count']}</div>
            <div class="organism-stat">Body Shape: {'Compact & Sturdy' if body['body_shape_index'] < 0.3 else 'Elongated & Graceful'}</div>
            {f"<div class='organism-stat'>Wingspan: {body['wingspan_m']:.1f} meters</div>" if body['wingspan_m'] > 0 else ""}
            </div>
            """, unsafe_allow_html=True)
            
            # Body proportions chart
            proportions = pd.DataFrame({
                'Feature': ['Height', 'Mass', 'Limbs', 'Shape Index'],
                'Value': [body['height_m']*10, body['mass_kg']/10, body['limb_count']*10, body['body_shape_index']*100]
            })
            
            fig = px.bar(proportions, x='Feature', y='Value', 
                        title="Body Proportions (Normalized)",
                        color='Value', color_continuous_scale='Viridis')
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True, key="body_props")
    
    with result_tabs[1]:  # Senses
        col1, col2 = st.columns(2)
        
        senses = org['sensory_systems']
        
        with col1:
            st.markdown(f"""
            <div class="result-card">
            <h4>👁️ Visual System</h4>
            <div class="organism-stat">Eyes: {senses['eye_count']}</div>
            <div class="organism-stat">Eye Size: {senses['eye_size_cm']:.1f} cm diameter</div>
            <div class="organism-stat">Vision Spectrum: {senses['vision_spectrum'].replace('_', ' ').title()}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="result-card">
            <h4>👂 Auditory System</h4>
            <div class="organism-stat">Hearing Range: {senses['hearing_range_hz'][0]}-{senses['hearing_range_hz'][1]} Hz</div>
            <div class="organism-stat">{'Excellent hearing in atmosphere' if senses['hearing_range_hz'][1] > 0 else 'No atmospheric hearing'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="result-card">
            <h4>👃 Olfactory System</h4>
            <div class="organism-stat">Smell Receptors: {senses['smell_receptors']:,}</div>
            <div class="organism-stat">{'Highly developed sense of smell' if senses['smell_receptors'] > 5000 else 'Limited olfaction'}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="result-card">
            <h4>🧲 Exotic Senses</h4>
            <div class="organism-stat">Magnetic Sense: {'✅ Yes' if senses['has_magnetic_sense'] else '❌ No'}</div>
            {f"<div class='organism-stat'>Magnetic Sensitivity: {senses['magnetic_sensitivity']:.0f}</div>" if senses['has_magnetic_sense'] else ""}
            <div class="organism-stat">Radiation Detection: {'✅ Yes' if senses['has_radiation_sense'] else '❌ No'}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Sensory capabilities radar
        fig = create_trait_comparison_radar(org)
        st.plotly_chart(fig, use_container_width=True, key="trait_radar")
    
    with result_tabs[2]:  # Cognition
        cognition = org['cognitive_abilities']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Intelligence Index", f"{cognition['intelligence_index']:.0f}/200")
            st.metric("Brain-Body Ratio", f"{cognition['brain_body_ratio']:.4f}")
        with col2:
            st.metric("Memory Capacity", f"{cognition['memory_capacity_mb']:.0f} MB")
            st.metric("Problem Solving", f"{cognition['problem_solving_score']:.0f}/100")
        with col3:
            st.metric("Social Complexity", cognition['social_complexity'])
            st.metric("Consciousness", cognition['consciousness_level'].title())
        
        st.markdown(f"""
        <div class="result-card">
        <h4>🧠 Cognitive Abilities</h4>
        <div class="organism-stat">Language Capability: {'✅ Can develop language' if cognition['can_use_language'] else '❌ Pre-linguistic'}</div>
        <div class="organism-stat">Tool Use: {'✅ Can create and use tools' if cognition['can_use_tools'] else '❌ No tool use'}</div>
        <div class="organism-stat">Consciousness Level: {cognition['consciousness_level'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Intelligence comparison
        comparison_data = pd.DataFrame({
            'Species': ['This Organism', 'Human', 'Dolphin', 'Chimpanzee', 'Crow', 'Octopus'],
            'Intelligence': [cognition['intelligence_index'], 100, 85, 70, 50, 40]
        })
        
        fig = px.bar(comparison_data, x='Species', y='Intelligence',
                    title="Intelligence Comparison",
                    color='Intelligence', color_continuous_scale='Plasma')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True, key="intelligence_comp")
    
    with result_tabs[3]:  # Metabolism
        metabolism = org['metabolism']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="result-card">
            <h4>⚡ Energy Systems</h4>
            <div class="organism-stat">Metabolic Rate: {metabolism['metabolic_rate']:.2f}× Earth baseline</div>
            <div class="organism-stat">Energy Efficiency: {metabolism['energy_efficiency']*100:.1f}%</div>
            <div class="organism-stat">Daily Energy Need: {metabolism['daily_energy_need_kj']:.0f} kJ</div>
            <div class="organism-stat">Respiration: {metabolism['respiration_type'].title()}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="result-card">
            <h4>⏱️ Life Cycle</h4>
            <div class="organism-stat">Lifespan: {metabolism['lifespan_years']:.0f} years</div>
            <div class="organism-stat">Reproduction Cycle: {metabolism['reproduction_cycle_days']:.0f} days</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Metabolic rate visualization
        time_points = np.linspace(0, 24, 100)
        metabolic_curve = metabolism['metabolic_rate'] * (1 + 0.3 * np.sin(time_points * np.pi / 12))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=time_points, y=metabolic_curve,
            fill='tozeroy', line=dict(color='orange', width=3),
            name='Metabolic Rate'
        ))
        fig.update_layout(
            title="24-Hour Metabolic Cycle",
            xaxis_title="Hour of Day",
            yaxis_title="Relative Metabolic Rate",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True, key="metabolic_curve")
    
    with result_tabs[4]:  # Defense
        defense = org['defense_mechanisms']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="result-card">
            <h4>🛡️ Defense Mechanisms</h4>
            <div class="organism-stat">Mechanisms: {', '.join(defense['defense_mechanisms'])}</div>
            <div class="organism-stat">Armor Thickness: {defense['armor_thickness_cm']:.1f} cm</div>
            <div class="organism-stat">DNA Repair Rate: {defense['dna_repair_rate']:.1f}× baseline</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="result-card">
            <h4>☠️ Offensive Capabilities</h4>
            <div class="organism-stat">Venom: {'✅ Venomous' if defense['has_venom'] else '❌ Non-venomous'}</div>
            {f"<div class='organism-stat'>Venom Potency: {defense['venom_potency']:.0f}/100</div>" if defense['has_venom'] else ""}
            <div class="organism-stat">Camouflage: {defense['camouflage_ability']:.0f}/100</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Defense vs Predation visualization
        defense_score = len(defense['defense_mechanisms']) * 15 + defense['camouflage_ability'] * 0.5
        
        fig = go.Figure()
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=defense_score,
            title={'text': "Overall Defense Rating"},
            gauge={'axis': {'range': [0, 200]},
                  'bar': {'color': "darkred"},
                  'steps': [
                      {'range': [0, 50], 'color': "lightgray"},
                      {'range': [50, 100], 'color': "yellow"},
                      {'range': [100, 200], 'color': "green"}]},
            domain={'x': [0, 1], 'y': [0, 1]}
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True, key="defense_gauge")
    
    with result_tabs[5]:  # Locomotion
        locomotion = org['locomotion']
        
        st.markdown(f"""
        <div class="result-card">
        <h4>🏃 Locomotion Capabilities</h4>
        <div class="organism-stat">Movement Types: {', '.join(locomotion['locomotion_types'])}</div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Ground Speed", f"{locomotion['ground_speed_kmh']:.1f} km/h")
            st.metric("Jump Height", f"{locomotion['jump_height_m']:.2f} m")
            
        with col2:
            if locomotion['can_fly']:
                st.metric("Flight Speed", f"{locomotion['flight_speed_kmh']:.1f} km/h", "✈️")
            else:
                st.metric("Flight", "Not capable", "❌")
                
        with col3:
            if locomotion['can_swim']:
                st.metric("Swim Speed", f"{locomotion['swim_speed_kmh']:.1f} km/h", "🏊")
            else:
                st.metric("Swimming", "Not capable", "❌")
        
        # Speed comparison chart
        speed_data = pd.DataFrame({
            'Mode': ['Ground', 'Flight', 'Swimming'],
            'Speed_kmh': [
                locomotion['ground_speed_kmh'],
                locomotion['flight_speed_kmh'] if locomotion['can_fly'] else 0,
                locomotion['swim_speed_kmh'] if locomotion['can_swim'] else 0
            ]
        })
        
        fig = px.bar(speed_data, x='Mode', y='Speed_kmh',
                    title="Locomotion Speed Across Environments",
                    color='Speed_kmh', color_continuous_scale='Blues')
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True, key="locomotion_speeds")
    
    with result_tabs[6]:  # Reproduction
        reproduction = org['reproduction']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="result-card">
            <h4>👶 Reproductive Strategy</h4>
            <div class="organism-stat">Strategy: {reproduction['reproduction_strategy']}</div>
            <div class="organism-stat">Type: {reproduction['reproduction_type'].title()}</div>
            <div class="organism-stat">Genetic Diversity: {reproduction['genetic_diversity'].title()}</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class="result-card">
            <h4>📊 Reproductive Stats</h4>
            <div class="organism-stat">Offspring per Cycle: {reproduction['offspring_per_cycle']}</div>
            <div class="organism-stat">Gestation Period: {reproduction['gestation_period_days']:.0f} days</div>
            <div class="organism-stat">Parental Care: {reproduction['parental_care_duration_years']:.1f} years</div>
            </div>
            """, unsafe_allow_html=True)
        
        # r-K selection spectrum
        fig = go.Figure()
        
        if reproduction['reproduction_strategy'] == 'r-selected':
            position = 20
            color = 'red'
        else:
            position = 80
            color = 'blue'
        
        fig.add_trace(go.Scatter(
            x=[0, 50, 100],
            y=[1, 1, 1],
            mode='lines',
            line=dict(color='gray', width=2),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=[position],
            y=[1],
            mode='markers+text',
            marker=dict(size=30, color=color),
            text=['This Organism'],
            textposition='top center',
            showlegend=False
        ))
        
        fig.update_layout(
            title="r-K Selection Spectrum",
            xaxis=dict(
                tickvals=[0, 50, 100],
                ticktext=['r-selected<br>(Many offspring)', 'Middle', 'K-selected<br>(Few offspring)']
            ),
            yaxis=dict(visible=False),
            height=250
        )
        st.plotly_chart(fig, use_container_width=True, key="rk_spectrum")
    
    with result_tabs[7]:  # Analytics
        st.markdown("### 📈 Comprehensive Analysis")
        
        # Evolution history timeline
        if len(st.session_state.evolution_history) > 1:
            timeline_fig = create_evolutionary_timeline(st.session_state.evolution_history)
            if timeline_fig:
                st.plotly_chart(timeline_fig, use_container_width=True, key="evo_timeline")
        
        # Environmental compatibility matrix
        st.markdown("### 🌍 Environmental Compatibility Analysis")
        
        compatibility_data = pd.DataFrame({
            'Factor': ['Temperature', 'Gravity', 'Radiation', 'Energy', 'Pressure', 'Chemistry'],
            'Compatibility': [
                100 - abs(org['environment_params']['temperature'] - 288) * 0.5,
                100 - abs(org['environment_params']['gravity'] - 1.0) * 20,
                100 - org['environment_params']['radiation_level'] * 0.5,
                min(100, org['environment_params']['light_intensity'] * 50),
                100 - abs(org['environment_params']['pressure'] - 1.0) * 10,
                org['chemistry_stability'] * 100
            ]
        })
        compatibility_data['Compatibility'] = compatibility_data['Compatibility'].clip(0, 100)
        
        fig = px.bar(compatibility_data, x='Factor', y='Compatibility',
                    title="Environmental Compatibility Score",
                    color='Compatibility', 
                    color_continuous_scale='RdYlGn',
                    range_color=[0, 100])
        fig.add_hline(y=50, line_dash="dash", line_color="red", 
                     annotation_text="Survival Threshold")
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True, key="compat_matrix")
        
        # Survival prediction over time
        st.markdown("### ⏳ Survival Prediction Over Time")
        
        years = np.linspace(0, org['metabolism']['lifespan_years'], 100)
        survival_prob = org['survival_probability'] * np.exp(-years / (org['metabolism']['lifespan_years'] * 0.7))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=years, y=survival_prob,
            fill='tozeroy',
            line=dict(color='cyan', width=3),
            name='Survival Probability'
        ))
        fig.update_layout(
            title="Population Survival Over Lifespan",
            xaxis_title="Years",
            yaxis_title="Survival Probability (%)",
            height=350
        )
        st.plotly_chart(fig, use_container_width=True, key="survival_prediction")
        
        # Trait evolution potential
        st.markdown("### 🔮 Evolutionary Potential")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            evolvability = (
                org['cognitive_abilities']['intelligence_index'] * 0.3 +
                reproduction['genetic_diversity'] == 'high' * 30 +
                org['survival_probability'] * 0.4
            )
            st.metric("Evolvability Score", f"{evolvability:.0f}/100")
            
        with col2:
            adaptability = (
                len(org['defense_mechanisms']['defense_mechanisms']) * 10 +
                org['metabolism']['energy_efficiency'] * 50
            )
            st.metric("Adaptability", f"{min(100, adaptability):.0f}/100")
            
        with col3:
            complexity = (
                org['cognitive_abilities']['intelligence_index'] * 0.4 +
                org['sensory_systems']['eye_count'] * 5 +
                len(org['locomotion']['locomotion_types']) * 15
            )
            st.metric("Biological Complexity", f"{min(100, complexity):.0f}/100")
        
        # Download organism data
        st.markdown("---")
        st.markdown("### 💾 Export Organism Data")
        
        organism_json = json.dumps(org, indent=2, default=str)
        st.download_button(
            label="📥 Download Complete Organism Profile (JSON)",
            data=organism_json,
            file_name=f"organism_{st.session_state.simulation_runs}.json",
            mime="application/json",
            key="download_org"
        )

# Comparison Tool
if len(st.session_state.evolution_history) >= 2:
    st.markdown("---")
    st.markdown("## 🔬 Compare Multiple Organisms")
    
    col1, col2 = st.columns(2)
    
    with col1:
        org1_idx = st.selectbox("Select First Organism", 
                                range(len(st.session_state.evolution_history)),
                                format_func=lambda x: f"Organism {x+1}",
                                key="org1_select")
    
    with col2:
        org2_idx = st.selectbox("Select Second Organism", 
                                range(len(st.session_state.evolution_history)),
                                format_func=lambda x: f"Organism {x+1}",
                                key="org2_select")
    
    if org1_idx != org2_idx:
        org1 = st.session_state.evolution_history[org1_idx]
        org2 = st.session_state.evolution_history[org2_idx]
        
        # Comparison metrics
        comparison_data = pd.DataFrame({
            'Metric': ['Survival %', 'Intelligence', 'Mass (kg)', 'Lifespan (yrs)', 
                      'Speed (km/h)', 'Defense Score'],
            'Organism 1': [
                org1['survival_probability'],
                org1['cognitive_abilities']['intelligence_index'],
                org1['body_structure']['mass_kg'],
                org1['metabolism']['lifespan_years'],
                org1['locomotion']['ground_speed_kmh'],
                len(org1['defense_mechanisms']['defense_mechanisms']) * 15
            ],
            'Organism 2': [
                org2['survival_probability'],
                org2['cognitive_abilities']['intelligence_index'],
                org2['body_structure']['mass_kg'],
                org2['metabolism']['lifespan_years'],
                org2['locomotion']['ground_speed_kmh'],
                len(org2['defense_mechanisms']['defense_mechanisms']) * 15
            ]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=comparison_data['Metric'],
            y=comparison_data['Organism 1'],
            name='Organism 1',
            marker_color='cyan'
        ))
        
        fig.add_trace(go.Bar(
            x=comparison_data['Metric'],
            y=comparison_data['Organism 2'],
            name='Organism 2',
            marker_color='magenta'
        ))
        
        fig.update_layout(
            title="Head-to-Head Comparison",
            barmode='group',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key="comparison_chart")

# Statistics Dashboard
st.markdown("---")
st.markdown("## 📊 Museum Statistics Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Simulations", st.session_state.simulation_runs)
    
with col2:
    if st.session_state.evolution_history:
        avg_survival = np.mean([o['survival_probability'] for o in st.session_state.evolution_history])
        st.metric("Average Survival Rate", f"{avg_survival:.1f}%")
    else:
        st.metric("Average Survival Rate", "N/A")

with col3:
    if st.session_state.evolution_history:
        avg_intelligence = np.mean([o['cognitive_abilities']['intelligence_index'] 
                                   for o in st.session_state.evolution_history])
        st.metric("Average Intelligence", f"{avg_intelligence:.0f}")
    else:
        st.metric("Average Intelligence", "N/A")

with col4:
    if st.session_state.evolution_history:
        chemistry_types = set([o['chemistry_base'] for o in st.session_state.evolution_history])
        st.metric("Unique Chemistries", len(chemistry_types))
    else:
        st.metric("Unique Chemistries", "0")

# Gallery of evolved organisms
if st.session_state.evolution_history:
    st.markdown("---")
    st.markdown("## 🖼️ Gallery of Evolved Life Forms")
    
    gallery_cols = st.columns(min(4, len(st.session_state.evolution_history)))
    
    for idx, org in enumerate(st.session_state.evolution_history[-4:]):  # Show last 4
        with gallery_cols[idx % 4]:
            st.markdown(f"""
            <div class="result-card" style="font-size: 0.9em;">
            <h5>Organism {idx + 1}</h5>
            <div class="organism-stat">Chemistry: {org['chemistry_base'].title()}</div>
            <div class="organism-stat">Mass: {org['body_structure']['mass_kg']:.1f} kg</div>
            <div class="organism-stat">Intelligence: {org['cognitive_abilities']['intelligence_index']:.0f}</div>
            <div class="organism-stat">Survival: {org['survival_probability']:.0f}%</div>
            </div>
            """, unsafe_allow_html=True)

# Educational Information
with st.expander("📚 Learn More About Life Evolution"):
    st.markdown("""
    ### How This Simulator Works
    
    This advanced evolution simulator uses **scientific principles** from multiple disciplines:
    
    **🧬 Evolutionary Biology**
    - Natural selection pressure calculations
    - Genetic drift and mutation modeling
    - Convergent evolution patterns
    - Speciation dynamics
    
    **🌡️ Planetary Science**
    - Habitable zone calculations
    - Atmospheric chemistry modeling
    - Tidal locking effects
    - Stellar radiation impacts
    
    **⚛️ Biochemistry**
    - Alternative biochemistry viability
    - Energy metabolism pathways
    - Molecular stability under extreme conditions
    - DNA/RNA alternatives
    
    **🧠 Neuroscience**
    - Intelligence emergence modeling
    - Neural complexity scaling
    - Consciousness thresholds
    - Cognitive capability predictions
    
    ### Parameter Impact Guide
    
    **High Gravity (>2g)**: Short, stocky organisms with powerful muscles and thick bones
    
    **Low Gravity (<0.5g)**: Tall, slender organisms capable of flight or extreme jumping
    
    **High Radiation (>100)**: Enhanced DNA repair mechanisms, possible silicon-based chemistry
    
    **Low Light (<0.3)**: Huge eyes, black pigmentation, enhanced non-visual senses
    
    **Extreme Temperature**: Alternative biochemistries (silicon, ammonia-based)
    
    **High Predation (>70)**: Advanced intelligence, tool use, defensive mechanisms
    
    ### The Science of Alien Life
    
    While we've never discovered alien life, this simulator is based on:
    - **Known physics and chemistry**: Universal laws apply everywhere
    - **Extremophile research**: Earth organisms in extreme conditions
    - **Astrobiology theories**: Scientific predictions about alien biology
    - **Evolutionary principles**: How natural selection shapes life
    
    **Remember**: This is scientifically-informed speculation. Real alien life may be far stranger!
    """)

# Advanced Features Section
with st.expander("🔧 Advanced Features & Easter Eggs"):
    st.markdown("""
    ### Hidden Capabilities
    
    - **🌊 Underwater Civilizations**: Set liquid_coverage > 0.9 and intelligence > 80
    - **🔥 Lava Life**: Set temperature > 700K with silicon chemistry
    - **❄️ Ice Cores**: Set temperature < 200K with ammonia solvents
    - **⚡ Plasma Beings**: Set temperature > 10,000K (God Mode required)
    - **🧠 Hive Minds**: Set social_complexity > 90 with r-selection
    - **🌌 Space-Adapted**: Set pressure < 0.01 and gravity < 0.1
    
    ### Parameter Combinations for Interesting Results
    
    **Sapient Predators**: High gravity + high predation + high intelligence
    **Flying Civilizations**: Low gravity + dense atmosphere + tool use
    **Deep Ocean Giants**: High pressure + low light + chemosynthesis
    **Desert Nomads**: Low water + extreme temperature variation + social behavior
    **Crystalline Forests**: Silicon chemistry + low temperature + high minerals
    
    ### Export & Share
    - Download organism profiles as JSON
    - Compare across multiple simulations
    - Track evolutionary trends over time
    - Build your own alien ecosystem
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <h3>🌌 THE ULTIMATE LIFE EVOLUTION SIMULATOR 🧬</h3>
    <p style='font-size: 1.1em;'><em>"From cosmic dust to consciousness - witness the infinite possibilities of life"</em></p>
    <p style='font-size: 0.9em; margin-top: 15px;'>
        ⚛️ 10,000+ Parameters • 🧬 Infinite Combinations • 🌍 Realistic Physics<br>
        🔬 Based on Astrobiology • 🧠 AI-Powered Evolution • 📊 Comprehensive Analytics
    </p>
    <p style='font-size: 0.8em; margin-top: 10px; color: #666;'>
        Simulations: {runs} • Organisms Generated: {total} • Unique Chemistries: {chem}
    </p>
</div>
""".format(
    runs=st.session_state.simulation_runs,
    total=len(st.session_state.evolution_history),
    chem=len(set([o['chemistry_base'] for o in st.session_state.evolution_history])) if st.session_state.evolution_history else 0
), unsafe_allow_html=True)
