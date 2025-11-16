import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import time
import graphviz

# Page config
st.set_page_config(
    page_title="Museum of Alien Life",
    page_icon="👽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set default plotly theme for dark mode
pio.templates.default = "plotly_dark"

# Custom CSS
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;700&display=swap');

    /* Core App Styling */
    body {
        font-family: 'Exo 2', sans-serif;
    }

    /* Main container background */
    .main > div {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='%232d3748' fill-opacity='0.4'%3E%3Cpath d='M0 38.59l2.83-2.83 1.41 1.41L1.41 40H0v-1.41zM0 1.4l2.83 2.83 1.41-1.41L1.41 0H0v1.41zM38.59 40l-2.83-2.83 1.41-1.41L40 38.59V40h-1.41zM40 1.41l-2.83 2.83-1.41-1.41L38.59 0H40v1.41zM20 18.6l2.83-2.83 1.41 1.41L21.41 20l2.83 2.83-1.41 1.41L20 21.41l-2.83 2.83-1.41-1.41L18.59 20l-2.83-2.83 1.41-1.41L20 18.59z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
        background-color: #0D1117; /* Near-black */
    }

    /* Sidebar styling */
    .st-emotion-cache-16txtl3 {
        background-color: rgba(13, 17, 23, 0.8);
        backdrop-filter: blur(5px);
    }

    /* Main Header */
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        font-family: 'Exo 2', sans-serif;
        background: linear-gradient(45deg, #00BCD4 0%, #FFD700 100%); /* Cyan to Gold */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
    }

    /* Wing Header */
    .wing-header {
        font-size: 2rem;
        font-family: 'Exo 2', sans-serif;
        color: #00BCD4; /* Accent Cyan */
        border-bottom: 3px solid #00BCD4;
        padding-bottom: 10px;
        margin-top: 20px;
    }

    /* Glassmorphism Cards */
    .exhibit-card {
        background: rgba(45, 55, 72, 0.5); /* Semi-transparent dark blue-gray */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
        height: 100%; /* Make cards in a row equal height */
    }

    /* Glassmorphism Info Box */
    .info-box {
        background: rgba(45, 55, 72, 0.4); /* Semi-transparent dark blue-gray */
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #00BCD4; /* Accent Cyan */
        margin: 10px 0;
        color: #E2E8F0; /* Light gray text */
    }

    /* Improve tab styling for dark mode */
    .st-emotion-cache-1s44j7o button {
        background-color: transparent;
        color: #A0AEC0; /* Muted text for inactive tabs */
        border-radius: 8px 8px 0 0;
        border-bottom: 2px solid transparent;
    }
    .st-emotion-cache-1s44j7o button:hover {
        background-color: rgba(0, 188, 212, 0.1);
        color: #00BCD4;
    }
    .st-emotion-cache-1s44j7o button[aria-selected="true"] {
        color: #00BCD4; /* Active tab color */
        border-bottom: 2px solid #00BCD4;
    }

    /* General text color */
    .st-emotion-cache-1r4qj8v, .st-emotion-cache-1y4p8pa, .st-emotion-cache-1kyxreq {
        color: #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for lazy loading
if 'current_wing' not in st.session_state:
    st.session_state.current_wing = "Home"
if 'current_exhibit' not in st.session_state:
    st.session_state.current_exhibit = None
if 'evolution_run' not in st.session_state:
    st.session_state.evolution_run = False
if 'sim_selection_pressure' not in st.session_state:
    st.session_state.sim_selection_pressure = "Moderate"
if 'sim_env_stress' not in st.session_state:
    st.session_state.sim_env_stress = []


# Helper function to generate alien landscape
def generate_alien_landscape(color_scheme, gravity_level, star_type):
    """Generate procedural alien landscape visualization"""
    fig = go.Figure()
    
    # Generate terrain
    x = np.linspace(0, 100, 200)
    if gravity_level == "high":
        y = np.sin(x/5) * 2 + np.random.normal(0, 0.5, 200)  # Flat terrain
        plant_height = 3
    elif gravity_level == "low":
        y = np.sin(x/3) * 15 + np.random.normal(0, 2, 200)  # Mountainous
        plant_height = 25
    else:
        y = np.sin(x/4) * 8 + np.random.normal(0, 1, 200)
        plant_height = 10
    
    # Base terrain
    fig.add_trace(go.Scatter(
        x=x, y=y, fill='tozeroy',
        fillcolor=color_scheme['ground'],
        line=dict(color=color_scheme['ground'], width=2),
        name='Terrain',
        hoverinfo='skip'
    ))
    
    # Add alien plants
    for i in range(0, 100, 15):
        plant_x = i
        plant_base_y = np.interp(plant_x, x, y)
        fig.add_trace(go.Scatter(
            x=[plant_x, plant_x],
            y=[plant_base_y, plant_base_y + plant_height],
            mode='lines',
            line=dict(color=color_scheme['plant'], width=4),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Sky gradient effect
    fig.add_trace(go.Scatter(
        x=x, y=[max(y) + 30] * len(x),
        fill='tonexty',
        fillcolor=color_scheme['sky'],
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        title=f"Alien Landscape: {star_type} Star System ({gravity_level.title()} Gravity)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        showlegend=False
    )
    
    return fig

# Helper function for 3D molecule visualization
def create_molecule_3d(molecule_type):
    """Create 3D molecular structure"""
    if molecule_type == "carbon":
        # Carbon chain
        atoms = pd.DataFrame({
            'x': [0, 1, 2, 3, 4],
            'y': [0, 0.5, 0, 0.5, 0],
            'z': [0, 0, 0, 0, 0],
            'atom': ['C', 'C', 'C', 'C', 'C'],
            'size': [20, 20, 20, 20, 20],
            'color': ['#A0AEC0', '#A0AEC0', '#A0AEC0', '#A0AEC0', '#A0AEC0']
        })
    else:  # silicon
        atoms = pd.DataFrame({
            'x': [0, 1, 2],
            'y': [0, 0, 0],
            'z': [0, 0, 0],
            'atom': ['Si', 'Si', 'Si'],
            'size': [25, 25, 25]
        })
        atoms['color'] = ['#63B3ED', '#63B3ED', '#63B3ED'] # Blue
    
    fig = go.Figure(data=[go.Scatter3d(
        x=atoms['x'],
        y=atoms['y'],
        z=atoms['z'],
        mode='markers+text',
        marker=dict(size=atoms['size'], color=atoms['color'], opacity=0.9),
        text=atoms['atom'],
        textposition="top center",
        textfont=dict(size=14, color='white')
    )])
    
    # Add bonds
    for i in range(len(atoms)-1):
        fig.add_trace(go.Scatter3d(
            x=[atoms.loc[i, 'x'], atoms.loc[i+1, 'x']],
            y=[atoms.loc[i, 'y'], atoms.loc[i+1, 'y']],
            z=[atoms.loc[i, 'z'], atoms.loc[i+1, 'z']],
            mode='lines',
            line=dict(color='rgba(255, 255, 255, 0.5)', width=5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        height=400,
        title=f"{molecule_type.title()}-Based Molecular Chain"
    )
    
    return fig

# Main header
st.markdown('<h1 class="main-header">The Museum of Universal Life</h1>', unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #A0AEC0;'>*Exploring Every Possible Form of Life in the Universe*</h3>", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/300x150/667eea/ffffff?text=Museum+of+Life", use_container_width=True)
    st.markdown("## 🎫 Navigation")
    
    wing_choice = st.radio(
        "Select Wing:",
        ["Home", "Wing 1: Life As We Know It", "Wing 2: Life As We Don't Know It", "Wing 3: Environmental Sculpting", "Tree of Universal Life"],
        key="wing_selector"
    )
    st.session_state.current_wing = wing_choice
    
    st.markdown("---")
    st.markdown("### 📊 Museum Stats")
    st.metric("Exhibits", "15+", "+3")
    st.metric("Life Forms Catalogued", "1M+", "+50K")
    st.metric("Planets Studied", "10,000+", "+127")

# HOME PAGE
if st.session_state.current_wing == "Home":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="exhibit-card">
            <h3>🧬 Wing 1</h3>
            <p>Life As We Know It</p>
            <small>Carbon-based biology & convergent evolution</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="exhibit-card">
            <h3>👾 Wing 2</h3>
            <p>Life As We Don't Know It</p>
            <small>Exotic biochemistry & extreme environments</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="exhibit-card">
            <h3>🌍 Wing 3</h3>
            <p>Environmental Sculpting</p>
            <small>How gravity & stars shape life</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Welcome visualization
    st.subheader("📈 Universal Distribution of Elements in Life")
    
    element_data = pd.DataFrame({
        'Element': ['Carbon', 'Hydrogen', 'Oxygen', 'Nitrogen', 'Phosphorus', 'Sulfur', 'Silicon', 'Other'],
        'Percentage': [18, 10, 65, 3, 1, 0.25, 0.01, 2.74],
        'Type': ['Essential', 'Essential', 'Essential', 'Essential', 'Essential', 'Essential', 'Alternative', 'Trace']
    })
    
    fig = px.sunburst(
        element_data,
        path=['Type', 'Element'],
        values='Percentage',
        color='Percentage',
        color_continuous_scale='Cividis',
        title='Elemental Composition in Known Life'
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True, key="home_sunburst")
    
    st.info("🎯 **Mission Statement**: This museum represents humanity's attempt to catalog every conceivable form of life, from the familiar carbon-based organisms of Earth to the exotic, theoretical beings that might exist in the harshest corners of our universe.")

# WING 1: LIFE AS WE KNOW IT
elif st.session_state.current_wing == "Wing 1: Life As We Know It":
    st.markdown('<h2 class="wing-header">🧬 Wing 1: Life As We Know It (The Carbon Gallery)</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Carbon Foundation", "Convergent Evolution", "DNA Alternatives"])
    
    with tab1:
        st.subheader("💎 The Carbon-Based Standard")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <h4>Why Carbon is Special</h4>
            <ul>
                <li>✅ Common throughout the universe</li>
                <li>✅ Forms four-way bonds</li>
                <li>✅ Creates long, stable chains</li>
                <li>✅ Enables huge complex molecules</li>
                <li>✅ Foundation of DNA & proteins</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Carbon properties comparison
            properties_df = pd.DataFrame({
                'Property': ['Bond Strength', 'Complexity', 'Stability', 'Versatility', 'Cosmic Abundance'],
                'Carbon': [95, 100, 90, 100, 85],
                'Silicon': [75, 60, 70, 70, 90]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=properties_df['Carbon'],
                theta=properties_df['Property'],
                fill='toself',
                name='Carbon',
                line_color='#48BB78' # Green
            ))
            fig.add_trace(go.Scatterpolar(
                r=properties_df['Silicon'],
                theta=properties_df['Property'],
                fill='toself',
                name='Silicon',
                line_color='#00BCD4' # Cyan
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                title="Carbon vs Silicon: Life-Enabling Properties",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True, key="carbon_radar")
        
        with col2:
            # 3D molecule visualization
            st.plotly_chart(create_molecule_3d("carbon"), use_container_width=True, key="carbon_molecule_3d")
            
            st.success("🔬 **Scientific Fact**: Over 1 million possible carbon-based alternatives to DNA have been identified by scientists!")
    
    with tab2:
        st.subheader("🔄 The Hall of Convergent Evolution")
        st.markdown("*Similar environments create similar solutions across the cosmos*")
        
        # Convergent evolution examples
        convergent_examples = pd.DataFrame({
            'Feature': ['Eyes', 'Flight', 'Echolocation', 'Bioluminescence', 'Venom', 'Camouflage'],
            'Times_Evolved_on_Earth': [40, 4, 4, 50, 100, 200],
            'Likelihood_on_Exoplanets': [95, 85, 70, 80, 90, 95]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=convergent_examples['Feature'],
            y=convergent_examples['Times_Evolved_on_Earth'],
            name='Times Evolved on Earth',
            marker_color='#00BCD4'
        ))
        fig.add_trace(go.Scatter(
            x=convergent_examples['Feature'],
            y=convergent_examples['Likelihood_on_Exoplanets'],
            name='Likelihood on Exoplanets (%)',
            yaxis='y2',
            mode='lines+markers',
            marker=dict(size=10, color='#FFD700'), # Gold
            line=dict(width=3)
        ))
        fig.update_layout(
            title="Convergent Evolution: Earth's Greatest Hits",
            yaxis=dict(title='Times Evolved'),
            yaxis2=dict(title='Exoplanet Likelihood (%)', overlaying='y', side='right'),
            height=450
        )
        st.plotly_chart(fig, use_container_width=True, key="convergent_bar")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Eye Evolution Events", "40+", "Independent origins")
        with col2:
            st.metric("Flight Evolution", "4×", "Insects, Birds, Bats, Pterosaurs")
        with col3:
            st.metric("Predicted Similarity", "70%", "On Earth-like planets")
    
    with tab3:
        st.subheader("🧬 DNA Alternatives Gallery")
        
        # DNA alternatives visualization
        dna_alts = pd.DataFrame({
            'Type': ['Standard DNA', 'XNA (Xeno)', 'PNA (Peptide)', 'TNA (Threose)', 'LNA (Locked)', 'GNA (Glycol)'],
            'Stability': [85, 95, 90, 88, 98, 80],
            'Complexity': [100, 85, 75, 70, 80, 65],
            'Temperature_Tolerance': [70, 95, 85, 75, 90, 85],
            'Discovered': [1953, 1990, 1991, 2000, 1998, 1992]
        })
        
        fig = px.scatter_3d(
            dna_alts,
            x='Stability',
            y='Complexity',
            z='Temperature_Tolerance',
            color='Type',
            size=[30]*len(dna_alts),
            title='3D Comparison of DNA Alternatives',
            labels={'Stability': 'Molecular Stability', 
                   'Complexity': 'Informational Complexity',
                   'Temperature_Tolerance': 'Temperature Range'}
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True, key="dna_scatter3d")
        
        st.warning("⚗️ These alternative nucleic acids could form the basis of life on planets with extreme conditions!")

# WING 2: LIFE AS WE DON'T KNOW IT
elif st.session_state.current_wing == "Wing 2: Life As We Don't Know It":
    st.markdown('<h2 class="wing-header">👾 Wing 2: Life As We Don\'t Know It (Exotic Biochemistry)</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Silicon Life", "Extreme Environments", "Theoretical Beings"])
    
    with tab1:
        st.subheader("🔷 The Silicon Contender")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <h4>Silicon-Based Life: The Alternative</h4>
            <p><strong>Advantages:</strong></p>
            <ul>
                <li>✅ Forms four-way bonds (like carbon)</li>
                <li>✅ Abundant in universe</li>
                <li>✅ Stable at high temperatures</li>
            </ul>
            <p><strong>Challenges:</strong></p>
            <ul>
                <li>❌ Weaker bonds than carbon</li>
                <li>❌ Forms solid rock with oxygen (SiO₂)</li>
                <li>❌ Requires oxygen-free environment</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Temperature range comparison
            temp_data = pd.DataFrame({
                'Temperature (K)': np.linspace(100, 600, 100),
                'Carbon_Viability': np.where(np.linspace(100, 600, 100) < 373, 
                                           100, 100 - (np.linspace(100, 600, 100) - 373) * 0.5),
                'Silicon_Viability': np.where(np.linspace(100, 600, 100) > 200,
                                            np.minimum(100, (np.linspace(100, 600, 100) - 200) * 0.3),
                                            0)
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=temp_data['Temperature (K)'],
                y=temp_data['Carbon_Viability'],
                fill='tozeroy',
                name='Carbon Life',
                line=dict(color='#48BB78') # Green
            ))
            fig.add_trace(go.Scatter(
                x=temp_data['Temperature (K)'],
                y=temp_data['Silicon_Viability'],
                fill='tozeroy',
                name='Silicon Life',
                line=dict(color='#00BCD4') # Cyan
            ))
            fig.update_layout(
                title='Temperature Viability Ranges',
                xaxis_title='Temperature (Kelvin)',
                yaxis_title='Life Viability (%)',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True, key="temp_viability")
        
        with col2:
            st.plotly_chart(create_molecule_3d("silicon"), use_container_width=True, key="silicon_molecule_3d")
            
            # Titan environment simulation
            st.markdown("#### 🪐 Titan: A Silicon Paradise?")
            titan_data = {
                'Property': ['Temperature', 'Pressure', 'Methane Lakes', 'Oxygen Level'],
                'Value': [-179, 1.5, 'Abundant', 'None'],
                'Silicon_Friendly': ['✅', '✅', '✅', '✅']
            }
            st.table(pd.DataFrame(titan_data))
            
            st.info("⏱️ Silicon-based life on Titan might have ultra-slow metabolisms with lifecycles lasting millions of years!")
    
    with tab2:
        st.subheader("🌋 Extreme Environment Exhibits")
        
        # Extreme environments comparison
        extreme_envs = pd.DataFrame({
            'Environment': ['Molten Rock', 'Neutron Star Surface', 'Plasma Clouds', 'Deep Ocean Vents', 'Acidic Lakes'],
            'Temperature (K)': [1500, 1e6, 10000, 600, 300],
            'Pressure (atm)': [1000, 1e20, 0.001, 300, 1],
            'Theoretical_Life': ['Silicate Organisms', 'Macronuclei Life', 'Plasma Crystals', 'Extremophiles', 'Acid-Lovers'],
            'Likelihood': [30, 5, 15, 95, 90]
        })
        
        # Log scale scatter plot
        fig = px.scatter(
            extreme_envs,
            x='Temperature (K)',
            y='Pressure (atm)',
            size='Likelihood',
            color='Theoretical_Life',
            hover_data=['Environment'],
            title='Extreme Environments Life Map',
            log_x=True,
            log_y=True,
            size_max=50
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True, key="extreme_scatter")
        
        # Detailed environment cards
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="exhibit-card">
            <h4>🌋 Molten Silicate Life</h4>
            <p><strong>Environment:</strong> Inside molten rock</p>
            <p><strong>Composition:</strong> Self-organizing silicate patterns</p>
            <p><strong>Metabolism:</strong> Thermochemical reactions</p>
            <p><strong>Likelihood:</strong> Low (30%)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="exhibit-card">
            <h4>⚡ Plasma Crystal Life</h4>
            <p><strong>Environment:</strong> Cosmic dust clouds</p>
            <p><strong>Composition:</strong> Self-organizing plasma</p>
            <p><strong>Metabolism:</strong> Electromagnetic interactions</p>
            <p><strong>Likelihood:</strong> Speculative (15%)</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.subheader("🌟 Theoretical Beings Gallery")
        
        # Neutron star life visualization
        st.markdown("#### ⚛️ Macronuclei Life on Neutron Stars")
        
        neutron_data = pd.DataFrame({
            'Particle_Density': np.logspace(15, 18, 50),
            'Life_Probability': 100 / (1 + np.exp(-(np.logspace(15, 18, 50) - 1e17) / 1e16))
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=neutron_data['Particle_Density'],
            y=neutron_data['Life_Probability'],
            fill='tozeroy',
            line=dict(color='#B794F4', width=3), # Purple
            name='Theoretical Viability'
        ))
        fig.update_layout(
            title='Macronuclei Life Formation Probability',
            xaxis_title='Particle Density (particles/cm³)',
            yaxis_title='Formation Probability (%)',
            xaxis_type='log',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key="neutron_prob")
        
        st.error("⚠️ **Warning**: This exhibit contains theoretical life forms that exist beyond our current understanding of physics!")
        
        # Comparison table
        theoretical_life = pd.DataFrame({
            'Type': ['Standard Biological', 'Silicon-Based', 'Plasma Crystal', 'Macronuclei', 'AI/Digital'],
            'Timescale': ['Years', 'Millions of Years', 'Milliseconds', 'Microseconds', 'Nanoseconds'],
            'Size': ['µm - m', 'mm - m', 'km', 'fm', 'Virtual'],
            'Detection': ['Easy', 'Moderate', 'Hard', 'Nearly Impossible', 'N/A']
        })
        st.dataframe(theoretical_life, use_container_width=True)

# WING 3: ENVIRONMENTAL SCULPTING
elif st.session_state.current_wing == "Wing 3: Environmental Sculpting":
    st.markdown('<h2 class="wing-header">🌍 Wing 3: Environmental Sculpting</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Gravity Effects", "Stellar Influence", "Alien Gardens"])
    
    with tab1:
        st.subheader("⚖️ The Gravity Gallery")
        
        # Gravity simulator
        gravity_level = st.select_slider(
            "Select Planetary Gravity",
            options=["Low (0.3g)", "Earth (1g)", "High (2g)", "Super-Earth (3g)"],
            value="Earth (1g)",
            key="gravity_slider"
        )
        
        # Parse gravity value
        g_value = {"Low (0.3g)": 0.3, "Earth (1g)": 1.0, "High (2g)": 2.0, "Super-Earth (3g)": 3.0}[gravity_level]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Body structure visualization
            body_proportions = pd.DataFrame({
                'Body_Part': ['Legs', 'Torso', 'Arms', 'Head'],
                'Thickness': [10 * g_value, 8 * g_value, 6 * g_value, 5 * g_value],
                'Strength_Required': [100 * g_value, 80 * g_value, 60 * g_value, 40 * g_value]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=body_proportions['Body_Part'],
                y=body_proportions['Thickness'],
                name='Bone Thickness',
                marker_color='#F56565' # Red
            ))
            fig.add_trace(go.Bar(
                x=body_proportions['Body_Part'],
                y=body_proportions['Strength_Required'],
                name='Muscle Mass Required',
                marker_color='#4299E1' # Blue
            ))
            fig.update_layout(
                title=f'Body Structure at {gravity_level}',
                barmode='group',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True, key="gravity_body_struct")
            
            # Creature statistics
            if g_value < 1:
                st.success("""
                **Low Gravity Adaptations:**
                - 📏 Slender, elongated bodies
                - 🦴 Lightweight skeletons
                - 🌿 Plants grow to towering heights
                - 🦅 Flight is easier
                """)
            else:
                st.warning("""
                **High Gravity Adaptations:**
                - 💪 Dense muscle mass
                - 🦴 Thick, robust bones
                - 🌱 Stunted plant life
                - 🐌 Slow, powerful movement
                """)
        
        with col2:
            # Plant height simulation
            plant_heights = pd.DataFrame({
                'Gravity': [0.3, 0.5, 1.0, 1.5, 2.0, 3.0],
                'Max_Plant_Height_m': [50, 30, 15, 10, 7, 3],
                'Animal_Jump_Height_m': [5, 3, 1.5, 0.8, 0.5, 0.2]
            })
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=plant_heights['Gravity'],
                y=plant_heights['Max_Plant_Height_m'],
                mode='lines+markers',
                name='Max Plant Height',
                line=dict(color='#48BB78', width=3), # Green
                marker=dict(size=10)
            ))
            fig.add_trace(go.Scatter(
                x=plant_heights['Gravity'],
                y=plant_heights['Animal_Jump_Height_m'],
                mode='lines+markers',
                name='Animal Jump Height',
                line=dict(color='#ED8936', width=3), # Orange
                marker=dict(size=10),
                yaxis='y2'
            ))
            fig.update_layout(
                title='Gravity Impact on Life Forms',
                xaxis_title='Gravity (g)',
                yaxis_title='Plant Height (m)',
                yaxis2=dict(title='Jump Height (m)', overlaying='y', side='right'),
                height=400
            )
            # Add current gravity marker
            fig.add_vline(x=g_value, line_dash="dash", line_color="#FFD700", 
                         annotation_text="Selected", annotation_position="top")
            st.plotly_chart(fig, use_container_width=True, key="gravity_impact")
    
    with tab2:
        st.subheader("⭐ Hall of Senses: Stellar Influence")
        
        # Star type selector
        star_type = st.selectbox(
            "Select Star Type",
            ["Red Dwarf", "Yellow Sun (Earth)", "Blue Giant"],
            key="star_selector"
        )
        
        # Star properties
        star_data = {
            "Red Dwarf": {"temp": 3000, "color": "#F56565", "brightness": 0.3},
            "Yellow Sun (Earth)": {"temp": 5778, "color": "#FFD700", "brightness": 1.0},
            "Blue Giant": {"temp": 15000, "color": "#4299E1", "brightness": 3.0}
        }
        
        current_star = star_data[star_type]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Temperature", f"{current_star['temp']} K")
        with col2:
            st.metric("Brightness", f"{current_star['brightness']:.1f}× Solar")
        with col3:
            eye_size = int(100 / current_star['brightness'])
            st.metric("Eye Size Needed", f"{eye_size}% larger")
        
        # Wavelength emission spectrum
        wavelengths = np.linspace(300, 800, 500)
        
        def planck_law(wavelength, temp):
            h = 6.626e-34
            c = 3.0e8
            k = 1.381e-23
            return (2*h*c**2 / wavelength**5) / (np.exp(h*c / (wavelength * k * temp)) - 1)
        
        intensity = planck_law(wavelengths * 1e-9, current_star['temp'])
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=wavelengths,
            y=intensity / np.max(intensity) * 100,
            fill='tozeroy',
            line=dict(color=current_star['color'], width=2),
            name=star_type
        ))
        fig.add_vrect(x0=380, x1=450, fillcolor="purple", opacity=0.1, annotation_text="Violet")
        fig.add_vrect(x0=450, x1=495, fillcolor="blue", opacity=0.1, annotation_text="Blue")
        fig.add_vrect(x0=495, x1=570, fillcolor="green", opacity=0.1, annotation_text="Green")
        fig.add_vrect(x0=570, x1=590, fillcolor="yellow", opacity=0.1, annotation_text="Yellow")
        fig.add_vrect(x0=590, x1=620, fillcolor="orange", opacity=0.1, annotation_text="Orange")
        fig.add_vrect(x0=620, x1=750, fillcolor="red", opacity=0.1, annotation_text="Red")
        
        fig.update_layout(
            title=f'Light Spectrum from {star_type}',
            xaxis_title='Wavelength (nm)',
            yaxis_title='Relative Intensity (%)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True, key="star_spectrum")
        
        # Sensory adaptations
        if star_type == "Red Dwarf":
            st.info("""
            🔴 **Red Dwarf Adaptations:**
            - 👁️ Massive eyes to capture dim light
            - 🖤 Black vegetation (absorbs all wavelengths)
            - 🌡️ Cold-adapted biology
            - 🦇 Enhanced non-visual senses
            """)
        elif star_type == "Blue Giant":
            st.info("""
            🔵 **Blue Giant Adaptations:**
            - 🕶️ UV-filtering eye structures
            - 🔴 Red vegetation (reflects blue light)
            - ☀️ Heat-resistant proteins
            - 🦎 Rapid mutations from UV exposure
            """)
        else:
            st.success("""
            🟡 **Yellow Sun (Earth-like):**
            - 👁️ Moderate-sized eyes
            - 🟢 Green vegetation (reflects green light)
            - 🌡️ Comfortable temperature range
            - 🌍 Balanced sensory systems
            """)
    
    with tab3:
        st.subheader("🌺 The Alien Garden")
        st.markdown("*How star color determines plant pigmentation*")
        
        # Garden visualization selector
        garden_type = st.radio(
            "View Garden Under:",
            ["Red Dwarf Star", "Yellow Sun (Earth)", "Blue Giant Star", "Purple Earth (Ancient)"],
            horizontal=True,
            key="garden_radio"
        )
        
        # Generate alien landscape
        color_schemes = {
            "Red Dwarf Star": {
                'ground': 'rgba(80, 60, 50, 0.8)',
                'plant': 'rgba(10, 10, 10, 0.9)',
                'sky': 'rgba(150, 50, 50, 0.3)'
            },
            "Yellow Sun (Earth)": {
                'ground': 'rgba(139, 90, 43, 0.8)',
                'plant': 'rgba(34, 139, 34, 0.9)',
                'sky': 'rgba(135, 206, 235, 0.3)'
            },
            "Blue Giant Star": {
                'ground': 'rgba(200, 180, 160, 0.8)',
                'plant': 'rgba(180, 50, 50, 0.9)',
                'sky': 'rgba(70, 130, 255, 0.3)'
            },
            "Purple Earth (Ancient)": {
                'ground': 'rgba(100, 80, 70, 0.8)',
                'plant': 'rgba(128, 0, 128, 0.9)',
                'sky': 'rgba(200, 150, 200, 0.3)'
            }
        }
        
        gravity_map = {
            "Red Dwarf Star": "low",
            "Yellow Sun (Earth)": "normal",
            "Blue Giant Star": "high",
            "Purple Earth (Ancient)": "normal"
        }
        
        landscape_fig = generate_alien_landscape(
            color_schemes[garden_type],
            gravity_map[garden_type],
            garden_type
        )
        st.plotly_chart(landscape_fig, use_container_width=True, key="alien_garden_viz")
        
        # Photosynthesis efficiency chart
        st.markdown("#### 🌿 Photosynthetic Efficiency by Star Type")
        
        photosynthesis_data = pd.DataFrame({
            'Star_Type': ['Red Dwarf', 'Yellow Sun', 'Blue Giant', 'Purple (Retinol)'],
            'Efficiency': [45, 85, 65, 55],
            'Pigment': ['Melanin-like', 'Chlorophyll', 'Phycoerythrin', 'Retinol'],
            'Color': ['Black', 'Green', 'Red', 'Purple']
        })
        
        fig = px.bar(
            photosynthesis_data,
            x='Star_Type',
            y='Efficiency',
            color='Color',
            color_discrete_map={'Black': '#4A5568', 'Green': '#48BB78', 'Red': '#F56565', 'Purple': '#B794F4'},
            title='Photosynthetic Efficiency Across Different Star Systems',
            text='Pigment'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True, key="photosynthesis_efficiency")
        
        st.success("🟣 **Fascinating Fact**: Purple, not green, may be life's favorite color! Early Earth may have been dominated by purple organisms using retinol instead of chlorophyll.")
        
        # Color comparison grid
        st.markdown("#### 🎨 Vegetation Color Across the Cosmos")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("**🔴 Red Dwarf**")
            st.markdown("🖤 Black plants")
        with col2:
            st.markdown("**🟡 Yellow Sun**")
            st.markdown("🟢 Green plants")
        with col3:
            st.markdown("**🔵 Blue Giant**")
            st.markdown("🔴 Red plants")
        with col4:
            st.markdown("**🟣 Ancient Earth**")
            st.markdown("🟣 Purple plants")

# ADVANCED FEATURES SECTION
if st.session_state.current_wing == "Home":
    st.markdown("---")
    st.markdown("## 🔬 Advanced Research Labs")
    
    research_tab1, research_tab2, research_tab3, research_tab4 = st.tabs([
        "🧪 Life Form Simulator", 
        "🌡️ Habitability Calculator", 
        "🧬 DNA Mutation Lab",
        "📊 Exoplanet Database"
    ])
    
    with research_tab1:
        st.subheader("🧪 Alien Life Form Simulator")
        st.markdown("*Design your own alien organism based on environmental parameters*")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sim_gravity = st.slider("Gravity (g)", 0.1, 5.0, 1.0, 0.1, key="sim_gravity")
            sim_temp = st.slider("Temperature (K)", 100, 800, 300, 10, key="sim_temp")
            sim_pressure = st.slider("Pressure (atm)", 0.1, 100.0, 1.0, 0.5, key="sim_pressure")
        
        with col2:
            sim_atmosphere = st.multiselect(
                "Atmospheric Composition",
                ["Oxygen", "Nitrogen", "CO2", "Methane", "Hydrogen", "Ammonia"],
                ["Nitrogen", "Oxygen"],
                key="sim_atmosphere"
            )
            sim_water = st.select_slider(
                "Water Availability",
                ["None", "Trace", "Moderate", "Abundant"],
                "Moderate",
                key="sim_water"
            )
            sim_radiation = st.slider("Radiation Level", 0, 100, 20, 5, key="sim_radiation")
        
        with col3:
            sim_chemistry = st.radio(
                "Base Chemistry",
                ["Carbon", "Silicon", "Exotic"],
                key="sim_chemistry"
            )
            sim_energy = st.selectbox(
                "Energy Source",
                ["Photosynthesis", "Chemosynthesis", "Thermal", "Radiation"],
                key="sim_energy"
            )
        
        if st.button("🧬 Generate Organism", key="generate_organism"):
            # Calculate organism traits
            body_mass = 50 * sim_gravity
            limb_count = max(2, int(8 / sim_gravity))
            eye_count = 2 if "Oxygen" in sim_atmosphere else 4
            skin_thickness = sim_radiation / 10
            metabolism_rate = sim_temp / 300
            
            col_a, col_b = st.columns(2)
            st.session_state.organism_generated = True
            
            with col_a:
                st.markdown("### 👾 Generated Organism Profile")
                organism_stats = pd.DataFrame({
                    'Trait': ['Body Mass', 'Limb Count', 'Eye Count', 'Skin Thickness', 'Metabolism Rate', 'Lifespan'],
                    'Value': [
                        f"{body_mass:.1f} kg",
                        f"{limb_count}",
                        f"{eye_count}",
                        f"{skin_thickness:.1f} cm",
                        f"{metabolism_rate:.2f}x Earth",
                        f"{int(100/metabolism_rate)} years"
                    ]
                })
                st.table(organism_stats)
                
                # Survival rating
                survival_score = (
                    (100 - abs(sim_temp - 300)) * 0.3 +
                    (100 - sim_radiation) * 0.25 +
                    (len(sim_atmosphere) * 10) * 0.2 +
                    (["None", "Trace", "Moderate", "Abundant"].index(sim_water) * 25) * 0.25
                )
                
                st.metric("Survival Rating", f"{survival_score:.0f}%", 
                         "Viable" if survival_score > 50 else "Challenging")
            
            with col_b:
                # Organism visualization
                trait_comparison = pd.DataFrame({
                    'Trait': ['Strength', 'Speed', 'Intelligence', 'Senses', 'Endurance', 'Adaptability'],
                    'Value': [
                        sim_gravity * 30,
                        100 / sim_gravity,
                        metabolism_rate * 50,
                        eye_count * 15,
                        (100 - sim_radiation) * 0.8,
                        len(sim_atmosphere) * 15
                    ]
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=trait_comparison['Value'],
                    theta=trait_comparison['Trait'],
                    fill='toself',
                    line_color='#00BCD4',
                    fillcolor='rgba(0, 188, 212, 0.3)'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    title="Organism Trait Profile",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, key="organism_traits")
        
    with research_tab2:
        st.subheader("🌡️ Planetary Habitability Calculator")
        st.markdown("*Calculate the habitability score of any exoplanet*")
        
        col1, col2 = st.columns(2)
        
        with col1:
            planet_mass = st.number_input("Planet Mass (Earth = 1)", 0.1, 10.0, 1.0, 0.1, key="planet_mass")
            planet_radius = st.number_input("Planet Radius (Earth = 1)", 0.5, 5.0, 1.0, 0.1, key="planet_radius")
            star_distance = st.number_input("Distance from Star (AU)", 0.1, 5.0, 1.0, 0.1, key="star_distance")
            star_temp_hab = st.number_input("Star Temperature (K)", 2000, 20000, 5778, 100, key="star_temp_hab")
            
            has_magnetic_field = st.checkbox("Has Magnetic Field", True, key="magnetic_field")
            has_atmosphere_hab = st.checkbox("Has Atmosphere", True, key="has_atmosphere")
            has_water_hab = st.checkbox("Has Liquid Water", False, key="has_water")
            tidal_locked = st.checkbox("Tidally Locked", False, key="tidal_locked")
        
        with col2:
            # Calculate habitability factors
            gravity_hab = planet_mass / (planet_radius ** 2)
            goldilocks_factor = 100 * np.exp(-((star_distance - 1.0) ** 2) / 0.5)
            temp_factor = 100 * np.exp(-((star_temp_hab - 5778) ** 2) / 10000000)
            
            # Total habitability
            base_score = (goldilocks_factor * 0.3 + temp_factor * 0.2)
            bonus_score = (
                (30 if has_magnetic_field else 0) +
                (25 if has_atmosphere_hab else 0) +
                (20 if has_water_hab else 0) +
                (-15 if tidal_locked else 5)
            )
            total_hab = min(100, base_score + bonus_score)
            
            st.markdown("### 📊 Habitability Analysis")
            
            # Gauge chart
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=total_hab,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Habitability Score"},
                delta={'reference': 50},
                gauge={
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                    'bar': {'color': "#00BCD4"},
                    'steps': [
                        {'range': [0, 30], 'color': "#742A2A"},
                        {'range': [30, 60], 'color': "#B7791F"},
                        {'range': [60, 100], 'color': "#2F855A"}
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True, key="habitability_gauge")
            
            # Factor breakdown
            factors_df = pd.DataFrame({
                'Factor': ['Goldilocks Zone', 'Star Type', 'Magnetic Field', 'Atmosphere', 'Liquid Water', 'Rotation'],
                'Score': [
                    goldilocks_factor * 0.3,
                    temp_factor * 0.2,
                    30 if has_magnetic_field else 0,
                    25 if has_atmosphere_hab else 0,
                    20 if has_water_hab else 0,
                    -15 if tidal_locked else 5
                ]
            })
            
            fig = px.bar(factors_df, x='Factor', y='Score', 
                        title="Habitability Factor Breakdown",
                        color='Score',
                        color_continuous_scale=px.colors.diverging.RdYlGn)
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True, key="hab_factors")
            
            if total_hab > 70:
                st.success("🌍 **Highly Habitable!** This planet could support Earth-like life.")
            elif total_hab > 40:
                st.warning("⚠️ **Marginally Habitable.** Life is possible but challenging.")
            else:
                st.error("☠️ **Inhospitable.** Extreme conditions make life unlikely.")
    
    with research_tab3:
        st.subheader("🧬 DNA Mutation & Evolution Lab")
        st.markdown("*Simulate evolutionary pressures and genetic mutations*")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### Environmental Pressures")
            mutation_rate = st.slider("Mutation Rate (%)", 0.1, 10.0, 1.0, 0.1, key="mutation_rate")
            selection_pressure = st.select_slider(
                "Selection Pressure",
                ["Weak", "Moderate", "Strong", "Extreme"],
                "Moderate",
                key="selection_pressure"
            )
            generations = st.slider("Generations", 10, 1000, 100, 10, key="generations")
            population_size = st.slider("Population Size", 100, 10000, 1000, 100, key="pop_size")
            
            environmental_stress = st.multiselect(
                "Environmental Stresses",
                ["High Radiation", "Temperature Extremes", "Predation", "Food Scarcity", "Disease"],
                ["Predation"],
                key="env_stress"
            )
            
            if st.button("🧬 Run Evolution Simulation", key="run_evolution"):
                st.session_state.evolution_run = True
                # Store sim settings for deep dive
                st.session_state.sim_selection_pressure = selection_pressure
                st.session_state.sim_env_stress = environmental_stress
        
        with col2:
            if 'evolution_run' in st.session_state and st.session_state.evolution_run:
                # Simulate evolution
                pressure_multiplier = {"Weak": 0.5, "Moderate": 1.0, "Strong": 1.5, "Extreme": 2.0}[selection_pressure]
                gen_data = []
                fitness = 50
                genetic_diversity = 100
                
                for gen in range(0, generations, 10):
                    # Fitness increases with selection, decreases with stress
                    stress_factor = len(environmental_stress) * 0.2
                    fitness += np.random.normal(pressure_multiplier * 2 - stress_factor, 1)
                    fitness = np.clip(fitness, 0, 100)
                    
                    # Diversity decreases with strong selection
                    genetic_diversity -= pressure_multiplier * 0.5 + np.random.normal(0, 2)
                    genetic_diversity = np.clip(genetic_diversity, 20, 100)
                    
                    # Beneficial mutations
                    beneficial = mutation_rate * pressure_multiplier * np.random.random()
                    
                    gen_data.append({
                        'Generation': gen,
                        'Fitness': fitness,
                        'Diversity': genetic_diversity,
                        'Beneficial_Mutations': beneficial
                    })
                
                evo_df = pd.DataFrame(gen_data)
                
                # Evolution over time
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=evo_df['Generation'], y=evo_df['Fitness'],
                    mode='lines', name='Population Fitness',
                    line=dict(color='#48BB78', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=evo_df['Generation'], y=evo_df['Diversity'],
                    mode='lines', name='Genetic Diversity',
                    line=dict(color='#4299E1', width=3)
                ))
                fig.add_trace(go.Scatter(
                    x=evo_df['Generation'], y=evo_df['Beneficial_Mutations'] * 100,
                    mode='markers', name='Beneficial Mutations',
                    marker=dict(color='#F56565', size=8)
                ))
                fig.update_layout(
                    title="Evolution Simulation Results",
                    xaxis_title="Generation",
                    yaxis_title="Value (%)",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, key="evolution_chart")
                
                # Final results
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Final Fitness", f"{fitness:.1f}%", f"+{fitness-50:.1f}%")
                with col_b:
                    st.metric("Genetic Diversity", f"{genetic_diversity:.1f}%", 
                             f"{genetic_diversity-100:.1f}%")
                with col_c:
                    total_mutations = sum(evo_df['Beneficial_Mutations'])
                    st.metric("Total Beneficial Mutations", f"{total_mutations:.1f}")
                
                # Store final results for deep dive
                st.session_state.final_fitness = fitness
                st.session_state.final_diversity = genetic_diversity
    
    with research_tab4:
        st.subheader("📊 Exoplanet Database Explorer")
        st.markdown("*Explore discovered exoplanets and their characteristics*")
        
        # Generate synthetic exoplanet data
        np.random.seed(42)
        n_planets = 500
        
        exoplanet_data = pd.DataFrame({
            'Name': [f'Kepler-{i}b' if i % 2 == 0 else f'TRAPPIST-{i}e' for i in range(n_planets)],
            'Mass': np.random.lognormal(0, 1, n_planets),
            'Radius': np.random.lognormal(0, 0.5, n_planets),
            'Distance': np.random.uniform(10, 1000, n_planets),
            'Star_Type': np.random.choice(['Red Dwarf', 'Yellow Sun', 'Orange Dwarf', 'Blue Giant'], n_planets, p=[0.5, 0.3, 0.15, 0.05]),
            'Orbital_Period': np.random.lognormal(2, 1.5, n_planets),
            'Temperature': np.random.normal(400, 200, n_planets),
            'Discovery_Year': np.random.randint(1995, 2025, n_planets)
        })
        
        exoplanet_data['Habitable'] = (
            (exoplanet_data['Temperature'] > 200) & 
            (exoplanet_data['Temperature'] < 350) &
            (exoplanet_data['Mass'] > 0.3) &
            (exoplanet_data['Mass'] < 3)
        )
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### 🔍 Filter Exoplanets")
            
            filter_star = st.multiselect(
                "Star Type",
                ['Red Dwarf', 'Yellow Sun', 'Orange Dwarf', 'Blue Giant'],
                ['Red Dwarf', 'Yellow Sun'],
                key="filter_star"
            )
            
            mass_range = st.slider(
                "Mass Range (Earth = 1)",
                0.0, 10.0, (0.5, 3.0),
                key="mass_range"
            )
            
            temp_range = st.slider(
                "Temperature Range (K)",
                0, 1000, (200, 400),
                key="temp_range"
            )
            
            show_habitable_only = st.checkbox("Show Only Habitable", False, key="show_hab_only")
            
            # Filter data
            filtered_data = exoplanet_data[
                (exoplanet_data['Star_Type'].isin(filter_star)) &
                (exoplanet_data['Mass'] >= mass_range[0]) &
                (exoplanet_data['Mass'] <= mass_range[1]) &
                (exoplanet_data['Temperature'] >= temp_range[0]) &
                (exoplanet_data['Temperature'] <= temp_range[1])
            ]
            
            if show_habitable_only:
                filtered_data = filtered_data[filtered_data['Habitable']]
            
            st.metric("Planets Found", len(filtered_data), 
                     f"{len(filtered_data)/len(exoplanet_data)*100:.1f}% of total")
            st.metric("Potentially Habitable", filtered_data['Habitable'].sum())
        
        with col2:
            # 3D scatter plot
            fig = px.scatter_3d(
                filtered_data,
                x='Mass',
                y='Radius',
                z='Temperature',
                color='Star_Type',
                size='Orbital_Period',
                hover_data=['Name', 'Distance', 'Discovery_Year'],
                title='Exoplanet Distribution (3D)',
                labels={'Mass': 'Mass (Earth)', 'Radius': 'Radius (Earth)', 'Temperature': 'Temp (K)'},
                opacity=0.7
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True, key="exoplanet_3d")
        
        # Timeline of discoveries
        st.markdown("#### 📅 Discovery Timeline")
        discovery_timeline = filtered_data.groupby('Discovery_Year').size().reset_index(name='Count')
        
        fig = px.area(
            discovery_timeline,
            x='Discovery_Year',
            y='Count',
            title='Exoplanet Discoveries Over Time',
            labels={'Discovery_Year': 'Year', 'Count': 'Number of Planets'}
        )
        fig.update_traces(line_color='#00BCD4', fillcolor='rgba(0, 188, 212, 0.3)')
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True, key="discovery_timeline")
        
        # Data table
        with st.expander("📋 View Detailed Planet Data"):
            st.dataframe(
                filtered_data[['Name', 'Mass', 'Radius', 'Temperature', 'Star_Type', 'Habitable']].head(50),
                use_container_width=True
            )

# Deep Dive section for Evolution Lab
if st.session_state.current_wing == "Home" and 'evolution_run' in st.session_state and st.session_state.evolution_run:
    st.markdown("---")
    st.header("🏛️ Elite Evolved Architectures: A Deep Dive")
    st.markdown("This section provides a multi-faceted analysis of the top-performing genotypes from the final population, deconstructing the architectural, causal, and evolutionary properties that contributed to their success.")

    # Use final values from the simulation
    final_fitness = st.session_state.final_fitness
    final_diversity = st.session_state.final_diversity
    np.random.seed(int(final_fitness + final_diversity)) # Seed for deterministic randomness
    
    expander_title = f"**Rank 1:** Final Dominant Genotype | Fitness: `{final_fitness:.2f}`"
    with st.expander(expander_title, expanded=True):
        
        # Define tabs for the deep dive
        tab_vitals, tab_ancestry = st.tabs([
            "🌐 Vitals & Architecture", 
            "🌳 Genealogy & Ancestry",
        ])
        
        # --- TAB 1: Vitals & Architecture ---
        with tab_vitals:
            vitals_col1, vitals_col2 = st.columns([1, 1])
            with vitals_col1:
                st.markdown("#### Evolved Trait Profile")
                
                # --- DYNAMIC TRAIT GENERATION ---
                trait_pool = {
                    "High Radiation": ["Radiation Shielding", "DNA Repair"],
                    "Temperature Extremes": ["Thermal Regulation", "Structural Stability"],
                    "Predation": ["Stealth", "Defensive Plating"],
                    "Food Scarcity": ["Energy Storage", "Metabolic Efficiency"],
                    "Disease": ["Immune Response", "Cellular Purity"],
                    "pressure": ["Competitive Edge", "Resource Acquisition"],
                }
                
                # Select traits based on simulation inputs
                selected_traits = trait_pool['pressure']
                for stress in st.session_state.sim_env_stress:
                    selected_traits.extend(trait_pool[stress])
                
                # Pick 5-7 unique traits for the chart
                num_traits_to_show = min(len(selected_traits), np.random.randint(5, 8))
                display_traits = np.random.choice(selected_traits, num_traits_to_show, replace=False)
                
                # Assign values based on fitness and diversity
                trait_values = [
                    np.clip(final_fitness * np.random.uniform(0.8, 1.2) + np.random.randint(-10, 10), 0, 100)
                    for _ in display_traits
                ]

                # Create a radar chart for evolved traits
                evolved_traits = pd.DataFrame({
                    'Trait': display_traits,
                    'Value': trait_values
                })
                
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=evolved_traits['Value'],
                    theta=evolved_traits['Trait'],
                    fill='toself',
                    line_color='#00BCD4',
                    fillcolor='rgba(0, 188, 212, 0.3)'
                ))
                fig.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    title="Dominant Genotype Trait Profile",
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True, key="evolved_trait_radar")

            with vitals_col2:
                st.markdown("#### Architectural Evolution")
                
                # --- DEDICATED CONTROLS ---
                evo_col1, evo_col2 = st.columns(2)
                with evo_col1:
                    max_gens = st.slider("Max Evolution Generations", 10, 500, 100, 10, key="max_evo_gens")
                with evo_col2:
                    anim_speed = st.select_slider("Animation Speed", ["Slow", "Normal", "Fast"], "Normal", key="anim_speed")
                
                delay_map = {"Slow": 0.9, "Normal": 0.7, "Fast": 0.3}
                animation_delay = delay_map[anim_speed]

                blueprint_placeholder = st.empty()
                
                if st.button("Animate Architectural Evolution", key="animate_architecture"):
                    # --- DYNAMIC ANIMATED EVOLUTION ---
                    base_nodes = 3
                    max_additional_nodes = int(20 * (final_fitness / 100))
                    
                    for gen in range(0, max_gens + 1, 5):
                        progress = gen / max_gens
                        
                        # Interpolate parameters based on generation
                        current_nodes = int(base_nodes + progress * max_additional_nodes)
                        connection_prob = 0.2 + progress * (final_fitness / 100 - 0.2)
                        
                        with blueprint_placeholder.container():
                            st.markdown(f"**Visualizing Generation:** `{gen}/{max_gens}`")
                            graph = graphviz.Digraph('Genotype', graph_attr={'bgcolor': 'transparent'})
                            graph.attr('node', shape='circle', style='filled', fontname='Exo 2', color='#00BCD4', fillcolor='#2D3748', fontcolor='#E2E8F0')
                            graph.attr('edge', color='#A0AEC0')
                            
                            nodes = [f"G{i}" for i in range(current_nodes)]
                            
                            # Add nodes
                            for node in nodes:
                                graph.node(node)
                            
                            # Add connections
                            for i in range(current_nodes):
                                if np.random.random() < connection_prob:
                                    target_node = np.random.choice(nodes)
                                    if nodes[i] != target_node:
                                        graph.edge(nodes[i], target_node)
                            
                            st.graphviz_chart(graph, use_container_width=True)
                        
                        time.sleep(animation_delay)


        # --- TAB 2: Genealogy & Ancestry ---
        with tab_ancestry:
            st.markdown("#### Evolutionary Lineage")
            
            # Create a simple ancestry tree
            tree = graphviz.Digraph('Ancestry', graph_attr={'bgcolor': 'transparent'})
            tree.attr('node', shape='box', style='rounded,filled', fontname='Exo 2', color='#00BCD4', fillcolor='#2D3748', fontcolor='#E2E8F0')
            tree.attr('edge', fontname='Exo 2', fontsize='10', color='#A0AEC0', fontcolor='#A0AEC0')
            tree.attr(rankdir='BT')

            tree.node('Final', 'Final Dominant Genotype', fillcolor='#B7791F', fontcolor='white')
            tree.node('Ancestor1', 'Ancestor (Gen -50)')
            tree.node('Ancestor2', 'Ancestor (Gen -80)')
            tree.node('Origin', 'Origin Population')
            
            tree.edge('Ancestor1', 'Final', label=' Strong Selection')
            tree.edge('Ancestor2', 'Ancestor1', label=' Beneficial Mutation')
            tree.edge('Origin', 'Ancestor2', label=' Initial Adaptation')
            
            st.graphviz_chart(tree, use_container_width=True)
            st.info("This chart traces the key evolutionary steps that led to the emergence of the final dominant genotype from the origin population.")


# Interactive Timeline Feature
if st.session_state.current_wing == "Wing 1: Life As We Know It":
    st.markdown("---")
    st.markdown("## 🕰️ Evolution Timeline Viewer")
    
    timeline_years = st.slider(
        "Select Time Period (Billions of Years Ago)",
        4.5, 0.0, (3.5, 0.5),
        key="timeline_slider"
    )
    
    # Evolution events
    events = [
        {'time': 4.5, 'event': 'Earth Formation', 'color': '#A0AEC0'},
        {'time': 3.8, 'event': 'First Life (Prokaryotes)', 'color': '#4299E1'},
        {'time': 2.7, 'event': 'Photosynthesis Begins', 'color': '#48BB78'},
        {'time': 2.0, 'event': 'Eukaryotic Cells', 'color': '#B794F4'},
        {'time': 1.2, 'event': 'Sexual Reproduction', 'color': '#F687B3'},
        {'time': 0.6, 'event': 'Cambrian Explosion', 'color': '#F56565'},
        {'time': 0.4, 'event': 'Plants Colonize Land', 'color': '#9AE6B4'},
        {'time': 0.25, 'event': 'Dinosaurs Appear', 'color': '#ED8936'},
        {'time': 0.065, 'event': 'Dinosaur Extinction', 'color': '#C53030'},
        {'time': 0.002, 'event': 'Homo Sapiens', 'color': '#FFD700'}
    ]
    
    filtered_events = [e for e in events if timeline_years[1] <= e['time'] <= timeline_years[0]]
    
    if filtered_events:
        fig = go.Figure()
        
        for event in filtered_events:
            fig.add_trace(go.Scatter(
                x=[event['time']],
                y=[1],
                mode='markers+text',
                marker=dict(size=20, color=event['color']),
                text=event['event'],
                textposition='top center',
                name=event['event'],
                hovertemplate=f"<b>{event['event']}</b><br>{event['time']} BYA<extra></extra>"
            ))
        
        fig.update_layout(
            title="Evolutionary Milestones",
            xaxis_title="Billions of Years Ago",
            xaxis=dict(autorange='reversed'),
            yaxis=dict(visible=False),
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True, key="evolution_timeline")

# Biosignature Detection Game
if st.session_state.current_wing == "Wing 2: Life As We Don't Know It":
    st.markdown("---")
    st.markdown("## 🔬 Biosignature Detection Challenge")
    st.markdown("*Can you identify signs of life in atmospheric data?*")
    
    if 'game_score' not in st.session_state:
        st.session_state.game_score = 0
        st.session_state.game_attempts = 0
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate random atmospheric spectrum
        if st.button("🌍 Scan New Planet", key="scan_planet"):
            has_life = np.random.random() > 0.5
            st.session_state.current_planet_life = has_life
            st.session_state.game_attempts += 1
            
            wavelengths = np.linspace(300, 2500, 500)
            baseline = np.random.normal(50, 5, 500)
            
            if has_life:
                # Add biosignature spikes
                o2_spike = 30 * np.exp(-((wavelengths - 760) ** 2) / 100)
                ch4_spike = 20 * np.exp(-((wavelengths - 1650) ** 2) / 500)
                h2o_spike = 25 * np.exp(-((wavelengths - 950) ** 2) / 200)
                spectrum = baseline + o2_spike + ch4_spike + h2o_spike
            else:
                # Just baseline noise
                spectrum = baseline + np.random.normal(0, 3, 500)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=wavelengths,
                y=spectrum,
                mode='lines',
                line=dict(color='#00BCD4', width=2),
                fill='tozeroy'
            ))
            
            # Mark key biosignature wavelengths
            fig.add_vline(x=760, line_dash="dash", line_color="#F56565", 
                         annotation_text="O₂", annotation_position="top")
            fig.add_vline(x=1650, line_dash="dash", line_color="#48BB78", 
                         annotation_text="CH₄", annotation_position="top")
            fig.add_vline(x=950, line_dash="dash", line_color="#4299E1", 
                         annotation_text="H₂O", annotation_position="top")
            
            fig.update_layout(
                title="Atmospheric Spectrum",
                xaxis_title="Wavelength (nm)",
                yaxis_title="Absorption Intensity",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True, key="biosig_spectrum")
    
    with col2:
        st.markdown("### 🎮 Your Analysis")
        
        if 'current_planet_life' in st.session_state:
            user_guess = st.radio(
                "Does this planet have life?",
                ["Yes - Life Present", "No - Lifeless"],
                key="life_guess"
            )
            
            if st.button("Submit Analysis", key="submit_analysis"):
                user_says_life = user_guess == "Yes - Life Present"
                correct = user_says_life == st.session_state.current_planet_life
                
                if correct:
                    st.success("✅ Correct! Well done!")
                    st.session_state.game_score += 1
                else:
                    st.error("❌ Incorrect. Study the biosignature peaks!")
                
                st.markdown("---")
                st.metric("Score", f"{st.session_state.game_score}/{st.session_state.game_attempts}")
                st.progress(st.session_state.game_score / max(st.session_state.game_attempts, 1))
        else:
            st.info("Click 'Scan New Planet' to start the challenge!")

# Comparative Anatomy Tool
if st.session_state.current_wing == "Wing 3: Environmental Sculpting":
    st.markdown("---")
    st.markdown("## 🦴 Comparative Anatomy Lab")
    st.markdown("*Compare anatomical features across different gravity levels*")
    
    anatomy_feature = st.selectbox(
        "Select Anatomical System",
        ["Skeletal Structure", "Circulatory System", "Respiratory System", "Muscular System"],
        key="anatomy_feature"
    )
    
    gravity_levels = [0.3, 0.5, 1.0, 1.5, 2.0, 3.0]
    
    if anatomy_feature == "Skeletal Structure":
        bone_data = pd.DataFrame({
            'Gravity': gravity_levels,
            'Bone_Density': [50, 70, 100, 130, 160, 200],
            'Bone_Thickness': [0.5, 0.7, 1.0, 1.5, 2.0, 3.0],
            'Joint_Strength': [30, 50, 100, 150, 200, 250]
        })
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=bone_data['Gravity'], y=bone_data['Bone_Density'], 
                            name='Bone Density', marker_color='#4299E1'))
        fig.add_trace(go.Bar(x=bone_data['Gravity'], y=bone_data['Bone_Thickness']*50, 
                            name='Bone Thickness', marker_color='#F56565'))
        fig.add_trace(go.Scatter(x=bone_data['Gravity'], y=bone_data['Joint_Strength'], 
                                name='Joint Strength', mode='lines+markers', 
                                line=dict(color='#48BB78', width=3)))
        fig.update_layout(title="Skeletal Adaptations Across Gravity Levels", 
                         xaxis_title="Gravity (g)", barmode='group', height=400)
        st.plotly_chart(fig, use_container_width=True, key="skeletal_comp")
    
    elif anatomy_feature == "Circulatory System":
        cardio_data = pd.DataFrame({
            'Gravity': gravity_levels,
            'Heart_Size': [80, 90, 100, 120, 150, 200],
            'Blood_Pressure': [60, 80, 100, 130, 160, 200],
            'Vessel_Thickness': [0.8, 0.9, 1.0, 1.3, 1.6, 2.0]
        })
        
        fig = px.line(cardio_data, x='Gravity', y=['Heart_Size', 'Blood_Pressure', 'Vessel_Thickness'],
                     title="Cardiovascular System Scaling",
                     labels={'value': 'Relative Size/Pressure', 'variable': 'Feature'})
        fig.update_traces(mode='lines+markers', line_shape='spline')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True, key="cardio_comp")

# WING 4: TREE OF UNIVERSAL LIFE
elif st.session_state.current_wing == "Tree of Universal Life":
    st.markdown('<h2 class="wing-header">🌳 The Tree of Universal Life</h2>', unsafe_allow_html=True)
    st.markdown("*A speculative graph connecting all known and theoretical forms of life.*")

    # Create a graphlib graph object
    graph = graphviz.Digraph('UniversalTree', engine='dot', graph_attr={'bgcolor': 'transparent'})
    graph.attr('node', shape='box', style='rounded,filled', fontname='Exo 2', color='#00BCD4', fillcolor='#2D3748', fontcolor='#E2E8F0')
    graph.attr('edge', fontname='Exo 2', fontsize='10', color='#A0AEC0', fontcolor='#A0AEC0')
    graph.attr(rankdir='TB', size='10,10', splines='curved')

    # Nodes
    graph.node('LUCA', 'Last Universal Common Ancestor (LUCA)', fillcolor='#B7791F', fontcolor='white')
    
    # Carbon-based branch
    with graph.subgraph(name='cluster_carbon') as c:
        c.attr(label='Carbon-Based Life', style='rounded,filled', color='#2F855A', fillcolor='rgba(47, 133, 90, 0.2)', fontname='Exo 2', fontcolor='#9AE6B4')
        c.node('Prokaryotes')
        c.node('Eukaryotes')
        c.node('Animals')
        c.node('Plants')
        c.node('Fungi')
        c.edge('LUCA', 'Prokaryotes', label=' First Life')
        c.edge('Prokaryotes', 'Eukaryotes', label=' Endosymbiosis')
        c.edge('Eukaryotes', 'Animals')
        c.edge('Eukaryotes', 'Plants')
        c.edge('Eukaryotes', 'Fungi')

    # Exotic/Theoretical branch
    with graph.subgraph(name='cluster_exotic') as c:
        c.attr(label='Exotic & Theoretical Life', style='rounded,filled', color='#C53030', fillcolor='rgba(197, 48, 48, 0.2)', fontname='Exo 2', fontcolor='#FEB2B2')
        c.node('SiliconLife', 'Silicon-Based Life\n(e.g., on Titan)')
        c.node('PlasmaLife', 'Plasma-Based Life\n(Cosmic Clouds)')
        c.node('NuclearLife', 'Macronuclei Life\n(Neutron Stars)')
        c.edge('LUCA', 'SiliconLife', label='Alternative\nBiochemistry', style='dashed')
        c.edge('SiliconLife', 'PlasmaLife', label='Extreme\nConditions', style='dashed')
        c.edge('PlasmaLife', 'NuclearLife', label='Beyond Known\nPhysics', style='dashed')

    st.graphviz_chart(graph, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #A0AEC0;'>
    <p>The Museum of Universal Life | Powered by Scientific Speculation</p>
    <p><em>"The universe is not only stranger than we imagine, it is stranger than we can imagine." - J.B.S. Haldane</em></p>
    <p style='font-size: 0.8em; margin-top: 10px;'>Advanced Research Labs • Evolutionary Simulators • Exoplanet Database</p>
</div>
""", unsafe_allow_html=True)
