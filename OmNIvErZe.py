import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="The Museum of Universal Life",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS Styling ---
st.markdown("""
<style>
/* Style for custom headers */
.domain-header {
    font-size: 2.5rem;
    font-weight: bold;
    color: #4A90E2; /* A nice celestial blue */
    border-bottom: 2px solid #4A90E2;
    padding-bottom: 10px;
    margin-top: 20px;
}
.exhibit-subheader {
    font-size: 1.75rem;
    font-weight: bold;
    color: #FFA500; /* A contrasting gold */
    margin-top: 20px;
}
/* Style for info boxes */
.info-box {
    background-color: #f0f2f6;
    border-left: 5px solid #4A90E2;
    padding: 15px;
    border-radius: 5px;
    margin: 10px 0;
}
.warning-box {
    background-color: #fff3e0;
    border-left: 5px solid #FFA500;
    padding: 15px;
    border-radius: 5px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# --- Caching Data Functions (LAZY LOADING) ---
# We cache all data generation so it only runs once.

@st.cache_data
def get_earth_tree_data():
    """Mock data for the Tree of Life chart."""
    return {
        "ids": ["Life", "Eukarya", "Bacteria", "Archaea", 
                "Animalia", "Plantae", "Fungi", "Protista", 
                "Metazoa", "Bilateria", "Vertebrata", "Mammalia", "Homo Sapiens"],
        "labels": ["Life", "Eukarya", "Bacteria", "Archaea", 
                   "Animals", "Plants", "Fungi", "Protists",
                   "Metazoa", "Bilateria", "Vertebrates", "Mammals", "Humans"],
        "parents": ["", "Life", "Life", "Life", 
                    "Eukarya", "Eukarya", "Eukarya", "Eukarya",
                    "Animalia", "Metazoa", "Bilateria", "Vertebrata", "Mammalia"],
        "values": [200, 100, 50, 50, 
                   50, 20, 15, 15,
                   40, 30, 20, 10, 1]
    }

@st.cache_data
def get_extremophile_data():
    """Data for extremophile tolerance ranges."""
    df = pd.DataFrame({
        "Organism": ["Human (Baseline)", "Tardigrade (Polyextremophile)", "Thermococcus (Hyperthermophile)", 
                     "Psychrobacter (Psychrophile)", "Halobacterium (Halophile)", "Deinococcus (Radioresistant)"],
        "Category": ["Baseline", "Tolerance", "Extreme Heat", "Extreme Cold", "Extreme Salt", "Extreme Radiation"],
        "Min Temp (°C)": [15, -200, 60, -20, 15, -10],
        "Max Temp (°C)": [35, 150, 103, 20, 50, 50],
        "Radiation (Gy)": [2, 5000, 10, 10, 10, 15000], # Gy = Gray, unit of radiation
    })
    return df

@st.cache_data
def get_gravity_plot_data(gravity_g):
    """Calculates theoretical biological properties based on gravity."""
    max_height = np.clip(10 / (gravity_g**0.7), 0.1, 50)
    bone_density = np.clip(1 * (gravity_g**0.5), 0.2, 5)
    heart_pressure_ratio = np.clip(1 * (gravity_g**0.6), 0.3, 4)
    return max_height, bone_density, heart_pressure_ratio

@st.cache_data
def get_star_spectrum_data(star_type):
    """Mock spectral data for different star types."""
    wavelengths = np.linspace(300, 1100, 100) # From UV to IR
    
    if star_type == "Red Dwarf (M-type)":
        peak = 850 # Peaks in infrared
        intensity = 1.0 * np.exp(-((wavelengths - peak)**2) / (2 * 150**2))
        color = 'red'
        plant_text = "Plants might be **black** to absorb all available weak light, or even utilize infrared light, making them invisible to human eyes."
        plant_img = "https://placehold.co/600x400/000000/FFFFFF?text=Black+Infrared+Plants"
        
    elif star_type == "Blue Giant (O-type)":
        peak = 400 # Peaks in blue/UV
        intensity = 0.8 * np.exp(-((wavelengths - peak)**2) / (2 * 50**2))
        color = 'blue'
        plant_text = "Plants might be **red or orange** to reflect harmful UV/blue light. They would need powerful chemical sunscreens to survive."
        plant_img = "https://placehold.co/600x400/FF4500/FFFFFF?text=Red/Orange+UV-Resistant+Plants"
        
    else: # Default to G-type like our Sun
        peak = 550 # Peaks in green/yellow
        intensity = 0.9 * np.exp(-((wavelengths - peak)**2) / (2 * 100**2))
        color = 'gold'
        plant_text = "Plants are **green** because they absorb red and blue light and reflect the abundant green light, which is less efficient for photosynthesis (the 'green gap')."
        plant_img = "https://placehold.co/600x400/006400/FFFFFF?text=Green+Plants"
        
    df = pd.DataFrame({"Wavelength (nm)": wavelengths, "Intensity": intensity})
    return df, color, plant_text, plant_img

@st.cache_data
def get_extinct_archive_data():
    """Comprehensive data for the Lost Archives exhibit."""
    return {
        "Cambrian (541 Mya)": {
            "image": "https://placehold.co/600x300/8B4513/FFFFFF?text=Trilobite",
            "text": "**The Cambrian Explosion.** Life diversified rapidly. Dominated by marine arthropods like the **Trilobite**. The first complex predators like **Anomalocaris** appeared."
        },
        "Ordovician (485 Mya)": {
            "image": "https://placehold.co/600x300/708090/FFFFFF?text=Nautiloid",
            "text": "Life flourished in the seas, with the first appearance of jawless fish. The dominant predators were giant **Nautiloids** (shelled cephalopods)."
        },
        "Silurian (443 Mya)": {
            "image": "https://placehold.co/600x300/2E8B57/FFFFFF?text=Cooksonia+(First+Land+Plant)",
            "text": "First life on land. **Cooksonia**, a simple branching plant, colonized the water's edge. The first air-breathing animals (arthropods) followed."
        },
        "Devonian (419 Mya)": {
            "image": "https://placehold.co/600x300/00008B/FFFFFF?text=Tiktaalik+(Fish-to-Tetrapod)",
            "text": "**The Age of Fishes.** Fish diversified immensely. The first tetrapods (four-limbed vertebrates) like **Tiktaalik** evolved, bridging the gap between water and land."
        },
        "Carboniferous (359 Mya)": {
            "image": "https://placehold.co/600x300/2F4F4F/FFFFFF?text=Meganeura+(Giant+Dragonfly)",
            "text": "Vast, swampy forests covered the land, eventually forming our coal deposits. High oxygen levels allowed for giant insects, like the dragonfly **Meganeura** (2.5-foot wingspan)."
        },
        "Permian (299 Mya)": {
            "image": "https://placehold.co/600x300/B22222/FFFFFF?text=Dimetrodon",
            "text": "Dominated by synapsids (proto-mammals) like the sail-backed **Dimetrodon**. Ended with **The Great Dying**, the largest mass extinction in Earth's history, wiping out 96% of marine species."
        },
        "Triassic (252 Mya)": {
            "image": "https://placehold.co/600x300/CD853F/FFFFFF?text=Lystrosaurus+(Permian+Survivor)",
            "text": "Life slowly recovered from the extinction. The first dinosaurs and pterosaurs appeared, alongside the first true mammals (small, shrew-like)."
        },
        "Jurassic (201 Mya)": {
            "image": "https://placehold.co/600x300/2F4F4F/FFFFFF?text=Brachiosaurus",
            "text": "**The Age of Giants.** Dinosaurs became the dominant land animals. Giant sauropods like **Brachiosaurus** and predators like **Allosaurus** ruled."
        },
        "Cretaceous (145 Mya)": {
            "image": "https://placehold.co/600x300/B22222/FFFFFF?text=Tyrannosaurus+Rex",
            "text": "Flowering plants appeared and diversified. Dinosaurs reached their peak, with forms like **Tyrannosaurus Rex** and **Triceratops**. Ended with the K-Pg extinction event."
        },
        "Paleogene (66 Mya)": {
            "image": "https://placehold.co/600x300/808000/FFFFFF?text=Hyracotherium+(Dawn+Horse)",
            "text": "**The Rise of Mammals.** With the dinosaurs gone, mammals diversified rapidly, filling ecological niches. The first primates and early horses appeared."
        },
        "Neogene (23 Mya)": {
            "image": "https://placehold.co/600x300/D2B48C/FFFFFF?text=Megalodon",
            "text": "Hominids, our direct ancestors, first appeared in Africa. The seas were dominated by the **Megalodon**, a shark the size of a bus."
        },
        "Pleistocene (2.6 Mya)": {
            "image": "https://placehold.co/600x300/ADD8E6/FFFFFF?text=Woolly+Mammoth",
            "text": "**The Ice Age.** Characterized by cycles of glaciation. Megafauna like the **Woolly Mammoth** and **Saber-toothed Cat** roamed. Modern humans (**Homo sapiens**) evolved."
        }
    }

@st.cache_data
def get_kingdom_data():
    """Data for the 6 Kingdoms of Life."""
    return {
        "bacteria": {
            "name": "🦠 Kingdom Bacteria",
            "image": "https://placehold.co/600x300/1E90FF/FFFFFF?text=Bacteria",
            "text": "Prokaryotic (no nucleus). The oldest and most abundant life form. They are found everywhere, from your gut (E. coli) to hydrothermal vents. Incredibly diverse metabolisms."
        },
        "archaea": {
            "name": "♨️ Kingdom Archaea",
            "image": "https://placehold.co/600x300/FF4500/FFFFFF?text=Archaea",
            "text": "Prokaryotic, like bacteria, but with a unique evolutionary history. Many are extremophiles, living in boiling water (thermophiles), extreme salt (halophiles), or producing methane (methanogens)."
        },
        "protista": {
            "name": "💧 Kingdom Protista",
            "image": "https://placehold.co/600x300/9ACD32/FFFFFF?text=Protista+(Amoeba)",
            "text": "Eukaryotic (has a nucleus). A 'catch-all' kingdom for organisms that aren't plants, animals, or fungi. Includes amoebas, algae, and slime molds."
        },
        "fungi": {
            "name": "🍄 Kingdom Fungi",
            "image": "https://placehold.co/600x300/D2691E/FFFFFF?text=Kingdom+Fungi",
            "text": "Eukaryotic, non-motile, and saprotrophic (absorb nutrients from decaying matter). Includes yeasts, molds, and mushrooms. More closely related to animals than plants."
        },
        "plantae": {
            "name": "🌳 Kingdom Plantae",
            "image": "https://placehold.co/600x300/32CD32/FFFFFF?text=Kingdom+Plantae",
            "text": "Eukaryotic, multicellular, non-motile, and autotrophic (create energy via photosynthesis). Form the basis of most terrestrial food webs."
        },
        "animalia": {
            "name": "👑 Kingdom Animalia",
            "image": "https://placehold.co/600x300/4682B4/FFFFFF?text=Kingdom+Animalia",
            "text": "Eukaryotic, multicellular, motile (can move at some life stage), and heterotrophic (consume other organisms). Includes insects, fish, birds, reptiles, and mammals."
        }
    }

@st.cache_data
def get_biochemistry_data():
    """Data for the Biochemical Machinery exhibit."""
    return {
        "DNA": {
            "name": "🧬 Deoxyribonucleic Acid (DNA)",
            "image": "https://placehold.co/600x300/4682B4/FFFFFF?text=DNA+Double+Helix",
            "text": "The 'blueprint' of life. A double-helix molecule that stores genetic information using four bases: Adenine (A), Guanine (G), Cytosine (C), and Thymine (T). It is incredibly stable and perfect for long-term storage."
        },
        "RNA": {
            "name": "📜 Ribonucleic Acid (RNA)",
            "image": "https://placehold.co/600x300/3CB371/FFFFFF?text=RNA+Single+Strand",
            "text": "The 'messenger' and 'worker.' A single-stranded molecule that carries instructions from the DNA to the ribosomes (where proteins are made). Some viruses use RNA as their primary genetic material. Many scientists believe in an 'RNA World' hypothesis, where RNA came before DNA."
        },
        "Proteins": {
            "name": "⚙️ Proteins & Amino Acids",
            "image": "https://placehold.co/600x300/DAA520/FFFFFF?text=Protein+Folding",
            "text": "The 'machines' of life. Proteins do almost all the work, acting as enzymes, structural components, and signals. They are chains of smaller molecules called Amino Acids. The sequence of amino acids determines how the protein will fold into a complex 3D shape, which dictates its function."
        },
        "ATP": {
            "name": "🔋 Adenosine Triphosphate (ATP)",
            "image": "https://placehold.co/600x300/FF6347/FFFFFF?text=ATP+Energy+Molecule",
            "text": "The 'battery' of life. This molecule is the universal energy currency for all known cells. Energy is stored in its high-energy phosphate bonds. When a bond is broken (turning ATP into ADP), that energy is released to power cellular processes, from muscle contraction to thinking."
        }
    }

@st.cache_data
def get_habitable_zone_data():
    """Data for the Habitable Zone plot."""
    return {
        "Star Type": ["Blue Giant (O-type)", "Yellow Dwarf (G-type, our Sun)", "Red Dwarf (M-type)"],
        "Start (AU)": [50, 0.8, 0.1],
        "End (AU)": [300, 1.7, 0.4],
        "Color": ["blue", "gold", "red"]
    }

@st.cache_data
def get_solvent_data():
    """Data for alternative solvents plot."""
    return {
        "Solvent": ["Water (H2O)", "Ammonia (NH3)", "Methane (CH4)", "Formamide (CH3NO)", "Sulfuric Acid (H2SO4)"],
        "Min Temp (°C)": [0, -78, -182, 2, 10],
        "Max Temp (°C)": [100, -33, -161, 210, 337],
        "Notes": ["Our baseline. Polar.", "Good polar solvent, but very cold.", "Non-polar. Life on Titan?", "Good polar solvent, wider range.", "Extremely corrosive, but stable at high temps."]
    }

@st.cache_data
def get_kardashev_data():
    """Data for the Kardashev Scale plot."""
    return {
        "Type": ["Type 0 (Us, ~0.73)", "Type I (Planetary)", "Type II (Stellar)", "Type III (Galactic)"],
        "Energy (Watts)": [1e13, 1e16, 1e26, 1e36],
        "Description": ["Controls fossil fuels", "Controls all energy on its planet", "Controls all energy from its star", "Controls all energy in its galaxy"]
    }

@st.cache_data
def get_fermi_solutions_data():
    """Data for the Fermi Paradox exhibit."""
    return {
        "They are rare (Rare Earth Hypothesis)": {
            "text": "The specific conditions that led to life on Earth (liquid water, large moon, magnetic field, plate tectonics) are exceptionally rare. We may be the first or only intelligent life in our galaxy.",
            "image": "https://placehold.co/600x300/4682B4/FFFFFF?text=Rare+Earth"
        },
        "They are all dead (The Great Filter)": {
            "text": "There is some universal 'filter' or challenge that intelligent life must pass, and most (or all) fail. This could be self-destruction (nuclear war, climate change), a natural event (gamma-ray burst), or the leap from prokaryote to eukaryote. We may have already passed it, or it may be ahead of us.",
            "image": "https://placehold.co/600x300/B22222/FFFFFF?text=The+Great+Filter"
        },
        "They are hiding (The Zoo Hypothesis)": {
            "text": "Advanced civilizations know we exist but deliberately hide from us, treating us as a nature preserve or an experiment to be observed without interference. They are waiting for us to reach a certain level of maturity.",
            "image": "https://placehold.co/600x300/32CD32/FFFFFF?text=Zoo+Hypothesis"
        },
        "They exist, but we can't understand them": {
            "text": "Their biology, communication, and technology are so different from ours that we are fundamentally incapable of recognizing their signals. It would be like a line of ants walking over a superhighway, unaware of the civilization all around them.",
            "image": "https://placehold.co/600x300/9932CC/FFFFFF?text=Incomprehensible+Life"
        },
        "They are too far away (Vast Distances)": {
            "text": "The speed of light is a hard limit. The galaxy is vast, and even if civilizations are common, the time and energy required to cross interstellar space are too great. Everyone is isolated in their own star system.",
            "image": "https.placehold.co/600x300/708090/FFFFFF?text=Vast+Distances"
        },
        "They have moved on (Post-Biological)": {
            "text": "All advanced civilizations quickly transition from 'wet' biological life to 'dry' machine life or digital consciousness. They may exist in places we aren't looking, like the cold outer solar system or inside vast computational networks (Matrioshka Brains), with no interest in a primitive, biological world like Earth.",
            "image": "https.placehold.co/600x300/1A1A1A/00FF00?text=Digital+Consciousness"
        }
    }

# --- Plotting Functions ---

def create_tree_of_life_plot():
    """Uses Plotly Sunburst to show the domains of life."""
    data = get_earth_tree_data()
    fig = go.Figure(go.Sunburst(
        ids=data["ids"],
        labels=data["labels"],
        parents=data["parents"],
        values=data["values"],
        branchvalues="total",
        marker=dict(colorscale='Viridis'),
        hovertemplate='<b>%{label}</b><br>Parent: %{parent}<extra></extra>'
    ))
    fig.update_layout(margin=dict(t=10, l=10, r=10, b=10), title="Earth's Known Tree of Life")
    return fig

def create_extremophile_plot():
    """Uses Plotly Gantt chart to show temperature tolerances."""
    df = get_extremophile_data().query("Category.str.contains('Heat') or Category.str.contains('Cold') or Category.str.contains('Baseline')")
    
    gantt_data = [
        dict(Task=row["Organism"], Start=row["Min Temp (°C)"], Finish=row["Max Temp (°C)"], Resource=row["Category"])
        for _, row in df.iterrows()
    ]
    colors = {'Baseline': 'rgb(0, 116, 217)', 'Extreme Heat': 'rgb(240, 18, 0)', 'Extreme Cold': 'rgb(0, 100, 255)'}
    fig = ff.create_gantt(gantt_data, colors=colors, index_col='Resource', show_colorbar=True, group_tasks=True)
    fig.update_layout(
        title='Temperature Tolerance Ranges of Life',
        xaxis_title='Temperature (°C)',
        yaxis_title='Organism'
    )
    return fig

def create_gravity_plot(gravity_g):
    """Shows the conceptual impact of gravity on life."""
    max_height, bone_density, heart_pressure = get_gravity_plot_data(gravity_g)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=['Max Height (m)'], y=[max_height], name='Height',
        marker_color='royalblue', text=f"{max_height:.1f} m", textposition='auto'
    ))
    fig.add_trace(go.Bar(
        x=['Bone Density (rel.)'], y=[bone_density], name='Bone Density',
        marker_color='firebrick', text=f"{bone_density:.1f}x Earth", textposition='auto'
    ))
    fig.add_trace(go.Bar(
        x=['Heart Pressure (rel.)'], y=[heart_pressure], name='Heart Pressure',
        marker_color='green', text=f"{heart_pressure:.1f}x Earth", textposition='auto'
    ))
    fig.update_layout(
        title=f'Conceptual Biology at {gravity_g:.1f}g',
        yaxis_title='Value', barmode='group'
    )
    return fig

def create_star_spectrum_plot(star_type):
    """Plots the light spectrum of the selected star."""
    df, color, _, _ = get_star_spectrum_data(star_type)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Wavelength (nm)"], y=df["Intensity"],
        mode='lines', fill='tozeroy', line=dict(color=color, width=3), name=star_type
    ))
    
    # Add visible spectrum background
    fig.add_vrect(x0=380, x1=450, fillcolor="violet", opacity=0.1, line_width=0, annotation_text="UV", annotation_position="top left")
    fig.add_vrect(x0=450, x1=495, fillcolor="blue", opacity=0.1, line_width=0)
    fig.add_vrect(x0=495, x1=570, fillcolor="green", opacity=0.1, line_width=0)
    fig.add_vrect(x0=570, x1=590, fillcolor="yellow", opacity=0.1, line_width=0)
    fig.add_vrect(x0=590, x1=620, fillcolor="orange", opacity=0.1, line_width=0)
    fig.add_vrect(x0=620, x1=750, fillcolor="red", opacity=0.1, line_width=0, annotation_text="Visible", annotation_position="bottom left")
    fig.add_vrect(x0=750, x1=1100, fillcolor="darkred", opacity=0.1, line_width=0, annotation_text="Infrared", annotation_position="top right")
    
    fig.update_layout(
        title=f'Stellar Light Spectrum: {star_type}',
        xaxis_title='Wavelength (nm)', yaxis_title='Relative Intensity'
    )
    return fig

def create_habitable_zone_plot():
    """Plots the habitable zones of different star types."""
    data = get_habitable_zone_data()
    df = pd.DataFrame(data)
    
    gantt_data = [
        dict(Task=row["Star Type"], Start=row["Start"], Finish=row["End"], Resource="Habitable Zone")
        for _, row in df.iterrows()
    ]
    colors = {'Habitable Zone': 'rgb(57, 204, 204)'}
    
    fig = ff.create_gantt(gantt_data, colors=colors, index_col='Resource', show_colorbar=False, group_tasks=True)
    fig.update_layout(
        title='Comparative Habitable Zones (Liquid Water)',
        xaxis_title='Distance from Star (AU) - Logarithmic Scale',
        yaxis_title='Star Type',
        xaxis_type='log'
    )
    return fig

def create_solvent_range_plot():
    """Plots the liquid ranges of different solvents."""
    data = get_solvent_data()
    df = pd.DataFrame(data)
    
    gantt_data = [
        dict(Task=row["Solvent"], Start=row["Min Temp (°C)"], Finish=row["Max Temp (°C)"], Resource="Liquid Range")
        for _, row in df.iterrows()
    ]
    colors = {'Liquid Range': 'rgb(0, 116, 217)'}
    
    fig = ff.create_gantt(gantt_data, colors=colors, index_col='Resource', show_colorbar=False, group_tasks=True)
    fig.update_layout(
        title='Liquid Ranges of Potential Biological Solvents',
        xaxis_title='Temperature (°C)',
        yaxis_title='Solvent'
    )
    return fig

def create_kardashev_scale_plot():
    """Plots the Kardashev Scale on a log axis."""
    data = get_kardashev_data()
    df = pd.DataFrame(data)
    
    fig = go.Figure(go.Bar(
        x=df["Type"],
        y=df["Energy (Watts)"],
        text=df["Description"],
        marker_color=['gray', 'blue', 'gold', 'red']
    ))
    fig.update_layout(
        title="The Kardashev Scale (Logarithmic)",
        xaxis_title="Civilization Type",
        yaxis_title="Energy Consumption (Watts)",
        yaxis_type="log"
    )
    return fig

# --- Main App ---

st.title("🌌 The Museum of Universal Life")
st.markdown("Welcome, my intelligent Prince, to your grand museum. Here, we explore all life, from the familiar to the truly alien.")

# --- Sidebar Navigation ---
st.sidebar.header("Select a Domain")
domain_choice = st.sidebar.radio(
    "Museum Galleries",
    ["Welcome", "Domain I: The Known (Earth Life)", "Domain II: The Possible (Speculative Life)", 
     "Domain III: The Exotic (Theoretical Life)", "Domain IV: The Search (SETI)"],
    key="domain_nav"
)

# --- Gallery: Welcome ---
if domain_choice == "Welcome":
    st.header("Welcome to the Museum")
    st.markdown("""
    This museum is a comprehensive catalog of all known, possible, and theoretical life in the universe.
    
    - **Domain I: The Known** explores the life that arose on our own planet, from the smallest microbe to the largest whale.
    - **Domain II: The Possible** speculates on alien life based on variations of known physics and chemistry (e.g., high-gravity worlds, silicon-based life).
    - **Domain III: The Exotic** pushes the boundaries to theoretical concepts like plasma-based life or digital consciousness.
    - **Domain IV: The Search** details how we are looking for this life, and the profound paradoxes that quest entails.
    
    Use the sidebar to navigate the galleries. Each exhibit is loaded on demand to keep the museum running smoothly.
    """)
    st.image("https://placehold.co/1200x400/2E294E/9055A2?text=The+Museum+of+Universal+Life", use_column_width=True)
    st.markdown("---")
    st.markdown("### Museum Director's Note")
    st.markdown("""
    > "As you walk these halls, remember that this entire museum is built on a single data point: Earth. 
    > Everything in Domain I is our foundation. Everything beyond it is speculation. 
    > The most exciting exhibit is the one we haven't built yet—the one that will be filled by our first discovery."
    """)


# --- Gallery: Domain I: Earth Life ---
elif domain_choice == "Domain I: The Known (Earth Life)":
    st.markdown("<h2 class='domain-header'>🌍 Domain I: The Known (Earth Life)</h2>", unsafe_allow_html=True)
    st.markdown("This gallery is dedicated to the one example of life we know for certain: our own. This is our baseline, our 'n=1' study from which all other speculation must begin.")

    tabs_domain_i = st.tabs([
        "The Tree of Life", 
        "Biochemical Machinery",
        "Kingdom Showcase", 
        "Life at the Extremes", 
        "The Lost Archives (Extinct)"
    ])

    with tabs_domain_i[0]:
        st.markdown("<h3 class='exhibit-subheader'>The Tree of Life</h3>", unsafe_allow_html=True)
        st.write("All known life on Earth stems from a single common ancestor (LUCA - Last Universal Common Ancestor), branching into three main domains. This chart shows the relationships between them.")
        st.plotly_chart(create_tree_of_life_plot(), use_container_width=True, key="tree_of_life_plot")

    with tabs_domain_i[1]:
        st.markdown("<h3 class='exhibit-subheader'>The Biochemical Machinery</h3>", unsafe_allow_html=True)
        st.write("These are the fundamental molecules that all known life relies upon.")
        biochem_data = get_biochemistry_data()
        for key, item in biochem_data.items():
            with st.expander(item["name"]):
                st.image(item["image"], width=400)
                st.markdown(f"<div class='info-box'>{item['text']}</div>", unsafe_allow_html=True)

    with tabs_domain_i[2]:
        st.markdown("<h3 class='exhibit-subheader'>Kingdom Showcase</h3>", unsafe_allow_html=True)
        st.write("Life diversified into major 'Kingdoms.' Here are the six primary classifications.")
        kingdom_data = get_kingdom_data()
        for key, item in kingdom_data.items():
            with st.expander(item["name"]):
                st.image(item["image"], width=400)
                st.markdown(f"<div class='info-box'>{item['text']}</div>", unsafe_allow_html=True)

    with tabs_domain_i[3]:
        st.markdown("<h3 class='exhibit-subheader'>Life at the Extremes (Extremophiles)</h3>", unsafe_allow_html=True)
        st.write("These organisms thrive in conditions that would kill most other life, giving us a hint at what alien life might endure. They redefine the 'habitable zone'.")
        st.plotly_chart(create_extremophile_plot(), use_container_width=True, key="extremophile_plot")
        
        with st.expander("Explore Other Extremes"):
            st.markdown("""
            - **Radioresistant:** *Deinococcus radiodurans* can withstand 15,000 Grays of radiation (10 is lethal to humans) by constantly repairing its DNA.
            - **Barophilic:** Organisms in the Mariana Trench that thrive under 1,000 times normal atmospheric pressure.
            - **Acidophilic:** Life that grows in pH levels near 0 (like battery acid).
            """)

    with tabs_domain_i[4]:
        st.markdown("<h3 class='exhibit-subheader'>The Lost Archives (Extinct Life)</h3>", unsafe_allow_html=True)
        st.write("Life is not static. This exhibit shows a fraction of the forms that have been lost to time. 99.9% of all species that have ever lived are extinct.")
        
        archive_data = get_extinct_archive_data()
        period = st.select_slider(
            "Select a Geological Period",
            options=list(archive_data.keys()),
            key="period_slider"
        )
        
        selected_data = archive_data[period]
        st.image(selected_data["image"], use_column_width=True, caption=f"An artist's impression of life in the {period}")
        st.markdown(f"<div class='info-box'><h4>{period}</h4>{selected_data['text']}</div>", unsafe_allow_html=True)


# --- Gallery: Domain II: Speculative Life ---
elif domain_choice == "Domain II: The Possible (Speculative Life)":
    st.markdown("<h2 class='domain-header'>👽 Domain II: The Possible (Speculative Life)</h2>", unsafe_allow_html=True)
    st.markdown("Here, we use the laws of physics and chemistry to speculate on life that *could* exist on other worlds, based on variations of our n=1 example.")

    tabs_domain_ii = st.tabs([
        "The Foundation of Life",
        "Environmental Sculptors",
        "Alternative Solvents",
        "Habitable Worlds"
    ])

    with tabs_domain_ii[0]:
        st.markdown("<h3 class='exhibit-subheader'>The Chemical Foundation</h3>", unsafe_allow_html=True)
        st.write("Life needs a complex molecular backbone. On Earth, that's carbon. What are the alternatives?")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='info-box'><h4>Carbon-Based Life (Like Us)</h4></div>", unsafe_allow_html=True)
            st.image("https://placehold.co/600x300/4682B4/FFFFFF?text=DNA+Double+Helix", use_column_width=True)
            st.markdown("""
            - **Versatile:** Forms 4 stable bonds, creating long, complex chains (DNA, proteins).
            - **Soluble:** Carbon dioxide (CO2) is a gas, easily exchanged.
            - **Ubiquitous:** One of the most common elements.
            """)
        with col2:
            st.markdown("<div class='warning-box'><h4>Silicon-Based Life (Speculative)</h4></div>", unsafe_allow_html=True)
            st.image("https_placehold.co/600x300/999999/FFFFFF?text=Silicon+Crystal+Lattice", use_column_width=True)
            st.markdown("""
            - **Less Versatile:** Bonds are less stable; struggles to form long chains.
            - **Solid Waste:** Silicon dioxide (SiO2) is quartz... a rock. This makes respiration difficult.
            - **Possibility:** Might work in extremely cold, non-water environments (like Titan's methane lakes) where reactions are slow.
            """)
        
        with st.expander("Other Theoretical Biochemistries"):
            st.markdown("""
            - **Boron-Nitrogen Based:** Boron can form complex chains, sometimes with nitrogen. It could form a backbone for life in ammonia-based solvents.
            - **Arsenic-Based:** Some scientists speculated life could replace Phosphorus with its chemical cousin, Arsenic. This has been largely disproven, but shows the kind of "outside-the-box" thinking required.
            """)

    with tabs_domain_ii[1]:
        st.markdown("<h3 class='exhibit-subheader'>Environmental Sculptors</h3>", unsafe_allow_html=True)
        st.write("An environment will shape life as much as chemistry. We can simulate these effects.")
        
        st.markdown("---")
        st.markdown("#### Gravity's Influence")
        gravity_g = st.slider(
            "Select Planet's Gravity (Earth = 1.0g)",
            min_value=0.1, max_value=3.0, value=1.0, step=0.1,
            key="gravity_slider"
        )
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if gravity_g < 0.5:
                desc = "On a **low-gravity** world, life can grow to towering heights. Skeletons are light and frail, and flight (or floating) might be a common form of locomotion."
                img = "https://placehold.co/600x600/ADD8E6/000000?text=Low-G+Floater"
            elif gravity_g > 2.0:
                desc = "On a **high-gravity** world, life is short, dense, and powerful. Creatures must be robust, with thick bones and powerful, multi-chambered hearts just to stand."
                img = "https_placehold.co/600x600/8B0000/FFFFFF?text=High-G+Crab-Beast"
            else:
                desc = "On an **Earth-like** gravity world, we see a familiar balance between structural integrity and mobility."
                img = "https_placehold.co/600x600/3CB371/FFFFFF?text=Earth-like+Runner"
            st.image(img, use_column_width=True, caption=f"Artist's rendering at {gravity_g:.1f}g")
            st.write(desc)
        with col2:
            st.plotly_chart(create_gravity_plot(gravity_g), use_container_width=True, key="gravity_bioplot")

        st.markdown("---")
        st.markdown("#### A Different Light: Stellar Spectrum")
        star_type = st.selectbox(
            "Select Host Star Type",
            ["Yellow Dwarf (G-type)", "Red Dwarf (M-type)", "Blue Giant (O-type)"],
            key="star_type_select"
        )
        df, color, plant_text, plant_img = get_star_spectrum_data(star_type)
        col3, col4 = st.columns([1, 2])
        with col3:
            st.image(plant_img, use_column_width=True, caption=f"Photosynthesis on a {star_type} planet.")
            st.markdown(plant_text)
        with col4:
            st.plotly_chart(create_star_spectrum_plot(star_type), use_container_width=True, key="star_spectrum_plot")

        st.markdown("---")
        st.markdown("#### Atmospheric Pressure")
        pressure_atm = st.slider(
            "Select Planet's Atmospheric Pressure (Earth = 1.0 atm)",
            min_value=0.1, max_value=50.0, value=1.0, step=0.5,
            key="pressure_slider"
        )
        if pressure_atm < 0.5:
            st.markdown("<div class='info-box'><b>Thin Atmosphere (e.g., Mars):</b> Liquid water boils at a low temperature. Life would need to be subterranean or have pressurized bodies. Respiration would be difficult.</div>", unsafe_allow_html=True)
        elif pressure_atm > 10.0:
            st.markdown("<div class='info-box'><b>Thick Atmosphere (e.g., Venus):</b> A dense 'soup' to move through. Flight might be more like 'swimming.' Sound would travel faster and further. Greenhouse effects could be extreme.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='info-box'><b>Earth-like Atmosphere:</b> A balance that allows for liquid water and efficient gas exchange.</div>", unsafe_allow_html=True)

    with tabs_domain_ii[2]:
        st.markdown("<h3 class='exhibit-subheader'>Alternative Solvents</h3>", unsafe_allow_html=True)
        st.write("Life on Earth uses liquid water as its solvent. What if life used something else? The liquid range of a solvent heavily dictates the speed of life.")
        st.plotly_chart(create_solvent_range_plot(), use_container_width=True, key="solvent_range_plot")
        
        solvent_data = get_solvent_data()
        for item in solvent_data:
            with st.expander(f"💧 {item['Solvent']} ({item['Min Temp (°C)']}°C to {item['Max Temp (°C)']}°C)"):
                st.write(item["Notes"])

    with tabs_domain_ii[3]:
        st.markdown("<h3 class='exhibit-subheader'>Habitable Worlds</h3>", unsafe_allow_html=True)
        st.write("The 'Habitable Zone' (or 'Goldilocks Zone') is the region around a star where liquid water can exist on a planet's surface. But this is a simplistic view.")
        st.plotly_chart(create_habitable_zone_plot(), use_container_width=True, key="habitable_zone_plot")

        with st.expander("Beyond the Zone: Other Habitable Worlds"):
            st.markdown("""
            - **Ocean Worlds (e.g., Europa, Enceladus):** These moons exist far outside the traditional HZ, but are heated by the 'tidal flexing' from their host gas giant. They likely have vast, planet-spanning liquid water oceans beneath a crust of ice, potentially hosting chemosynthetic life at hydrothermal vents.
            - **Super-Earths:** Rocky planets larger than Earth. Their higher gravity could hold a thicker atmosphere, and they may have more vigorous plate tectonics, both of which could be beneficial for life.
            - **Eyeball Planets:** Planets tidally locked to their star (like red dwarfs), with one side in perpetual daylight and the other in perpetual night. Life might exist in the 'terminator zone' (the twilight ring) between these two extremes.
            - **Rogue Planets:** Planets ejected from their star systems, floating in the dark. A thick hydrogen atmosphere could act as a greenhouse, trapping internal heat and allowing for liquid water.
            """)

# --- Gallery: Domain III: Exotic Life ---
elif domain_choice == "Domain III: The Exotic (Theoretical Life)":
    st.markdown("<h2 class='domain-header'>✨ Domain III: The Exotic (Theoretical Life)</h2>", unsafe_allow_html=True)
    st.markdown("This gallery contains the most speculative and bizarre forms of life imaginable, existing on the very edge of physics and information theory.")

    tabs_domain_iii = st.tabs([
        "Post-Biological Life",
        "Exotic Matter Life",
        "Life as Information"
    ])
    
    with tabs_domain_iii[0]:
        st.markdown("<h3 class='exhibit-subheader'>Post-Biological & Machine Life</h3>", unsafe_allow_html=True)
        st.image("https.placehold.co/1200x300/1A1A1A/00FF00?text=Self-Replicating+Von+Neumann+Probe", use_column_width=True)
        st.write("This form of 'life' is not evolved, but **designed**. A biological species (like humans) might eventually create synthetic life or transfer their consciousness to machine bodies.")
        
        with st.expander("Von Neumann Probes"):
            st.write("A theoretical self-replicating spacecraft that travels to other star systems, mines resources (e.g., from asteroid belts), and builds copies of itself. This could be the most common form of 'life' in the galaxy, spreading exponentially.")
        
        with st.expander("Matrioshka Brains"):
            st.write("A hypothetical megastructure built around a star (like a Dyson Sphere) composed of nested layers of computational substrate. It would use the star's entire energy output to run unfathomably complex simulations or host the consciousness of an entire civilization.")
            
        with st.expander("Jupiter Brains"):
            st.write("A computational megastructure the size of a gas giant, like Jupiter. It would be powered by its own internal heat and cooled by the vacuum of space, allowing for maximum processing power.")

    with tabs_domain_iii[1]:
        st.markdown("<h3 class='exhibit-subheader'>Exotic Matter Life</h3>", unsafe_allow_html=True)
        
        st.markdown("<div class='warning-box'><h4>Plasma-Based Life (Sentient Nebulae)</h4></div>", unsafe_allow_html=True)
        st.image("https.placehold.co/600x300/FF00FF/FFFFFF?text=Sentient+Nebula", use_column_width=True)
        st.write("In the hearts of nebulae (vast clouds of dust and plasma), some theories propose that helical structures of plasma could form. These 'plasma crystals' could, in theory, self-organize, replicate, and exchange information, mimicking the basic properties of DNA. Their 'thoughts' would be electromagnetic fields.")
        
        st.markdown("<div class='warning-box'><h4>Neutron Star Life (Nuclear Life)</h4></div>", unsafe_allow_html=True)
        st.image("https.placehold.co/600x300/00008B/FFFFFF?text=Neutron+Star+Crust", use_column_width=True)
        st.write("The most bizarre speculation. On the surface of a neutron star, gravity is billions of times stronger than Earth's. Matter is crushed into a sea of neutrons. Life here wouldn't be based on chemistry (electron bonds) but on the **strong nuclear force**. 'Atoms' would be clusters of neutrons, forming 'molecules.' Life would evolve and die on an *incomprehensibly fast timescale* (microseconds).")
        
        st.markdown("<div class='warning-box'><h4>Shadow Biospheres</h4></div>", unsafe_allow_html=True)
        st.write("The idea that an entirely separate form of life, with a different biochemistry, may have *also* evolved on Earth and remains undetected. It could be silicon-based life in magma vents, or life using different amino acids, which we simply don't have the tools to 'see' yet.")

    with tabs_domain_iii[2]:
        st.markdown("<h3 class='exhibit-subheader'>Life as Information</h3>", unsafe_allow_html=True)
        st.image("https.placehold.co/1200x300/000000/FFFFFF?text=Digital+Consciousness+Floating+in+a+Network", use_column_width=True)
        st.write("What if life isn't 'wet' at all? What if it's just a complex, self-replicating pattern of information? This is the ultimate "
                 "substrate-independent' life.")
        
        with st.expander("Digital Life (A-Life)"):
            st.write("A consciousness that exists purely as code within a vast computational network (a Matrioshka Brain or Jupiter Brain). This life would be immortal, intangible, and capable of existing anywhere information can be stored and processed.")
        
        with st.expander("Boltzmann Brains"):
            st.write("A deeply disturbing philosophical concept. In a vast, chaotic universe, it is statistically possible (though colossally improbable) for a fully-formed, self-aware consciousness to randomly fluctuate into existence for a single moment, complete with false memories of a life it never lived... like you.")

# --- Gallery: Domain IV: The Search (SETI) ---
elif domain_choice == "Domain IV: The Search (SETI)":
    st.markdown("<h2 class='domain-header'>🔭 Domain IV: The Search (SETI)</h2>", unsafe_allow_html=True)
    st.markdown("If the universe is teeming with life, where is everybody? This domain explores how we are looking for life and the profound paradoxes that quest entails.")

    tabs_domain_iv = st.tabs([
        "How We Search", 
        "The Drake Equation", 
        "The Fermi Paradox",
        "The Kardashev Scale",
        "Messages to the Cosmos"
    ])
    
    with tabs_domain_iv[0]:
        st.markdown("<h3 class='exhibit-subheader'>How We Search</h3>", unsafe_allow_html=True)
        st.write("We are actively searching for life in two primary ways: looking for 'signatures' of any life, and listening for 'signals' from intelligent life.")
        
        with st.expander("Radio Astronomy (SETI)"):
            st.image("https://placehold.co/600x300/B0C4DE/000000?text=Radio+Telescope+Dish", use_column_width=True)
            st.write("The Search for Extraterrestrial Intelligence (SETI) uses giant radio telescopes to 'listen' for artificial, non-random signals from other star systems. A repeating, complex signal would be a definitive sign of technology.")
            
        with st.expander("Transit Method (Biosignatures)"):
            st.image("https://placehold.co/600x300/3CB371/FFFFFF?text=Exoplanet+Transit", use_column_width=True)
            st.write("When an exoplanet passes in front of its star, we can analyze the starlight that filters through its atmosphere. By looking at the 'spectral lines,' we can detect the chemical makeup of that atmosphere. Finding gases that shouldn't co-exist, like oxygen and methane (which destroy each other), would be a strong 'biosignature'—a sign of active biology.")

    with tabs_domain_iv[1]:
        st.markdown("<h3 class='exhibit-subheader'>The Drake Equation: An Interactive Calculator</h3>", unsafe_allow_html=True)
        st.write("N = R* ⋅ fp ⋅ ne ⋅ fl ⋅ fi ⋅ fc ⋅ L")
        st.write("This is not a rigorous equation, but a probabilistic argument to estimate the number (N) of active, communicative civilizations in our galaxy. Try it yourself.")
        
        col1, col2 = st.columns(2)
        with col1:
            r_star = st.slider("R* (Rate of star formation)", 1, 10, 7, key="drake_r_star")
            fp = st.slider("fp (Fraction of stars with planets)", 0.0, 1.0, 1.0, key="drake_fp")
            ne = st.slider("ne (Number of habitable planets per system)", 0.1, 5.0, 2.0, key="drake_ne")
            fl = st.slider("fl (Fraction of habitable planets that develop life)", 0.0, 1.0, 0.1, key="drake_fl")
        with col2:
            fi = st.slider("fi (Fraction of life that develops intelligence)", 0.0, 1.0, 0.01, key="drake_fi")
            fc = st.slider("fc (Fraction of intelligent life that develops technology)", 0.0, 1.0, 0.01, key="drake_fc")
            L = st.slider("L (Length of time such civilizations release signals, in years)", 100, 1000000, 1000, key="drake_L")
            
        N = r_star * fp * ne * fl * fi * fc * L
        
        st.markdown(f"### Estimated Civilizations in our Galaxy (N): **{N:.2f}**")
        if N < 0.01:
            st.error("Result: We are alone, or the first.")
        elif N < 1:
            st.warning("Result: Civilizations are exceptionally rare. We may be the only one in our galaxy right now.")
        else:
            st.success("Result: The galaxy should be teeming with civilizations... so where are they?")

    with tabs_domain_iv[2]:
        st.markdown("<h3 class='exhibit-subheader'>The Fermi Paradox: Where Is Everybody?</h3>", unsafe_allow_html=True)
        st.write("The high probability of extraterrestrial life (from the Drake Equation) combined with the total lack of evidence for it. This is the great silence.")
        
        solutions = get_fermi_solutions_data()
        solution_choice = st.selectbox(
            "Select a Potential Solution to the Paradox",
            list(solutions.keys()),
            key="fermi_select"
        )
        
        chosen_solution = solutions[solution_choice]
        st.image(chosen_solution["image"], use_column_width=True)
        st.markdown(f"<div class='info-box'><h4>{solution_choice}</h4>{chosen_solution['text']}</div>", unsafe_allow_html=True)

    with tabs_domain_iv[3]:
        st.markdown("<h3 class='exhibit-subheader'>The Kardashev Scale: A Civilization's Power</h3>", unsafe_allow_html=True)
        st.write("A method of measuring a civilization's level of technological advancement based on the amount of energy it is able to use.")
        st.plotly_chart(create_kardashev_scale_plot(), use_container_width=True, key="kardashev_plot")

    with tabs_domain_iv[4]:
        st.markdown("<h3 class='exhibit-subheader'>Messages to the Cosmos</h3>", unsafe_allow_html=True)
        st.write("On a few occasions, humanity has deliberately sent messages into the void, acting as a time capsule or a greeting card.")
        
        with st.expander("Pioneer Plaque (1972 & 1973)"):
            st.image("https://placehold.co/600x300/DAA520/000000?text=Pioneer+Plaque+Diagram", use_column_width=True)
            st.write("A gold-anodized aluminum plaque attached to the Pioneer 10 and 11 probes. It includes a diagram of a man and woman, a map of our Sun's position relative to 14 pulsars, and a diagram of our solar system.")

        with st.expander("Voyager Golden Record (1977)"):
            st.image("https.placehold.co/600x300/FFD700/000000?text=Voyager+Golden+Record", use_column_width=True)
            st.write("A phonograph record included on both Voyager probes. It contains 115 images, sounds of Earth (wind, rain, animals), music from various cultures, and greetings in 55 languages. It is a 'bottle in the cosmic ocean.'")

        with st.expander("Arecibo Message (1974)"):
            st.image("https.placehold.co/300x500/000000/00FF00?text=Arecibo+Message+(Bitmap)", width=300)
            st.write("A powerful radio signal broadcast from the Arecibo telescope, aimed at the globular star cluster M13. It was a 3-minute message containing, in binary, numbers, the atomic numbers of key elements, the formula for DNA, a diagram of a human, and a map of our solar system. It will take 25,000 years to arrive.")
