"""Contains utility functions for the modelling process"""
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
def get_preprocessor(df, target_col):
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

    # Remove target feature from categorica list
    if target_col not in categorical_features:
        print('Target column not found')
        return
    categorical_features.remove(target_col)
    # Preprocessing the features
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat_encoder', OneHotEncoder(drop='first', sparse_output=False),
             categorical_features
             ),
            ('scaler', StandardScaler(), numeric_features)
        ]
    )
    return preprocessor