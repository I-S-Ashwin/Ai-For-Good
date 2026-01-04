# 🛡️ SafeHaven AI

**Snowflake-Native Ultra-Interactive Home Inspection Workspace**

SafeHaven AI is a next-generation inspection platform that leverages **Snowflake Cortex AI** (Vision, Search, Llama 3) to analyze home defects, estimate costs, and ensure legal compliance.

![SafeHaven Concept](https://images.unsplash.com/photo-1582281298055-e25b84a30b0b?q=80&w=1000&auto=format&fit=crop)

---

## 🚀 Key Features

*   **Multimodal Analysis**: Ingests images and audio (Wall Tap Tests).
*   **Cortex Vision**: Detects defects like water damage, cracks, and mold.
*   **Smart Cost Estimator**: Algorithmic repair pricing based on severity & region.
*   **Legal Shield**: RAG-powered building code compliance checks (IBC/NEC).
*   **Audio Forensics**: Spectral analysis to detect tile delamination.
*   **Glassmorphism UI**: Premium Streamlit interface.

## 📂 Project Structure

```text
AiForGood/
├── backend/
│   ├── audio_forensics.py  # Audio analysis UDF
│   ├── cost_estimator.py   # Pricing Logic
│   ├── legal_rag.py        # Cortex Search Logic
│   ├── report_generator.py # PDF Export
│   ├── validators.py       # Pydantic Output Validation
│   └── utils.py            # Security & Helpers
├── frontend/
│   ├── streamlit_app.py    # Main UI Application
│   └── style.css           # Glassmorphism Theme
├── tests/
│   └── test_backend.py     # Automated Pytest Suite
├── safehaven_db_setup.sql  # Snowflake SQL Setup Script
├── requirements.txt        # Python Dependencies
├── verify_deployment.py    # Integration Verify Script
└── README.md               # This file
```

## 🛠️ Setup & Usage

### 1. Snowflake Setup
Run the `safehaven_db_setup.sql` script in a Snowflake Worksheet to create the Database, Schema, and Assets Stage.

### 2. Local Development
1.  **Install Dependencies**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  **Run Application**:
    ```bash
    streamlit run frontend/streamlit_app.py
    ```
    *Note: The app will run in **Demo Mode** if no Snowflake credentials are configured.*

### 3. Testing
Run the automated test suite to verify logic:
```bash
pytest tests/
```

---

**Built for the Google DeepMind "AI for Good" Challenge.**
