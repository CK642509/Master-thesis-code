import os 

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)



# get the path of target folder
path = input("The path of target folder:")
folder_name = path.split("\\")[-1] # split with "\" and select the last one
print("folder name: " + str(folder_name))

# txt file number
num = 0

# If there is txt, read it and paste it into a new sheet
for file in os.listdir(path):
    if file.endswith(".txt"):
        # Create a folder
        createFolder(path+"\\removed")
        
        with open(path + "\\" + file, "r") as file_obj:
            file_name = file_obj.name.split('\\')[-1]
            name = file_name.rsplit('.',1)[0] # .rsplit('.',1)[0] to remove ".txt"

            log_list = file_obj.readlines()
            length = len(log_list)
            print(str(num) + ". " + str(file_name))
            print("Total " + str(length) + " rows.")

            for r in range(length):
                # remove first two /t
                log_list[r] = log_list[r].split("\t",2)[-1]
                
        with open(path + "\\removed\\" + name + "_OK.txt", "w") as file_obj:
            file_obj.write("".join(log_list))
            
        num = num + 1



