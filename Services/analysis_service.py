"""
AnalysisService - Performs interactive analysis on planets dataset using Plotly.
This service handles data processing, statistical calculations, and chart generation.
"""
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os
from Services.data_service import DataService

class AnalysisService:
    def __init__(self, data_service: DataService):
        """
        Initializes the service with a data source.
        Ensures the plots directory exists for potential static exports.
        """
        self.data_service = data_service
        self.plots_dir = "static/plots"
        os.makedirs(self.plots_dir, exist_ok=True)

    def run_question(self, question_id: int) -> dict:
        """
        Main entry point for executing analysis based on the user's selection.
        Routes the request to the appropriate private method.
        """
        if question_id == 1:
            return self.question_1_discoveries_per_year()
        elif question_id == 2:
            return self.question_2_counts_by_method()
        elif question_id == 3:
            return self.question_3_orbital_period()
        elif question_id == 4:
            return self.question_4_mass_distribution()
        elif question_id == 5:
            return self.question_5_method_vs_mass()
        else:
            return {
                'title': 'Error',
                'result': 'Invalid question ID',
                'graph_html': None
            }

    def _generate_table_html(self, df):
        """
        Helper method to convert a Pandas DataFrame into a Bootstrap-styled HTML table.
        """
        return df.to_html(index=False, classes='table table-hover', border=0, justify='center')

    def _fig_to_html(self, fig):
        """
        Customizes Plotly figure appearance for a dark theme and converts it to an HTML div.
        Includes interactive tools in the modebar for user exploration.
        """
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0.2)', 
            font_color="white",
            title_font_size=20,
            margin=dict(l=20, r=20, t=60, b=20),
            modebar_add=["v1hovermode", "drawline", "drawcircle", "drawrect"]
        )
        # Styling axes for clear visibility against the background
        fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color="white")
        fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.1)', color="white")
    
        return pio.to_html(fig, full_html=False, include_plotlyjs='cdn', config={'displayModeBar': True})

    def _handle_empty_data(self, title):
        """
        Returns a graceful response if the dataset is empty after filtering or cleaning.
        Prevents the application from crashing when trying to visualize empty data.
        """
        return {
            'title': title,
            'result': '<p class="text-warning text-center">No matching data found for this specific analysis.</p>',
            'graph_html': '<div class="alert alert-info">Insufficient data to generate a visualization.</div>',
            'is_plotly': True
        }

    def question_1_discoveries_per_year(self) -> dict:
        """Analyzes which years had the most planet discoveries."""
        df = self.data_service.get_df()
        data = df['year'].dropna()

        if data.empty:
            return self._handle_empty_data('Discoveries Per Year')

        discoveries = data.value_counts().sort_index()
        top_years = discoveries.nlargest(10).sort_index()

        fig = px.line(
            x=top_years.index, y=top_years.values,
            labels={'x': 'Year', 'y': 'Discoveries'},
            title='Planets Discoveries Over Top 10 Years',
            markers=True, template="plotly_dark"
        )
        
        result_df = pd.DataFrame({'Year': top_years.index, 'Discoveries': top_years.values})
        return {
            'title': 'Discoveries Per Year (Top 10)',
            'result': self._generate_table_html(result_df),
            'graph_html': self._fig_to_html(fig),
            'is_plotly': True
        }

    def question_2_counts_by_method(self) -> dict:
        """Compares the frequency of different detection methods used."""
        df = self.data_service.get_df()
        data = df['method'].dropna()

        if data.empty:
            return self._handle_empty_data('Detection Methods')

        method_counts = data.value_counts().head(10)

        fig = px.bar(
            x=method_counts.index, y=method_counts.values,
            labels={'x': 'Detection Method', 'y': 'Number of Planets'},
            title='Top 10 Detection Methods',
            color=method_counts.values, template="plotly_dark"
        )

        result_df = pd.DataFrame({'Method': method_counts.index, 'Count': method_counts.values})
        return {
            'title': 'Planet Counts by Detection Method',
            'result': self._generate_table_html(result_df),
            'graph_html': self._fig_to_html(fig),
            'is_plotly': True
        }

    def question_3_orbital_period(self) -> dict:
        """
        Visualizes the distribution of orbital periods.
        Filters outliers to ensure the graph is clear and readable.
        """
        df = self.data_service.get_df()
        
        # 1. Focus on planets with an orbital period between 0 and 500 days
        # This covers most planets and avoids the 'empty graph' or 'squashed' look.
        orbital_filtered = df[(df['orbital_period'] > 0) & (df['orbital_period'] <= 500)]['orbital_period'].dropna()

        if orbital_filtered.empty:
            return self._handle_empty_data('Orbital Period Distribution')

        # 2. Generate a clean Histogram
        fig = px.histogram(
            orbital_filtered, 
            x=orbital_filtered,
            nbins=50, 
            title='Orbital Period Distribution (Up to 500 Days)',
            labels={'x': 'Orbital Period (Days)', 'count': 'Number of Planets'}, 
            template="plotly_dark",
            color_discrete_sequence=['#ff7f50'], # Coral color
            opacity=0.85
        )

        # 3. Clean up the layout
        fig.update_layout(
            bargap=0.1,
            xaxis_title="Orbital Period (Days)",
            yaxis_title="Planet Count",
            showlegend=False
        )

        # 4. Statistical summary for the result section
        result = f"""
        <div class='data-summary text-center text-dark'>
            <p><strong>Planets in View:</strong> {len(orbital_filtered)} (Periods ≤ 500 days)</p>
            <p><strong>Average Period:</strong> {orbital_filtered.mean():.2f} days</p>
            <small class="text-muted">* Long-period outliers were hidden to improve clarity.</small>
        </div>
        """
        return {
            'title': 'Orbital Period Distribution',
            'result': result,
            'graph_html': self._fig_to_html(fig),
            'is_plotly': True
        }

    def question_4_mass_distribution(self) -> dict:
        """
        Visualizes the distribution of planet masses.
        Filters extreme outliers to reveal the detailed distribution of smaller planets.
        """
        df = self.data_service.get_df()
        
        # 1. Filter for planets with mass between 0 and 2 Jupiter Masses (MJ)
        # This removes the massive outliers that squash the graph.
        mass_filtered = df[(df['mass'] > 0) & (df['mass'] <= 2)]['mass'].dropna()

        if mass_filtered.empty:
            return self._handle_empty_data('Mass Distribution')

        # 2. Create a detailed Histogram
        fig = px.histogram(
            mass_filtered, 
            x=mass_filtered,
            nbins=60, # Increased bins for better resolution
            title='Detailed Mass Distribution (Up to 2 MJ)',
            labels={'x': 'Mass (Jupiter Masses - MJ)', 'count': 'Number of Planets'}, 
            template="plotly_dark",
            color_discrete_sequence=['#90ee90'], # Light green
            opacity=0.85
        )

        # 3. Enhance layout for readability
        fig.update_layout(
            bargap=0.1,
            xaxis_title="Jupiter Masses (MJ)",
            yaxis_title="Planet Count",
            showlegend=False
        )

        # 4. Results summary for the UI
        result = f"""
        <div class='data-summary text-center text-dark'>
            <p><strong>Planets Analyzed:</strong> {len(mass_filtered)} (Mass ≤ 2 MJ)</p>
            <p><strong>Median Mass:</strong> {mass_filtered.median():.3f} MJ</p>
            <small class="text-muted">* Excluded heavy gas giants (>2 MJ) to focus on smaller planet distribution.</small>
        </div>
        """
        return {
            'title': 'Planet Mass Distribution',
            'result': result,
            'graph_html': self._fig_to_html(fig),
            'is_plotly': True
        }

    def question_5_method_vs_mass(self) -> dict:
        """
        Correlates detection methods with the average mass of the planets found.
        Includes dynamic feedback on available data points.
        """
        df = self.data_service.get_df()
        
        # 1. Clean data: Drop rows where mass or method is missing
        # This is the reason why some methods might disappear from the top 10 list
        df_clean = df.dropna(subset=['mass', 'method'])

        if df_clean.empty:
            return self._handle_empty_data('Average Mass by Method')

        # 2. Grouping and calculating average mass
        top_methods = df_clean['method'].value_counts().head(10).index
        df_top = df_clean[df_clean['method'].isin(top_methods)]
        avg_mass = df_top.groupby('method')['mass'].mean().sort_values(ascending=False)

        # 3. Generating the Plotly visualization
        fig = px.bar(
            x=avg_mass.index, y=avg_mass.values,
            labels={'x': 'Detection Method', 'y': 'Avg Mass (MJ)'},
            title='Average Planet Mass by Detection Method',
            color=avg_mass.values, 
            template="plotly_dark",
            color_continuous_scale='Viridis'
        )

        # 4. Preparing the result table and summary text
        result_df = pd.DataFrame({
            'Method': avg_mass.index, 
            'Avg Mass (MJ)': avg_mass.values.round(2)
        })

        # FIX: Wrapped in 'data-summary' and added dynamic explanation for the data count
        result_html = f"""
        <div class='data-summary text-center text-dark'>
            <p><strong>Note:</strong> Out of all methods, only <strong>{len(avg_mass)}</strong> had valid mass records for this analysis.</p>
            {self._generate_table_html(result_df)}
        </div>
        """

        return {
            'title': 'Average Mass by Method (Top 10)',
            'result': result_html,
            'graph_html': self._fig_to_html(fig),
            'is_plotly': True
        }