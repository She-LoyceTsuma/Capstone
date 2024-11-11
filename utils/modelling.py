"""Contains utility functions for the modelling process"""
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np


def get_preprocessor(df, target_col=None):
    """Function to retrun the preprocessor
    Parameters:
        df(pd.DataFrame): the data
        target_name(str): The target column name
    returns:
        Preprocessor object
    """
    #Select categorical columns for one-hot encoding 
    # and numeric columns for scaling
    numeric_features = df.select_dtypes(exclude='object').columns.tolist()
    categorical_features = df.select_dtypes(include='object').columns.tolist()
    
    # apply lowercase to categorical features
    df[categorical_features] = df[categorical_features].apply(lambda x: x.str.lower())

    # Remove target feature from categorical list
    if target_col:
        categorical_features.remove(target_col)
    # Preprocessing the features
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat_encoder', OneHotEncoder(drop='first', sparse_output=False,
                                          handle_unknown='ignore'),
             categorical_features
             ),
            ('scaler', StandardScaler(), numeric_features)
        ]
        
    )
    return preprocessor


# function to split date to year month and day
def split_date_col(df, date_cols):
    """Splits the dates of the specified columns 
    and adds them as new features also deletes original date column
    
    Parameters:
        df(Pd.DataFrame): the dataframe containing the features
        date_cols([str]): list of the date columns
    Returns:
        Pd.Dataframe: edited df with new features
    """
    
    # iterating through the cols
    for col in date_cols:
        # convert to datetime
        df[col] = df[col].apply(pd.to_datetime)
        # split the date
        df[f'{col}_year'] = df[col].dt.year
        # make month and day as cosine and sine to show the cyclic nature
        df[f'{col}_cosine_month'] = df[col].dt.month.apply(
            lambda x: np.cos(2 * np.pi * x / 12)
        )
        df[f'{col}_sine_month'] = df[col].dt.month.apply(
            lambda x: np.sin(2 * np.pi * x / 12)
        )
        df[f'{col}_cosine_day'] = df[col].dt.day.apply(
            lambda x: np.cos(2 * np.pi * x / 12)
        )
        df[f'{col}_sine_day'] = df[col].dt.day.apply(
            lambda x: np.sin(2 * np.pi * x / 12)
        )
        
        
        # drop original_date
        df.drop(col, axis=1, inplace=True)
        
    return df


def prepare_model_data(data_dict):
    """Preprocessing the data recieved by the api

    Args:
        data_dict (dict): the data from the claim to predict
    """
    data_dict['auto_make_model'] = f"{data_dict['auto_make']}_{data_dict['auto_model']}"
    del data_dict['auto_make']
    del data_dict['auto_model']
    
    data_dict['incident_hour_of_the_day'] = data_dict['incident_hour_of_day']
    del data_dict['incident_hour_of_day']
    
    data_dict['capital-gains'] = data_dict['capital_gain']
    del data_dict['capital_gain']
    
    data_dict['capital-loss'] = data_dict['capital_loss']
    del data_dict['capital_loss']
    
    data_dict = {k: [v] for k, v in data_dict.items()}
    
    df = pd.DataFrame(data_dict)
    
    # convert inident hour of the day to ensure the cyclic nature is captured
    df['incident_sine_hour'] = df['incident_hour_of_the_day'].map(
    lambda x: np.sin(2 * np.pi * x / 24)
    )

    df['incident_cosine_hour'] = df['incident_hour_of_the_day'].map(
        lambda x: np.cos(2 * np.pi * x / 24)
    )
    
    # dropping the incident_hour _of_day dolumn
    df.drop('incident_hour_of_the_day', axis=1, inplace=True)
    
    date_columns = ['policy_bind_date', 'incident_date']
    
    # split date to introduce the cyclic nature for days and months
    df = split_date_col(df, date_columns)
    
    # drop total amount to avoid collinearity
    df.drop('total_claim_amount', axis=1, inplace=True)
    
    # drop the columns not needed
    df.drop('incident_location' ,axis=1,inplace=True)
    
    return df
    