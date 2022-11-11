import numpy as np
global X_m
global Y_m
X_m=[]
Y_m=[]

def student_entrypoint(Measured_Bandwidth, Previous_Throughput, Buffer_Occupancy, Available_Bitrates, Video_Time, Chunk, Rebuffering_Time, Preferred_Bitrate ):
    #student can do whatever they want from here going forward
    global bitrate
    R_i = list(Available_Bitrates.items())
    R_i.sort(key=lambda tup: tup[1] , reverse=True)

    # step 1: estimate the next bandwidth by using the previous throughput
    xn = max(Measured_Bandwidth,Previous_Throughput)
    Y_m.append(xn)
    X_m.append(len(X_m)+1)
    # step 2: smooth the estimate bandwidth by utilizing the smooth function
    Y_nm = np.array(Y_m)
    X_nm = np.array(X_m)
    A = np.vstack([X_nm, np.ones(len(X_nm))]).T
    k, b = np.linalg.lstsq(A, Y_nm, rcond=None)[0]
    yn=k*xn+b
    # step 3: estimate the next bitrate by using the smoothed function yn


    return bitrate