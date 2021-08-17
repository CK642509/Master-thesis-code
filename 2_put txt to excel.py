import pandas as pd
import os


# find the peak
def analyzepeak(df, title, peak, peak_width=10):
    # define peak range
    peak_lower = peak - peak_width
    peak_upper = peak + peak_width
    
    # calculate maximum
    df_max = df.loc[(df[title] >= peak_lower) & (df[title] <= peak_upper)].max().to_frame().T

    # get max average
    avg_max = df_max.iloc[0]["Average"]

    # get index of max average in raw data to get its STDEVA
    id_list = df.index[df["Average"] == avg_max].tolist()
    std = df.iloc[id_list[0]]["STDEVA"]
    wavenum = df.iloc[id_list[0]][title]
    
    # assign correct STDEVA 
    df_max.loc[:, "STDEVA"] = std

    # assign correct title
    df_max.loc[:, title] = wavenum
    
    return df_max


# calculate average and standard deviation
def avgstd(result):
    # calculate average
    avg_data = result.copy()
    avg_data.drop(avg_data.columns[0], axis=1, inplace=True)
    avg_data["Average"] = avg_data.mean(axis=1)
    avg_data = avg_data.iloc[:,-1]


    # calculate standard deviation
    std_data = result.copy()
    std_data.drop(std_data.columns[[0]], axis=1, inplace=True)
    std_data["STDEVA"] = std_data.std(axis=1)
    std_data = std_data.iloc[:,-1]


    # combine all data and average
    result2 = pd.concat([result, avg_data, std_data], axis=1)

    return result2


# collect all txt into a dataframe
def txt_to_df(data_list):

    # for counting txt number
    num = 0

    result = []
    
    # only open txt
    for i in range(len(data_list)):
        if data_list[i].endswith(".txt"):
            num = num + 1

            if num == 1:
                data = pd.read_csv(path + "\\" + data_list[i], sep="\t", header=None)
                data.columns = [title, data_list[i]]
            
            elif num > 1:
                data2 = pd.read_csv(path + "\\" + data_list[i], sep="\t", header=None)
                data2.drop(data2.columns[0], axis=1, inplace=True)
                data2.columns = [data_list[i]]
        
                frames = [data, data2]
                result = pd.concat(frames, axis=1)

                data = result

    return result


path = "abc"
folder_num = 0

while path != "q":
    folder_num = folder_num + 1

    print("Enter q to quit...")
    
    # get the path of target folder
    path = input("The path of target folder:")
    if path == "q":
        break
    
    folder_name = path.split("\\")[-1] # split with "\" and select the last one
    print("Folder name: " + str(folder_name))

    # get the data list
    try:
        data_list = os.listdir(path)
        print(data_list)
        
    except FileNotFoundError:
        print("File NOT found!")
        break


    # define first column title
    title = "wavenumber"

    # collect all txt into a dataframe
    df = txt_to_df(data_list)

    # calculate average and standard deviation
    result2 = avgstd(df)
    print(result2)

    # define peak to analyze
    # peak = [612, 773, 1185, 1314, 1363, 1512] # R6G
    peak = [620] # Kanamycine
    # peak = [740] # adenine
        
    # analyze all the peak
    for p in peak:
        peak_data = analyzepeak(result2, title, p, 10)
        result2 = pd.concat([result2, peak_data])

    print(result2)

    # save as csv
    result2.to_csv(path + "\\" + folder_name + ".csv", index=False)

    # show informations
    print("\n" + str(folder_num) + ". " + folder_name + " folder is finished!\n")

