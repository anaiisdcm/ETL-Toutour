import numpy as np
import numpy.random as rd
import pandas as pd


"""
This file contains function to add noise to pandas dataframe.
"""

# load pandas dataframe from generated csv
# file_in = "./data_out/dogs_dataset.csv"
file_in = "./data_in/demo.csv" # file for testing
file_out = "./data_noisy/WTF.csv"

df_in = pd.read_csv(file_in)



"""
Function to nullify several rows. Rows are randomly chosen. Editing is in place.
All values of the chosen rows will be None or NaN.
Args :
    df : pandas dataframe whose rows will be nullified
    n_rows : the number of row to nullify
Returns :
    df with n_rows randomly chosen null rows
"""
def NullRowMaker(df, n_rows):
    r, c = df.shape
    if n_rows >= r//2 :
        print(f"Asking to nullify {n_rows} rows in dataframe that contains only {r}. Not doing it")
        n_rows = r//2
    
    # choose rows randomly
    r_to_null = rd.choice(r, n_rows)
    df.loc[r_to_null] = None
    return df

"""
Function to replace randomly chosen values by None or NaN. Editing is in place.
Ags :
    df : pandas dataframe to replace values by None
    n_nulls : total number of values to replace by None or Nan
"""
def RandomNullMaker(df, n_nulls):
    r, c = df.shape
    if n_nulls >= r*c/5 :
        print(f"Asking to nullify {n_nulls} elements in dataframe ({r}x{c}) that contains only {r*c}. Not doing it")
        n_nulls = r*c//5
    
    # choose rows and columns randomly
    r_to_null = rd.randint(0, r-1, n_nulls)
    c_to_null = rd.randint(0, c-1, n_nulls)        
    # nullify
    for i in range(n_nulls):
        df.loc[ r_to_null[i] , df.columns.values[c_to_null[i]] ] = None
    return df
    
"""
Function to insert fake values into a selection of columns. 
Automatically handle columns type (numeric or not). Editing is in place.
Replacement values are computed to be at least 4 std deviation from mean. Can be negative.
Args :
    df : dataframe to edit
    columns : selection of columns in which to tweak values in
    n_faked_c : nummber of values to tweak in each column
"""
def ExageratedValues(df, columns, n_faked_c):
    r, c = df.shape
    for c in columns :
        if c not in df.columns.values :
            print(f" ! {c} not in df columns")
        elif df[c].dtype != np.int64 and df[c].dtype != np.float64 :
            print(f" ! column {c} is not numeric")
            # column is not a number
            pass
        else :
            # column is a number
            m = np.mean(df[c])
            s = np.std(df[c])
            vals = m + rd.choice([-1, 1], 1) * rd.randint(4, 10, n_faked_c)*s
            vals = np.floor(vals).astype(int)
            for v in vals :
                df.loc[rd.randint(0, r, 1), c] = v
    return df
        
        
def make_noise():
    """
    Add noise (all kind) to automatically generated data
    """
    # TODO
    return None
    




if __name__ == "__main__":
    """
    This file contains function to add noise to pandas dataframe.
    """

    # load pandas dataframe from generated csv
    # file_in = "./data_out/dogs_dataset.csv"
    file_in = "./data_in/demo.csv" # file for testing
    file_out = "./data_noisy/WTF.csv"


    """
    Test section
    """
    print(df_in)
    print()

    # print(NullRowMaker(df_in, 1))
    # print(RandomNullMaker(df_in, 3))
    print(ExageratedValues(df_in, ['yy', 'C', 'A'], 2))















