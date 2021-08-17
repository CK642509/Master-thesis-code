import pandas as pd
import os
from os import walk
from os.path import join

# get the path of target folder
path = input("The path of target folder:")
folder_name = path.split("\\")[-1]

# for counting txt number
num = 0

# start
for root, dirs, files in walk(path):
    for f in files:
        if f.endswith(".csv"):
            num = num + 1
            
            root_name = root.split("\\")[-1]
            print(str(num) + ". Folder / File: " + str(root_name) + " / " + str(f))
            name = f.split(".")[0]
            

            fullpath = join(root, f)

            if num == 1:
                df = pd.read_csv(fullpath, sep=",")
                df.drop(df.columns[1:-2], axis=1, inplace=True)
                df_re = df.rename(columns={"Average": name+"_Avg", "STDEVA": name+"_STD"})
                
            elif num > 1:
                df2 = pd.read_csv(fullpath, sep=",")
                df2.drop(df2.columns[:-2], axis=1, inplace=True)
                df2_re = df2.rename(columns={"Average": name+"_Avg", "STDEVA": name+"_STD"})
        
                frames = [df_re, df2_re]
                result = pd.concat(frames, axis=1)
            
                df_re = result

print(result)


# save as csv
result.to_csv(path + "\\" + folder_name + ".csv", index=False)

# finished
print("Finished!")
