# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 11:54:15 2018

@author: HW def2864
0-0-6 add standard deviation calculation, average on single spectrum file, fit average function on circular mapping 190619

0-0-4 change part of code into function can be called by other
0-0-3 change the way of import and export data form csv moldue to numpy function
0-0-2 can remove the baselie of mutliple sigle and mapping spectra data in the same folder
"""
from time import time, strftime, localtime
initial_time = time()
from traceback import print_exc
import os
import numpy as np
from scipy.interpolate import interp1d



FWHM = 50 # FWHM
step = 0.5
m = round((FWHM -1) / 2) # clipping window
m = 50
folder_name = '{} {} {}'.format(os.path.basename(__file__)[:-3], strftime("%y%m%d %H%M", localtime()), m)
no_brain_avg = True
delimiter = "\t"

def remove_baseline(file_name, m, step, folder_name = 'rb 0-0-4'):
    # check whether the exist of result dictionary
    delimiter = "\t"
    single_spec = False
    
    
    # import spectra
    data_in = np.genfromtxt(file_name, delimiter=delimiter)
    count = 0
    while np.isnan(data_in[0, count]):     # cehck mapping 第一列前幾行會是空格
        count += 1
    
    if count == 0 and len(data_in[0]) == 2: # 只有一條光譜的話，labspc存檔會是直的須轉置
        rawdata = data_in.transpose()
        if rawdata[0,0] > rawdata[0,-1]:
            rawdata = np.flip(rawdata, 1) #labspec 存檔是由大到小
        single_spec = True

    else:
        rawdata = data_in[:,count:]
        if rawdata[0,0] > rawdata[0,-1]:
            rawdata = np.flip(rawdata, axis=1)

        rawdata = rawdata[np.any(rawdata, axis=1)] # 把全為零的光譜刪掉

    
    # 創結果資料夾
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

    
    # 內插光譜
    x_data = np.arange(int(rawdata[0,0])+1, int(rawdata[0,-1]) + step , step)
    
    y_data = np.zeros((len(rawdata), len(x_data)), dtype=np.float32)
    y_data[0] = x_data
    
    print('讀取處理結束', time() - initial_time)
    
    for spectrum in range(1,len(rawdata)):
        
        lin_f = interp1d(rawdata[0], rawdata[spectrum], kind='cubic')
        y_data[spectrum] = lin_f(x_data)
        
        # remove baseline
        # statistics-sensitive nonlinear iterative peak-clipping algorithm
        # we use second order with a constant window size w (odd number)
    print('內插光譜結束', time() - initial_time)
       
        
        
    
    def clip_baseline(y_data, m):
        background = np.copy(y_data)  
        n = len(background)
        z = np.zeros(n)
        for p in range(m,0,-1):      # m to 1
            for i in range(p,(n-p)):
                a1 = background[i]
                lowerB = i-p
                upperB = i+p
                if lowerB >= 0 and upperB <= n:
                    a2 = (background[lowerB] + background[upperB]) / 2
                elif lowerB < 0:
                    a2 = (background[0] + background[upperB]) / 2
                    print(1)
                elif (i+p) > n:
                    a2 = (background[lowerB] + background[n]) / 2
                    print(2)
                elif lowerB < 0 and upperB > n:
                    a2 = (background[0] + background[n]) / 2
                    print(3)

                z[i] = min(a1,a2)
            
            for i in range(p,(n-p)):
                background[i] = z[i]
        return background
    
    
        
    # export spectra
    

    def save_result(x_data, y_data, backgrounds, name = ''):
        debaselined = y_data-backgrounds
        debaselined[0] = x_data
        if count == 0 and len(y_data) <= 2:
            y_data = y_data.transpose()
            backgrounds = backgrounds.transpose()
            debaselined = debaselined.transpose()
        
        
        savedata('', name + 'interpolate', y_data, file_name)
        savedata('', name + 'background', backgrounds, file_name)
        savedata('sb', name + 'debaselined', debaselined, file_name)
    
    backgrounds = np.copy(y_data)
    for spectrum in range(1,len(backgrounds)): 
        backgrounds[spectrum] = clip_baseline(y_data[spectrum], m)

    print('背景逼近結束', time() - initial_time)
    
    
    save_result(x_data, y_data, backgrounds, name = '')
    
    
    
    if no_brain_avg and len(rawdata) > 2:
        raw_avg = np.zeros((2,len(rawdata[0])))
        rb_avg = np.zeros((2,len(x_data)))
        raw_avg[0] = rawdata[0]
        rb_avg[0] = x_data
        raw_avg[1] = np.mean(rawdata[1:,], axis=0)
        rb_avg[1] = np.mean((y_data-backgrounds)[1:,], axis=0)
        savedata('raw_avg', 'raw {} avg'.format(len(rawdata)-1), raw_avg.transpose(), file_name)
        savedata('rb_avg', 'rb {} avg'.format(len(rawdata)-1), rb_avg.transpose(), file_name)

        raw_std= np.zeros((2,len(rawdata[0])))
        rb_std = np.zeros((2,len(x_data)))
        raw_std[0] = rawdata[0]
        rb_std[0] = x_data
        raw_std[1] = np.std(rawdata[1:,], axis=0, dtype=np.float64, ddof=1)
        rb_std[1] = np.std((y_data-backgrounds)[1:,], axis=0, dtype=np.float64, ddof=1) 
        #Means Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N represents the number of elements. By default ddof is zero.
        savedata('raw_std', 'raw {} std'.format(len(rawdata)-1), raw_std.transpose(), file_name)
        savedata('rb_std', 'rb {} std'.format(len(rawdata)-1), rb_std.transpose(), file_name)
        
        raw_rsd= np.zeros((2,len(rawdata[0])))
        rb_rsd = np.zeros((2,len(x_data)))
        raw_rsd[0] = rawdata[0]
        rb_rsd[0] = x_data
        raw_rsd[1] = raw_std[1]/raw_avg[1]
        rb_rsd[1] = rb_std[1]/rb_avg[1]
        #Means Delta Degrees of Freedom. The divisor used in calculations is N - ddof, where N represents the number of elements. By default ddof is zero.
        savedata('raw_rsd', 'raw {} rsd'.format(len(rawdata)-1), raw_rsd.transpose(), file_name)
        savedata('rb_rsd', 'rb {} rsd'.format(len(rawdata)-1), rb_rsd.transpose(), file_name)
        
        
    print('計算儲存結束', time() - initial_time, '\n')
    
    return single_spec


def savedata(subfolder, outputname, nparray, file_name):
        if not os.path.isdir(folder_name + '\\' + subfolder):
            os.mkdir(folder_name + '\\' + subfolder)
        np.savetxt(folder_name + '\\' + subfolder + "\\{} {} window{}.txt".format(os.path.splitext(file_name)[0], outputname, m), nparray, delimiter=delimiter, fmt='%g')

    
files = []
single_spce_files = []
path = "."
for f in os.listdir(path):
    #print (os.path.splitext(f))
    if os.path.isfile(f) and os.path.splitext(f)[1]==".txt":
        files.append(f)


result = "\n"
for f in files:
    
    
    try:
        print("delete baseline on ", f)
        print('開始處理光譜', time() - initial_time)
        single_spec = remove_baseline(f, 50, 0.5, folder_name)         
        if single_spec == True:
            single_spce_files.append([f, f.rfind('_')])

    except:
        print("->無法處理")
        result += "無法處理: " + f + "\n"
        print_exc()

s_file_group_name = {}

for s_file in single_spce_files:
    if s_file[0][:s_file[1]] in s_file_group_name.keys():
        s_file_group_name[s_file[0][:s_file[1]]].append(s_file[0])
    else:
         s_file_group_name[s_file[0][:s_file[1]]] = [s_file[0]]


for g in s_file_group_name:
    raw_np_array = []
    rb_np_array = []
    
    for f in s_file_group_name[g]:
        data_in = np.genfromtxt(f, delimiter=delimiter)
        rawdata = data_in.transpose()
        if rawdata[0,0] > rawdata[0,-1]:
            rawdata = np.flip(rawdata, 1) #labspec 存檔是由大到小
        raw_np_array.append(rawdata[1])

    raw_array = np.array(raw_np_array)
    
    raw_avg = np.zeros((2,len(rawdata[0])))
    raw_avg[0] = rawdata[0]
    raw_avg[1] = np.mean(raw_array, axis=0)
    raw_std = np.zeros((2,len(rawdata[0])))
    raw_std[0] = rawdata[0]
    raw_std[1] = np.std(raw_array, axis=0, dtype=np.float64, ddof=1)
    raw_rsd = np.zeros((2,len(rawdata[0])))
    raw_rsd[0] = rawdata[0]
    raw_rsd[1] = raw_std[1]/raw_avg[1]
    savedata('raw_avg', 'raw {} avg'.format(len(raw_np_array)), raw_avg.transpose(), g)
    savedata('raw_std', 'raw {} std'.format(len(raw_np_array)), raw_std.transpose(), g)
    savedata('raw_rsd', 'raw {} rsd'.format(len(raw_np_array)), raw_rsd.transpose(), g)
    
    
    for f in s_file_group_name[g]:
        data_in = np.genfromtxt(folder_name + '\\' + 'sb' + "\\{} {} window{}.txt".format(os.path.splitext(f)[0],'debaselined', m), delimiter=delimiter)
        rbdata = data_in.transpose()
        if rbdata[0,0] > rbdata[0,-1]:
            rbdata = np.flip(rbdata, 1) #labspec 存檔是由大到小
        rb_np_array.append(rbdata[1])

    rb_array = np.array(rb_np_array)
    rb_avg = np.zeros((2,len(rbdata[0])))
    rb_avg[0] = rbdata[0]
    rb_avg[1] = np.mean(rb_array, axis=0)
    rb_std = np.zeros((2,len(rbdata[0])))
    rb_std[0] = rbdata[0]
    rb_std[1] = np.std(rb_array, axis=0, dtype=np.float64, ddof=1)
    rb_rsd = np.zeros((2,len(rbdata[0])))
    rb_rsd[0] = rbdata[0]
    rb_rsd[1] = rb_std[1]/rb_avg[1]
    savedata('rb_avg', 'rb {} avg'.format(len(rb_np_array)), rb_avg.transpose(), g)
    savedata('rb_std', 'rb {} std'.format(len(rb_np_array)), rb_std.transpose(), g)
    savedata('rb_rsd', 'rb {} rsd'.format(len(rb_np_array)), rb_rsd.transpose(), g)



from pprint import pprint
print('單一光譜平均計算分組')
pprint(s_file_group_name)





print(result)
print('總費時', time() - initial_time)
y=input("按任意鍵結束")