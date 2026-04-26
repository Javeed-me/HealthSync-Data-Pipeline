"""
Visualization functions for healthcare data dashboard.
Creates matplotlib charts for patient vitals and alerts.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def plot_heart_rate_per_patient(df: pd.DataFrame) -> plt.Figure:
    """Create a bar chart showing average heart rate per patient."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sort by patient_id for better visualization
    df_sorted = df.sort_values('patient_id')
    
    # Create bar chart
    bars = ax.bar(
        df_sorted['patient_id'].astype(str), 
        df_sorted['avg_heart_rate'],
        color='#4CAF50',
        edgecolor='#2E7D32',
        alpha=0.8
    )
    
    # Highlight abnormal patients (abnormal_count > 0)
    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        if row['abnormal_count'] > 0:
            bars[i].set_color('#F44336')
            bars[i].set_edgecolor('#B71C1C')
    
    ax.set_xlabel('Patient ID', fontsize=12)
    ax.set_ylabel('Average Heart Rate (bpm)', fontsize=12)
    ax.set_title('Average Heart Rate per Patient', fontsize=14, fontweight='bold')
    ax.axhline(y=80, color='orange', linestyle='--', alpha=0.7, label='Normal Upper Bound (80 bpm)')
    ax.axhline(y=60, color='blue', linestyle='--', alpha=0.7, label='Normal Lower Bound (60 bpm)')
    ax.legend(loc='upper right')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_temperature_trends(df: pd.DataFrame) -> plt.Figure:
    """Create a line chart showing temperature trends over patients (simulated time)."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sort by patient_id to simulate time progression
    df_sorted = df.sort_values('patient_id')
    
    # Create line chart
    ax.plot(
        df_sorted['patient_id'].astype(str), 
        df_sorted['avg_temperature'],
        marker='o',
        linewidth=2,
        markersize=8,
        color='#2196F3',
        markerfacecolor='white',
        markeredgecolor='#2196F3',
        markeredgewidth=2
    )
    
    # Highlight abnormal temperatures
    for i, (idx, row) in enumerate(df_sorted.iterrows()):
        if row['avg_temperature'] > 38 or row['avg_temperature'] < 36:
            ax.scatter([str(row['patient_id'])], [row['avg_temperature']], 
                      color='#F44336', s=150, zorder=5, marker='X')
    
    ax.set_xlabel('Patient ID (Time Sequence)', fontsize=12)
    ax.set_ylabel('Average Temperature (°C)', fontsize=12)
    ax.set_title('Temperature Trends Over Time', fontsize=14, fontweight='bold')
    ax.axhline(y=38, color='red', linestyle='--', alpha=0.7, label='Fever Threshold (38°C)')
    ax.axhline(y=36, color='blue', linestyle='--', alpha=0.7, label='Hypothermia Threshold (36°C)')
    ax.legend(loc='upper right')
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_abnormal_distribution(df: pd.DataFrame) -> plt.Figure:
    """Create a pie chart showing distribution of abnormal vs normal patients."""
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Calculate counts
    abnormal_count = (df['abnormal_count'] > 0).sum()
    normal_count = len(df) - abnormal_count
    
    # Create pie chart
    sizes = [normal_count, abnormal_count]
    labels = ['Normal', 'Abnormal']
    colors = ['#4CAF50', '#F44336']
    explode = (0, 0.1)  # Explode the abnormal slice
    
    wedges, texts, autotexts = ax.pie(
        sizes, 
        explode=explode,
        labels=labels, 
        colors=colors,
        autopct='%1.1f%%',
        startangle=90,
        shadow=True,
        textprops={'fontsize': 12}
    )
    
    # Style the percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(14)
    
    ax.set_title('Distribution of Normal vs Abnormal Patients', fontsize=14, fontweight='bold')
    
    # Add legend
    ax.legend(
        [f'Normal: {normal_count} patients', f'Abnormal: {abnormal_count} patients'],
        loc='lower right',
        fontsize=10
    )
    
    plt.tight_layout()
    return fig


def plot_blood_pressure(df: pd.DataFrame) -> plt.Figure:
    """Create a grouped bar chart for blood pressure (systolic and diastolic)."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Sort by patient_id
    df_sorted = df.sort_values('patient_id')
    
    x = range(len(df_sorted))
    width = 0.35
    
    # Create grouped bars
    bars1 = ax.bar(
        [i - width/2 for i in x], 
        df_sorted['avg_bp_systolic'],
        width, 
        label='Systolic',
        color='#FF5722',
        alpha=0.8
    )
    bars2 = ax.bar(
        [i + width/2 for i in x], 
        df_sorted['avg_bp_diastolic'],
        width, 
        label='Diastolic',
        color='#9C27B0',
        alpha=0.8
    )
    
    ax.set_xlabel('Patient ID', fontsize=12)
    ax.set_ylabel('Blood Pressure (mmHg)', fontsize=12)
    ax.set_title('Blood Pressure: Systolic vs Diastolic', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(df_sorted['patient_id'].astype(str))
    ax.legend()
    ax.axhline(y=120, color='red', linestyle='--', alpha=0.5, label='Normal Systolic (120)')
    ax.axhline(y=80, color='blue', linestyle='--', alpha=0.5, label='Normal Diastolic (80)')
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_vitals_summary(df: pd.DataFrame) -> plt.Figure:
    """Create a summary dashboard with multiple metrics."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # 1. Heart Rate Distribution
    ax1 = axes[0, 0]
    ax1.hist(df['avg_heart_rate'], bins=10, color='#4CAF50', edgecolor='#2E7D32', alpha=0.8)
    ax1.axvline(df['avg_heart_rate'].mean(), color='red', linestyle='--', label=f'Mean: {df["avg_heart_rate"].mean():.1f}')
    ax1.set_xlabel('Heart Rate (bpm)')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Heart Rate Distribution')
    ax1.legend()
    
    # 2. Temperature Distribution
    ax2 = axes[0, 1]
    ax2.hist(df['avg_temperature'], bins=10, color='#2196F3', edgecolor='#1565C0', alpha=0.8)
    ax2.axvline(df['avg_temperature'].mean(), color='red', linestyle='--', label=f'Mean: {df["avg_temperature"].mean():.1f}°C')
    ax2.set_xlabel('Temperature (°C)')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Temperature Distribution')
    ax2.legend()
    
    # 3. Abnormal Count by Patient
    ax3 = axes[1, 0]
    df_sorted = df.sort_values('abnormal_count', ascending=False).head(10)
    colors = ['#F44336' if x > 0 else '#4CAF50' for x in df_sorted['abnormal_count']]
    ax3.barh(df_sorted['patient_id'].astype(str), df_sorted['abnormal_count'], color=colors)
    ax3.set_xlabel('Abnormal Count')
    ax3.set_ylabel('Patient ID')
    ax3.set_title('Top Patients by Abnormal Count')
    
    # 4. Vitals Correlation
    ax4 = axes[1, 1]
    # Create a simple correlation visualization
    vitals = df[['avg_heart_rate', 'avg_temperature', 'avg_bp_systolic', 'avg_bp_diastolic']].dropna()
    if len(vitals) > 0:
        corr = vitals.corr()
        im = ax4.imshow(corr, cmap='RdYlGn', aspect='auto', vmin=-1, vmax=1)
        ax4.set_xticks(range(len(corr.columns)))
        ax4.set_yticks(range(len(corr.columns)))
        ax4.set_xticklabels(['HR', 'Temp', 'Sys', 'Dia'], fontsize=10)
        ax4.set_yticklabels(['HR', 'Temp', 'Sys', 'Dia'], fontsize=10)
        ax4.set_title('Vitals Correlation Matrix')
        
        # Add correlation values
        for i in range(len(corr)):
            for j in range(len(corr)):
                ax4.text(j, i, f'{corr.iloc[i, j]:.2f}', ha='center', va='center', fontsize=9)
        
        plt.colorbar(im, ax=ax4)
    
    plt.suptitle('Healthcare Vitals Summary Dashboard', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig
