# ============================================================================
# SAFEHAVEN AI - ULTRA UI FRONTEND
# ============================================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_image_comparison import image_comparison
import time
import os
import sys

# Add backend path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -----------------------------------------------------------------------------
# 1. SETUP & CSS INJECTION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SafeHaven AI",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def inject_custom_css():
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
    # Inject Background Asset (Video or Image)
    # Priority: 1. Local 'background.mp4' 2. Local 'background_frame.png' 3. Local 'repaired.png'
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    bg_video_path = os.path.join(BASE_DIR, 'background.mp4')
    # Use the new "Cinematic Frame" as result of the video generation
    bg_image_path = os.path.join(BASE_DIR, "img", "background_frame.png")
    
    bg_element = ""
    
    if os.path.exists(bg_video_path):
        # User provided video
        with open(bg_video_path, "rb") as v:
            video_bytes = v.read()
            b64_video = base64.b64encode(video_bytes).decode()
            
        bg_element = f"""
            <video autoplay muted loop playsinline class="video-background">
                <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
            </video>
        """
    elif os.path.exists(bg_image_path):
        # Fallback to Cinematic Frame
        # NOTE: Using standard string (not f-string) for the template to avoid brace confusion
        # IMPORTANT: Removing indentation to prevent Markdown code block rendering
        bg_element = """
<style>
.video-background {
    background-image: url("data:image/png;base64,__IMG_BASE64__");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}
</style>
<div class="video-background"></div>
"""
        import base64
        with open(bg_image_path, "rb") as img:
            b64_img = base64.b64encode(img.read()).decode()
            bg_element = bg_element.replace("__IMG_BASE64__", b64_img)
    else:
        # Emergency Fallback
        bg_element = """<div class="video-background" style="background: linear-gradient(135deg, #000, #111);"></div>"""

    st.markdown(f"""
        <style>
            /* Critical: Force Streamlit containers to be transparent */
            .stApp {{ background: transparent !important; }}
            [data-testid="stAppViewContainer"] {{ background: transparent !important; }}
            [data-testid="stHeader"] {{ background: transparent !important; }}
            
            .video-background {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                z-index: -100;
                object-fit: cover;
                filter: brightness(0.7) contrast(1.2); /* High Contrast for Nike Vibe */
                pointer-events: none;
            }}
            
            /* KPI Alignment Fix */
            .kpi-value {{
                white-space: nowrap; /* Prevent wrapping */
                overflow: hidden;
                text-overflow: ellipsis;
                font-size: clamp(2rem, 3.5vw, 3.5rem) !important; /* Slightly reduced max size */
            }}
        </style>
        {bg_element}
    """, unsafe_allow_html=True)


inject_custom_css()

# Initialize Session State
if 'selected_room' not in st.session_state:
    st.session_state.selected_room = "Kitchen"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
    


# -----------------------------------------------------------------------------
# 2. SIDEBAR (THE COMMAND CENTER)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🏗️ SafeHaven")
    st.caption("v2.0.4 | Ultra-Secure")
    
    # Inspector Profile
    st.markdown("""
        <div style="display: flex; align-items: center; margin-bottom: 20px;">
            <div style="width: 40px; height: 40px; background-color: #D0FF00; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; color: black;">JD</div>
            <div style="margin-left: 10px;">
                <div style="font-weight: 600; text-transform: uppercase; font-family: 'Oswald'; letter-spacing: 1px;">John Doe</div>
                <div style="font-size: 0.7em; color: #777; text-transform: uppercase;">Lead Inspector</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Property Filter
    st.selectbox("📍 Property Selector", ["123 Maple Street", "The Glass Penthouse", "Industrial Lofts A"])
    
    # Upload Zone
    st.markdown("### 📤 Upload Assets")
    st.file_uploader("Inspection Data", type=['png', 'jpg', 'wav'], accept_multiple_files=True, key="uploaded_evidence")
    
    st.info("System Ready. Connected to Snowflake Cortex.", icon="🟢")

# -----------------------------------------------------------------------------
# 3. MAIN DASHBOARD (MISSION CONTROL)
# -----------------------------------------------------------------------------

# Hero Section: KPI Cards (Row 1)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

def render_kpi(col, label, value, delta=None, color=""):
    with col:
        st.markdown(f"""
        <div class="glass-card kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {f'<div style="color: {color}; font-size: 0.8rem;">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

# Demo Data Engine for Dynamic Experience
ROOM_DATA = {
    "Kitchen": {"score": "82/100", "defects": "3", "cost": "$4,250", "legal": "1", "delta_score": "▲ 2%", "delta_defects": "▼ 1 Resolved"},
    "Bedroom": {"score": "95/100", "defects": "0", "cost": "$0", "legal": "0", "delta_score": "▲ 5%", "delta_defects": "All Clear"},
    "Bath": {"score": "65/100", "defects": "5", "cost": "$8,100", "legal": "3", "delta_score": "▼ 12%", "delta_defects": "▲ 2 New"},
    "Living": {"score": "88/100", "defects": "1", "cost": "$850", "legal": "0", "delta_score": "━ Stable", "delta_defects": "Minor"}
}

current_data = ROOM_DATA.get(st.session_state.selected_room, ROOM_DATA["Kitchen"])

render_kpi(kpi1, "Habitability Score", current_data["score"], current_data["delta_score"], "#D0FF00" if "▲" in current_data["delta_score"] else "#FF2E2E")
render_kpi(kpi2, "Critical Defects", current_data["defects"], current_data["delta_defects"], "#FF2E2E" if int(current_data["defects"]) > 0 else "#D0FF00")
render_kpi(kpi3, "Est. Repair Cost", current_data["cost"], "Based on local materials", "#FFAA00")
render_kpi(kpi4, "Legal Violations", current_data["legal"], "Requires Permits" if int(current_data["legal"]) > 0 else "Compliant", "#29B5E8")

# Split Layout (Row 2)
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown("### 🗺️ Interactive Floor Plan")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Dummy 2x2 Grid for Floor Plan
    # User clicks button -> Updates session state
    r1_c1, r1_c2 = st.columns(2)
    r2_c1, r2_c2 = st.columns(2)
    
    def room_btn(col, name, icon):
        if col.button(f"{icon} {name}", use_container_width=True, key=name):
            st.session_state.selected_room = name
            
    room_btn(r1_c1, "Kitchen", "🍽️")
    room_btn(r1_c2, "Bedroom", "🛏️")
    room_btn(r2_c1, "Bath", "🚽")
    room_btn(r2_c2, "Living", "🛋️")
    
    st.markdown(f"**Currently Monitoring:** `{st.session_state.selected_room}`")
    st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    st.markdown("### 🤖 SafeBot")
    # Fixed height chat window simulation
    chat_container = st.container(height=300)
    
    with chat_container:
        if not st.session_state.chat_history:
             st.session_state.chat_history.append({"role": "assistant", "content": f"Hello! analyzing data for {st.session_state.selected_room}. Ask me anything."})
        
        for msg in st.session_state.chat_history:
            st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("Query Cortex..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        # Mock Response
        response = "Based on Article 210 of the NEC, that outlet requires GFCI protection."
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()

# -----------------------------------------------------------------------------
# 4. THE INSPECTION DECK (DETAILED FINDINGS)
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 5. CINEMATIC REPAIR (HIGGSFIELD VIDEO) & DIGITAL TWIN
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown(f"## 🔍 Inspection Deck: {st.session_state.selected_room}")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["👁️ Visual Repairs", "🔊 Audio Forensics", "⚖️ Legal Shield", "💰 Smart Estimate", "🧊 Digital Twin"])

with tab5:
    st.markdown("### 3D Spatial Twin")
    st.markdown("Interact with the **LiDAR Scan** of the property. Rotate, zoom, and measure directly in the browser.")
    
    # Embed a 3D Viewer (Sketchfab Mock)
    # Using a reliable public architectural scan (Van Gogh Room style or similar robust ID)
    sketchfab_embed = """
    <div class="viewer-3d-container">
        <iframe title="Lidar Room Scan" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share src="https://sketchfab.com/models/442c548d94744641ba879119c58b9e58/embed?autostart=1&ui_controls=1&ui_infos=0&ui_inspector=0&ui_stop=0&ui_watermark=0&ui_watermark_link=0" style="width: 100%; height: 500px;">
        </iframe>
    </div>
    """
    st.components.v1.html(sketchfab_embed, height=520)
    
    c3d_1, c3d_2 = st.columns(2)
    with c3d_1:
         st.markdown("""
         <div class="glass-card">
            <h4>📐 Dimensions</h4>
            <div style="display:flex; justify-content:space-between; color:#777;">
                <span>Ceiling Height:</span> <span style="color:white; font-weight:bold;">9' 6"</span>
            </div>
            <div style="display:flex; justify-content:space-between; color:#777;">
                <span>Total Area:</span> <span style="color:white; font-weight:bold;">245 sq ft</span>
            </div>
         </div>
         """, unsafe_allow_html=True)
    with c3d_2:
        st.button("Scan New Room (LiDAR)", use_container_width=True)

with tab1:
    st.markdown("### 👁️ Visual Repairs & Cinematic Restoration")
    
    # Visual Comparison Only (Video is now pervasive background)
    st.markdown("**Defect vs. Restoration**")
    
    # Resolve Paths Absolutely to avoid "frontend/frontend" errors
    # __file__ is inside frontend/, so we look in ./img/relative_to_frontend
    BASE_FRONTEND_DIR = os.path.dirname(os.path.abspath(__file__))
    IMG_DIR = os.path.join(BASE_FRONTEND_DIR, "img")
    
    def get_asset_path(filename):
        return os.path.join(IMG_DIR, filename)

    # Dynamic Image Map based on Room Context
    # Fallback to 'defect_matched.png' (Kitchen style) if room specific not found
    IMAGE_MAP = {
        "Kitchen": ("defect_matched.png", "repaired_matched.png"),
        "Bedroom": ("bedroom_defect.png", "bedroom_repaired.png"),
        "Bath": ("bath_defect.png", "bath_repaired.png"),
        "Living": ("defect_matched.png", "repaired_matched.png") # Reusing kitchen/living style for now
    }
    
    
    # -----------------------------------------------------------------------------
    # LOGIC: Check for User Uploads to override Room Defaults
    # -----------------------------------------------------------------------------
    
    # Helper: "AI Restoration" Algorithm (Generative Proxy)
    # Replaces pixel-based smoothing with High-Fidelity Generative Assets ("Concept Restoration")
    from PIL import Image, ImageEnhance, ImageFilter, ImageOps
    
    def process_and_resize(img_obj, target_width=1200, target_height=600):
        # Resize to fixed banner style dimensions
        return img_obj.resize((target_width, target_height))

    def simulate_restoration(img_obj, scene_type="Kitchen"):
        """
        Uses a high-quality "After" image as a restoration target.
        This provides a 'Construction Vision' look.
        """
        # Determine which HQ asset to use
        if "bath" in scene_type.lower():
             hq_asset_name = "restored_bath_hq.png"
        else:
             hq_asset_name = "restored_kitchen_hq.png"
             
        hq_path = get_asset_path(hq_asset_name)
        
        if os.path.exists(hq_path):
            restored = Image.open(hq_path)
        else:
            # Fallback if asset missing (should not happen)
            restored = img_obj.filter(ImageFilter.MedianFilter(size=5))
            
        # Optional: We could color-match the restored image to the original, but usually 
        # users want to see the "New" look, not the old dirty colors.
        
        return restored

    user_upload = st.session_state.get("uploaded_evidence", [])
    
    if user_upload:
        # Scene Context Detection
        # In production, this call routes to `cortex.classify(image)`
        detected_scene = "Bath / Sanitary" if "bath" in st.session_state.selected_room.lower() else "Kitchen / Interior"
        
        st.success(f"⚡ Cortex Analysis Complete: Detected **{detected_scene}**", icon="🤖")
        # Visual Comparison: User Upload vs. AI Restoration of THAT upload
        
        original_pil = Image.open(user_upload[0])
        
        # 1. Generate the "Restored" version using the HQ Proxy
        restored_pil = simulate_restoration(original_pil, scene_type=detected_scene)
        
        # 2. Resize both for height control
        img1_source = process_and_resize(original_pil)
        # We resize the HQ asset to match the container, disregarding aspect ratio slightly for the banner effect
        # or we could center crop. For now, simple resize is robust.
        img2_source = process_and_resize(restored_pil)
        
        label_1_text = f"Evidence ({st.session_state.selected_room})"
        label_2_text = f"Vision: {detected_scene}"
        
    else:
        # Standard Room Logic
        room_key = st.session_state.selected_room if st.session_state.selected_room in IMAGE_MAP else "Kitchen"
        defect_file, repair_file = IMAGE_MAP[room_key]

        # Prefer Matched assets, fallback to standard
        d_path = get_asset_path(defect_file)
        if not os.path.exists(d_path): d_path = get_asset_path("defect.png")
        
        r_path = get_asset_path(repair_file)
        if not os.path.exists(r_path): r_path = get_asset_path("repaired.png")
        
        # Load and Resize Defaults
        try:
            p1 = Image.open(d_path) if os.path.exists(d_path) else None
            p2 = Image.open(r_path) if os.path.exists(r_path) else None
            
            if p1 and p2:
                 img1_source = process_and_resize(p1)
                 img2_source = process_and_resize(p2)
            else:
                 # Fallback URLS (Can't resize easily without downloading, assuming they work)
                 img1_source = "https://images.unsplash.com/photo-1582281298055-e25b84a30b0b?q=80&w=1000"
                 img2_source = "https://images.unsplash.com/photo-1560185127-6ed189bf02f4?q=80&w=1000"
        except Exception:
             # Safety net
             img1_source = "https://images.unsplash.com/photo-1582281298055-e25b84a30b0b?q=80&w=1000"
             img2_source = "https://images.unsplash.com/photo-1560185127-6ed189bf02f4?q=80&w=1000"

        label_1_text = f"Recorded: {st.session_state.selected_room}"
        label_2_text = "Cortex Restoration"

    # Full Width Experience (Values adjusted for "Easy View")
    image_comparison(
        img1=img1_source,
        img2=img2_source,
        label1=label_1_text,
        label2=label_2_text,
        width=1200, 
        starting_position=50,
        show_labels=True
    )
    
    # 3D Depth Analysis Section (New)
    st.markdown("### 🧊 3D Lidar & Depth Analysis")
    with st.expander("View 3D Sensor Data", expanded=True):
        c_depth1, c_depth2 = st.columns([2,1])
        with c_depth1:
            depth_path = get_asset_path("depth_map.png")
            if os.path.exists(depth_path):
                st.image(depth_path, caption="Lidar Depth Heatmap (cm accuracy)", use_container_width=True)
            else:
                st.info("Depth map generating...")
        with c_depth2:
            st.markdown("""
            <div class="glass-card">
                <h4>SCAN METRICS</h4>
                <div style="font-family:monospace; color:#D0FF00;">
                Points: 12,405,992<br>
                Density: 400 pts/sqft<br>
                Surface: <b>Roughness Detected</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 🔊 Audio Forensics")
    a_c1, a_c2 = st.columns([1, 2])
    with a_c1:
        st.markdown("**Recorded Sample**")
        st.audio("https://www2.cs.uic.edu/~i101/SoundFiles/BabyElephantWalk60.wav")
        st.caption("Tap test recorded at 14:02 PM")
    with a_c2:
        st.markdown("**Substrate Resonance**")
        # Mock Spec Data
        chart_data = pd.DataFrame(np.random.randn(50).cumsum(), columns=["Hollowness"])
        st.line_chart(chart_data, height=200)
        st.markdown("""<div class="status-badge badge-warning">⚠️ Low Density Detected</div>""", unsafe_allow_html=True)

with tab3:
    st.markdown("### ⚖️ Legal Shield Compliance")
    st.markdown("""
        <div class="legal-box">
            <h4>⚠️ Violation: IBC Section 2509.2</h4>
            <p>"Water-resistant gypsum backing board shall not be used in the following locations... where there will be direct exposure to water."</p>
            <hr style="border-color: #333;">
            <p style="font-size: 0.8em; color: #888;">Cited from: International Building Code (2024 Edition)</p>
        </div>
    """, unsafe_allow_html=True)
    l_c1, l_c2 = st.columns(2)
    with l_c1: st.button("📄 Generate Official Citation Report", use_container_width=True)
    with l_c2: st.button("🚩 Flag for Human Review", use_container_width=True)

with tab4:
    st.markdown("### 💰 Smart Cost Estimator")
    st.markdown("AI-driven repair cost estimation based on severity and local market rates.")
    
    ce_c1, ce_c2 = st.columns(2)
    with ce_c1:
        d_type = st.selectbox("Defect Type", ["water_damage", "structural_crack", "electrical_fault"])
        severity = st.slider("Severity Score", 0, 100, 85)
    with ce_c2:
        region = st.slider("Market Factor (Regional)", 0.8, 1.5, 1.2)
        if st.button("Calculate Estimate", type="primary", use_container_width=True):
             # Simple inline calc or import
             base = 500
             total = base * (severity/20) * region
             st.metric("Estimated Cost", f"${total:,.2f}")

# -----------------------------------------------------------------------------
# 6. SAFEBOT INTERFACE (BOTTOM)
