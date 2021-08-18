# Master-thesis-code

To speed up data processing, Python and ImageJ macro are applied. Python is utililized for data processing, including SERS spectrum data pretreatment and statistic analysis. ImageJ macro is utilized for selecting region of interest, including microwells and channels, and analyzation after the regions are selected. Here, the functions and descriptions of Python code and ImageJ macro code are written below.

## Python
#### 1_delete two column
* Function:
  * Delete the first two column of data (position information) and save as a new text file.
* Description
  * The SERS spectrum is debaselined by a software written by Prof. Wang’s lab, which has to input data with correct data structure. However, in SERS mapping, the recorded spectrum includes position information. It recorded the x,y position at first two column. Therefore, these two columns have to be removed before import into the debaseline software. 

#### 2_put txt to excel
* Function
  * Put all the text files in the same folder together in a new .csv file.
* Description
  * The output of debaseline software is a text file with single debaselined spectrum. However, for each experiments, there will be lots of SERS spectra. Combining these text file together for further statistic analyzation is needed. Also, the average and standard deviation of SERS spectra are also calculated after combining the text files. They are recorded at last two column. Only the text files in same folder, which has the same experiment condition, are combined.

#### 3_put last two column together
* Function
  * Put all the .csv file in the same folder together in a new .csv file.
* Description
  * After the average and standard deviation of SERS spectra are calculated, these spectrum should be plotted togrther to compare with each other. Therefore, extracting the average and standard deviation from each experiment conditions is needed.

## ImageJ
### Flourescence image (gradient and beads)
* Function:
  * After providing parameters, the microwells or the channels will be selected and analyzed.
* Description:
  * First, select the four corner of the microwell array or channel array. Second provide number of column, row, circle diameter or rectangular height and width. Third, generate the regions of interest. Forth, start analyzing each microwell or channel. This analyzation can be calculating the average fluorescence intensity or the number of beads. Finally, fill the regions of interest with different color for heatmap if needed.

### SERS imaging
* Function:
  * Turn the text file with intensities into a SERS image.
* Description:
  * Get all the intensity of 733 cm-1 peak and save in a text file. Then, the ImageJ macro will open the and turn it into a SERS image.


### SERS-AST
#### 1_create heatmap
* Function:
  * Turn all the text file with intensities in the same folder into SERS images.
* Description:
  * Prepare text files with intensity of 733 cm-1 peak and save them in the same folder. Then, the ImageJ macro will turn them all into SERS images in another folder.

#### 2_split image
* Function:
  * Get the SERS image of each channel if the input images include more than one channel.
* Description:
  * Select the folder with SERS images. Then, the ImageJ macro will open them and select 12 pixels (one channel). Third, the pixels will be duplicated and saved as a smaller SERS image in a folder.

#### 3_combine heatmap
* Function:
  * Combine all the SERS images of each channel and rearrange into a big SERS image, which is based on the original position of each channel.
* Description:
  * Select the folder with SERS images of each channel. Then, these SERS images will be opened and paste to a big SERS image.



