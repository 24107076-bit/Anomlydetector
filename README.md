# Intelligent Anomaly Detection & Investigation Hub 🕵️

An advanced Streamlit-based dashboard for UPI transaction monitoring, risk analytics, and AI-powered forensic investigation.

## Features
- **Global Dashboard**: Real-time fleet overview with risk analytics and transaction spreads.
- **UPI Investigations**: Deep-dive analysis of individual UPI cases with AI-generated forensic reports.
- **Cheque Clearing**: Smart OCR and verification of cheques using Google Gemini Vision.
- **AI-Powered Reasoning**: Integration with Google Gemini for explainable fraud detection.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <your-repository-url>
   cd Anomly_detector
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app1.py
   ```

## Configuration
- You will need a **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/).
- Enter the API key in the sidebar of the application to enable AI features.

## Project Structure
- `app1.py`: Main Streamlit application.
- `JSON/`: Directory containing mock database files (customers, merchants, transactions).
- `requirements.txt`: Python package dependencies.
