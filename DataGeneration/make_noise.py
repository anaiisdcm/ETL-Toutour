import numpy as np
import numpy.random as rd
import pandas as pd


"""
This file contains function to add noise to pandas dataframe.
"""

# load pandas dataframe from generated csv
# file_in = "./data_out/dogs_dataset.csv"
# file_in = "./data_in/demo.csv" # file for testing
# file_out = "./data_noisy/WTF.csv"

# df_in = pd.read_csv(file_in)



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
        
        
def make_noise(pc_null=20, pc_nullrows=5, pc_exagerated=10):
    """
    Add noise (all kind) to automatically generated data
    """
    to_nullify = ["Owner", ]
    to_exagerate = {"OwnerPayment":["amount"],
                    "past_walks":["distance"],
                    "Dog":["weight", "optimal_tour_duration", "athleticism"]}

    for e in to_nullify :
        df = pd.read_csv("./data_out/df_"+e+".csv")
        r, c = df.shape
        # nullify elements
        n_nulls = round(( r*c * pc_null) / 100)
        df = RandomNullMaker(df, n_nulls=n_nulls)
        # nullify rows
        n_rows = round(( r * pc_nullrows) / 100)
        df = NullRowMaker(df, n_rows)
        # save to csv
        df.to_csv(f"./data_noisy/df_noisy_{e}.csv", index=False)

    for e in to_exagerate :
        df = pd.read_csv("./data_out/df_"+e+".csv")
        r, c = df.shape
        # nullify elements
        n_faked_c = round(( r * pc_exagerated) / 100)
        ExageratedValues(df, columns=to_exagerate[e], n_faked_c=n_faked_c)
        # save to csv
        df.to_csv(f"./data_noisy/df_noisy_{e}.csv", index=False)
    return None
    




if __name__ == "__main__":
    make_noise(pc_null, pc_nullrows, pc_exagerated)














