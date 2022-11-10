


def student_entrypoint(Measured_Bandwidth, Previous_Throughput, Buffer_Occupancy, Available_Bitrates, Video_Time, Chunk, Rebuffering_Time, Preferred_Bitrate ):
    #student can do whatever they want from here going forward
    global bitrate
    R_i = list(Available_Bitrates.items())
    R_i.sort(key=lambda tup: tup[1] , reverse=True)

    # step 1: estimate the next bandwidth by using the previous throughput
    xn = Previous_Throughput
    # step 2: smooth the estimate bandwidth by utilizing the smooth function
    yn=xn
    # step 3: estimate the next bitrate by using the smoothed function yn

    return bitrate