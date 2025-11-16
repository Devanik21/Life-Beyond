import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io

# Page config
st.set_page_config(
    page_title="Museum of Alien Life",
    page_icon="👽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px;
    }
    .wing-header {
        font-size: 2rem;
        color: #667eea;
        border-bottom: 3px solid #667eea;
        padding-bottom: 10px;
        margin-top: 20px;
    }
    .exhibit-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for lazy loading
if 'current_wing' not in st.session_state:
    st.session_state.current_wing = "Home"
if 'current_exhibit' not in st.session_state:
    st.session_state.current_exhibit = None

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
            'size': [20, 20, 20, 20, 20]
        })
        color = 'gray'
    else:  # silicon
        atoms = pd.DataFrame({
            'x': [0, 1, 2],
            'y': [0, 0, 0],
            'z': [0, 0, 0],
            'atom': ['Si', 'Si', 'Si'],
            'size': [25, 25, 25]
        })
        color = 'darkblue'
    
    fig = go.Figure(data=[go.Scatter3d(
        x=atoms['x'],
        y=atoms['y'],
        z=atoms['z'],
        mode='markers+text',
        marker=dict(size=atoms['size'], color=color, opacity=0.8),
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
            line=dict(color='white', width=5),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            yaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            zaxis=dict(showbackground=False, showticklabels=False, showgrid=False),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        height=400,
        title=f"{molecule_type.title()}-Based Molecular Chain"
    )
    
    return fig

# Main header
st.markdown('<h1 class="main-header">🌌 The Museum of Universal Life 👽</h1>', unsafe_allow_html=True)
st.markdown("### *Exploring Every Possible Form of Life in the Universe*")

# Sidebar navigation
with st.sidebar:
    st.image("https://via.placeholder.com/300x150/667eea/ffffff?text=Museum+of+Life", use_container_width=True)
    st.markdown("## 🎫 Navigation")
    
    wing_choice = st.radio(
        "Select Wing:",
        ["Home", "Wing 1: Life As We Know It", "Wing 2: Life As We Don't Know It", "Wing 3: Environmental Sculpting", "Wing 4: Procedural Life Lab"],
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
        color_continuous_scale='Viridis',
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
                line_color='green'
            ))
            fig.add_trace(go.Scatterpolar(
                r=properties_df['Silicon'],
                theta=properties_df['Property'],
                fill='toself',
                name='Silicon',
                line_color='blue'
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
            marker_color='lightblue'
        ))
        fig.add_trace(go.Scatter(
            x=convergent_examples['Feature'],
            y=convergent_examples['Likelihood_on_Exoplanets'],
            name='Likelihood on Exoplanets (%)',
            yaxis='y2',
            mode='lines+markers',
            marker=dict(size=10, color='orange'),
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
                line=dict(color='green')
            ))
            fig.add_trace(go.Scatter(
                x=temp_data['Temperature (K)'],
                y=temp_data['Silicon_Viability'],
                fill='tozeroy',
                name='Silicon Life',
                line=dict(color='blue')
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
            line=dict(color='purple', width=3),
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
                marker_color='lightcoral'
            ))
            fig.add_trace(go.Bar(
                x=body_proportions['Body_Part'],
                y=body_proportions['Strength_Required'],
                name='Muscle Mass Required',
                marker_color='lightblue'
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
                line=dict(color='green', width=3),
                marker=dict(size=10)
            ))
            fig.add_trace(go.Scatter(
                x=plant_heights['Gravity'],
                y=plant_heights['Animal_Jump_Height_m'],
                mode='lines+markers',
                name='Animal Jump Height',
                line=dict(color='orange', width=3),
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
            fig.add_vline(x=g_value, line_dash="dash", line_color="red", 
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
            "Red Dwarf": {"temp": 3000, "color": "red", "brightness": 0.3},
            "Yellow Sun (Earth)": {"temp": 5778, "color": "yellow", "brightness": 1.0},
            "Blue Giant": {"temp": 15000, "color": "blue", "brightness": 3.0}
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
        fig.add_vrect(x0=380, x1=450, fillcolor="violet", opacity=0.2, annotation_text="Violet")
        fig.add_vrect(x0=450, x1=495, fillcolor="blue", opacity=0.2, annotation_text="Blue")
        fig.add_vrect(x0=495, x1=570, fillcolor="green", opacity=0.2, annotation_text="Green")
        fig.add_vrect(x0=570, x1=590, fillcolor="yellow", opacity=0.2, annotation_text="Yellow")
        fig.add_vrect(x0=590, x1=620, fillcolor="orange", opacity=0.2, annotation_text="Orange")
        fig.add_vrect(x0=620, x1=750, fillcolor="red", opacity=0.2, annotation_text="Red")
        
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
            color_discrete_map={'Black': 'black', 'Green': 'green', 'Red': 'red', 'Purple': 'purple'},
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

# WING 4: PROCEDURAL LIFE LAB
elif st.session_state.current_wing == "Wing 4: Procedural Life Lab":
    st.markdown('<h2 class="wing-header">🔬 Wing 4: Procedural Life Lab</h2>', unsafe_allow_html=True)
    st.markdown("### *Design your own alien life form by defining its universe!*")

    # Helper function to draw the creature
    def visualize_creature(params):
        """Generates a PIL image of the creature based on morphological parameters."""
        img_size = (400, 400)
        img = Image.new('RGBA', img_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        center_x, center_y = img_size[0] // 2, img_size[1] // 2
        
        # Body
        body_width = params['body_size']
        body_height = body_width * (2 if params['body_plan'] == 'Bilateral' else 1)
        body_color = {'Carbon': (100, 180, 100), 'Silicon': (150, 150, 180)}[params['base_element']]
        draw.ellipse([center_x - body_width/2, center_y - body_height/2, 
                      center_x + body_width/2, center_y + body_height/2], fill=body_color)

        # Legs
        if params['locomotion'] == 'Legs':
            leg_length = body_height * 0.7
            for i in range(params['appendages']):
                angle = (360 / params['appendages']) * i
                rad = np.deg2rad(angle)
                start_x = center_x + (body_width/2) * np.cos(rad)
                start_y = center_y + (body_height/2) * np.sin(rad)
                end_x = center_x + (body_width/2 + leg_length) * np.cos(rad)
                end_y = center_y + (body_height/2 + leg_length/2) * np.sin(rad)
                draw.line([start_x, start_y, end_x, end_y], fill=(50,50,50), width=5)

        # Eyes
        eye_color = (255, 255, 0) if params['senses'] == 'Vision' else (100,100,100)
        for i in range(params['eyes']):
            eye_angle = (180 / (params['eyes'] + 1)) * (i + 1) - 90
            rad = np.deg2rad(eye_angle)
            eye_x = center_x + (body_width/2.5) * np.cos(rad)
            eye_y = center_y - (body_height/2.5) * np.sin(rad)
            draw.ellipse([eye_x-5, eye_y-5, eye_x+5, eye_y+5], fill=eye_color)
            
        return img

    # Main generator function
    def generate_procedural_life(params):
        """Generates a description based on a dictionary of parameters."""
        desc = f"### Creature Profile: {params['name']}\n\n"
        
        # Biochemistry
        desc += f"This is a **{params['base_element']}-based** life form that thrives in a solvent of **{params['solvent']}**. "
        desc += f"Its genetic information is stored in a **{params['genetics']}-like** molecule. "
        
        # Environment
        desc += f"It originates from a planet with **{params['gravity']:.1f}g** of gravity and an atmospheric pressure of **{params['pressure']:.1f} atm**. "
        desc += f"The environment is rich in **{params['atmosphere']}** and has an average temperature of **{params['temperature']}°C**. "
        
        # Morphology
        desc += f"\n\n**Morphology & Adaptation:**\n"
        desc += f"- **Body Plan:** The creature exhibits a **{params['body_plan']}** symmetry with a body size relative index of **{params['body_size']}**. "
        if params['gravity'] > 1.5:
            desc += "Its form is low and wide to cope with the high gravity. "
        else:
            desc += "Its form is more elongated, suitable for lower gravity. "
            
        desc += f"- **Skeleton:** It possesses a **{params['skeleton']}** skeleton. "
        if params['skeleton'] == 'Exoskeleton':
            desc += "This provides excellent protection in its harsh environment. "
        else:
            desc += "This allows for greater flexibility and size. "
            
        desc += f"- **Locomotion:** It moves via **{params['locomotion']}**. With **{params['appendages']}** appendages, it is well-suited for its terrain. "
        desc += f"- **Senses:** Its primary sense is **{params['senses']}**, supported by **{params['eyes']}** eye-like organs. "
        if params['senses'] == 'Chemoreception':
            desc += "These organs 'taste' the chemical composition of the atmosphere. "
        else:
            desc += "These organs are adapted to the light spectrum of its star. "
            
        return desc

    # --- UI FOR PARAMETERS ---
    params = {}
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Creature Parameters")
        params['name'] = st.text_input("Creature Name", "Gleep Glorp")

        with st.expander("🪐 Planetary Environment", expanded=True):
            params['gravity'] = st.slider("Gravity (g)", 0.1, 5.0, 1.0, 0.1)
            params['temperature'] = st.slider("Surface Temperature (°C)", -200, 500, 15, 1)
            params['pressure'] = st.slider("Atmospheric Pressure (atm)", 0.01, 10.0, 1.0, 0.1)
            params['atmosphere'] = st.selectbox("Primary Gas", ["Nitrogen-Oxygen", "Methane", "Carbon Dioxide", "Hydrogen"])

        with st.expander("🧬 Biochemistry", expanded=True):
            params['base_element'] = st.selectbox("Base Element", ["Carbon", "Silicon"])
            params['solvent'] = st.selectbox("Solvent", ["Water", "Ammonia", "Methane"])
            params['genetics'] = st.selectbox("Genetic Molecule", ["DNA", "XNA", "PNA", "TNA"])

        with st.expander("🦾 Morphology", expanded=True):
            params['body_plan'] = st.radio("Body Plan", ["Bilateral", "Radial"], horizontal=True)
            params['skeleton'] = st.radio("Skeleton Type", ["Endoskeleton", "Exoskeleton", "Hydrostatic"], horizontal=True)
            params['locomotion'] = st.selectbox("Locomotion", ["Legs", "Fins", "Wings", "Slithering"])
            params['appendages'] = st.slider("Number of Appendages", 0, 16, 4, 1)
            params['body_size'] = st.slider("Relative Body Size", 10, 100, 50, 5)

        with st.expander("👁️ Sensory Organs"):
            params['senses'] = st.selectbox("Primary Sense", ["Vision", "Chemoreception", "Echolocation", "Electroreception"])
            params['eyes'] = st.slider("Number of 'Eyes'", 0, 10, 2, 1)

    with col2:
        st.subheader("Generated Life Form")
        
        # Generate and display the creature
        if st.button("✨ Generate Life Form"):
            st.session_state.creature_params = params

        if 'creature_params' in st.session_state:
            current_params = st.session_state.creature_params
            
            # Display visualization
            with st.container():
                st.markdown(f"<div class='exhibit-card' style='text-align: center;'>", unsafe_allow_html=True)
                creature_image = visualize_creature(current_params)
                st.image(creature_image, caption=f"Procedural visualization of {current_params['name']}", use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # Display description
            description = generate_procedural_life(current_params)
            st.markdown(f"<div class='info-box'>{description}</div>", unsafe_allow_html=True)
        else:
            st.info("Adjust the parameters on the left and click 'Generate Life Form' to begin.")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>🌌 The Museum of Universal Life | Powered by Scientific Speculation 🔬</p>
    <p><em>"The universe is not only stranger than we imagine, it is stranger than we can imagine." - J.B.S. Haldane</em></p>
</div>
""", unsafe_allow_html=True)
