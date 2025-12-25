import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from pathlib import Path
import json
from datetime import datetime
import matplotlib.pyplot as plt
import sys
from streamlit_option_menu import option_menu
import base64

# Page configuration
st.set_page_config(
    page_title="Supply Chain Intelligence Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #3B82F6;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 1rem;
    }
    .phase-card {
        background-color: #F0F9FF;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #E0F2FE;
        margin-bottom: 1rem;
    }
    .success-badge {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
    .warning-badge {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

class SupplyChainDashboard:
    def __init__(self):
        self.data_dir = Path("data")
        self.setup_directories()
        self.load_data()
        
    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            "data/raw",
            "data/processed", 
            "data/relational",
            "data/analytics",
            "data/ai",
            "data/final",
            "logs"
        ]
        for dir_path in directories:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    def load_data(self):
        """Load data from the most recent files"""
        try:
            # Load relational data
            relational_dir = self.data_dir / "relational"
            if relational_dir.exists():
                companies_files = list(relational_dir.glob("companies_*.csv"))
                facilities_files = list(relational_dir.glob("facilities_*.csv"))
                links_files = list(relational_dir.glob("company_facilities_*.csv"))
                
                if companies_files:
                    latest_companies = max(companies_files, key=os.path.getctime)
                    self.companies_df = pd.read_csv(latest_companies)
                
                if facilities_files:
                    latest_facilities = max(facilities_files, key=os.path.getctime)
                    self.facilities_df = pd.read_csv(latest_facilities)
                
                if links_files:
                    latest_links = max(links_files, key=os.path.getctime)
                    self.links_df = pd.read_csv(latest_links)
            
            # Load AI data
            ai_dir = self.data_dir / "ai"
            if ai_dir.exists():
                ai_files = list(ai_dir.glob("duplicate_companies_*.csv"))
                if ai_files:
                    latest_ai = max(ai_files, key=os.path.getctime)
                    self.ai_df = pd.read_csv(latest_ai)
            
            # Load final statistics
            final_dir = self.data_dir / "final"
            if final_dir.exists():
                stats_files = list(final_dir.glob("summary_stats_*.json"))
                if stats_files:
                    latest_stats = max(stats_files, key=os.path.getctime)
                    with open(latest_stats, 'r') as f:
                        self.summary_stats = json.load(f)
            
            # Load logs
            log_file = Path("logs/pipeline.log")
            if log_file.exists():
                with open(log_file, 'r') as f:
                    self.logs = f.readlines()[-100:]  # Last 100 lines
            
        except Exception as e:
            st.warning(f"Error loading data: {e}")
            self.companies_df = pd.DataFrame()
            self.facilities_df = pd.DataFrame()
            self.links_df = pd.DataFrame()
            self.ai_df = pd.DataFrame()
            self.summary_stats = {}
            self.logs = []
    
    def run_pipeline_phase(self, phase_number):
        """Execute a specific pipeline phase"""
        try:
            if phase_number == 1:
                from p1_scrape_oar import generate_oar_dataset
                generate_oar_dataset()
            elif phase_number == 2:
                from p2_clean_companies import CompanyCleaner
                CompanyCleaner().run()
            elif phase_number == 3:
                from p3_clean_facilities import FacilityProcessor
                FacilityProcessor().run()
            elif phase_number == 4:
                from p4_relational_builder import RelationalBuilder
                RelationalBuilder().run()
            elif phase_number == 5:
                from p5_analytics_dashboards import AnalyticsDashboard
                AnalyticsDashboard().run()
            elif phase_number == 6:
                from p6_ai_module import DuplicateDetector
                DuplicateDetector().run()
            elif phase_number == 7:
                from p7_export_final import FinalExporter
                FinalExporter().run()
            
            # Reload data after execution
            self.load_data()
            return True
        except Exception as e:
            st.error(f"Error executing phase {phase_number}: {e}")
            return False

def main():
    dashboard = SupplyChainDashboard()
    
    # Sidebar - Navigation
    with st.sidebar:
        st.image(
            "https://img.icons8.com/color/96/000000/factory.png",
            width=90
        )

        st.markdown(
            """
            <h2 style="
                text-align: center;
                color: var(--text-color);
            ">
                Supply Chain Intelligence
            </h2>
            """,
            unsafe_allow_html=True
        )

        selected = option_menu(
            menu_title="Navigation",
            options=["Dashboard", "Pipeline", "Data", "Analytics", "AI", "Configuration"],
            icons=["speedometer", "gear", "database", "bar-chart", "robot", "tools"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "var(--secondary-background-color)",
                },
                "icon": {
                    "color": "var(--primary-color)",
                    "font-size": "18px",
                },
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "var(--text-color)",
                },
                "nav-link-selected": {
                    "background-color": "var(--primary-color)",
                    "color": "white",
                },
            }
        )

    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 class='main-header'>🏭 Supply Chain Intelligence Dashboard</h1>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<p style='text-align: right; color: #6B7280;'>{datetime.now().strftime('%d %B %Y, %H:%M')}</p>", unsafe_allow_html=True)
    
    # Main page based on selection
    if selected == "Dashboard":
        show_dashboard(dashboard)
    elif selected == "Pipeline":
        show_pipeline(dashboard)
    elif selected == "Data":
        show_data_explorer(dashboard)
    elif selected == "Analytics":
        show_analytics(dashboard)
    elif selected == "AI":
        show_ai_module(dashboard)
    elif selected == "Configuration":
        show_configuration(dashboard)

def show_dashboard(dashboard):
    """Display main dashboard"""
    
    # Main metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_companies = len(dashboard.companies_df) if not dashboard.companies_df.empty else 0
        st.metric("Companies", f"{total_companies:,}")
    
    with col2:
        total_facilities = len(dashboard.facilities_df) if not dashboard.facilities_df.empty else 0
        st.metric("Facilities", f"{total_facilities:,}")
    
    with col3:
        if dashboard.summary_stats:
            avg_facilities = dashboard.summary_stats.get('average_facilities_per_company', 0)
            st.metric("Facilities/Company", f"{avg_facilities:.1f}")
        else:
            st.metric("Facilities/Company", "N/A")
    
    with col4:
        duplicates = len(dashboard.ai_df) if not dashboard.ai_df.empty else 0
        st.metric("Duplicates Detected", duplicates)
    
    # Main charts
    col1, col2 = st.columns(2)
    
    with col1:
        if not dashboard.companies_df.empty:
            st.markdown("<h3 class='sub-header'>Distribution by Country</h3>", unsafe_allow_html=True)
            country_counts = dashboard.companies_df['country'].value_counts()
            fig = px.pie(
                values=country_counts.values,
                names=country_counts.index,
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Blues_r
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if not dashboard.companies_df.empty and 'industry' in dashboard.companies_df.columns:
            st.markdown("<h3 class='sub-header'>Industry Distribution</h3>", unsafe_allow_html=True)
            industry_counts = dashboard.companies_df['industry'].value_counts().head(10)
            fig = px.bar(
                x=industry_counts.values,
                y=industry_counts.index,
                orientation='h',
                color=industry_counts.values,
                color_continuous_scale='Blues'
            )
            fig.update_layout(xaxis_title="Number of Companies", yaxis_title="Industry")
            st.plotly_chart(fig, use_container_width=True)
    
    # Pipeline status cards
    st.markdown("<h3 class='sub-header'>Pipeline Status</h3>", unsafe_allow_html=True)
    
    phases = [
        {"name": "1. Extraction", "status": Path("data/raw/oar_companies_raw.csv").exists()},
        {"name": "2. Cleaning", "status": len(list(Path("data/processed").glob("companies_cleaned_*.csv"))) > 0},
        {"name": "3. Facilities", "status": len(list(Path("data/processed").glob("facilities_cleaned_*.csv"))) > 0},
        {"name": "4. Relational", "status": len(list(Path("data/relational").glob("companies_*.csv"))) > 0},
        {"name": "5. Analytics", "status": len(list(Path("data/analytics").glob("*.png"))) > 0},
        {"name": "6. AI", "status": len(list(Path("data/ai").glob("*.csv"))) > 0},
        {"name": "7. Final Export", "status": len(list(Path("data/final").glob("*.csv"))) > 0},
    ]
    
    cols = st.columns(len(phases))
    for idx, (col, phase) in enumerate(zip(cols, phases)):
        with col:
            color = "🟢" if phase["status"] else "🔴"
            st.markdown(f"**{phase['name']}**")
            st.markdown(f"<h2>{color}</h2>", unsafe_allow_html=True)

def show_pipeline(dashboard):
    """Display pipeline control interface"""
    
    st.markdown("<h2 class='main-header'>🔄 Processing Pipeline</h2>", unsafe_allow_html=True)
    
    # Phase descriptions
    phases_info = {
        1: {"title": "Phase 1 - Data Extraction", 
            "description": "Synthetic OAR data generation",
            "output": "data/raw/oar_companies_raw.csv"},
        2: {"title": "Phase 2 - Company Cleaning", 
            "description": "Company normalization and deduplication",
            "output": "data/processed/companies_cleaned_*.csv"},
        3: {"title": "Phase 3 - Facility Processing", 
            "description": "Facility creation and relationships",
            "output": "data/processed/facilities_cleaned_*.csv"},
        4: {"title": "Phase 4 - Relational Structuring", 
            "description": "Validation and relational structure",
            "output": "data/relational/"},
        5: {"title": "Phase 5 - Analytics Dashboards", 
            "description": "Visualizations and analysis",
            "output": "data/analytics/"},
        6: {"title": "Phase 6 - AI Module", 
            "description": "Duplicate detection via embeddings",
            "output": "data/ai/duplicate_companies_*.csv"},
        7: {"title": "Phase 7 - Final Export", 
            "description": "Complete export with statistics",
            "output": "data/final/"}
    }
    
    # Execution controls
    st.markdown("<h3 class='sub-header'>Pipeline Execution</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Run Entire Pipeline", use_container_width=True):
            with st.spinner("Executing complete pipeline..."):
                for phase in range(1, 8):
                    st.info(f"Executing phase {phase}...")
                    success = dashboard.run_pipeline_phase(phase)
                    if not success:
                        st.error(f"Phase {phase} failed")
                        break
                else:
                    st.success("Pipeline executed successfully!")
                    st.rerun()
    
    with col2:
        selected_phase = st.selectbox(
            "Select Phase",
            options=list(phases_info.keys()),
            format_func=lambda x: phases_info[x]["title"]
        )
    
    with col3:
        if st.button(f"▶️ Execute Phase {selected_phase}", use_container_width=True):
            with st.spinner(f"Executing phase {selected_phase}..."):
                success = dashboard.run_pipeline_phase(selected_phase)
                if success:
                    st.success(f"Phase {selected_phase} executed successfully!")
                    st.rerun()
                else:
                    st.error("Execution failed")
    
    # Selected phase details
    st.markdown(f"<div class='phase-card'>", unsafe_allow_html=True)
    st.markdown(f"### {phases_info[selected_phase]['title']}")
    st.markdown(f"**Description:** {phases_info[selected_phase]['description']}")
    st.markdown(f"**Output:** `{phases_info[selected_phase]['output']}`")
    
    # Check if phase has been executed
    output_path = Path(phases_info[selected_phase]['output'].split("*")[0])
    if "*" in phases_info[selected_phase]['output']:
        files = list(Path(phases_info[selected_phase]['output'].split("*")[0].rsplit("/", 1)[0]).glob(
            phases_info[selected_phase]['output'].split("*")[1]))
        status = len(files) > 0
    else:
        status = output_path.exists()
    
    if status:
        st.markdown("<span class='success-badge'>✓ Executed</span>", unsafe_allow_html=True)
    else:
        st.markdown("<span class='warning-badge'>⏳ Pending</span>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Pipeline logs
    st.markdown("<h3 class='sub-header'>📝 Pipeline Logs</h3>", unsafe_allow_html=True)
    
    if dashboard.logs:
        with st.expander("View Logs", expanded=False):
            log_container = st.container(height=300)
            for log_line in reversed(dashboard.logs[-50:]):
                log_container.text(log_line.strip())
    else:
        st.info("No logs available")

def show_data_explorer(dashboard):
    """Interactive data explorer"""
    
    st.markdown("<h2 class='main-header'>📊 Data Explorer</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Companies", "Facilities", "Relationships", "Raw Data"])
    
    with tab1:
        if not dashboard.companies_df.empty:
            st.dataframe(
                dashboard.companies_df,
                use_container_width=True,
                height=400,
                column_config={
                    "company_id": "ID",
                    "company_name": "Name",
                    "country": "Country",
                    "industry": "Industry",
                    "facility_count": "Facility Count"
                }
            )
            
            # Company filters
            col1, col2 = st.columns(2)
            with col1:
                countries = st.multiselect(
                    "Filter by Country",
                    options=dashboard.companies_df['country'].unique() if not dashboard.companies_df.empty else [],
                    default=[]
                )
            
            with col2:
                industries = st.multiselect(
                    "Filter by Industry",
                    options=dashboard.companies_df['industry'].unique() if not dashboard.companies_df.empty and 'industry' in dashboard.companies_df.columns else [],
                    default=[]
                )
            
            # Filtered company statistics
            filtered_df = dashboard.companies_df
            if countries:
                filtered_df = filtered_df[filtered_df['country'].isin(countries)]
            if industries:
                filtered_df = filtered_df[filtered_df['industry'].isin(industries)]
            
            st.metric("Filtered Companies", len(filtered_df))
            
        else:
            st.warning("No company data available")
    
    with tab2:
        if not dashboard.facilities_df.empty:
            st.dataframe(
                dashboard.facilities_df,
                use_container_width=True,
                height=400
            )
            
            # Facility map by country
            if 'country' in dashboard.facilities_df.columns:
                facility_by_country = dashboard.facilities_df['country'].value_counts()
                fig = px.bar(
                    x=facility_by_country.index,
                    y=facility_by_country.values,
                    title="Facilities by Country",
                    color=facility_by_country.values,
                    color_continuous_scale='Viridis'
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No facility data available")
    
    with tab3:
        if not dashboard.links_df.empty:
            st.dataframe(
                dashboard.links_df,
                use_container_width=True,
                height=400
            )
            
            # Network visualization
            if not dashboard.companies_df.empty:
                # Create simple network graph
                company_facility_counts = dashboard.links_df.groupby('company_id').size()
                
                fig = go.Figure(data=[
                    go.Histogram(
                        x=company_facility_counts.values,
                        nbinsx=30,
                        marker_color='#3B82F6'
                    )
                ])
                
                fig.update_layout(
                    title="Facility Distribution per Company",
                    xaxis_title="Number of Facilities",
                    yaxis_title="Number of Companies"
                )
                
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No relationship data available")
    
    with tab4:
        raw_files = list(Path("data/raw").glob("*.csv"))
        if raw_files:
            selected_file = st.selectbox(
                "Select Raw File",
                options=raw_files,
                format_func=lambda x: x.name
            )
            
            if selected_file:
                raw_df = pd.read_csv(selected_file)
                st.dataframe(raw_df.head(100), use_container_width=True, height=400)
                st.metric("Total Rows", len(raw_df))
                st.metric("Columns", len(raw_df.columns))
        else:
            st.info("No raw files available")

def show_analytics(dashboard):
    """Analytics dashboards"""
    
    st.markdown("<h2 class='main-header'>📈 Analytics Dashboards</h2>", unsafe_allow_html=True)
    
    # Check if visualizations exist
    analytics_dir = Path("data/analytics")
    if analytics_dir.exists():
        png_files = list(analytics_dir.glob("*.png"))
        
        if png_files:
            col1, col2 = st.columns(2)
            
            with col1:
                companies_chart = analytics_dir / "companies_by_country.png"
                if companies_chart.exists():
                    st.image(str(companies_chart), caption="Companies by Country")
                else:
                    st.info("'Companies by Country' chart not available")
            
            with col2:
                facilities_chart = analytics_dir / "facilities_per_company.png"
                if facilities_chart.exists():
                    st.image(str(facilities_chart), caption="Facilities per Company")
                else:
                    st.info("'Facilities per Company' chart not available")
    
    # Additional interactive visualizations
    if not dashboard.companies_df.empty:
        st.markdown("<h3 class='sub-header'>Interactive Visualizations</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Bar chart of companies by country
            if 'country' in dashboard.companies_df.columns:
                country_data = dashboard.companies_df['country'].value_counts().reset_index()
                country_data.columns = ['country', 'count']
                
                fig = px.bar(
                    country_data,
                    x='country',
                    y='count',
                    title="Companies by Country",
                    color='count',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(xaxis_title="Country", yaxis_title="Number of Companies")
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Scatter plot of facilities vs countries
            if not dashboard.facilities_df.empty and 'country' in dashboard.facilities_df.columns:
                facilities_by_country = dashboard.facilities_df['country'].value_counts().reset_index()
                facilities_by_country.columns = ['country', 'facility_count']
                
                if not dashboard.companies_df.empty:
                    companies_by_country = dashboard.companies_df['country'].value_counts().reset_index()
                    companies_by_country.columns = ['country', 'company_count']
                    
                    merged_data = pd.merge(facilities_by_country, companies_by_country, on='country', how='outer')
                    merged_data['ratio'] = merged_data['facility_count'] / merged_data['company_count']
                    
                    fig = px.scatter(
                        merged_data,
                        x='company_count',
                        y='facility_count',
                        size='ratio',
                        color='country',
                        hover_name='country',
                        title="Facilities vs Companies by Country",
                        size_max=60
                    )
                    fig.update_layout(xaxis_title="Number of Companies", yaxis_title="Number of Facilities")
                    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed metrics
    st.markdown("<h3 class='sub-header'>📊 Detailed Metrics</h3>", unsafe_allow_html=True)
    
    if dashboard.summary_stats:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Companies",
                dashboard.summary_stats.get('total_companies', 'N/A')
            )
        
        with col2:
            st.metric(
                "Total Facilities",
                dashboard.summary_stats.get('total_facilities', 'N/A')
            )
        
        with col3:
            st.metric(
                "Average Facilities/Company",
                f"{dashboard.summary_stats.get('average_facilities_per_company', 0):.2f}"
            )
    
    # Data export
    st.markdown("<h3 class='sub-header'>📤 Data Export</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Companies CSV", use_container_width=True):
            if not dashboard.companies_df.empty:
                csv = dashboard.companies_df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()
                href = f'<a href="data:file/csv;base64,{b64}" download="companies.csv">Download CSV</a>'
                st.markdown(href, unsafe_allow_html=True)
    
    with col2:
        if st.button("📊 Download Statistics JSON", use_container_width=True):
            if dashboard.summary_stats:
                json_str = json.dumps(dashboard.summary_stats, indent=2)
                b64 = base64.b64encode(json_str.encode()).decode()
                href = f'<a href="data:file/json;base64,{b64}" download="stats.json">Download JSON</a>'
                st.markdown(href, unsafe_allow_html=True)
    
  
def show_ai_module(dashboard):
    """AI Module - Duplicate Detection"""
    
    st.markdown("<h2 class='main-header'>🤖 AI Module - Duplicate Detection</h2>", unsafe_allow_html=True)
    
    # AI module configuration
    with st.expander("⚙️ Model Configuration", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sample_size = st.slider("Sample Size", 20, 100, 30)
        
        with col2:
            similarity_threshold = st.slider("Similarity Threshold", 0.5, 1.0, 0.85, 0.05)
        
        with col3:
            model_choice = st.selectbox(
                "Embedding Model",
                ["all-MiniLM-L6-v2"]
            )
    
    # Run duplicate detection
    if st.button("🔍 Run Duplicate Detection", type="primary"):
        with st.spinner("Running duplicate detection..."):
            try:
                # Run phase 6 with parameters
                detector = None
                # Note: You'll need to adapt the code to accept these parameters
                success = dashboard.run_pipeline_phase(6)
                
                if success:
                    st.success("Detection completed successfully!")
                    dashboard.load_data()  # Reload data
                    st.rerun()
                else:
                    st.error("Detection failed")
            except Exception as e:
                st.error(f"Error: {e}")
    
    # Display results
    if not dashboard.ai_df.empty:
        st.markdown("<h3 class='sub-header'>📋 Detection Results</h3>", unsafe_allow_html=True)
        
        st.dataframe(
            dashboard.ai_df,
            use_container_width=True,
            height=300,
            column_config={
                "company_1_name": "Company 1",
                "company_2_name": "Company 2", 
                "similarity": st.column_config.NumberColumn(
                    "Similarity",
                    format="%.3f",
                    help="Similarity score between 0 and 1"
                )
            }
        )
        
        # Similarity visualization
        fig = px.histogram(
            dashboard.ai_df,
            x='similarity',
            nbins=20,
            title="Similarity Score Distribution",
            color_discrete_sequence=['#FF6B6B']
        )
        fig.add_vline(
            x=similarity_threshold,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Threshold: {similarity_threshold}"
        )
        fig.update_layout(xaxis_title="Similarity Score", yaxis_title="Number of Pairs")
        st.plotly_chart(fig, use_container_width=True)
        
        # Duplicate details
        st.markdown("<h3 class='sub-header'>🔍 Duplicate Analysis</h3>", unsafe_allow_html=True)
        
        for idx, row in dashboard.ai_df.iterrows():
            with st.expander(f"Pair #{idx+1}: {row['company_1_name']} ↔ {row['company_2_name']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**{row['company_1_name']}**")
                    st.markdown(f"ID: `{row['company_1_id']}`")
                    
                    # Find additional information
                    if not dashboard.companies_df.empty:
                        company_info = dashboard.companies_df[
                            dashboard.companies_df['company_id'] == row['company_1_id']
                        ]
                        if not company_info.empty:
                            st.markdown(f"Country: {company_info.iloc[0]['country']}")
                            if 'industry' in company_info.columns:
                                st.markdown(f"Industry: {company_info.iloc[0]['industry']}")
                
                with col2:
                    st.markdown(f"**{row['company_2_name']}**")
                    st.markdown(f"ID: `{row['company_2_id']}`")
                    
                    if not dashboard.companies_df.empty:
                        company_info = dashboard.companies_df[
                            dashboard.companies_df['company_id'] == row['company_2_id']
                        ]
                        if not company_info.empty:
                            st.markdown(f"Country: {company_info.iloc[0]['country']}")
                            if 'industry' in company_info.columns:
                                st.markdown(f"Industry: {company_info.iloc[0]['industry']}")
                
                # Similarity score
                st.progress(row['similarity'], text=f"Similarity Score: {row['similarity']:.3f}")
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("👁️ View Details", key=f"view_{idx}"):
                        st.info("Feature to be developed")
                with col2:
                    if st.button("✅ Keep Separate", key=f"keep_{idx}"):
                        st.success("Marked as distinct")
                with col3:
                    if st.button("🗑️ Merge", key=f"merge_{idx}"):
                        st.warning("Merge requested")
    
    else:
        st.info("No detection results available. Run the AI module first.")
    
    # AI module statistics
    if not dashboard.ai_df.empty:
        st.markdown("<h3 class='sub-header'>📊 AI Statistics</h3>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_pairs = len(dashboard.ai_df)
            st.metric("Pairs Detected", total_pairs)
        
        with col2:
            if total_pairs > 0:
                avg_similarity = dashboard.ai_df['similarity'].mean()
                st.metric("Average Similarity", f"{avg_similarity:.3f}")
            else:
                st.metric("Average Similarity", "N/A")
        
        with col3:
            high_similarity = len(dashboard.ai_df[dashboard.ai_df['similarity'] > 0.9])
            st.metric("Similarity > 0.9", high_similarity)

def show_configuration(dashboard):
    """System configuration"""
    
    st.markdown("<h2 class='main-header'>⚙️ System Configuration</h2>", unsafe_allow_html=True)
    
    st.markdown("<h3 class='sub-header'>About</h3>", unsafe_allow_html=True)
        
    st.markdown("""
        ### Supply Chain Intelligence Dashboard
        
        **Last Updated:** 25 December 2025
        
        ### Description
        This dashboard enables complete management of a supply chain data pipeline,
        from synthetic extraction to advanced AI analysis.
        
        ### Main Features
        - 🏭 Synthetic OAR data generation
        - 🧹 Company cleaning and normalization
        - 🔗 Relational structuring
        - 📈 Analytics dashboards
        - 🤖 AI duplicate detection
        - 📤 Final data exports
        
        ### Author
        Soukayna Tahiri
        """)
        
        # Contact information
    with st.expander(" Contact "):
            st.markdown("""
            **GitHub:** https://github.com/soukayna-thr
            
            ### User Guide
            1. Start with the **Pipeline** page to execute phases
            2. Explore data in **Data**
            3. Analyze results in **Analytics**
            4. Use the **AI** module for duplicate detection
            """)

if __name__ == "__main__":
    main()