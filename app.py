import streamlit as st
import pandas as pd
from utils.data_processor import DataProcessor
from utils.visualizations import Visualizer
import base64
import pdfkit

# Page configuration
st.set_page_config(
    page_title="Data Analysis Platform",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
with open('static/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Initialize session state
if 'data_processor' not in st.session_state:
    st.session_state.data_processor = None
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None
if 'df' not in st.session_state:
    st.session_state.df = None
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'visualizer' not in st.session_state:
    st.session_state.visualizer = Visualizer()

# Sidebar for API key
with st.sidebar:
    st.subheader("🔑 OpenAI API Configuration")
    api_key = st.text_input(
        "Enter OpenAI API Key",
        type="password",
        value=st.session_state.api_key,
        help="Enter your OpenAI API key to enable natural language queries"
    )

    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        if api_key:
            try:
                st.session_state.data_processor = DataProcessor(api_key)
                st.success("API key configured successfully!")
            except Exception as e:
                st.error(f"Error configuring API key: {str(e)}")
        else:
            st.session_state.data_processor = None

# Header
st.title("📊 Interactive Data Analysis Platform")
st.markdown("""
    <div style='background-color: #f8f9fa; padding: 1rem; border-radius: 8px; margin-bottom: 20px;'>
        Upload your Excel file and ask questions about your data in natural language.
    </div>
""", unsafe_allow_html=True)

# Main content
if not st.session_state.api_key:
    st.warning("Please enter your OpenAI API key in the sidebar to continue.")
else:
    # File upload section
    with st.container():
        st.subheader("📁 Upload Your Data")
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xls', 'xlsx'])

        if uploaded_file is not None and (st.session_state.uploaded_file != uploaded_file):
            st.session_state.uploaded_file = uploaded_file
            with st.spinner("Processing file..."):
                success, result = st.session_state.data_processor.load_excel(uploaded_file)
                if success:
                    st.session_state.df = result
                    st.success("File uploaded successfully!")

                    # Display data summary
                    summary = st.session_state.data_processor.generate_summary()
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Rows", summary["rows"])
                    with col2:
                        st.metric("Columns", summary["columns"])
                    with col3:
                        st.metric("Missing Values", summary["missing_values"])
                else:
                    st.error(f"Error loading file: {result}")

    if st.session_state.df is not None:
        # Tabs for different functionalities
        tab1, tab2 = st.tabs(["📝 Query Data", "📊 Advanced Visualization"])

        # Query Tab
        with tab1:
            st.subheader("🔍 Ask Questions About Your Data")
            query = st.text_input(
                "Enter your question:",
                placeholder="e.g., 'What is the average of column X?' or 'Show me a trend analysis'"
            )

            if query:
                st.write(f"Debug: Processing query: {query}")  # Debugging statement
                with st.spinner("Processing your question..."):
                    try:
                        success, result = st.session_state.data_processor.process_query(query)
                        st.write(f"Debug: Success: {success}, Result: {result}")  # Debugging statement
                    except Exception as e:
                        st.error(f"Error during query processing: {str(e)}")
                        st.write(f"Debug: Exception: {str(e)}")  # Debugging statement

                    if success:
                        st.markdown("### 📊 Results")
                        if isinstance(result, pd.DataFrame):
                            st.dataframe(result)

                            # Export buttons
                            col1, col2 = st.columns(2)  # Create two columns
                            with col1:
                                if st.button("Export to Excel"):
                                    result.to_excel("result.xlsx", index=False)
                                    st.success("Data exported to Excel successfully!")

                        elif isinstance(result, (pd.Series, list, str, int, float)):
                            st.write(result)

                        # Basic visualization of results
                        if isinstance(result, pd.DataFrame) and len(result.columns) > 0:
                            st.markdown("### 📈 Query Result Visualization")
                            numeric_cols = result.select_dtypes(include=['int64', 'float64']).columns
                            if len(numeric_cols) > 0:
                                col = numeric_cols[0]
                                fig = st.session_state.data_processor.create_visualization(col)
                                if fig:
                                    st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(result)
                st.write("Debug: Query processing completed.")  # Debugging statement

        # Advanced Visualization Tab
        with tab2:
            st.subheader("📊 Advanced Data Visualization")

            # Visualization controls
            col1, col2 = st.columns([2, 2])

            with col1:
                chart_type = st.selectbox(
                    "Select Chart Type",
                    options=list(Visualizer.CHART_TYPES.keys()),
                    format_func=lambda x: Visualizer.CHART_TYPES[x]
                )

                color_scheme = st.selectbox(
                    "Color Scheme",
                    options=['default', 'categorical', 'sequential', 'diverging'],
                    format_func=lambda x: x.title()
                )

            with col2:
                title = st.text_input("Chart Title", "")

            # Column selection based on chart type
            col1, col2, col3 = st.columns([2, 2, 2])

            numeric_cols = st.session_state.visualizer.get_numeric_columns(st.session_state.df)
            categorical_cols = st.session_state.visualizer.get_categorical_columns(st.session_state.df)
            all_cols = st.session_state.df.columns.tolist()

            with col1:
                if chart_type == 'histogram':
                    x_column = st.selectbox("Select Column", options=numeric_cols, key='x_col')
                    y_column = None
                elif chart_type == 'pie':
                    x_column = st.selectbox("Names Column", options=categorical_cols, key='x_col')
                    y_column = st.selectbox("Values Column", options=numeric_cols, key='y_col')
                else:
                    x_column = st.selectbox("X-Axis Column", options=all_cols, key='x_col')

            with col2:
                if chart_type not in ['histogram', 'pie']:
                    y_column = st.selectbox("Y-Axis Column", options=numeric_cols, key='y_col')

            with col3:
                if chart_type in ['scatter', 'bar']:
                    color_column = st.selectbox(
                        "Color By (Optional)",
                        options=['None'] + categorical_cols,
                        key='color_col'
                    )
                    color_column = None if color_column == 'None' else color_column
                else:
                    color_column = None

            # Create and display visualization
            if chart_type and x_column:
                with st.spinner("Creating visualization..."):
                    fig = st.session_state.visualizer.create_visualization(
                        st.session_state.df,
                        chart_type,
                        x_column,
                        y_column,
                        color_column,
                        title,
                        color_scheme
                    )
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error("Could not create visualization with the selected parameters")

        # Data preview
        st.subheader("📑 Data Preview")
        st.dataframe(st.session_state.df.head())

# Footer
st.markdown("""
    <div style='text-align: center; padding: 20px; color: #666;'>
        Built with Streamlit and PandasAI
    </div>
""", unsafe_allow_html=True)