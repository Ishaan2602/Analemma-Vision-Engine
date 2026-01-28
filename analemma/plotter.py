"""
Layer 3: The Visualizer (AnalemmaPlotter)

Create various visualizations of the analemma including:
- 2D Sky Charts (Altitude vs Azimuth)
- Figure-8 plots (EoT vs Declination)
- Time-series plots
- Interactive plots with Plotly
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Optional plotly for interactive plots
try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


class AnalemmaPlotter:
    """
    Visualize analemma data in various formats.
    
    Supports both static (matplotlib) and interactive (plotly) visualizations.
    
    Parameters
    ----------
    style : str, optional
        Matplotlib style to use (default: 'seaborn-v0_8-darkgrid')
    figure_size : tuple, optional
        Default figure size (width, height) in inches
    """
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid', 
                 figure_size: Tuple[int, int] = (10, 8)):
        """Initialize the plotter with style preferences."""
        self.style = style
        self.figure_size = figure_size
        
        # Try to set style, fall back to default if not available
        try:
            plt.style.use(style)
        except:
            try:
                plt.style.use('seaborn-darkgrid')
            except:
                pass  # Use default matplotlib style
    
    def plot_analemma(self, sky_data: List[Dict], 
                     title: str = "Analemma - Sun's Path Over One Year",
                     show_dates: bool = True,
                     date_interval: int = 30,
                     save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot the analemma as seen in the sky (Altitude vs Azimuth).
        
        Parameters
        ----------
        sky_data : list
            List of dictionaries from SkyMapper.map_to_horizon()
        title : str
            Plot title
        show_dates : bool
            Whether to annotate specific dates
        date_interval : int
            Days between date annotations
        save_path : str, optional
            If provided, save figure to this path
        
        Returns
        -------
        matplotlib.figure.Figure
            The created figure
        """
        # Extract data
        altitudes = [d['altitude'] for d in sky_data]
        azimuths = [d['azimuth'] for d in sky_data]
        dates = [d['date'] for d in sky_data]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Plot the analemma curve
        scatter = ax.scatter(azimuths, altitudes, 
                           c=range(len(sky_data)), 
                           cmap='twilight',
                           s=50, alpha=0.7, 
                           edgecolors='black', linewidth=0.5)
        
        # Add colorbar for day of year
        cbar = plt.colorbar(scatter, ax=ax, label='Day of Year')
        
        # Annotate specific dates
        if show_dates:
            for i, (az, alt, date) in enumerate(zip(azimuths, altitudes, dates)):
                if i % date_interval == 0:
                    ax.annotate(date.strftime('%b %d'),
                              (az, alt),
                              xytext=(5, 5), textcoords='offset points',
                              fontsize=8, alpha=0.7)
        
        # Formatting
        ax.set_xlabel('Azimuth (degrees)', fontsize=12)
        ax.set_ylabel('Altitude (degrees)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add compass directions
        ax.axvline(0, color='gray', linestyle='--', alpha=0.3, linewidth=1)
        ax.axvline(90, color='gray', linestyle='--', alpha=0.3, linewidth=1)
        ax.axvline(180, color='gray', linestyle='--', alpha=0.3, linewidth=1)
        ax.axvline(270, color='gray', linestyle='--', alpha=0.3, linewidth=1)
        
        ax.text(0, ax.get_ylim()[1], 'N', ha='center', va='bottom', fontsize=10)
        ax.text(90, ax.get_ylim()[1], 'E', ha='center', va='bottom', fontsize=10)
        ax.text(180, ax.get_ylim()[1], 'S', ha='center', va='bottom', fontsize=10)
        ax.text(270, ax.get_ylim()[1], 'W', ha='center', va='bottom', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_figure8(self, calc_data: List[Dict],
                    title: str = "Analemma Figure-8 (EoT vs Declination)",
                    save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot the classic figure-8 analemma (EoT vs Declination).
        
        This shows the pure astronomical components without observer location.
        
        Parameters
        ----------
        calc_data : list
            List of dictionaries from AnalemmaCalculator.calculate_year()
        title : str
            Plot title
        save_path : str, optional
            If provided, save figure to this path
        
        Returns
        -------
        matplotlib.figure.Figure
            The created figure
        """
        # Extract data
        eot = [d['eot'] for d in calc_data]
        declination = [d['declination'] for d in calc_data]
        
        # Create figure
        fig, ax = plt.subplots(figsize=self.figure_size)
        
        # Plot the figure-8
        scatter = ax.scatter(eot, declination,
                           c=range(len(calc_data)),
                           cmap='twilight',
                           s=50, alpha=0.7,
                           edgecolors='black', linewidth=0.5)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax, label='Day of Year')
        
        # Add reference lines
        ax.axhline(0, color='gray', linestyle='--', alpha=0.3, linewidth=1)
        ax.axvline(0, color='gray', linestyle='--', alpha=0.3, linewidth=1)
        
        # Formatting
        ax.set_xlabel('Equation of Time (minutes)', fontsize=12)
        ax.set_ylabel('Solar Declination (degrees)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # Add annotations for seasons
        ax.text(ax.get_xlim()[1], 23.45, 'Summer Solstice', 
               ha='right', va='bottom', fontsize=9, alpha=0.7)
        ax.text(ax.get_xlim()[1], -23.45, 'Winter Solstice',
               ha='right', va='top', fontsize=9, alpha=0.7)
        ax.text(ax.get_xlim()[1], 0, 'Equinoxes',
               ha='right', va='center', fontsize=9, alpha=0.7)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_time_series(self, calc_data: List[Dict],
                        save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot declination and EoT as time series over the year.
        
        Parameters
        ----------
        calc_data : list
            List of dictionaries from AnalemmaCalculator.calculate_year()
        save_path : str, optional
            If provided, save figure to this path
        
        Returns
        -------
        matplotlib.figure.Figure
            The created figure
        """
        # Extract data
        days = [d['day_of_year'] for d in calc_data]
        eot = [d['eot'] for d in calc_data]
        declination = [d['declination'] for d in calc_data]
        
        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        
        # Plot declination
        ax1.plot(days, declination, 'b-', linewidth=2, label='Solar Declination')
        ax1.axhline(0, color='gray', linestyle='--', alpha=0.3)
        ax1.axhline(23.45, color='red', linestyle=':', alpha=0.3, label='Obliquity')
        ax1.axhline(-23.45, color='red', linestyle=':', alpha=0.3)
        ax1.set_ylabel('Declination (degrees)', fontsize=12)
        ax1.set_title('Solar Declination Over One Year', fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # Plot equation of time
        ax2.plot(days, eot, 'r-', linewidth=2, label='Equation of Time')
        ax2.axhline(0, color='gray', linestyle='--', alpha=0.3)
        ax2.set_xlabel('Day of Year', fontsize=12)
        ax2.set_ylabel('EoT (minutes)', fontsize=12)
        ax2.set_title('Equation of Time Over One Year', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # Add month labels
        month_days = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for ax in [ax1, ax2]:
            ax.set_xticks(month_days)
            ax.set_xticklabels(month_names)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_sky_dome(self, sky_data: List[Dict],
                     title: str = "Analemma on Sky Dome",
                     save_path: Optional[str] = None) -> plt.Figure:
        """
        Plot analemma on a polar sky dome projection.
        
        Parameters
        ----------
        sky_data : list
            List of dictionaries from SkyMapper.map_to_horizon()
        title : str
            Plot title
        save_path : str, optional
            If provided, save figure to this path
        
        Returns
        -------
        matplotlib.figure.Figure
            The created figure
        """
        # Extract data
        altitudes = np.array([d['altitude'] for d in sky_data])
        azimuths = np.array([d['azimuth'] for d in sky_data])
        
        # Convert to polar coordinates (altitude becomes radius from edge)
        # Altitude 0° = edge (r=90), Altitude 90° = center (r=0)
        r = 90 - altitudes
        theta = np.radians(azimuths)
        
        # Create polar plot
        fig, ax = plt.subplots(figsize=self.figure_size, 
                              subplot_kw=dict(projection='polar'))
        
        # Plot analemma
        scatter = ax.scatter(theta, r,
                           c=range(len(sky_data)),
                           cmap='twilight',
                           s=50, alpha=0.7,
                           edgecolors='black', linewidth=0.5)
        
        # Formatting
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)  # Clockwise
        ax.set_ylim(0, 90)
        ax.set_yticks([0, 30, 60, 90])
        ax.set_yticklabels(['90°', '60°', '30°', '0°'])
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax, pad=0.1, label='Day of Year')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    def plot_interactive(self, sky_data: List[Dict],
                        title: str = "Interactive Analemma") -> go.Figure:
        """
        Create an interactive plotly visualization.
        
        Parameters
        ----------
        sky_data : list
            List of dictionaries from SkyMapper.map_to_horizon()
        title : str
            Plot title
        
        Returns
        -------
        plotly.graph_objects.Figure
            Interactive plotly figure
        """
        if not PLOTLY_AVAILABLE:
            raise RuntimeError("Interactive plots require plotly. "
                             "Install with: pip install plotly")
        
        # Extract data
        altitudes = [d['altitude'] for d in sky_data]
        azimuths = [d['azimuth'] for d in sky_data]
        dates = [d['date'].strftime('%Y-%m-%d') for d in sky_data]
        days = [d['day_of_year'] for d in sky_data]
        
        # Create interactive scatter plot
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=azimuths,
            y=altitudes,
            mode='markers',
            marker=dict(
                size=8,
                color=days,
                colorscale='Twilight',
                showscale=True,
                colorbar=dict(title="Day of Year"),
                line=dict(width=1, color='black')
            ),
            text=dates,
            hovertemplate='<b>%{text}</b><br>' +
                         'Azimuth: %{x:.1f}°<br>' +
                         'Altitude: %{y:.1f}°<br>' +
                         '<extra></extra>'
        ))
        
        # Update layout
        fig.update_layout(
            title=title,
            xaxis_title="Azimuth (degrees)",
            yaxis_title="Altitude (degrees)",
            hovermode='closest',
            width=1000,
            height=700,
            template='plotly_white'
        )
        
        # Add compass direction annotations
        for angle, direction in [(0, 'N'), (90, 'E'), (180, 'S'), (270, 'W')]:
            fig.add_vline(x=angle, line_dash="dash", line_color="gray", 
                         opacity=0.3, annotation_text=direction)
        
        return fig
    
    def plot_comparison(self, approx_data: List[Dict], 
                       precise_data: List[Dict],
                       save_path: Optional[str] = None) -> plt.Figure:
        """
        Compare approximate and high-precision calculations.
        
        Parameters
        ----------
        approx_data : list
            Data from approximate mode
        precise_data : list
            Data from high-precision mode
        save_path : str, optional
            If provided, save figure to this path
        
        Returns
        -------
        matplotlib.figure.Figure
            The created figure
        """
        # Extract data
        days = [d['day_of_year'] for d in approx_data]
        
        approx_dec = [d['declination'] for d in approx_data]
        precise_dec = [d['declination'] for d in precise_data]
        dec_diff = [abs(a - p) for a, p in zip(approx_dec, precise_dec)]
        
        approx_eot = [d['eot'] for d in approx_data]
        precise_eot = [d['eot'] for d in precise_data]
        eot_diff = [abs(a - p) for a, p in zip(approx_eot, precise_eot)]
        
        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # Declination comparison
        axes[0, 0].plot(days, approx_dec, 'b-', label='Approximate', alpha=0.7)
        axes[0, 0].plot(days, precise_dec, 'r--', label='High-Precision', alpha=0.7)
        axes[0, 0].set_ylabel('Declination (°)')
        axes[0, 0].set_title('Solar Declination Comparison')
        axes[0, 0].legend()
        axes[0, 0].grid(True, alpha=0.3)
        
        # Declination difference
        axes[0, 1].plot(days, dec_diff, 'g-', linewidth=2)
        axes[0, 1].set_ylabel('Absolute Difference (°)')
        axes[0, 1].set_title('Declination Difference')
        axes[0, 1].grid(True, alpha=0.3)
        
        # EoT comparison
        axes[1, 0].plot(days, approx_eot, 'b-', label='Approximate', alpha=0.7)
        axes[1, 0].plot(days, precise_eot, 'r--', label='High-Precision', alpha=0.7)
        axes[1, 0].set_xlabel('Day of Year')
        axes[1, 0].set_ylabel('EoT (minutes)')
        axes[1, 0].set_title('Equation of Time Comparison')
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3)
        
        # EoT difference
        axes[1, 1].plot(days, eot_diff, 'g-', linewidth=2)
        axes[1, 1].set_xlabel('Day of Year')
        axes[1, 1].set_ylabel('Absolute Difference (minutes)')
        axes[1, 1].set_title('EoT Difference')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.suptitle('Approximate vs High-Precision Mode Comparison',
                    fontsize=14, fontweight='bold')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        return fig
    
    @staticmethod
    def show():
        """Display all open matplotlib figures."""
        plt.show()
    
    @staticmethod
    def close_all():
        """Close all matplotlib figures."""
        plt.close('all')
