import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class Visualizer:
    CHART_TYPES = {
        'bar': 'Bar Chart',
        'line': 'Line Chart',
        'scatter': 'Scatter Plot',
        'histogram': 'Histogram',
        'box': 'Box Plot',
        'violin': 'Violin Plot',
        'pie': 'Pie Chart',
        'heatmap': 'Heatmap'
    }

    def __init__(self):
        self.color_schemes = {
            'default': ['#4B8BBE'],
            'categorical': px.colors.qualitative.Set3,
            'sequential': px.colors.sequential.Viridis,
            'diverging': px.colors.diverging.RdBu
        }

    def create_visualization(self, df, chart_type, x_column=None, y_column=None, 
                           color_column=None, title="", color_scheme='default'):
        """Create a visualization based on the specified parameters"""
        if df is None or df.empty:
            return None

        try:
            colors = self.color_schemes.get(color_scheme, self.color_schemes['default'])

            if chart_type == 'bar':
                fig = self._create_bar_chart(df, x_column, y_column, title, colors)
            elif chart_type == 'line':
                fig = self._create_line_chart(df, x_column, y_column, title, colors)
            elif chart_type == 'scatter':
                fig = self._create_scatter_plot(df, x_column, y_column, color_column, title, colors)
            elif chart_type == 'histogram':
                fig = self._create_histogram(df, x_column, title, colors)
            elif chart_type == 'box':
                fig = self._create_box_plot(df, x_column, y_column, title, colors)
            elif chart_type == 'violin':
                fig = self._create_violin_plot(df, x_column, y_column, title, colors)
            elif chart_type == 'pie':
                fig = self._create_pie_chart(df, x_column, y_column, title, colors)
            elif chart_type == 'heatmap':
                fig = self._create_heatmap(df, x_column, y_column, title)
            else:
                return None

            self._apply_common_styling(fig)
            return fig
        except Exception as e:
            print(f"Error creating visualization: {str(e)}")
            return None

    def _apply_common_styling(self, fig):
        """Apply common styling to all charts"""
        fig.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(family="Inter"),
            margin=dict(t=40, l=20, r=20, b=20),
            title_x=0.5,
            showlegend=True
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#f0f0f0')

    def _create_bar_chart(self, df, x_column, y_column, title, colors):
        return px.bar(
            df, x=x_column, y=y_column,
            title=title,
            template="simple_white",
            color_discrete_sequence=colors
        )

    def _create_line_chart(self, df, x_column, y_column, title, colors):
        return px.line(
            df, x=x_column, y=y_column,
            title=title,
            template="simple_white",
            color_discrete_sequence=colors
        )

    def _create_scatter_plot(self, df, x_column, y_column, color_column, title, colors):
        return px.scatter(
            df, x=x_column, y=y_column,
            color=color_column,
            title=title,
            template="simple_white",
            color_discrete_sequence=colors
        )

    def _create_histogram(self, df, x_column, title, colors):
        return px.histogram(
            df, x=x_column,
            title=title,
            template="simple_white",
            color_discrete_sequence=colors
        )

    def _create_box_plot(self, df, x_column, y_column, title, colors):
        return px.box(
            df, x=x_column, y=y_column,
            title=title,
            template="simple_white",
            color_discrete_sequence=colors
        )

    def _create_violin_plot(self, df, x_column, y_column, title, colors):
        return px.violin(
            df, x=x_column, y=y_column,
            title=title,
            template="simple_white",
            color_discrete_sequence=colors
        )

    def _create_pie_chart(self, df, names_column, values_column, title, colors):
        return px.pie(
            df, names=names_column, values=values_column,
            title=title,
            template="simple_white",
            color_discrete_sequence=colors
        )

    def _create_heatmap(self, df, x_column, y_column, title):
        # Create correlation matrix if no columns specified
        if x_column is None or y_column is None:
            correlation_matrix = df.corr()
            return go.Figure(data=go.Heatmap(
                z=correlation_matrix.values,
                x=correlation_matrix.columns,
                y=correlation_matrix.columns,
                colorscale='RdBu'
            ), layout=dict(title=title or 'Correlation Matrix'))

        # Create pivot table for specified columns
        pivot_table = pd.pivot_table(
            df, values=y_column, 
            index=x_column, 
            aggfunc='mean'
        )
        return go.Figure(data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale='RdBu'
        ), layout=dict(title=title))

    @staticmethod
    def get_numeric_columns(df):
        """Get list of numeric columns from dataframe"""
        return df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    @staticmethod
    def get_categorical_columns(df):
        """Get list of categorical columns from dataframe"""
        return df.select_dtypes(include=['object', 'category']).columns.tolist()