import numpy as np
import numpy.random as rd
import pandas as pd

file_in = "./data_out/dogs_dataset.csv"
file_in = "./data_in/demo.csv"
file_out = "./data_noisy/WTF.csv"

df_in = pd.read_csv(file_in)




def NullRowMaker(df, n_rows):
    r, c = df.shape
    if n_rows >= r//2 :
        print(f"Asking to nullify {n_rows} rows in dataframe that contains only {r}. Not doing it")
        n_rows = r//2
    
    # choose rows randomly
    r_to_null = rd.choice(r, n_rows)
    df.loc[r_to_null] = None
    return df


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
        
        


print(df_in)

# df_1 = NullRowMaker(df_in, 1)
# print(df_1)

# df_2 = RandomNullMaker(df_in, 3)
# print(df_2)

df_3 = ExageratedValues(df_in, ['yy', 'C'], 2)
print(df_3)









