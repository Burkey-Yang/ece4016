import numpy as np
global X_m
global Y_m
global Y_n
global V_time
global P_bitrate
global bitrate
X_m=[]
Y_m=[]
Y_n=[]
V_time=[]
P_bitrate=[]

def student_entrypoint(Measured_Bandwidth, Previous_Throughput, Buffer_Occupancy, Available_Bitrates, Video_Time, Chunk, Rebuffering_Time, Preferred_Bitrate ):
    #student can do whatever they want from here going forward
    
    R_i = list(Available_Bitrates.items())
    R_i.sort(key=lambda tup: tup[1] , reverse=True)

    # step 1: estimate the next bandwidth by using the previous throughput
    xn = max(Measured_Bandwidth,Previous_Throughput)
    Y_m.append(xn)
    X_m.append(len(X_m)+1)
    # step 2: smooth the estimate bandwidth by utilizing the smooth function

    #Linear smoother
    Y_nm = np.array(Y_m)
    X_nm = np.array(X_m)
    A = np.vstack([X_nm, np.ones(len(X_nm))]).T
    k, b = np.linalg.lstsq(A, Y_nm, rcond=None)[0]
    yn=k*xn+b
    #EWMA smoother
    if len(Y_n) == 0:
        Yn = Measured_Bandwidth
    else:
        Yn=-0.2*(Y_n[len(Y_n)-1]-xn)*(Video_Time - V_time[len(V_time)-1])+Y_n[len(Y_n)-1]
    V_time.append(Video_Time)
    Y_n.append(Yn)
    # step 3: estimate the next bitrate by using the smoothed function yn

    #dead zone quantizer
    R_up=0
    R_down=0
    for i in len(R_i):
        if R_i[i]<0.85*yn:
            R_up = R_i[i]
            break
    for i in len(R_i):
        if R_i[i]<yn:
            R_down = R_i[i]
            break

    if P_bitrate.empty() == True:
        bitrate = R_down
    else:
        if P_bitrate[len(P_bitrate)-1] < R_up:
            bitrate = R_up
        elif P_bitrate[len(P_bitrate)-1] < R_down:
            bitrate  = P_bitrate[len(P_bitrate)-1]
        else:
            bitrate = R_down
    P_bitrate.append(bitrate)
    return bitrate