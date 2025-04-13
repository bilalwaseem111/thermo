import streamlit as st # type: ignore
import matplotlib.pyplot as plt # type: ignore
import numpy as np # type: ignore
import io
from streamlit.components.v1 import html # type: ignore

# Page Configuration
st.set_page_config(
    page_title="My Thermodynamics Toolbox",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def load_css():
    st.markdown("""
    <style>
        :root {
            --primary: #2563eb;
            --secondary: #1e40af;
            --accent: #f59e0b;
            --accent2: #10b981;
            --dark: #1e293b;
            --light: #f8fafc;
            --glass-bg: rgba(255, 255, 255, 0.1);
            --border-radius: 12px;
            --box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0f172a, #1e293b);
            color: var(--light);
            margin: 0;
            padding: 0;
            min-height: 100vh;
        }

        .main-title {
            text-align: center;
            font-size: 4.5rem;
            font-weight: 900;
            letter-spacing: 2px;
            margin: 2rem 0;
            background: linear-gradient(90deg, #00f5ff, #8a2be2, #00f5ff);
            background-size: 200% auto;
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            animation: glow 3s ease-in-out infinite alternate, gradientShift 6s ease-in-out infinite;
            text-shadow: 0 0 10px rgba(138, 43, 226, 0.5), 0 0 20px rgba(0, 245, 255, 0.3);
            padding-bottom: 0.75rem;
            border-bottom: 3px solid rgba(255, 255, 255, 0.15);
        }

        @keyframes glow {
            0% {
                text-shadow: 0 0 5px rgba(0, 245, 255, 0.4), 0 0 10px rgba(138, 43, 226, 0.3);
            }
            100% {
                text-shadow: 0 0 20px rgba(0, 245, 255, 0.7), 0 0 40px rgba(138, 43, 226, 0.5);
            }
        }

        @keyframes gradientShift {
            0% {
                background-position: 0% center;
            }
            100% {
                background-position: 200% center;
            }
        }

        .section-title {
            font-size: 2rem;
            font-weight: 700;
            margin: 1.5rem 0 1rem;
            background: linear-gradient(to right, #f59e0b, #f97316);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid rgba(245, 158, 11, 0.3);
        }

        .sub-heading {
            text-align: center;
            font-size: 1.25rem;
            color: #94a3b8;
            margin-bottom: 2rem;
            font-style: italic;
        }

        .concept-card {
            background: rgba(30, 41, 59, 0.7);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: var(--box-shadow);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: transform 0.3s ease;
        }

        .concept-card:hover {
            transform: translateY(-5px);
            border-color: var(--accent);
        }

        .concept-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--accent);
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .calculator-card {
            background: rgba(30, 41, 59, 0.7);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--box-shadow);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .calculator-card:hover {
            border-color: var(--accent);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
        }

        .calculator-title {
            font-size: 1.3rem;
            margin-bottom: 1rem;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .result-card {
            background: rgba(37, 99, 235, 0.15);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-top: 1.5rem;
            border-left: 4px solid var(--accent);
            animation: fadeIn 0.5s ease-out;
        }

        .result-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent2);
            margin: 0.5rem 0;
        }

        .celebration {
            display: inline-block;
            animation: bounce 0.5s ease infinite alternate;
            margin-left: 0.5rem;
        }

        .footer {
            text-align: center;
            margin-top: 5rem;
            padding: 1.5rem;
            color: black;
            font-size: 2rem;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }

        .linkedin-link {
            display: inline-flex;
            align-items: center;
            gap: 0.3rem;
            color: #0a66c2 !important;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        .linkedin-link:hover {
            color: #38bdf8 !important;
            text-decoration: underline;
        }

        .linkedin-logo {
            height: 1.8rem;
            filter: drop-shadow(0 0 5px rgba(10, 102, 194, 0.7));
            transition: all 0.3s ease;
        }

        .linkedin-logo:hover {
            filter: drop-shadow(0 0 10px rgba(56, 189, 248, 0.9));
            transform: scale(1.1);
        }

        /* Consistent Calculate Button Styling */
        .stButton>button {
            width: 100% !important;
            border-radius: var(--border-radius) !important;
            background: linear-gradient(to right, var(--primary), var(--secondary)) !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 0.5rem 1rem !important;
            border: none !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
            transition: all 0.3s ease !important;
            height: 42px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15) !important;
            background: linear-gradient(to right, var(--secondary), var(--primary)) !important;
        }

        .stButton>button:active {
            transform: translateY(0) !important;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-5px); }
        }

        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-title {
                font-size: 2.5rem;
            }
            .section-title {
                font-size: 1.8rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)

load_css()

# Celebration animations
def show_confetti():
    html("""
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.4.0/dist/confetti.browser.min.js"></script>
    <script>
        confetti({
            particleCount: 150,
            spread: 70,
            origin: { y: 0.6 },
            colors: ['#f59e0b', '#10b981', '#3b82f6']
        });
    </script>
    """)

# Main App Content
st.markdown("""
    <h1 class='main-title'>Thermodynamics Toolbox</h1>
    <p class='sub-heading'>Professional-grade thermodynamic calculations and visualizations for engineers and scientists</p>
""", unsafe_allow_html=True)

# Thermodynamics Concepts Section
st.markdown('<div class="section-title">Imp Thermodynamics Concepts</div>', unsafe_allow_html=True)

concept_col1, concept_col2 = st.columns(2)

with concept_col1:
    with st.container():
        st.markdown("""
        <div class="concept-card">
            <div class="concept-title">🌡️ Zeroth Law of Thermodynamics</div>
            <p>Defines temperature and thermal equilibrium. If two systems are each in thermal equilibrium with a third, they are in equilibrium with each other.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class="concept-card">
            <div class="concept-title">⚡ First Law of Thermodynamics</div>
            <p>Energy cannot be created or destroyed, only transformed (ΔU = Q - W). The total energy of an isolated system is constant.</p>
        </div>
        """, unsafe_allow_html=True)

with concept_col2:
    with st.container():
        st.markdown("""
        <div class="concept-card">
            <div class="concept-title">🌀 Second Law of Thermodynamics</div>
            <p>Entropy of an isolated system never decreases. Heat cannot spontaneously flow from colder to hotter bodies (Clausius statement).</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown("""
        <div class="concept-card">
            <div class="concept-title">❄️ Third Law of Thermodynamics</div>
            <p>As temperature approaches absolute zero, the entropy of a perfect crystal approaches a constant minimum.</p>
        </div>
        """, unsafe_allow_html=True)

# Calculation Functions
def fig_to_bytes(fig):
    """Convert matplotlib figure to bytes for download"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    buf.seek(0)
    return buf

def entropy_calculator():
    with st.form("entropy_form", clear_on_submit=False):
        st.markdown('<div class="calculator-title">📈 Entropy Calculator (ΔS = Q/T)</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            Q = st.number_input("Heat (Q) [kJ]", min_value=0.0, step=0.1, key="entropy_Q", format="%.2f")
        with col2:
            T = st.number_input("Temp (T) [K]", min_value=0.1, step=0.1, key="entropy_T", format="%.2f")
        
        submitted = st.form_submit_button("Calculate")
        
        if submitted and T > 0:
            ΔS = Q / T
            show_confetti()
            st.markdown(f"""
            <div class='result-card'>
                <div>Entropy Change: <span class='result-value'>{ΔS:.4f} kJ/K <span class='celebration'>🎉</span></span></div>
                <div>ΔS = Q/T = {Q:.2f}/{T:.2f}</div>
                <div><small>For reversible processes, entropy change indicates system disorder</small></div>
            </div>
            """, unsafe_allow_html=True)
        elif submitted:
            st.error("Temperature must be > 0K")

def enthalpy_calculator():
    with st.form("enthalpy_form", clear_on_submit=False):
        st.markdown('<div class="calculator-title">🔥 Enthalpy Calculator (ΔH = U + PΔV)</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            U = st.number_input("Internal Energy [kJ]", step=0.1, key="enthalpy_U", format="%.2f")
        with col2:
            P = st.number_input("Pressure [kPa]", min_value=0.0, step=0.1, key="enthalpy_P", format="%.2f")
        with col3:
            ΔV = st.number_input("ΔVolume [m³]", step=0.0001, format="%.4f", key="enthalpy_V")
        
        submitted = st.form_submit_button("Calculate")
        
        if submitted:
            ΔH = U + (P * ΔV)
            show_confetti()
            st.markdown(f"""
            <div class='result-card'>
                <div>Enthalpy Change: <span class='result-value'>{ΔH:.4f} kJ <span class='celebration'>🔥</span></span></div>
                <div>ΔH = U + PΔV = {U:.2f} + {P:.2f}×{ΔV:.4f}</div>
                <div><small>Enthalpy represents total heat content of a system</small></div>
            </div>
            """, unsafe_allow_html=True)

def work_calculator():
    with st.form("work_form", clear_on_submit=False):
        st.markdown('<div class="calculator-title">⚡ Work Calculator (W = PΔV)</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            P = st.number_input("Pressure [kPa]", min_value=0.0, step=0.1, key="work_P", format="%.2f")
        with col2:
            ΔV = st.number_input("ΔVolume [m³]", step=0.0001, format="%.4f", key="work_V")
        
        submitted = st.form_submit_button("Calculate")
        
        if submitted:
            W = P * ΔV
            show_confetti()
            st.markdown(f"""
            <div class='result-card'>
                <div>Work Done: <span class='result-value'>{W:.4f} kJ <span class='celebration'>💪</span></span></div>
                <div>W = PΔV = {P:.2f} × {ΔV:.4f}</div>
                <div><small>Positive work indicates work done by the system</small></div>
            </div>
            """, unsafe_allow_html=True)

def efficiency_calculator():
    with st.form("efficiency_form", clear_on_submit=False):
        st.markdown('<div class="calculator-title">📊 Efficiency Calculator (η = W_out/Q_in)</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            W_out = st.number_input("Work Out [kJ]", min_value=0.0, step=0.1, key="eff_W", format="%.2f")
        with col2:
            Q_in = st.number_input("Heat In [kJ]", min_value=0.1, step=0.1, key="eff_Q", format="%.2f")
        
        submitted = st.form_submit_button("Calculate")
        
        if submitted and Q_in > 0:
            η = (W_out / Q_in) * 100
            show_confetti()
            st.markdown(f"""
            <div class='result-card'>
                <div>Efficiency: <span class='result-value'>{η:.2f}% <span class='celebration'>🚀</span></span></div>
                <div>η = (W_out/Q_in) × 100 = ({W_out:.2f}/{Q_in:.2f}) × 100</div>
                <div><small>Carnot efficiency is the theoretical maximum for heat engines</small></div>
            </div>
            """, unsafe_allow_html=True)
        elif submitted:
            st.error("Heat input must be > 0")

# Calculations Section
st.markdown('<div class="section-title">Thermodynamic Calculations</div>', unsafe_allow_html=True)

# Layout - 4 calculators in one row
col1, col2, col3, col4 = st.columns(4)
with col1:
    with st.container():
        entropy_calculator()
with col2:
    with st.container():
        enthalpy_calculator()
with col3:
    with st.container():
        work_calculator()
with col4:
    with st.container():
        efficiency_calculator()

# Diagrams Section
st.markdown('<div class="section-title"> Thermodynamic Diagrams</div>', unsafe_allow_html=True)
generate_diagram = st.checkbox("Show Diagram Generator", value=False)

if generate_diagram:
    def generate_diagram():
        with st.container():
            st.markdown('<div class="diagram-container">', unsafe_allow_html=True)
            
            diagram_type = st.radio("Choose Diagram Type:", 
                                   ["T-S Diagram", "P-V Diagram", "P-T Diagram"], 
                                   horizontal=True)
            
            if diagram_type == "T-S Diagram":
                st.markdown('<p class="plot-title">Temperature-Entropy Diagram</p>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    t_min = st.slider("Min Temp (K)", 200, 500, 300)
                    t_max = st.slider("Max Temp (K)", 300, 1000, 600)
                with col2:
                    s_min = st.slider("Min Entropy (kJ/kg·K)", 1, 3, 1)
                    s_max = st.slider("Max Entropy (kJ/kg·K)", 3, 10, 7)
                    process_type = st.selectbox("Process Type", ["Isentropic", "Isothermal", "Polytropic"])
                
                s = np.linspace(s_min, s_max, 200)
                if process_type == "Isentropic":
                    t = np.linspace(t_min, t_max, 200)
                elif process_type == "Isothermal":
                    t = np.full_like(s, (t_min + t_max) / 2)
                else:
                    t = t_min + (t_max - t_min) * (s - s_min) / (s_max - s_min)
                
                fig, ax = plt.subplots(figsize=(4, 2.5))  
                ax.plot(s, t, 'r-', linewidth=2)
                ax.set_xlabel("Entropy (S) [kJ/kg·K]")
                ax.set_ylabel("Temperature (T) [K]")
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.set_title(f"{process_type} Process")
                st.pyplot(fig)
            
            elif diagram_type == "P-V Diagram":
                st.markdown('<p class="plot-title">Pressure-Volume Diagram</p>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    p_min = st.slider("Min Pressure (kPa)", 100, 500, 200)
                    p_max = st.slider("Max Pressure (kPa)", 500, 2000, 1000)
                with col2:
                    v_min = st.slider("Min Volume (m³/kg)", 0.1, 1.0, 0.2)
                    v_max = st.slider("Max Volume (m³/kg)", 1.0, 5.0, 3.0)
                    process_type = st.selectbox("Process Type", ["Isobaric", "Isochoric", "Isothermal"])
                
                v = np.linspace(v_min, v_max, 200)
                if process_type == "Isothermal":
                    p = (p_max * v_min) / v
                elif process_type == "Isobaric":
                    p = np.full_like(v, (p_min + p_max) / 2)
                else:
                    p = np.linspace(p_min, p_max, 200)
                    v = np.full_like(p, (v_min + v_max) / 2)
                
                fig, ax = plt.subplots(figsize=(4, 2.5))
                ax.plot(v, p, 'b-', linewidth=2)
                ax.set_xlabel("Volume (V) [m³/kg]")
                ax.set_ylabel("Pressure (P) [kPa]")
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.set_title(f"{process_type} Process")
                st.pyplot(fig)
            
            elif diagram_type == "P-T Diagram":
                st.markdown('<p class="plot-title">Pressure-Temperature Diagram</p>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    p_min = st.slider("Min Pressure (kPa)", 100, 500, 200)
                    p_max = st.slider("Max Pressure (kPa)", 500, 2000, 1000)
                with col2:
                    t_min = st.slider("Min Temp (K)", 200, 500, 300)
                    t_max = st.slider("Max Temp (K)", 300, 1000, 600)
                    process_type = st.selectbox("Process Type", ["Isobaric", "Isothermal"])
                
                t = np.linspace(t_min, t_max, 200)
                if process_type == "Isobaric":
                    p = np.full_like(t, (p_min + p_max) / 2)
                else:
                    p = np.linspace(p_min, p_max, 200)
                    t = np.full_like(p, (t_min + t_max) / 2)
                
                fig, ax = plt.subplots(figsize=(4, 2.5))
                ax.plot(t, p, 'g-', linewidth=2)
                ax.set_xlabel("Temperature (T) [K]")
                ax.set_ylabel("Pressure (P) [kPa]")
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.set_title(f"{process_type} Process")
                st.pyplot(fig)
            
            st.markdown("</div>", unsafe_allow_html=True)

    generate_diagram()

# Footer
st.markdown("""
<div class="footer">
    <p>Made by Bilal Waseem 
    <a href="https://www.linkedin.com/in/bilal-waseem-b44006338" class="linkedin-link" target="_blank">
        <img src="https://content.linkedin.com/content/dam/me/business/en-us/amp/brand-site/v2/bg/LI-Bug.svg.original.svg" class="linkedin-logo" alt="LinkedIn">
    </a>
    </p>
</div>
""", unsafe_allow_html=True)
