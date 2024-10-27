"""This module contains utility functions for the analysis stage"""
#Importing Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


# Function for univariate analysis
# Define a function to implement univariate analysis
def univariate_analysis(df, cols=None, output_dir=None):
    """
    Performs comprehensive univariate analysis on numerical features.

    Parameters:
    - df: pandas DataFrame containing the data.
    - cols: list of columns to analyze. If None, all numerical columns are analyzed.
    - output_dir: directory to save plots. If None, plots are displayed but not saved.

    Returns:
    - analysis_results: A dictionary containing analysis results for each column.
    """
    if cols is None:
        cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    analysis_results = {}
    
    for col in cols:
        print(f"\nAnalyzing '{col}':")
        data = df[col].dropna()
        results = {}
        
        # Descriptive Statistics
        results['count'] = data.count()
        results['mean'] = data.mean()
        results['median'] = data.median()
        results['mode'] = data.mode().tolist()
        results['std_dev'] = data.std()
        results['variance'] = data.var()
        results['min'] = data.min()
        results['max'] = data.max()
        results['range'] = data.max() - data.min()
        results['skewness'] = data.skew()
        results['kurtosis'] = data.kurtosis()
        results['quantiles'] = data.quantile([0.25, 0.5, 0.75]).to_dict()
        
        # Distribution
        # Outlier Detection using IQR
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = data[(data < lower_bound) | (data > upper_bound)]
        results['num_outliers'] = len(outliers)
        results['outlier_values'] = outliers.tolist()
        
        # Normality Test
        # If p > 0.05, data is considered normally distributed
        if len(data) >= 3 and len(data) <= 5000:
            stat, p_value = stats.shapiro(data)
            results['normality_test'] = 'Shapiro-Wilk'
        else:
            stat, p_value = stats.normaltest(data)
            results['normality_test'] = 'D\'Agostino and Pearson'
        results['normality_pvalue'] = p_value
        results['is_normal_distribution'] = p_value > 0.05  
        
        # Visualization
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # Histogram and KDE
        sns.histplot(data, kde=True, ax=axes[0, 0], color='skyblue')
        axes[0, 0].set_title(f'Histogram of {col}')
        
        # Boxplot
        sns.boxplot(x=data, ax=axes[0, 1], color='lightgreen')
        axes[0, 1].set_title(f'Boxplot of {col}')
        
        # QQ Plot
        stats.probplot(data, dist="norm", plot=axes[1, 0])
        axes[1, 0].set_title(f'QQ Plot of {col}')
        
        # Violin Plot
        sns.violinplot(x=data, ax=axes[1, 1], color='lightcoral')
        axes[1, 1].set_title(f'Violin Plot of {col}')
        
        plt.tight_layout()
        
        if output_dir:
            plt.savefig(f'{output_dir}/{col}_analysis.png')
            plt.close()
        else:
            plt.show()
        
        # Store the results
        analysis_results[col] = results
        
        # Print the summary
        summary_df = pd.DataFrame.from_dict(results, orient='index', columns=['Value'])
        
        
    return print(summary_df)
