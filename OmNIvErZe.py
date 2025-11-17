import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import numpy as np
import pandas as pd
import time
import graphviz

# Page config
st.set_page_config(
    page_title="Museum of Universal Life",
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
    @import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;700&display=swap');

    /* Core App Styling */
    body, .stApp {
        font-family: 'Exo 2', sans-serif;
        background-color: #0D1117; /* Near-black */
    }

    /* Main container background with subtle pattern */
    .main > div {
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40' viewBox='0 0 40 40'%3E%3Cg fill-rule='evenodd'%3E%3Cg fill='%232d3748' fill-opacity='0.2'%3E%3Cpath d='M0 38.59l2.83-2.83 1.41 1.41L1.41 40H0v-1.41zM0 1.4l2.83 2.83 1.41-1.41L1.41 0H0v1.41zM38.59 40l-2.83-2.83 1.41-1.41L40 38.59V40h-1.41zM40 1.41l-2.83 2.83-1.41-1.41L38.59 0H40v1.41zM20 18.6l2.83-2.83 1.41 1.41L21.41 20l2.83 2.83-1.41 1.41L20 21.41l-2.83 2.83-1.41-1.41L18.59 20l-2.83-2.83 1.41-1.41L20 18.59z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: rgba(13, 17, 23, 0.8);
        backdrop-filter: blur(5px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Main Header */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        font-family: 'Exo 2', sans-serif;
        background: linear-gradient(45deg, #00BCD4 0%, #FFD700 100%); /* Cyan to Gold */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
        letter-spacing: 2px;
    }

    /* Wing Header */
    .wing-header {
        font-size: 2.5rem;
        font-family: 'Exo 2', sans-serif;
        color: #00BCD4; /* Accent Cyan */
        border-bottom: 2px solid #00BCD4;
        padding-bottom: 10px;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }

    /* Glassmorphism Cards */
    .exhibit-card {
        background: rgba(45, 55, 72, 0.5); /* Semi-transparent dark blue-gray */
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        height: 100%; /* Make cards in a row equal height */
        transition: all 0.3s ease;
    }
    .exhibit-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0, 188, 212, 0.2);
        border-color: rgba(0, 188, 212, 0.5);
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
        font-family: 'Exo 2', sans-serif;
        font-size: 1.1rem;
        padding: 10px 20px;
    }
    .st-emotion-cache-1s44j7o button:hover {
        background-color: rgba(0, 188, 212, 0.1);
        color: #00BCD4;
    }
    .st-emotion-cache-1s44j7o button[aria-selected="true"] {
        color: #00BCD4; /* Active tab color */
        border-bottom: 2px solid #00BCD4;
        background-color: rgba(0, 188, 212, 0.05);
    }

    /* General text color */
    .st-emotion-cache-1r4qj8v, .st-emotion-cache-1y4p8pa, .st-emotion-cache-1kyxreq, p, li {
        color: #CBD5E0; /* Lighter gray for better readability */
        font-weight: 300;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Exo 2', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for lazy loading
if 'current_wing' not in st.session_state:
    st.session_state.current_wing = "Home"
if 'show_carbon_radar' not in st.session_state:
    st.session_state.show_carbon_radar = False
if 'show_convergent_bar' not in st.session_state:
    st.session_state.show_convergent_bar = False
if 'show_dna_scatter' not in st.session_state:
    st.session_state.show_dna_scatter = False
if 'show_temp_viability' not in st.session_state:
    st.session_state.show_temp_viability = False
if 'show_extreme_scatter' not in st.session_state:
    st.session_state.show_extreme_scatter = False
if 'show_neutron_prob' not in st.session_state:
    st.session_state.show_neutron_prob = False
if 'show_gravity_body' not in st.session_state:
    st.session_state.show_gravity_body = False
if 'show_gravity_impact' not in st.session_state:
    st.session_state.show_gravity_impact = False
if 'show_star_spectrum' not in st.session_state:
    st.session_state.show_star_spectrum = False
if 'show_alien_garden' not in st.session_state:
    st.session_state.show_alien_garden = False

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
st.markdown("<h3 style='text-align: center; color: #A0AEC0; font-weight: 300;'>*Exploring Every Possible Form of Life in the Universe*</h3>", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.image("https://i.imgur.com/k9E7zFk.png", use_container_width=True) # Placeholder image
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
    st.markdown("""
    <div class="info-box">
    🎯 **Mission Statement**: This museum represents humanity's attempt to catalog every conceivable form of life, from the familiar carbon-based organisms of Earth to the exotic, theoretical beings that might exist in the harshest corners of our universe. It is a monument to imagination grounded in science, teaching us that while the laws of physics are universal, the forms that life can take within those laws are limited only by the number of worlds on which it can arise.
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="exhibit-card">
            <h3>🧬 Wing 1</h3>
            <h4>Life As We Know It</h4>
            <p>Explore the wonders of carbon-based biology and the surprising patterns of convergent evolution that might make alien life more familiar than you think.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="exhibit-card">
            <h3>👾 Wing 2</h3>
            <h4>Life As We Don't Know It</h4>
            <p>Venture into the speculative realm of exotic biochemistry, from silicon-based beings on Titan to crystalline life in plasma clouds.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="exhibit-card">
            <h3>🌍 Wing 3</h3>
            <h4>Environmental Sculpting</h4>
            <p>Witness how the fundamental forces of the cosmos—gravity, radiation, and stellar light—act as cosmic sculptors, shaping life into myriad forms.</p>
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

# WING 1: LIFE AS WE KNOW IT
elif st.session_state.current_wing == "Wing 1: Life As We Know It":
    st.markdown('<h2 class="wing-header">🧬 Wing 1: Life As We Know It (The Carbon Gallery)</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Carbon Foundation", "Convergent Evolution", "DNA Alternatives"])
    
    with tab1:
        st.subheader("💎 The Carbon-Based Standard")
        st.markdown("This exhibit explores why carbon is the centerpiece in the molecular machinery of life as we know it. Its unique ability to form four stable bonds allows for the creation of long, complex chains, providing the structural foundation for everything from DNA to proteins.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <h4>Why Carbon is Special</h4>
            <ul>
                <li>✅ **Cosmic Abundance:** Common throughout the universe.</li>
                <li>✅ **Bonding Versatility:** Forms four stable covalent bonds.</li>
                <li>✅ **Chain Formation:** Creates long, stable chains (catenation).</li>
                <li>✅ **Complexity:** Enables huge, complex molecules like DNA.</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.show_carbon_radar:
                properties_df = pd.DataFrame({
                    'Property': ['Bond Strength', 'Complexity', 'Stability', 'Versatility', 'Cosmic Abundance'],
                    'Carbon': [95, 100, 90, 100, 85],
                    'Silicon': [75, 60, 70, 70, 90]
                })
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(r=properties_df['Carbon'], theta=properties_df['Property'], fill='toself', name='Carbon', line_color='#48BB78'))
                fig.add_trace(go.Scatterpolar(r=properties_df['Silicon'], theta=properties_df['Property'], fill='toself', name='Silicon', line_color='#00BCD4'))
                fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), title="Carbon vs Silicon: Life-Enabling Properties", height=400)
                st.plotly_chart(fig, use_container_width=True, key="carbon_radar_chart")
                if st.button("Hide Chart", key="hide_carbon_radar_btn"):
                    st.session_state.show_carbon_radar = False
                    st.rerun()
            else:
                if st.button("Render Comparison Chart", key="show_carbon_radar_btn"):
                    st.session_state.show_carbon_radar = True
                    st.rerun()

        with col2:
            st.plotly_chart(create_molecule_3d("carbon"), use_container_width=True, key="carbon_molecule_3d")
            st.success("🔬 **Scientific Fact**: Over a million possible carbon-based alternatives to our own DNA have been identified by scientists, highlighting the immense diversity possible even within a familiar chemistry.")
    
    with tab2:
        st.subheader("🔄 The Hall of Convergent Evolution")
        st.markdown("This gallery explores a fascinating idea: even on distant, Earth-like planets, life might evolve familiar forms. Convergent evolution is the process where similar environmental pressures cause similar features to evolve independently. The 'greatest hits of evolution' could be on repeat across the cosmos.")
        
        if st.session_state.show_convergent_bar:
            convergent_examples = pd.DataFrame({
                'Feature': ['Eyes', 'Flight', 'Echolocation', 'Bioluminescence', 'Venom', 'Camouflage'],
                'Times_Evolved_on_Earth': [40, 4, 4, 50, 100, 200],
                'Likelihood_on_Exoplanets': [95, 85, 70, 80, 90, 95]
            })
            fig = go.Figure()
            fig.add_trace(go.Bar(x=convergent_examples['Feature'], y=convergent_examples['Times_Evolved_on_Earth'], name='Times Evolved on Earth', marker_color='#00BCD4'))
            fig.add_trace(go.Scatter(x=convergent_examples['Feature'], y=convergent_examples['Likelihood_on_Exoplanets'], name='Likelihood on Exoplanets (%)', yaxis='y2', mode='lines+markers', marker=dict(size=10, color='#FFD700'), line=dict(width=3)))
            fig.update_layout(title="Convergent Evolution: Earth's Greatest Hits", yaxis=dict(title='Times Evolved'), yaxis2=dict(title='Exoplanet Likelihood (%)', overlaying='y', side='right'), height=450)
            st.plotly_chart(fig, use_container_width=True, key="convergent_bar_chart")
            if st.button("Hide Chart", key="hide_convergent_bar_btn"):
                st.session_state.show_convergent_bar = False
                st.rerun()
        else:
            if st.button("Render Convergence Data", key="show_convergent_bar_btn"):
                st.session_state.show_convergent_bar = True
                st.rerun()

    with tab3:
        st.subheader("🧬 DNA Alternatives Gallery")
        st.markdown("While DNA is the blueprint for life on Earth, it is not the only possibility. This exhibit showcases alternative genetic molecules (Xeno Nucleic Acids) that could form the basis of life elsewhere.")
        
        if st.session_state.show_dna_scatter:
            dna_alts = pd.DataFrame({
                'Type': ['Standard DNA', 'XNA (Xeno)', 'PNA (Peptide)', 'TNA (Threose)', 'LNA (Locked)', 'GNA (Glycol)'],
                'Stability': [85, 95, 90, 88, 98, 80],
                'Complexity': [100, 85, 75, 70, 80, 65],
                'Temperature_Tolerance': [70, 95, 85, 75, 90, 85],
                'Discovered': [1953, 1990, 1991, 2000, 1998, 1992]
            })
            fig = px.scatter_3d(dna_alts, x='Stability', y='Complexity', z='Temperature_Tolerance', color='Type', size=[30]*len(dna_alts), title='3D Comparison of DNA Alternatives', labels={'Stability': 'Molecular Stability', 'Complexity': 'Informational Complexity', 'Temperature_Tolerance': 'Temperature Range'})
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True, key="dna_scatter3d_chart")
            if st.button("Hide Chart", key="hide_dna_scatter_btn"):
                st.session_state.show_dna_scatter = False
                st.rerun()
        else:
            if st.button("Render DNA Alternatives Chart", key="show_dna_scatter_btn"):
                st.session_state.show_dna_scatter = True
                st.rerun()

# WING 2: LIFE AS WE DON'T KNOW IT
elif st.session_state.current_wing == "Wing 2: Life As We Don't Know It":
    st.markdown('<h2 class="wing-header">👾 Wing 2: Life As We Don\'t Know It (The Exotic Biochemistry Hall)</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["The Silicon Contender", "Extreme Environments", "Theoretical Beings"])
    
    with tab1:
        st.subheader("🔷 The Silicon Contender")
        st.markdown("The most prominent exhibit in this wing is dedicated to silicon-based life. While silicon shares carbon's ability to form four bonds, it has critical differences. In the presence of oxygen, it forms solid rock (quartz), making it unsuitable for Earth-like biology. But in an oxygen-free world, it could be the foundation of life.")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("""
            <div class="info-box">
            <h4>Silicon-Based Life: A Profile</h4>
            <p><strong>Advantages:</strong> High-temperature stability, cosmic abundance.</p>
            <p><strong>Challenges:</strong> Weaker bonds, forms solid rock with oxygen.</p>
            <p><strong>Ideal Environment:</strong> Oxygen-free, cold, with a non-water solvent like liquid methane.</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.show_temp_viability:
                temp_data = pd.DataFrame({'Temperature (K)': np.linspace(100, 600, 100), 'Carbon_Viability': np.where(np.linspace(100, 600, 100) < 373, 100, 100 - (np.linspace(100, 600, 100) - 373) * 0.5), 'Silicon_Viability': np.where(np.linspace(100, 600, 100) > 200, np.minimum(100, (np.linspace(100, 600, 100) - 200) * 0.3), 0)})
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=temp_data['Temperature (K)'], y=temp_data['Carbon_Viability'], fill='tozeroy', name='Carbon Life', line=dict(color='#48BB78')))
                fig.add_trace(go.Scatter(x=temp_data['Temperature (K)'], y=temp_data['Silicon_Viability'], fill='tozeroy', name='Silicon Life', line=dict(color='#00BCD4')))
                fig.update_layout(title='Temperature Viability Ranges', xaxis_title='Temperature (Kelvin)', yaxis_title='Life Viability (%)', height=400)
                st.plotly_chart(fig, use_container_width=True, key="temp_viability_chart")
                if st.button("Hide Chart", key="hide_temp_viability_btn"):
                    st.session_state.show_temp_viability = False
                    st.rerun()
            else:
                if st.button("Render Viability Chart", key="show_temp_viability_btn"):
                    st.session_state.show_temp_viability = True
                    st.rerun()

        with col2:
            st.plotly_chart(create_molecule_3d("silicon"), use_container_width=True, key="silicon_molecule_3d")
            st.info("🪐 **Case Study: Titan** - Saturn's moon, with its frigid temperatures and liquid methane lakes, is a prime candidate for theoretical silicon-based life with ultra-slow metabolisms.")
    
    with tab2:
        st.subheader("🌋 Extreme Environment Exhibits")
        st.markdown("Life's tenacity may allow it to thrive in conditions we consider hellish. This exhibit maps the theoretical possibilities.")
        
        if st.session_state.show_extreme_scatter:
            extreme_envs = pd.DataFrame({'Environment': ['Molten Rock', 'Neutron Star Surface', 'Plasma Clouds', 'Deep Ocean Vents', 'Acidic Lakes'], 'Temperature (K)': [1500, 1e6, 10000, 600, 300], 'Pressure (atm)': [1000, 1e20, 0.001, 300, 1], 'Theoretical_Life': ['Silicate Organisms', 'Macronuclei Life', 'Plasma Crystals', 'Extremophiles', 'Acid-Lovers'], 'Likelihood': [30, 5, 15, 95, 90]})
            fig = px.scatter_3d(extreme_envs, x='Temperature (K)', y='Pressure (atm)', z='Likelihood', color='Theoretical_Life', size='Likelihood', hover_data=['Environment'], title='Extreme Environments Life Map', log_x=True, log_y=True, size_max=50)
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True, key="extreme_scatter_chart")
            if st.button("Hide Chart", key="hide_extreme_scatter_btn"):
                st.session_state.show_extreme_scatter = False
                st.rerun()
        else:
            if st.button("Render Environments Map", key="show_extreme_scatter_btn"):
                st.session_state.show_extreme_scatter = True
                st.rerun()

    with tab3:
        st.subheader("🌟 Theoretical Beings Gallery")
        st.markdown("Here we display the most speculative forms of life, beings that exist at the very edge of physics and imagination.")
        
        if st.session_state.show_neutron_prob:
            neutron_data = pd.DataFrame({'Particle_Density': np.logspace(15, 18, 50), 'Life_Probability': 100 / (1 + np.exp(-(np.logspace(15, 18, 50) - 1e17) / 1e16))})
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=neutron_data['Particle_Density'], y=neutron_data['Life_Probability'], fill='tozeroy', line=dict(color='#B794F4', width=3), name='Theoretical Viability'))
            fig.update_layout(title='Macronuclei Life Formation Probability on Neutron Stars', xaxis_title='Particle Density (particles/cm³)', yaxis_title='Formation Probability (%)', xaxis_type='log', height=400)
            st.plotly_chart(fig, use_container_width=True, key="neutron_prob_chart")
            if st.button("Hide Chart", key="hide_neutron_prob_btn"):
                st.session_state.show_neutron_prob = False
                st.rerun()
        else:
            if st.button("Render Neutron Star Life Chart", key="show_neutron_prob_btn"):
                st.session_state.show_neutron_prob = True
                st.rerun()

# WING 3: ENVIRONMENTAL SCULPTING
elif st.session_state.current_wing == "Wing 3: Environmental Sculpting":
    st.markdown('<h2 class="wing-header">🌍 Wing 3: Environmental Sculpting</h2>', unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["The Gravity Gallery", "The Hall of Senses", "The Alien Garden"])
    
    with tab1:
        st.subheader("⚖️ The Gravity Gallery")
        st.markdown("Witness how gravity, a fundamental force, acts as a cosmic sculptor, dictating the very body plan of life.")
        
        gravity_level = st.select_slider("Select Planetary Gravity", options=["Low (0.3g)", "Earth (1g)", "High (2g)", "Super-Earth (3g)"], value="Earth (1g)", key="gravity_slider")
        g_value = {"Low (0.3g)": 0.3, "Earth (1g)": 1.0, "High (2g)": 2.0, "Super-Earth (3g)": 3.0}[gravity_level]
        
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.show_gravity_body:
                body_proportions = pd.DataFrame({'Body_Part': ['Legs', 'Torso', 'Arms', 'Head'], 'Thickness': [10 * g_value, 8 * g_value, 6 * g_value, 5 * g_value], 'Strength_Required': [100 * g_value, 80 * g_value, 60 * g_value, 40 * g_value]})
                fig = go.Figure()
                fig.add_trace(go.Bar(x=body_proportions['Body_Part'], y=body_proportions['Thickness'], name='Bone Thickness', marker_color='#F56565'))
                fig.add_trace(go.Bar(x=body_proportions['Body_Part'], y=body_proportions['Strength_Required'], name='Muscle Mass Required', marker_color='#4299E1'))
                fig.update_layout(title=f'Body Structure at {gravity_level}', barmode='group', height=400)
                st.plotly_chart(fig, use_container_width=True, key="gravity_body_struct_chart")
                if st.button("Hide Chart", key="hide_gravity_body_btn"):
                    st.session_state.show_gravity_body = False
                    st.rerun()
            else:
                if st.button("Render Body Structure Chart", key="show_gravity_body_btn"):
                    st.session_state.show_gravity_body = True
                    st.rerun()

        with col2:
            if st.session_state.show_gravity_impact:
                plant_heights = pd.DataFrame({'Gravity': [0.3, 0.5, 1.0, 1.5, 2.0, 3.0], 'Max_Plant_Height_m': [50, 30, 15, 10, 7, 3], 'Animal_Jump_Height_m': [5, 3, 1.5, 0.8, 0.5, 0.2]})
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=plant_heights['Gravity'], y=plant_heights['Max_Plant_Height_m'], mode='lines+markers', name='Max Plant Height', line=dict(color='#48BB78', width=3), marker=dict(size=10)))
                fig.add_trace(go.Scatter(x=plant_heights['Gravity'], y=plant_heights['Animal_Jump_Height_m'], mode='lines+markers', name='Animal Jump Height', line=dict(color='#ED8936', width=3), marker=dict(size=10), yaxis='y2'))
                fig.update_layout(title='Gravity Impact on Life Forms', xaxis_title='Gravity (g)', yaxis_title='Plant Height (m)', yaxis2=dict(title='Jump Height (m)', overlaying='y', side='right'), height=400)
                fig.add_vline(x=g_value, line_dash="dash", line_color="#FFD700", annotation_text="Selected", annotation_position="top")
                st.plotly_chart(fig, use_container_width=True, key="gravity_impact_chart")
                if st.button("Hide Chart", key="hide_gravity_impact_btn"):
                    st.session_state.show_gravity_impact = False
                    st.rerun()
            else:
                if st.button("Render Gravity Impact Chart", key="show_gravity_impact_btn"):
                    st.session_state.show_gravity_impact = True
                    st.rerun()

    with tab2:
        st.subheader("⭐ Hall of Senses: Stellar Influence")
        st.markdown("Life adapts to the light of its star. This exhibit shows how different star types would necessitate different sensory organs.")
        
        star_type = st.selectbox("Select Star Type", ["Red Dwarf", "Yellow Sun (Earth)", "Blue Giant"], key="star_selector")
        star_data = {"Red Dwarf": {"temp": 3000, "color": "#F56565", "brightness": 0.3}, "Yellow Sun (Earth)": {"temp": 5778, "color": "#FFD700", "brightness": 1.0}, "Blue Giant": {"temp": 15000, "color": "#4299E1", "brightness": 3.0}}
        current_star = star_data[star_type]
        
        if st.session_state.show_star_spectrum:
            wavelengths = np.linspace(300, 800, 500)
            def planck_law(wavelength, temp):
                h, c, k = 6.626e-34, 3.0e8, 1.381e-23
                return (2*h*c**2 / wavelength**5) / (np.exp(h*c / (wavelength * k * temp)) - 1)
            intensity = planck_law(wavelengths * 1e-9, current_star['temp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=wavelengths, y=intensity / np.max(intensity) * 100, fill='tozeroy', line=dict(color=current_star['color'], width=2), name=star_type))
            fig.add_vrect(x0=380, x1=450, fillcolor="purple", opacity=0.1, annotation_text="Violet")
            fig.add_vrect(x0=450, x1=495, fillcolor="blue", opacity=0.1, annotation_text="Blue")
            fig.add_vrect(x0=495, x1=570, fillcolor="green", opacity=0.1, annotation_text="Green")
            fig.add_vrect(x0=570, x1=590, fillcolor="yellow", opacity=0.1, annotation_text="Yellow")
            fig.add_vrect(x0=590, x1=620, fillcolor="orange", opacity=0.1, annotation_text="Orange")
            fig.add_vrect(x0=620, x1=750, fillcolor="red", opacity=0.1, annotation_text="Red")
            fig.update_layout(title=f'Light Spectrum from {star_type}', xaxis_title='Wavelength (nm)', yaxis_title='Relative Intensity (%)', height=400)
            st.plotly_chart(fig, use_container_width=True, key="star_spectrum_chart")
            if st.button("Hide Chart", key="hide_star_spectrum_btn"):
                st.session_state.show_star_spectrum = False
                st.rerun()
        else:
            if st.button("Render Stellar Spectrum", key="show_star_spectrum_btn"):
                st.session_state.show_star_spectrum = True
                st.rerun()

    with tab3:
        st.subheader("🌺 The Alien Garden")
        st.markdown("A visually stunning display of alien botany. Our plants are green because they reflect the green light from our yellow sun. This garden showcases the bizarre alternatives.")
        
        garden_type = st.radio("View Garden Under:", ["Red Dwarf Star", "Yellow Sun (Earth)", "Blue Giant Star", "Purple Earth (Ancient)"], horizontal=True, key="garden_radio")
        
        if st.session_state.show_alien_garden:
            color_schemes = {"Red Dwarf Star": {'ground': 'rgba(80, 60, 50, 0.8)', 'plant': 'rgba(10, 10, 10, 0.9)', 'sky': 'rgba(150, 50, 50, 0.3)'}, "Yellow Sun (Earth)": {'ground': 'rgba(139, 90, 43, 0.8)', 'plant': 'rgba(34, 139, 34, 0.9)', 'sky': 'rgba(135, 206, 235, 0.3)'}, "Blue Giant Star": {'ground': 'rgba(200, 180, 160, 0.8)', 'plant': 'rgba(180, 50, 50, 0.9)', 'sky': 'rgba(70, 130, 255, 0.3)'}, "Purple Earth (Ancient)": {'ground': 'rgba(100, 80, 70, 0.8)', 'plant': 'rgba(128, 0, 128, 0.9)', 'sky': 'rgba(200, 150, 200, 0.3)'}}
            gravity_map = {"Red Dwarf Star": "low", "Yellow Sun (Earth)": "normal", "Blue Giant Star": "high", "Purple Earth (Ancient)": "normal"}
            landscape_fig = generate_alien_landscape(color_schemes[garden_type], gravity_map[garden_type], garden_type)
            st.plotly_chart(landscape_fig, use_container_width=True, key="alien_garden_viz_chart")
            if st.button("Hide Garden", key="hide_alien_garden_btn"):
                st.session_state.show_alien_garden = False
                st.rerun()
        else:
            if st.button("Render Alien Garden", key="show_alien_garden_btn"):
                st.session_state.show_alien_garden = True
                st.rerun()

# WING 4: TREE OF UNIVERSAL LIFE
elif st.session_state.current_wing == "Tree of Universal Life":
    st.markdown('<h2 class="wing-header">🌳 The Tree of Universal Life</h2>', unsafe_allow_html=True)
    st.markdown("A speculative graph connecting all known and theoretical forms of life, branching from a Last Universal Common Ancestor (LUCA).")

    graph = graphviz.Digraph('UniversalTree', engine='dot', graph_attr={'bgcolor': 'transparent', 'rankdir': 'TB', 'splines': 'ortho'})
    graph.attr('node', shape='box', style='rounded,filled', fontname='Exo 2', color='#00BCD4', fillcolor='#2D3748', fontcolor='#E2E8F0')
    graph.attr('edge', fontname='Exo 2', fontsize='10', color='#A0AEC0', fontcolor='#A0AEC0')

    graph.node('LUCA', 'Last Universal Common Ancestor (LUCA)', fillcolor='#B7791F', fontcolor='white')
    
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
<div style='text-align: center; color: #A0AEC0; font-weight: 300;'>
    <p>The Museum of Universal Life | Powered by Scientific Speculation & Imagination</p>
    <p><em>"The universe is not only stranger than we imagine, it is stranger than we can imagine." - J.B.S. Haldane</em></p>
</div>
""", unsafe_allow_html=True)
