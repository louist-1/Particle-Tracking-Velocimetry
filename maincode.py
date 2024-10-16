# Importing Relevant Libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import statistics

# Function to rescale videos to fit and view on computer screen
def rescale(frame, scale):
    width = int(frame.shape[1]*scale)
    height = int(frame.shape[0]*scale)
    dimensions = (width, height)
    return cv2.resize(frame, dimensions, interpolation = cv2.INTER_CUBIC)

# Main set of code as a function to allow calling using multiple videos
def maincode(cap): # Argument is video path/name
    # Appendable lists for circles and time
    c = [] 
    t = []
    told = 0
    while (cap.isOpened()):  # While video is open     
        
        ret, frame = cap.read() # Split video into frames
        
        # Rescale each frame by calling previous rescale function
        frame_resized = rescale(frame, 0.25)     
        
        #Applying post effects:
        
        # Convert to grayscale
        gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
        # Binarise the grayscaled image
        threshold, thresh = cv2.threshold(gray, 190, 255, cv2.THRESH_BINARY)
        #Apply Gaussian blur to the binarised frame
        blur = cv2.GaussianBlur(thresh,(9,9),0)
        # canny = cv2.Canny(blur, 125, 175)
    
        # If letter 'q' is pressed break video
        if cv2.waitKey(25) & 0xFF == ord('q'): 
                break    
     
        #Find circles in frame after blurring and other effects. 
        circles = cv2.HoughCircles(
        blur,
        cv2.HOUGH_GRADIENT, 1,
        minDist = 60,
        param1 = 50, param2 = 13,
        minRadius = 40, maxRadius=70,
        )
        
        
        if circles is not None: # If a circle is found
        
            # Changing data type to an unsigned integer
            circles = np.uint16(np.around(circles)) 
            
            for circ in circles[0, :]:
                tnew = told + 1 # Adding a time/ frame counting system
                
                # Split found circles into coordinated (x,y) 
                # and radius size ('r')
                x, y, r = circ 
                # Append into list of c and multiple by -1 
                # (flips consecutive graphs in y direction)
                c.append(circ*-1) 
                
                # Append time and switch to new time step
                told = tnew
                t.append(told)
            
            # Plot circles with found coordinates onto the frames with blur 
            # and original resized frames with a purple circle with radius r
            # (Can change depending on how viewage preferences)
            # Note if eliptical 'circle' is found radius will be larger and 
            # a larger circle will be mapped onto frame
            cv2.circle(frame_resized, (x, y), r, (112,41,99), 3)
            cv2.circle(blur, (x, y), r, (112,41,99), 3)
            
            
        cv2.imshow('circles', blur) #Show drawn circles on the blured frames
    # Once loop is finished or broken release video and close all windows
    cap.release()
    cv2.destroyAllWindows()
    return np.array(c), np.array(t) # Return arrays of circle and time data

# Function to calculate coefficient of restitution (COR)
def Calc_COR(data):
    #Use scipy to find peaks, in the y cicle data
    peaks = find_peaks(data[:,1], height=-800, prominence=200)
    
    #Extract the verticle heights 
    heights = peaks[1]['peak_heights']
    
    # Append heights into two arrays and add a 1 in the first place of one. 
    # This is a makeshift way to shift the list to do the next calculation.
    heights2 = np.append(heights, heights[-1])
    heightsplus = np.append(heights[0], heights)
    
    # Square root all values in each list
    sqrth = np.sqrt(abs(heights2))
    sqrthplus = np.sqrt(abs(heightsplus))
    
    # Divide height 2 by height 1, height 3 by height 2 etc...
    # Returns COR values across bounce
    dh = sqrthplus/sqrth
    
    #Printing list of COR calculated excluding the added '1' and its effects.
    print(dh[1:-1])
    
    # Calculate mean of CORs excluding the added '1' and its effects.
    COR = statistics.mean(dh[1:-1])
    
    COR_rounded = round(COR, 3) #Round to 3dp
    return peaks, heights, COR_rounded 

# Function tying all previous functions together
def final(video):
    c1, t1 = maincode(video)
    peaks, heights, COR = Calc_COR(c1)
    xpos = t1[peaks[0]] 

    return c1, t1, peaks, heights, COR, xpos #Return all useful values

#Getting sets of data matching the 4 videos
c1 , t1, peaks1, heights1, COR1, xpos1 = final(cv2.VideoCapture("BigDrop1.mp4"))
c2 , t2, peaks2, heights2, COR2, xpos2 = final(cv2.VideoCapture("BigDrop2.mp4"))
c3 , t3, peaks3, heights3, COR3, xpos3 = final(cv2.VideoCapture("SmallDrop1.mp4"))
c4 , t4, peaks4, heights4, COR4, xpos4 = final(cv2.VideoCapture("SmallDrop2.mp4"))

def subplotsfn(videopeakplot): # Small function maintaining integrity of the plots
    if videopeakplot > 7:
        plotnumber = plotnumber + 1
    return plotnumber

        
fig, (axs) = plt.subplots(1, 4)# Create subplots
fig.set_size_inches(12, 4)# Sizings
#Add overall x and y label
fig.supylabel('Y Displacement (Relative to frame)', fontsize = 14)
fig.supxlabel('Time (Frame Number)', fontsize = 14)



# Function to plot each previous set of data
def plotting(c1,t1,heights,COR,xpos,no,plot_title):
    
    # Plotting height against time - 
    # can uncheck line 143 if scatter plot is wanted instead of line
    # plt.scatter(t1, c1[:, 1], color = 'c', s =10, label = 'Ball Trajectory')
    axs[no].plot(t1, c1[:, 1], color = 'c')
    
    #Scatter the peaks onto gaph
    axs[no].scatter(xpos, heights,color = 'm', s = 80, marker = 'x', 
                label = COR)
    
    # Configerations for aesthetic and readability
    axs[no].legend()
    axs[no].set_xlim(xmin=0)
    axs[no].grid()
    axs[no].set_title(plot_title, fontsize = 13)
    
    # Next hashed line is optional to remove ticks on y axis.
    
    # axs[no].tick_params(axis='y',labelcolor='none', which='both', top=False, 
                        # bottom=False, left=False, right=False)

    return

#Calling plotting functions with chosen arguments
plotting(c1,t1,heights1,COR1,xpos1,(0),'42cm Drop 1')
plotting(c2,t2,heights2,COR2,xpos2,(1),'42cm Drop 2')
plotting(c3,t3,heights3,COR3,xpos3,(2),'21cm Drop 1')
plotting(c4,t4,heights4,COR4,xpos4,(3),'21cm Drop 2')
