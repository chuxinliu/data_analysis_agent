import pandas as pd

def load_crash_data():
    """
    Load and preprocess crash data from CSV file
    Returns preprocessed DataFrame with selected columns and injury indicator
    """
    df = pd.read_csv("crashdata.csv")
    
    # Select relevant columns
    df = df[['CRASH DATE', 'LATITUDE', 'LONGITUDE', 'NUMBER OF PERSONS INJURED']]
    
    # Create binary injury indicator
    df['INJURED'] = (df['NUMBER OF PERSONS INJURED'] > 0)
    
    return df

if __name__ == "__main__":
    # Test data loading
    df = load_crash_data()
    print("Sample of crash data:")
    print(df.head()) 