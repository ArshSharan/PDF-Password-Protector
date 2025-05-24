import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO
from streamlit_extras.stylable_container import stylable_container

st.set_page_config(
    page_title="🔒 PDF Password Protector",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;500;700&display=swap');
    
    :root {
        --primary: #00f0ff;
        --secondary: #ff00ff;
        --dark: #0a0a12;
        --light: #f0f0ff;
        --accent: #7b2dff;
    }
    
    html, body, [class*="css"] {
        font-family: 'Rajdhani', sans-serif;
        background-color: var(--dark);
        color: var(--light);
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        color: var(--primary) !important;
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
        letter-spacing: 2px;
    }
    
    .stApp {
        background-color: var(--dark);
        background-image: radial-gradient(circle at 20% 30%, rgba(123, 45, 255, 0.08) 0%, transparent 30%),
                          radial-gradient(circle at 80% 70%, rgba(0, 240, 255, 0.08) 0%, transparent 30%);
        overflow: hidden;
    }
    
    /* 🔥 REMOVE all glow effects on hover */
    button, .stButton>button, .stFileUploader>div>div, .stCheckbox>div>div, input, textarea, select {
        outline: none !important;
        box-shadow: none !important;
        transition: none !important;
    }
    
    /* Button styling */
    .stButton>button {
        border: 2px solid var(--primary) !important;
        background: rgba(10, 10, 20, 0.5) !important;
        color: var(--primary) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-weight: bold !important;
        border-radius: 6px !important;
    }
    
    /* File uploader */
    .stFileUploader>div>div {
        border: 2px dashed var(--primary) !important;
        background: rgba(10, 10, 20, 0.5) !important;
        color: var(--primary) !important;
        border-radius: 8px !important;
    }
    
    /* Text input */
    .stTextInput>div>div>input {
        background: rgba(10, 10, 20, 0.5) !important;
        color: var(--primary) !important;
        border: 2px solid var(--primary) !important;
        border-radius: 6px !important;
    }
    
    /* Error/success blocks */
    .stSuccess {
        background: rgba(0, 240, 255, 0.08) !important;
        border-left: 4px solid var(--primary) !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    .stError {
        background: rgba(255, 0, 100, 0.08) !important;
        border-left: 4px solid #ff0064 !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    .stWarning {
        background: rgba(255, 165, 0, 0.08) !important;
        border-left: 4px solid orange !important;
        border-radius: 0 8px 8px 0 !important;
    }
    
    .cyber-terminal {
        background: rgba(0, 0, 0, 0.7);
        border: 1px solid var(--primary);
        border-radius: 8px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: var(--primary);
    }
    
    *:focus, *:active {
        outline: none !important;
        box-shadow: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- ASCII ART HEADER ---
ascii_art = r"""
   ________  ______  __________ _    ____________  _____ ______
  / ____/\ \/ / __ )/ ____/ __ \ |  / / ____/ __ \/ ___// ____/
 / /      \  / __  / __/ / /_/ / | / / __/ / /_/ /\__ \/ __/   
/ /___    / / /_/ / /___/ _, _/| |/ / /___/ _, _/___/ / /___   
\____/   /_/_____/_____/_/ |_| |___/_____/_/ |_|/____/_____/  
"""

# --- MAIN UI ---
st.markdown(f"""
<div style="text-align: center; margin-bottom: 30px;">
    <div style="color: var(--primary); font-size: 10px; opacity: 0.8; font-family: 'Courier New', monospace; white-space: pre; line-height: 1.2;">{ascii_art}</div>
    <h1 style="margin-top: -10px; font-size: 3em;">PDF SECURITY LOCK</h1>
    <p style="color: var(--light); letter-spacing: 2px;">ENCRYPT PDF FILES WITH MILITARY-GRADE PROTECTION</p>
    <div style="height: 2px; background: linear-gradient(90deg, transparent, var(--primary), transparent); margin: 10px auto; width: 50%;"></div>
</div>
""", unsafe_allow_html=True)

# --- FILE UPLOADER ---
with stylable_container(
    key="uploader",
    css_styles="""
        {
            border: 2px dashed var(--primary);
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            background: rgba(10, 10, 20, 0.5);
            margin-bottom: 30px;
        }
    """,
):
    uploaded_file = st.file_uploader("UPLOAD PDF FILE", type=["pdf"], label_visibility="collapsed")

password = st.text_input("ENTER ENCRYPTION PASSWORD", type="password")

if st.button("🔐 ENCRYPT PDF", key="encrypt_button"):
    if uploaded_file and password:
        try:
            with st.spinner('APPLYING ENCRYPTION...'):
                reader = PdfReader(uploaded_file)
                writer = PdfWriter()

                for page in reader.pages:
                    writer.add_page(page)

                writer.encrypt(user_password=password, owner_password=None, use_128bit=True)

                output = BytesIO()
                writer.write(output)
                output.seek(0)

            with stylable_container(
                key="success_container",
                css_styles="""
                    {
                        border-left: 4px solid var(--primary);
                        padding: 15px 20px;
                        background: rgba(0, 0, 0, 0.5);
                        margin-bottom: 20px;
                        border-radius: 0 8px 8px 0;
                    }
                """,
            ):
                st.success("ENCRYPTION SUCCESSFUL! FILE IS NOW SECURE.")
            
            with stylable_container(
                key="download_button",
                css_styles="""
                    {
                        text-align: center;
                        margin-top: 20px;
                    }
                """,
            ):
                st.download_button(
                    label="📥 DOWNLOAD SECURED PDF",
                    data=output,
                    file_name="secured.pdf",
                    mime="application/pdf"
                )
                
        except Exception as e:
            with stylable_container(
                key="error_container",
                css_styles="""
                    {
                        border-left: 4px solid #ff0064;
                        padding: 15px 20px;
                        background: rgba(0, 0, 0, 0.5);
                        margin-bottom: 20px;
                        border-radius: 0 8px 8px 0;
                    }
                """,
            ):
                st.error(f"ENCRYPTION FAILED: {str(e)}")
    else:
        with stylable_container(
            key="warning_container",
            css_styles="""
                {
                    border-left: 4px solid orange;
                    padding: 15px 20px;
                    background: rgba(0, 0, 0, 0.5);
                    margin-bottom: 20px;
                    border-radius: 0 8px 8px 0;
                }
            """,
        ):
            st.warning("PLEASE UPLOAD A PDF FILE AND ENTER A PASSWORD")

st.markdown("""
<div style="text-align: center; margin-top: 50px; color: var(--light); font-size: 0.8em; opacity: 0.7;">
    <div style="height: 1px; background: linear-gradient(90deg, transparent, var(--primary), transparent); margin: 20px auto; width: 30%;"></div>
    CYBERVERSE SECURITY v3.0 | [SYSTEM: ONLINE] | [ENCRYPTION: AES-128]
</div>
""", unsafe_allow_html=True)