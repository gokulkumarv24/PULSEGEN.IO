"""
Module Extraction AI Agent - Streamlit Web Interface

Advanced web application for extracting structured information from documentation websites.
Features intelligent web scraping, AI-powered content analysis, and professional UI design.

Creator: Gokul Kumar V
GitHub: https://github.com/gokulkumarv24
LinkedIn: https://www.linkedin.com/in/gokul-kumar-v-236a24217

This application provides a user-friendly interface for URL input, real-time processing,
and beautifully formatted JSON output display with advanced animations and interactions.
"""

import streamlit as st
import json
import sys
import os
from datetime import datetime
import validators
import traceback

# Add src directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from web_scraper import WebScraper
    from content_processor import ContentProcessor
    from ai_extractor import AIModuleExtractor
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

class StreamlitApp:
    def __init__(self):
        """Initialize the Streamlit application."""
        self.setup_page_config()
        self.setup_session_state()
    
    def setup_page_config(self):
        """Configure Streamlit page settings."""
        st.set_page_config(
            page_title="PULSEGEN.IO - Module Extraction AI",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Add custom CSS for advanced, creative professional styling
        st.markdown("""
        <style>
        /* Import Professional Typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Crimson+Text:wght@400;600&display=swap');
        /* Import Font Awesome for professional icons */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        
        /* Advanced Animations */
        @keyframes slideInFromLeft {
            0% { transform: translateX(-100%); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes slideInFromRight {
            0% { transform: translateX(100%); opacity: 0; }
            100% { transform: translateX(0); opacity: 1; }
        }
        
        @keyframes fadeInUp {
            0% { transform: translateY(30px); opacity: 0; }
            100% { transform: translateY(0); opacity: 1; }
        }
        
        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }
        
        @keyframes shimmer {
            0% { background-position: -200px 0; }
            100% { background-position: calc(200px + 100%) 0; }
        }
        
        @keyframes rotateIcon {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px);
            }
            50% {
                transform: translateY(-20px);
            }
        }
        
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {
                transform: translateY(0);
            }
            40% {
                transform: translateY(-8px);
            }
            60% {
                transform: translateY(-4px);
            }
        }
        
        @keyframes gradient-shift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* Global Styles - Clean & Professional */
        .main {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #fdfdfd 0%, #f8f9fa 100%);
            color: #1a1a1a;
        }
        
        /* Advanced Interactive Cards */
        .feature-card {
            position: relative;
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            animation: fadeInUp 0.6s ease-out;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(44, 62, 80, 0.15);
        }
        
        .feature-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(44, 62, 80, 0.05), transparent);
            transition: left 0.5s;
        }
        
        .feature-card:hover::before {
            left: 100%;
        }
        
        /* Interactive Processing Animation */
        .processing-animation {
            position: relative;
            overflow: hidden;
        }
        
        .processing-animation::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent 0%, rgba(44, 62, 80, 0.1) 50%, transparent 100%);
            animation: shimmer 2s infinite;
        }
        
        /* Professional Button Styles with Advanced Interactions */
        .stButton > button {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border: none;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            padding: 0.8rem 2rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(44,62,80,0.2);
            position: relative;
            overflow: hidden;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #34495e 0%, #2c3e50 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(44,62,80,0.3);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 4px 15px rgba(44,62,80,0.4);
        }
        
        /* Advanced Progress Bar */
        .stProgress > div > div > div {
            background: linear-gradient(90deg, #3498db, #2980b9, #2c3e50);
            background-size: 200% 200%;
            animation: shimmer 2s ease-in-out infinite alternate;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(52, 152, 219, 0.3);
        }
        
        /* Sidebar Advanced Styling */
        .css-1d391kg {
            background: linear-gradient(180deg, #f8f9fa 0%, #ecf0f1 100%);
            border-right: 3px solid #2c3e50;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }
        
        /* Advanced Expander */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .streamlit-expanderHeader:hover {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-color: #2c3e50;
            transform: scale(1.01);
            box-shadow: 0 5px 15px rgba(44,62,80,0.1);
        }
        
        /* Advanced Metric Cards */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            border: 2px solid #e9ecef;
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }
        
        [data-testid="metric-container"]:hover {
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 15px 35px rgba(0,0,0,0.12);
            border-color: #2c3e50;
        }
        
        [data-testid="metric-container"]::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3498db, #2980b9, #2c3e50);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        [data-testid="metric-container"]:hover::before {
            transform: scaleX(1);
        }
        
        /* Code Blocks - Advanced Editor Style */
        .stCodeBlock {
            border: 2px solid #e1e4e8;
            border-radius: 12px;
            background: linear-gradient(135deg, #f6f8fa 0%, #ffffff 100%);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
            position: relative;
            overflow: hidden;
        }
        
        .stCodeBlock::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #e74c3c, #f39c12, #2ecc71, #3498db);
        }
        
        /* Form Elements - Advanced Professional */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea {
            border: 2px solid #e9ecef;
            border-radius: 10px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            padding: 1rem;
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {
            border-color: #2c3e50;
            box-shadow: 0 0 0 3px rgba(44,62,80,0.1), inset 0 2px 4px rgba(0,0,0,0.05);
            outline: none;
            transform: scale(1.01);
        }
        
        /* Advanced Alert Messages */
        .stAlert {
            border-radius: 12px;
            border: none;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }
        
        .stAlert::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: currentColor;
        }
        
        /* Hide Streamlit Branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Advanced Professional Scrollbar */
        ::-webkit-scrollbar {
            width: 12px;
            height: 12px;
        }
        
        ::-webkit-scrollbar-track {
            background: linear-gradient(180deg, #f1f3f4 0%, #e8eaf6 100%);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
            border-radius: 10px;
            border: 2px solid #f1f3f4;
            transition: all 0.3s ease;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(180deg, #34495e 0%, #2c3e50 100%);
            border-color: #e8eaf6;
        }
        
        /* Typography Improvements */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Crimson Text', Georgia, serif;
            color: #1a1a1a;
            font-weight: 600;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }
        
        /* Advanced Layout */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
            animation: fadeInUp 0.8s ease-out;
        }
        
        /* Professional Tables */
        .dataframe {
            border: 2px solid #e1e4e8;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 14px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        /* Advanced Tab Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 4px;
            border-radius: 12px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            border: 2px solid transparent;
            border-radius: 8px;
            color: #6c757d;
            font-weight: 500;
            padding: 0.75rem 1.5rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(44, 62, 80, 0.05);
            color: #2c3e50;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            border-color: #2c3e50;
            color: #ffffff;
            box-shadow: 0 4px 15px rgba(44,62,80,0.3);
        }
        
        /* Loading Animation */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #2c3e50;
            border-radius: 50%;
            animation: rotateIcon 1s linear infinite;
        }
        
        /* Success Checkmark Animation */
        .checkmark {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #2ecc71;
            position: relative;
        }
        
        .checkmark::after {
            content: '✓';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def setup_session_state(self):
        """Initialize session state variables."""
        if 'extraction_results' not in st.session_state:
            st.session_state.extraction_results = None
        if 'processing_status' not in st.session_state:
            st.session_state.processing_status = None
        if 'scraped_pages' not in st.session_state:
            st.session_state.scraped_pages = []
    
    def render_header(self):
        """Render the application header."""
        # Advanced, creative header design
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 50%, #2c3e50 100%);
            background-size: 200% 200%;
            animation: shimmer 3s ease-in-out infinite alternate;
            padding: 4rem 2rem 3rem 2rem;
            margin-bottom: 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
            border-radius: 0 0 25px 25px;
            box-shadow: 0 10px 30px rgba(44,62,80,0.3);
        ">
            <div style="
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
                background-size: 50px 50px;
                animation: slideInFromLeft 2s ease-out;
                opacity: 0.1;
            "></div>
            <!-- Floating particles effect -->
            <div style="
                position: absolute;
                top: 20%;
                left: 10%;
                width: 4px;
                height: 4px;
                background: #3498db;
                border-radius: 50%;
                animation: float 3s ease-in-out infinite;
                opacity: 0.7;
            "></div>
            <div style="
                position: absolute;
                top: 60%;
                right: 15%;
                width: 3px;
                height: 3px;
                background: #2ecc71;
                border-radius: 50%;
                animation: float 4s ease-in-out infinite reverse;
                opacity: 0.6;
            "></div>
            <div style="
                position: absolute;
                top: 40%;
                left: 80%;
                width: 2px;
                height: 2px;
                background: #f39c12;
                border-radius: 50%;
                animation: float 2.5s ease-in-out infinite;
                opacity: 0.8;
            "></div>
            <h1 style="
                color: #ffffff;
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 3.5rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                letter-spacing: -0.02em;
                text-shadow: 0 4px 8px rgba(0,0,0,0.3);
                animation: fadeInUp 1s ease-out;
                position: relative;
                z-index: 2;
            ">PULSEGEN.IO</h1>
            <div style="
                width: 100px;
                height: 3px;
                background: linear-gradient(90deg, #3498db, #ffffff, #3498db);
                margin: 1rem auto;
                border-radius: 2px;
                animation: shimmer 2s infinite;
            "></div>
            <h2 style="
                color: #ecf0f1;
                font-family: 'Inter', sans-serif;
                font-size: 1.2rem;
                font-weight: 500;
                margin-bottom: 1.5rem;
                text-transform: uppercase;
                letter-spacing: 0.2em;
                animation: slideInFromRight 1.2s ease-out;
                position: relative;
                z-index: 2;
            ">Module Extraction AI Agent</h2>
            <p style="
                color: #bdc3c7;
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                margin: 0 auto;
                max-width: 700px;
                line-height: 1.7;
                animation: fadeInUp 1.4s ease-out;
                position: relative;
                z-index: 2;
            ">
                <i class="fas fa-magic" style="margin-right: 8px; color: #3498db;"></i>
                Extract structured information from documentation websites using advanced artificial intelligence.
                <br>
                <i class="fas fa-cogs" style="margin-right: 8px; color: #e74c3c;"></i>
                Analyze help documentation and identify key modules with intelligent descriptions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Advanced interactive feature highlights
        st.markdown("""
        <div style="margin: 2rem 0; animation: fadeInUp 0.8s ease-out 0.5s both;">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class="feature-card" style="
                text-align: center; 
                padding: 2rem 1.5rem; 
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                border: 2px solid #e9ecef; 
                border-radius: 15px;
                margin: 0.5rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                cursor: pointer;
            ">
                <div style="
                    font-size: 2rem; 
                    margin-bottom: 1rem; 
                    color: #2c3e50;
                    transition: all 0.3s ease;
                    animation: pulse 2s infinite;
                ">
                    <i class="fas fa-search"></i>
                </div>
                <h4 style="
                    margin: 0 0 0.5rem 0; 
                    font-size: 1rem; 
                    font-weight: 700; 
                    color: #2c3e50;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">SMART CRAWLING</h4>
                <p style="
                    margin: 0; 
                    font-size: 0.85rem; 
                    color: #7f8c8d;
                    line-height: 1.5;
                ">Intelligent web scraping with advanced algorithms</p>
                <div style="
                    width: 30px;
                    height: 2px;
                    background: linear-gradient(90deg, #3498db, #2980b9);
                    margin: 0.75rem auto 0;
                    border-radius: 1px;
                "></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="feature-card" style="
                text-align: center; 
                padding: 2rem 1.5rem; 
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                border: 2px solid #e9ecef; 
                border-radius: 15px;
                margin: 0.5rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                cursor: pointer;
                animation-delay: 0.1s;
            ">
                <div style="
                    font-size: 2rem; 
                    margin-bottom: 1rem; 
                    color: #2c3e50;
                    transition: all 0.3s ease;
                ">
                    <i class="fas fa-brain"></i>
                </div>
                <h4 style="
                    margin: 0 0 0.5rem 0; 
                    font-size: 1rem; 
                    font-weight: 700; 
                    color: #2c3e50;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">AI ANALYSIS</h4>
                <p style="
                    margin: 0; 
                    font-size: 0.85rem; 
                    color: #7f8c8d;
                    line-height: 1.5;
                ">Advanced language models & pattern recognition</p>
                <div style="
                    width: 30px;
                    height: 2px;
                    background: linear-gradient(90deg, #e74c3c, #c0392b);
                    margin: 0.75rem auto 0;
                    border-radius: 1px;
                "></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="feature-card" style="
                text-align: center; 
                padding: 2rem 1.5rem; 
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                border: 2px solid #e9ecef; 
                border-radius: 15px;
                margin: 0.5rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                cursor: pointer;
                animation-delay: 0.2s;
            ">
                <div style="
                    font-size: 2rem; 
                    margin-bottom: 1rem; 
                    color: #2c3e50;
                    transition: all 0.3s ease;
                ">
                    <i class="fas fa-chart-bar"></i>
                </div>
                <h4 style="
                    margin: 0 0 0.5rem 0; 
                    font-size: 1rem; 
                    font-weight: 700; 
                    color: #2c3e50;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">STRUCTURED OUTPUT</h4>
                <p style="
                    margin: 0; 
                    font-size: 0.85rem; 
                    color: #7f8c8d;
                    line-height: 1.5;
                ">JSON format results with hierarchical data</p>
                <div style="
                    width: 30px;
                    height: 2px;
                    background: linear-gradient(90deg, #f39c12, #e67e22);
                    margin: 0.75rem auto 0;
                    border-radius: 1px;
                "></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="feature-card" style="
                text-align: center; 
                padding: 2rem 1.5rem; 
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); 
                border: 2px solid #e9ecef; 
                border-radius: 15px;
                margin: 0.5rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.08);
                cursor: pointer;
                animation-delay: 0.3s;
            ">
                <div style="
                    font-size: 2rem; 
                    margin-bottom: 1rem; 
                    color: #2c3e50;
                    transition: all 0.3s ease;
                ">
                    <i class="fas fa-bolt"></i>
                </div>
                <h4 style="
                    margin: 0 0 0.5rem 0; 
                    font-size: 1rem; 
                    font-weight: 700; 
                    color: #2c3e50;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                ">REAL-TIME</h4>
                <p style="
                    margin: 0; 
                    font-size: 0.85rem; 
                    color: #7f8c8d;
                    line-height: 1.5;
                ">Instant processing with live progress tracking</p>
                <div style="
                    width: 30px;
                    height: 2px;
                    background: linear-gradient(90deg, #2ecc71, #27ae60);
                    margin: 0.75rem auto 0;
                    border-radius: 1px;
                "></div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Render the sidebar with configuration options."""
        with st.sidebar:
            # Professional sidebar header
            st.markdown("""
            <div style="
                background: #2c3e50;
                color: #ffffff;
                padding: 1.5rem;
                margin: -1rem -1rem 2rem -1rem;
                text-align: center;
            ">
                <h3 style="
                    margin: 0;
                    font-family: 'Inter', sans-serif;
                    font-size: 1.1rem;
                    font-weight: 600;
                    letter-spacing: 0.05em;
                ">CONFIGURATION</h3>
                <p style="
                    margin: 0.5rem 0 0 0;
                    font-size: 0.8rem;
                    opacity: 0.8;
                    font-weight: 400;
                ">Customize extraction settings</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Scraping settings section
            st.markdown("""
            <div style="margin-bottom: 1.5rem;">
                <h4 style="
                    margin: 0 0 1rem 0;
                    color: #2c3e50;
                    font-family: 'Inter', sans-serif;
                    font-size: 0.9rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    border-bottom: 1px solid #e9ecef;
                    padding-bottom: 0.5rem;
                ">Web Scraping</h4>
            </div>
            """, unsafe_allow_html=True)
            
            delay = st.slider(
                "Request delay (seconds)", 
                0.5, 5.0, 1.0, 0.5, 
                help="Delay between HTTP requests for respectful crawling"
            )
            max_pages = st.slider(
                "Maximum pages", 
                10, 100, 30, 5,
                help="Limit the number of pages to process"
            )
            max_depth = st.slider(
                "Crawling depth", 
                1, 5, 2, 1,
                help="Maximum depth to follow links from starting URL"
            )
            
            # AI settings section
            st.markdown("""
            <div style="margin: 2rem 0 1.5rem 0;">
                <h4 style="
                    margin: 0 0 1rem 0;
                    color: #2c3e50;
                    font-family: 'Inter', sans-serif;
                    font-size: 0.9rem;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.05em;
                    border-bottom: 1px solid #e9ecef;
                    padding-bottom: 0.5rem;
                ">AI Processing</h4>
            </div>
            """, unsafe_allow_html=True)
            
            use_openai = st.checkbox(
                "Enable OpenAI API", 
                value=False,
                help="Use OpenAI GPT for enhanced analysis (optional)"
            )
            openai_key = ""
            if use_openai:
                openai_key = st.text_input(
                    "OpenAI API Key", 
                    type="password", 
                    help="Enter your OpenAI API key"
                )
                st.info("**Note**: Enhanced AI analysis with GPT models")
            else:
                st.success("**Default**: Advanced rule-based extraction (no API required)")
            
            # Performance information
            st.markdown("""
            <div style="
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 1rem;
                margin-top: 2rem;
            ">
                <h5 style="
                    margin: 0 0 0.75rem 0;
                    color: #495057;
                    font-family: 'Inter', sans-serif;
                    font-size: 0.85rem;
                    font-weight: 600;
                ">Performance Guidelines</h5>
                <ul style="
                    margin: 0;
                    padding-left: 1.2rem;
                    color: #6c757d;
                    font-size: 0.8rem;
                    line-height: 1.5;
                ">
                    <li>Lower delay = faster processing</li>
                    <li>Higher depth = more comprehensive analysis</li>
                    <li>OpenAI API = enhanced descriptions</li>
                    <li>Rule-based mode = consistent performance</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            return {
                'delay': delay,
                'max_pages': max_pages,
                'max_depth': max_depth,
                'use_openai': use_openai,
                'openai_key': openai_key
            }
    
    def render_input_section(self):
        """Render the URL input section."""
        # Advanced, creative section header with animations
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 50%, #ffffff 100%);
            border: 2px solid #e9ecef;
            border-left: 6px solid #3498db;
            border-radius: 15px;
            padding: 2.5rem;
            margin: 2rem 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.08);
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 3px;
                background: linear-gradient(90deg, #3498db, #2ecc71, #f39c12, #e74c3c);
                background-size: 400% 100%;
                animation: shimmer 3s linear infinite;
            "></div>
            <div style="
                display: flex;
                align-items: center;
                margin-bottom: 1.5rem;
                animation: slideInFromLeft 0.8s ease-out;
            ">
                <div style="
                    font-size: 2.5rem;
                    color: #3498db;
                    margin-right: 15px;
                    animation: rotateIcon 4s linear infinite;
                ">
                    <i class="fas fa-link"></i>
                </div>
                <div>
                    <h2 style="
                        margin: 0;
                        color: #2c3e50;
                        font-family: 'Crimson Text', Georgia, serif;
                        font-size: 2rem;
                        font-weight: 700;
                        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    ">Input Documentation URLs</h2>
                    <div style="
                        width: 60px;
                        height: 2px;
                        background: linear-gradient(90deg, #3498db, #2ecc71);
                        margin-top: 8px;
                        border-radius: 1px;
                        animation: pulse 2s infinite;
                    "></div>
                </div>
            </div>
            <p style="
                margin: 0;
                color: #6c757d;
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                line-height: 1.7;
                animation: fadeInUp 1s ease-out 0.3s both;
            ">
                <i class="fas fa-magic" style="color: #e74c3c; margin-right: 8px;"></i>
                Provide documentation websites for intelligent module extraction and AI-powered analysis
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced input method selection with creative styling
        st.markdown("""
        <div style="margin: 2rem 0;">
            <h3 style="
                color: #2c3e50;
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 1.5rem;
                font-weight: 600;
                text-align: center;
                margin-bottom: 1.5rem;
            ">
                <i class="fas fa-cogs" style="color: #f39c12; margin-right: 10px;"></i>
                Input Method Selection
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Custom radio button styling
        st.markdown("""
        <style>
            .stRadio > div {
                display: flex;
                justify-content: center;
                gap: 2rem;
                margin: 2rem 0;
            }
            
            .stRadio > div > label {
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 1rem 1.5rem;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                min-width: 150px;
                text-align: center;
            }
            
            .stRadio > div > label:hover {
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border-color: #3498db;
                transform: translateY(-2px);
                box-shadow: 0 8px 25px rgba(52, 152, 219, 0.2);
            }
        </style>
        """, unsafe_allow_html=True)
        
        input_method = st.radio(
            "Choose how you want to provide URLs for analysis",
            ("Single URL", "Multiple URLs", "Upload URL List"),
            horizontal=True,
            help="Select the input method for providing documentation URLs"
        )
        
        urls = []
        
        if input_method == "Single URL":
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                padding: 2rem;
                border-radius: 15px;
                border: 2px solid #e9ecef;
                margin: 1.5rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            ">
                <h4 style="
                    color: #2c3e50;
                    font-family: 'Inter', sans-serif;
                    font-size: 1.2rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    text-align: center;
                ">
                    <i class="fas fa-globe" style="color: #3498db; margin-right: 8px;"></i>
                    Documentation URL
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced input styling
            st.markdown("""
            <style>
                .stTextInput > div > div > input {
                    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
                    border: 2px solid #e9ecef !important;
                    border-radius: 12px !important;
                    padding: 1rem !important;
                    font-size: 1rem !important;
                    color: #2c3e50 !important;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
                    transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1) !important;
                }
                
                .stTextInput > div > div > input:focus {
                    border-color: #3498db !important;
                    box-shadow: 0 6px 25px rgba(52, 152, 219, 0.2), 0 0 0 3px rgba(52, 152, 219, 0.1) !important;
                    transform: translateY(-2px) scale(1.01) !important;
                    background: #ffffff !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            url = st.text_input(
                "Enter documentation URL",
                placeholder="https://help.example.com or https://docs.example.com",
                help="Enter a single documentation website URL",
                label_visibility="collapsed"
            )
            if url:
                urls = [url]
                
        elif input_method == "Multiple URLs":
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                padding: 2rem;
                border-radius: 15px;
                border: 2px solid #e9ecef;
                margin: 1.5rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            ">
                <h4 style="
                    color: #2c3e50;
                    font-family: 'Inter', sans-serif;
                    font-size: 1.2rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    text-align: center;
                ">
                    <i class="fas fa-list" style="color: #2ecc71; margin-right: 8px;"></i>
                    Multiple Documentation URLs
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced textarea styling
            st.markdown("""
            <style>
                .stTextArea > div > div > textarea {
                    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
                    border: 2px solid #e9ecef !important;
                    border-radius: 12px !important;
                    padding: 1rem !important;
                    font-size: 1rem !important;
                    color: #2c3e50 !important;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
                    transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1) !important;
                    font-family: 'Inter', monospace !important;
                }
                
                .stTextArea > div > div > textarea:focus {
                    border-color: #2ecc71 !important;
                    box-shadow: 0 6px 25px rgba(46, 204, 113, 0.2), 0 0 0 3px rgba(46, 204, 113, 0.1) !important;
                    transform: scale(1.01) !important;
                    background: #ffffff !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            url_text = st.text_area(
                "Enter multiple URLs",
                placeholder="https://help.example.com\nhttps://docs.example.com\nhttps://support.example.com",
                height=120,
                help="Enter URLs, one per line",
                label_visibility="collapsed"
            )
            if url_text:
                urls = [url.strip() for url in url_text.split('\n') if url.strip()]
        
        else:  # Upload URL list
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
                padding: 2rem;
                border-radius: 15px;
                border: 2px solid #e9ecef;
                margin: 1.5rem 0;
                box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            ">
                <h4 style="
                    color: #2c3e50;
                    font-family: 'Inter', sans-serif;
                    font-size: 1.2rem;
                    font-weight: 600;
                    margin-bottom: 1rem;
                    text-align: center;
                ">
                    <i class="fas fa-upload" style="color: #f39c12; margin-right: 8px;"></i>
                    Upload URL List
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            # Enhanced file uploader styling
            st.markdown("""
            <style>
                .stFileUploader > div {
                    background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
                    border: 2px dashed #e9ecef !important;
                    border-radius: 12px !important;
                    padding: 2rem !important;
                    transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1) !important;
                }
                
                .stFileUploader > div:hover {
                    border-color: #f39c12 !important;
                    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important;
                    transform: scale(1.01) !important;
                    box-shadow: 0 8px 25px rgba(243, 156, 18, 0.1) !important;
                }
            </style>
            """, unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Upload URL list file",
                type=['txt'],
                help="Upload a text file containing URLs, one per line",
                label_visibility="collapsed"
            )
            if uploaded_file:
                urls = [url.strip() for url in uploaded_file.read().decode().split('\n') if url.strip()]
        
        # Enhanced URL validation with creative presentation
        if urls:
            valid_urls = []
            invalid_urls = []
            
            for url in urls:
                if validators.url(url):
                    valid_urls.append(url)
                else:
                    invalid_urls.append(url)
            
            # Advanced validation display
            if valid_urls:
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                    border: 2px solid #28a745;
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                    animation: fadeInUp 0.5s ease-out;
                ">
                    <h5 style="
                        color: #155724;
                        font-family: 'Inter', sans-serif;
                        font-weight: 600;
                        margin-bottom: 1rem;
                    ">
                        <i class="fas fa-check-circle" style="margin-right: 8px;"></i>
                        Valid URLs Found: {}
                    </h5>
                </div>
                """.format(len(valid_urls)), unsafe_allow_html=True)
                
                # Show valid URLs with advanced styling
                with st.expander("View Valid URLs", expanded=False):
                    for i, url in enumerate(valid_urls, 1):
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                            border-left: 4px solid #28a745;
                            padding: 0.75rem 1rem;
                            margin: 0.5rem 0;
                            border-radius: 0 8px 8px 0;
                            font-family: 'Inter', monospace;
                            font-size: 0.9rem;
                        ">
                            <strong>{i}.</strong> {url}
                        </div>
                        """, unsafe_allow_html=True)
            
            if invalid_urls:
                st.markdown("""
                <div style="
                    background: linear-gradient(135deg, #f8d7da 0%, #f1b0b7 100%);
                    border: 2px solid #dc3545;
                    border-radius: 12px;
                    padding: 1.5rem;
                    margin: 1rem 0;
                    animation: fadeInUp 0.5s ease-out;
                ">
                    <h5 style="
                        color: #721c24;
                        font-family: 'Inter', sans-serif;
                        font-weight: 600;
                        margin-bottom: 1rem;
                    ">
                        <i class="fas fa-exclamation-triangle" style="margin-right: 8px;"></i>
                        Invalid URLs Found: {}
                    </h5>
                </div>
                """.format(len(invalid_urls)), unsafe_allow_html=True)
                
                # Show invalid URLs
                with st.expander("View Invalid URLs", expanded=False):
                    for i, url in enumerate(invalid_urls, 1):
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                            border-left: 4px solid #dc3545;
                            padding: 0.75rem 1rem;
                            margin: 0.5rem 0;
                            border-radius: 0 8px 8px 0;
                            font-family: 'Inter', monospace;
                            font-size: 0.9rem;
                            color: #721c24;
                        ">
                            <strong>{i}.</strong> {url}
                        </div>
                        """, unsafe_allow_html=True)
            
            # Advanced submit button section
            if valid_urls:
                st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    # Creative submit button
                    st.markdown("""
                    <style>
                        .big-button {
                            background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
                            color: white !important;
                            border: none !important;
                            border-radius: 15px !important;
                            padding: 1rem 2rem !important;
                            font-size: 1.2rem !important;
                            font-weight: 700 !important;
                            text-transform: uppercase !important;
                            letter-spacing: 0.1em !important;
                            box-shadow: 0 8px 25px rgba(46, 204, 113, 0.3) !important;
                            transition: all 0.3s cubic-bezier(0.4, 0.0, 0.2, 1) !important;
                            position: relative !important;
                            overflow: hidden !important;
                            width: 100% !important;
                        }
                        
                        .big-button:hover {
                            background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%) !important;
                            box-shadow: 0 12px 35px rgba(46, 204, 113, 0.4) !important;
                            transform: translateY(-3px) scale(1.02) !important;
                        }
                        
                        .big-button::before {
                            content: '';
                            position: absolute;
                            top: 0;
                            left: -100%;
                            width: 100%;
                            height: 100%;
                            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
                            transition: left 0.5s;
                        }
                        
                        .big-button:hover::before {
                            left: 100%;
                        }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    if st.button(
                        f"🚀 ANALYZE {len(valid_urls)} WEBSITE{'S' if len(valid_urls) > 1 else ''}",
                        use_container_width=True,
                        type="primary",
                        key="analyze_button"
                    ):
                        return valid_urls
            
            return valid_urls if 'valid_urls' in locals() else []
        
        return []
    
    def render_processing_section(self, urls, config):
        """Render the processing section with start button."""
        # Clean processing section header
        st.markdown("""
        <div style="
            background: #ffffff;
            border: 1px solid #e9ecef;
            border-left: 4px solid #2c3e50;
            padding: 2rem;
            margin: 2rem 0;
        ">
            <h2 style="
                margin: 0 0 0.5rem 0;
                color: #2c3e50;
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 1.8rem;
                font-weight: 600;
            ">Processing Center</h2>
            <p style="
                margin: 0;
                color: #7f8c8d;
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
            ">Execute extraction or manage results</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional action buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if urls:
                start_processing = st.button(
                    "Start Extraction",
                    type="primary",
                    width='stretch',
                    help="Begin analyzing the provided URLs"
                )
            else:
                st.markdown("""
                <div style="
                    background: #f8f9fa;
                    color: #6c757d;
                    padding: 0.75rem;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                ">
                    <strong>Start Extraction</strong><br>
                    <small>Add URLs first</small>
                </div>
                """, unsafe_allow_html=True)
                start_processing = False
        
        with col2:
            if st.session_state.extraction_results:
                download_data = json.dumps(st.session_state.extraction_results, indent=2)
                filename = f"pulsegen_modules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                st.download_button(
                    "Download JSON",
                    data=download_data,
                    file_name=filename,
                    mime="application/json",
                    width='stretch',
                    help="Download extraction results as JSON file"
                )
            else:
                st.markdown("""
                <div style="
                    background: #f8f9fa;
                    color: #6c757d;
                    padding: 0.75rem;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                ">
                    <strong>Download JSON</strong><br>
                    <small>No results available</small>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            if st.session_state.extraction_results or st.session_state.scraped_pages:
                clear_results = st.button(
                    "Clear Results", 
                    width='stretch',
                    help="Clear all results and start fresh"
                )
                if clear_results:
                    st.session_state.extraction_results = None
                    st.session_state.processing_status = None
                    st.session_state.scraped_pages = []
                    st.success("Results cleared successfully")
                    st.rerun()
            else:
                st.markdown("""
                <div style="
                    background: #f8f9fa;
                    color: #6c757d;
                    padding: 0.75rem;
                    border: 1px solid #e9ecef;
                    border-radius: 4px;
                    text-align: center;
                    font-family: 'Inter', sans-serif;
                ">
                    <strong>Clear Results</strong><br>
                    <small>Nothing to clear</small>
                </div>
                """, unsafe_allow_html=True)
        
        if start_processing and urls:
            self.process_urls(urls, config)
    
    def process_urls(self, urls, config):
        """Process URLs and extract modules."""
        try:
            st.session_state.processing_status = "Starting..."
            
            # Professional processing display
            st.markdown("""
            <div style="
                background: #f8f9fa;
                border: 1px solid #e9ecef;
                border-left: 4px solid #2c3e50;
                padding: 1.5rem;
                margin: 1rem 0;
                text-align: center;
            ">
                <h3 style="color: #2c3e50; margin: 0 0 0.5rem 0; font-family: 'Inter', sans-serif;">
                    Processing in Progress
                </h3>
                <p style="color: #6c757d; margin: 0; font-size: 0.9rem;">
                    Analyzing documentation URLs with AI agents...
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize components
            scraper = WebScraper(
                delay=config['delay'],
                max_depth=config['max_depth'],
                max_pages=config['max_pages']
            )
            
            processor = ContentProcessor()
            
            extractor = AIModuleExtractor(
                api_key=config['openai_key'] if config['use_openai'] else None
            )
            
            # Enhanced progress tracking
            progress_container = st.container()
            
            with progress_container:
                # Custom progress bar
                progress_bar = st.progress(0)
                status_placeholder = st.empty()
                
                # Step 1: Web scraping
                with status_placeholder.container():
                    st.markdown("""
                    <div style="
                        background: #e3f2fd;
                        border: 1px solid #2196f3;
                        border-left: 4px solid #2196f3;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0 0 0.25rem 0; color: #1976d2; font-family: 'Inter', sans-serif;">
                            Step 1: Web Scraping
                        </h4>
                        <p style="margin: 0; color: #1976d2; font-size: 0.9rem;">
                            Crawling documentation websites...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                progress_bar.progress(10)
                
                scraped_pages = scraper.crawl_website(urls)
                st.session_state.scraped_pages = scraped_pages
                
                if not scraped_pages:
                    st.error("No content could be extracted from the provided URLs.")
                    return
                
                progress_bar.progress(40)
                
                with status_placeholder.container():
                    st.markdown(f"""
                    <div style="
                        background: #f3e5f5;
                        border: 1px solid #9c27b0;
                        border-left: 4px solid #9c27b0;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0 0 0.25rem 0; color: #7b1fa2; font-family: 'Inter', sans-serif;">
                            Step 2: Content Analysis
                        </h4>
                        <p style="margin: 0; color: #7b1fa2; font-size: 0.9rem;">
                            Found {len(scraped_pages)} pages, analyzing content structure...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Step 2: Content processing
                progress_bar.progress(60)
                processed_content = processor.process_pages(scraped_pages)
                
                progress_bar.progress(80)
                
                with status_placeholder.container():
                    ai_mode = "OpenAI GPT" if config['use_openai'] and config['openai_key'] else "Advanced Rule-based"
                    st.markdown(f"""
                    <div style="
                        background: #e8f5e8;
                        border: 1px solid #4caf50;
                        border-left: 4px solid #4caf50;
                        padding: 1rem;
                        margin: 0.5rem 0;
                    ">
                        <h4 style="margin: 0 0 0.25rem 0; color: #388e3c; font-family: 'Inter', sans-serif;">
                            Step 3: AI Module Extraction
                        </h4>
                        <p style="margin: 0; color: #388e3c; font-size: 0.9rem;">
                            Using {ai_mode} analysis to extract modules...
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Step 3: AI extraction
                extracted_modules = extractor.extract_modules(processed_content)
                validated_modules = extractor.validate_output_format(extracted_modules)
                
                progress_bar.progress(100)
                
                # Success message
                status_placeholder.markdown("""
                <div style="
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-left: 4px solid #28a745;
                    padding: 1.5rem;
                    text-align: center;
                    color: #155724;
                    margin: 1rem 0;
                ">
                    <h3 style="margin: 0 0 0.5rem 0; font-family: 'Inter', sans-serif;">
                        Extraction Completed Successfully
                    </h3>
                    <p style="margin: 0; font-size: 0.9rem;">
                        Your modules have been extracted and are ready for review
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            # Store results
            st.session_state.extraction_results = validated_modules
            st.session_state.processing_status = "completed"
            
            # Auto-refresh to show results
            st.rerun()
            
        except Exception as e:
            st.markdown("""
            <div style="
                background: #ffebee;
                border: 1px solid #f44336;
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            ">
                <h4 style="color: #d32f2f; margin: 0 0 0.5rem 0;">
                    <i class="fas fa-exclamation-triangle"></i> Processing Error
                </h4>
                <p style="color: #d32f2f; margin: 0;">An error occurred during processing. Please check the details below and try again.</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.expander("Error Details", expanded=True):
                st.error(f"Error: {str(e)}")
                st.code(traceback.format_exc(), language='python')
            
            st.session_state.processing_status = "error"
    
    def render_results_section(self):
        """Render the results section."""
        if st.session_state.extraction_results:
            # Professional results header
            st.markdown("""
            <div style="
                background: #ffffff;
                border: 1px solid #e9ecef;
                border-left: 4px solid #2c3e50;
                padding: 2rem;
                margin: 2rem 0;
            ">
                <h2 style="
                    margin: 0 0 0.5rem 0;
                    color: #2c3e50;
                    font-family: 'Crimson Text', Georgia, serif;
                    font-size: 1.8rem;
                    font-weight: 600;
                ">Extraction Results</h2>
                <p style="
                    margin: 0;
                    color: #7f8c8d;
                    font-family: 'Inter', sans-serif;
                    font-size: 1rem;
                ">AI-powered analysis complete. Review your structured modules below.</p>
            </div>
            """, unsafe_allow_html=True)
            
            results = st.session_state.extraction_results
            
            # Professional summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_submodules = sum(len(module.get('Submodules', {})) for module in results)
            avg_submodules = total_submodules / len(results) if results else 0
            
            with col1:
                st.markdown(f"""
                <div style="
                    background: #ffffff;
                    border: 1px solid #e9ecef;
                    padding: 1.5rem;
                    text-align: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <h1 style="margin: 0; font-size: 2rem; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        {len(results)}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem; font-weight: 500;">
                        Total Modules
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="
                    background: #ffffff;
                    border: 1px solid #e9ecef;
                    padding: 1.5rem;
                    text-align: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <h1 style="margin: 0; font-size: 2rem; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        {total_submodules}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem; font-weight: 500;">
                        Total Submodules
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="
                    background: #ffffff;
                    border: 1px solid #e9ecef;
                    padding: 1.5rem;
                    text-align: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <h1 style="margin: 0; font-size: 2rem; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        {len(st.session_state.scraped_pages)}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem; font-weight: 500;">
                        Pages Analyzed
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div style="
                    background: #ffffff;
                    border: 1px solid #e9ecef;
                    padding: 1.5rem;
                    text-align: center;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                ">
                    <h1 style="margin: 0; font-size: 2rem; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        {avg_submodules:.1f}
                    </h1>
                    <p style="margin: 0.5rem 0 0 0; color: #7f8c8d; font-size: 0.9rem; font-weight: 500;">
                        Avg Sub/Module
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display format selection
            st.markdown("### Display Format")
            display_format = st.radio(
                "Select display format for results",
                ("Structured View", "JSON View", "Table View"),
                horizontal=True,
                help="Choose how you want to view the extracted modules"
            )
            
            if display_format == "Structured View":
                self.render_structured_results(results)
            elif display_format == "JSON View":
                st.markdown("#### Raw JSON Output")
                st.code(json.dumps(results, indent=2), language='json')
            else:
                st.markdown("#### Tabular Data View")
                self.render_table_results(results)
    
    def render_structured_results(self, results):
        """Render results in a structured, user-friendly format."""
        st.markdown("#### Module Structure Analysis")
        
        for i, module in enumerate(results):
            # Professional module cards
            with st.expander(f"{module['module']}", expanded=i < 2):
                # Module description
                st.markdown(f"""
                <div style="
                    background: #f8f9fa;
                    border: 1px solid #e9ecef;
                    border-left: 4px solid #2c3e50;
                    padding: 1rem;
                    margin-bottom: 1rem;
                ">
                    <h4 style="margin: 0 0 0.75rem 0; color: #2c3e50; font-family: 'Inter', sans-serif;">
                        Module Description
                    </h4>
                    <p style="
                        margin: 0;
                        color: #495057;
                        font-size: 1rem;
                        line-height: 1.6;
                        font-family: 'Inter', sans-serif;
                    ">{module['Description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                submodules = module.get('Submodules', {})
                if submodules:
                    st.markdown(f"""
                    <div style="
                        background: #ffffff;
                        border: 1px solid #e9ecef;
                        padding: 1rem;
                        margin-top: 1rem;
                    ">
                        <h4 style="
                            margin: 0 0 1rem 0;
                            color: #495057;
                            font-family: 'Inter', sans-serif;
                        ">Submodules ({len(submodules)})</h4>
                    """, unsafe_allow_html=True)
                    
                    # Display submodules in a clean grid
                    sub_cols = st.columns(2)
                    for idx, (sub_name, sub_desc) in enumerate(submodules.items()):
                        with sub_cols[idx % 2]:
                            st.markdown(f"""
                            <div style="
                                background: #ffffff;
                                border: 1px solid #dee2e6;
                                padding: 1rem;
                                margin-bottom: 0.75rem;
                                box-shadow: 0 1px 3px rgba(0,0,0,0.05);
                            ">
                                <h5 style="
                                    margin: 0 0 0.5rem 0;
                                    color: #2c3e50;
                                    font-family: 'Inter', sans-serif;
                                    font-size: 0.95rem;
                                    font-weight: 600;
                                ">{sub_name}</h5>
                                <p style="
                                    margin: 0;
                                    color: #6c757d;
                                    font-size: 0.9rem;
                                    line-height: 1.5;
                                    font-family: 'Inter', sans-serif;
                                ">{sub_desc}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="
                        background: #fff3cd;
                        border: 1px solid #ffeaa7;
                        padding: 1rem;
                        margin-top: 1rem;
                        text-align: center;
                    ">
                        <p style="
                            margin: 0;
                            color: #856404;
                            font-family: 'Inter', sans-serif;
                            font-style: italic;
                        ">No submodules identified for this module</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    def render_table_results(self, results):
        """Render results in table format."""
        import pandas as pd
        
        # Create table data
        table_data = []
        for module in results:
            submodules = module.get('Submodules', {})
            if submodules:
                for sub_name, sub_desc in submodules.items():
                    table_data.append({
                        'Module': module['module'],
                        'Module Description': module['Description'],
                        'Submodule': sub_name,
                        'Submodule Description': sub_desc
                    })
            else:
                table_data.append({
                    'Module': module['module'],
                    'Module Description': module['Description'],
                    'Submodule': 'N/A',
                    'Submodule Description': 'N/A'
                })
        
        if table_data:
            df = pd.DataFrame(table_data)
            st.dataframe(df, width='stretch')
    
    def render_debug_section(self):
        """Render debug information section."""
        if st.session_state.scraped_pages:
            with st.expander("Debug Information"):
                st.subheader("Scraped Pages")
                for i, page in enumerate(st.session_state.scraped_pages[:5]):  # Show first 5
                    st.write(f"**Page {i+1}:** {page.get('title', 'No title')}")
                    st.write(f"URL: {page.get('url', 'No URL')}")
                    st.write(f"Content length: {len(page.get('content', ''))} characters")
                    if page.get('content'):
                        st.text_area(
                            f"Content preview {i+1}",
                            page['content'][:300] + "..." if len(page['content']) > 300 else page['content'],
                            height=100,
                            key=f"content_{i}"
                        )
                    st.divider()
    
    def run(self):
        """Main application runner."""
        self.render_header()
        
        # Get configuration from sidebar
        config = self.render_sidebar()
        
        # Main content
        urls = self.render_input_section()
        
        self.render_processing_section(urls, config)
        
        self.render_results_section()
        
        self.render_debug_section()
        
        # Enhanced Footer
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="
            background: #2c3e50;
            color: #ffffff;
            padding: 3rem 2rem;
            text-align: center;
            margin-top: 3rem;
            border-top: 1px solid #34495e;
        ">
            <h3 style="
                margin: 0 0 1rem 0;
                font-family: 'Crimson Text', Georgia, serif;
                font-size: 1.8rem;
                font-weight: 600;
                letter-spacing: -0.01em;
            ">PULSEGEN.IO</h3>
            <p style="
                margin: 0 0 2rem 0;
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                opacity: 0.8;
                max-width: 600px;
                margin-left: auto;
                margin-right: auto;
                line-height: 1.6;
            ">
                Advanced AI-driven system for intelligent documentation analysis and structured data extraction.
                Built with modern technologies for enterprise-grade performance.
            </p>
            <div style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 2rem;
                max-width: 800px;
                margin: 0 auto;
            ">
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        <i class="fas fa-search"></i>
                    </div>
                    <h4 style="
                        margin: 0 0 0.25rem 0;
                        font-family: 'Inter', sans-serif;
                        font-size: 0.9rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">Smart Crawling</h4>
                    <p style="
                        margin: 0;
                        font-size: 0.8rem;
                        opacity: 0.7;
                        font-family: 'Inter', sans-serif;
                    ">Intelligent web scraping</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        <i class="fas fa-brain"></i>
                    </div>
                    <h4 style="
                        margin: 0 0 0.25rem 0;
                        font-family: 'Inter', sans-serif;
                        font-size: 0.9rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">AI Analysis</h4>
                    <p style="
                        margin: 0;
                        font-size: 0.8rem;
                        opacity: 0.7;
                        font-family: 'Inter', sans-serif;
                    ">Advanced NLP processing</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        <i class="fas fa-chart-bar"></i>
                    </div>
                    <h4 style="
                        margin: 0 0 0.25rem 0;
                        font-family: 'Inter', sans-serif;
                        font-size: 0.9rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">Structured Data</h4>
                    <p style="
                        margin: 0;
                        font-size: 0.8rem;
                        opacity: 0.7;
                        font-family: 'Inter', sans-serif;
                    ">JSON format output</p>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 1.2rem; margin-bottom: 0.5rem;">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <h4 style="
                        margin: 0 0 0.25rem 0;
                        font-family: 'Inter', sans-serif;
                        font-size: 0.9rem;
                        font-weight: 600;
                        text-transform: uppercase;
                        letter-spacing: 0.05em;
                    ">Real-time</h4>
                    <p style="
                        margin: 0;
                        font-size: 0.8rem;
                        opacity: 0.7;
                        font-family: 'Inter', sans-serif;
                    ">Instant processing</p>
                </div>
            </div>
            <hr style="
                border: none;
                height: 1px;
                background: #34495e;
                margin: 2rem auto;
                max-width: 600px;
            ">
            <p style="
                margin: 0;
                font-family: 'Inter', sans-serif;
                font-size: 0.8rem;
                opacity: 0.6;
                line-height: 1.5;
            ">
                Built with Python, OpenAI GPT, and Streamlit<br>
                Powered by advanced natural language processing and machine learning
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Professional Creator Contact Footer
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 2rem;
            margin-top: 3rem;
            border-radius: 15px 15px 0 0;
            text-align: center;
            position: relative;
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 3px;
                background: linear-gradient(90deg, #3498db, #2ecc71, #f39c12, #e74c3c);
                background-size: 400% 100%;
                animation: shimmer 3s linear infinite;
            "></div>
            <div style="
                display: flex;
                align-items: center;
                justify-content: center;
                margin-bottom: 1.5rem;
                animation: fadeInUp 1s ease-out;
            ">
                <div style="
                    font-size: 2rem;
                    margin-right: 15px;
                    animation: pulse 2s infinite;
                ">
                    <i class="fas fa-code"></i>
                </div>
                <div>
                    <h3 style="
                        margin: 0;
                        color: #ecf0f1;
                        font-family: 'Crimson Text', Georgia, serif;
                        font-size: 1.5rem;
                        font-weight: 600;
                    ">Created by Gokul Kumar V</h3>
                    <div style="
                        width: 50px;
                        height: 2px;
                        background: linear-gradient(90deg, #3498db, #2ecc71);
                        margin: 8px auto 0;
                        border-radius: 1px;
                        animation: pulse 2s infinite;
                    "></div>
                </div>
            </div>
            <div style="
                display: flex;
                justify-content: center;
                gap: 2rem;
                margin-bottom: 1.5rem;
                animation: slideInFromLeft 1.2s ease-out;
            ">
                <a href="https://github.com/gokulkumarv24" target="_blank" style="
                    display: flex;
                    align-items: center;
                    color: #ecf0f1;
                    text-decoration: none;
                    background: linear-gradient(135deg, #333, #444);
                    padding: 0.75rem 1.5rem;
                    border-radius: 10px;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    font-family: 'Inter', sans-serif;
                    font-weight: 500;
                ">
                    <i class="fab fa-github" style="font-size: 1.2rem; margin-right: 8px;"></i>
                    GitHub Profile
                </a>
                <a href="https://www.linkedin.com/in/gokul-kumar-v-236a24217" target="_blank" style="
                    display: flex;
                    align-items: center;
                    color: #ecf0f1;
                    text-decoration: none;
                    background: linear-gradient(135deg, #0077b5, #005885);
                    padding: 0.75rem 1.5rem;
                    border-radius: 10px;
                    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                    font-family: 'Inter', sans-serif;
                    font-weight: 500;
                ">
                    <i class="fab fa-linkedin" style="font-size: 1.2rem; margin-right: 8px;"></i>
                    LinkedIn Profile
                </a>
            </div>
            <p style="
                margin: 0;
                color: #bdc3c7;
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                line-height: 1.6;
                animation: fadeInUp 1.4s ease-out;
            ">
                <i class="fas fa-heart" style="color: #e74c3c; margin-right: 5px;"></i>
                Passionate about AI, Machine Learning, and Building Intelligent Solutions
                <br>
                <i class="fas fa-envelope" style="color: #3498db; margin-right: 5px;"></i>
                Connect with me for collaboration opportunities and project discussions
            </p>
        </div>
        
        <style>
            /* Enhanced link hover effects */
            a[href*="github.com"]:hover {
                background: linear-gradient(135deg, #444, #555) !important;
                transform: translateY(-2px) scale(1.05) !important;
                box-shadow: 0 8px 25px rgba(0,0,0,0.3) !important;
            }
            
            a[href*="linkedin.com"]:hover {
                background: linear-gradient(135deg, #005885, #0077b5) !important;
                transform: translateY(-2px) scale(1.05) !important;
                box-shadow: 0 8px 25px rgba(0, 119, 181, 0.3) !important;
            }
        </style>
        """, unsafe_allow_html=True)

def main():
    """Main function to run the Streamlit app."""
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()