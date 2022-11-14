#import numpy as np
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
    #xn = max(Measured_Bandwidth,Previous_Throughput)
    xn=Previous_Throughput
    Y_m.append(xn)
    X_m.append(len(X_m)+1)
    # step 2: smooth the estimate bandwidth by utilizing the smooth function

    #Linear smoother
    #Y_nm = np.array(Y_m)
    #X_nm = np.array(X_m)
    #A = np.vstack([X_nm, np.ones(len(X_nm))]).T
    #k, b = np.linalg.lstsq(A, Y_nm, rcond=None)[0]
    #yn=k*xn+b
    #EWMA smoother
    if len(Y_n) == 0:
        Yn = Measured_Bandwidth
    else:
        Yn=-0.2*(Y_n[len(Y_n)-1]-xn)*(Video_Time - V_time[len(V_time)-1])+Y_n[len(Y_n)-1]
    V_time.append(Video_Time)
    Y_n.append(Yn)
    print(Yn)
    # step 3: estimate the next bitrate by using the smoothed function yn

    #dead zone quantizer
    R_up=0
    R_down=0
    real_up=0
    real_down=0
    up_d=int(R_i[0][0])
    down_d=int(R_i[0][0])
    if real_down == 0:
    	real_down = int(R_i[0][0])
    for i in range(len(R_i)):
        if R_i[i][1]<0.85*Yn:
            R_up = R_i[i][1]
            real_up = int(R_i[i][0])
            break
    for i in range(len(R_i)):
        if R_i[i][1]<Yn:
            R_down = R_i[i][1]
            real_down = int(R_i[i][0])
            break
    
    if len(P_bitrate) == 0:
        bitrate = real_down
    else:
        if P_bitrate[len(P_bitrate)-1] < R_up:
            bitrate = real_up
            up_d = abs(bitrate-Yn)
        elif P_bitrate[len(P_bitrate)-1] < R_down:
            bitrate  = P_bitrate[len(P_bitrate)-1]
            up_d = abs(bitrate-Yn)
        else:
            bitrate = real_down
            up_d = abs(bitrate-Yn)

    for i in range(len(R_i)):
        if abs(int(R_i[i][0]) - Yn) < up_d:
            bitrate = int(R_i[i][0])
            up_d = abs(bitrate-Yn)
    P_bitrate.append(bitrate)
    return bitrate
