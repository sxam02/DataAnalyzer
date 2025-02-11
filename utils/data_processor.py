import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI
import plotly.express as px
import streamlit as st

class DataProcessor:
    def __init__(self, api_key):
        """Initialize with API key"""
        if not api_key:
            raise ValueError("OpenAI API key is required")
        try:
            self.llm = OpenAI(api_token=api_key)
            self.df = None
            self.smart_df = None
            self.fallback_mode = False
            self._initialize_pandasai()
        except Exception as e:
            st.warning("Initializing in basic mode due to PandasAI configuration issues.")
            self.fallback_mode = True
            self.df = None

    def _initialize_pandasai(self):
        """Initialize PandasAI with error handling"""
        try:
            # Test PandasAI initialization with a small DataFrame
            test_df = pd.DataFrame({'test': [1, 2, 3]})
            SmartDataframe(test_df, config={"llm": self.llm})
            self.fallback_mode = False
        except Exception as e:
            st.warning(f"""
                Running in compatibility mode due to initialization error: {str(e)}
                Basic data analysis features will still work.
                """)
            self.fallback_mode = True

    def load_excel(self, file):
        """Load and validate Excel file"""
        try:
            self.df = pd.read_excel(file)
            if not self.fallback_mode:
                try:
                    self.smart_df = SmartDataframe(self.df, config={"llm": self.llm})
                except Exception as e:
                    st.warning("""
                        Notice: Switching to compatibility mode. 
                        Basic data analysis features will still work.
                        """)
                    self.fallback_mode = True
            return True, self.df
        except Exception as e:
            return False, f"Error loading file: {str(e)}"

    def process_query(self, query):
        """Process natural language query using PandasAI or fallback to basic pandas"""
        try:
            if self.df is None:
                return False, "No data loaded. Please upload a file first."

            if self.fallback_mode:
                # Enhanced basic pandas operations
                try:
                    query = query.lower()
                    result = None

                    # Basic statistical operations
                    if any(word in query for word in ["average", "mean"]):
                        result = self.df.mean(numeric_only=True)
                    elif "median" in query:
                        result = self.df.median(numeric_only=True)
                    elif "sum" in query:
                        result = self.df.sum(numeric_only=True)
                    elif "count" in query:
                        result = len(self.df)
                    elif "describe" in query:
                        result = self.df.describe()
                    elif "unique" in query:
                        # Find column names in query
                        for col in self.df.columns:
                            if col.lower() in query.lower():
                                result = self.df[col].unique()
                                break
                    elif "correlation" in query or "corr" in query:
                        result = self.df.corr()
                    elif "top" in query or "first" in query:
                        n = 5  # default
                        for num in range(1, 21):
                            if str(num) in query:
                                n = num
                                break
                        result = self.df.head(n)
                    else:
                        result = self.df.head()

                    if result is not None:
                        return True, result
                    return False, "Could not process query in basic mode. Try using simpler queries like 'show average' or 'describe data'."
                except Exception as e:
                    return False, f"Error processing basic query: {str(e)}"
            else:
                # Use PandasAI for advanced queries
                try:
                    result = self.smart_df.chat(str(query))
                    return True, result
                except Exception as e:
                    st.warning("Advanced query failed, falling back to basic mode.")
                    self.fallback_mode = True
                    return self.process_query(query)  # Retry with fallback mode

        except Exception as e:
            return False, f"Unexpected error: {str(e)}"

    def generate_summary(self):
        """Generate basic summary statistics of the dataset"""
        if self.df is None:
            return None

        try:
            summary = {
                "rows": len(self.df),
                "columns": len(self.df.columns),
                "numeric_columns": len(self.df.select_dtypes(include=['int64', 'float64']).columns),
                "missing_values": self.df.isnull().sum().sum(),
                "column_types": dict(self.df.dtypes.value_counts())
            }
            return summary
        except Exception as e:
            st.error(f"Error generating summary: {str(e)}")
            return {
                "rows": 0,
                "columns": 0,
                "numeric_columns": 0,
                "missing_values": 0,
                "column_types": {}
            }

    def create_visualization(self, column_name, chart_type="bar"):
        """Create visualization based on column data"""
        if self.df is None:
            return None

        try:
            if chart_type == "bar":
                fig = px.bar(self.df, x=column_name)
            elif chart_type == "line":
                fig = px.line(self.df, x=self.df.index, y=column_name)
            elif chart_type == "histogram":
                fig = px.histogram(self.df, x=column_name)
            else:
                return None

            return fig
        except Exception:
            return None