# generate wav file containing sine waves
# FB36 - 20120617
import math, wave, array
import numpy as np
import cv2

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Function returs the luma component. Inputs the RGB values
def luma(B,G,R):
    return 16.0 + (.003906 * ((65.738 * R) + (129.057 * G) + (25.064 * B)))

# Function returs the blue difference component. Inputs the RGB values
def BY(B,G,R):
    return 128.0 + (.003906 * ((-37.945 * R) + (-74.494 * G) + (112.439 * B)))

# Function returs the red difference component. Inputs the RGB values
def RY(B,G,R):
    return 128.0 + (.003906 * ((112.439 * R) + (-94.154 * G) + (-18.285 * B)))

# Function returns the corresponding frequency for the input pixel Values
def freq(v):
    return 1500 + (v * 3.1372549)

#Function that attaches the VIS code at the start
def VIS_code(mode):
    if mode == "PD90": #VIS code for PD90 - 99d -> 1100011b
        #data_append(0.000000001,2000)
        # data_append(1900,100)
        # data_append(1500,100)
        # data_append(1900,100)
        # data_append(1500,100)
        # data_append(2300,100)
        # data_append(1500,100)
        # data_append(2300,100)
        # data_append(1500,100)

        g.write('1900(300.000) ') # Leader Tone
        data_append(1900,300.000)
        g.write('1200(10.000) ') # break
        data_append(1200,10.000)
        g.write('1900(300.000) ') # Leader Tone
        data_append(1900,300.000)
        g.write('1200(30.000)') # Start bit
        data_append(1200,30.000)
        #1100hz = “1”, 1300hz = “0”
        g.write('1100(30.000)') #1
        data_append(1100,30.000)
        g.write('1100(30.000)') #1
        data_append(1100,30.000)
        g.write('1300(30.000)') #0
        data_append(1300,30.000)
        g.write('1300(30.000)') #0
        data_append(1300,30.000)
        g.write('1300(30.000)') #0
        data_append(1300,30.000)
        g.write('1100(30.000)') #1
        data_append(1100,30.000)
        g.write('1100(30.000)') #1
        data_append(1100,30.000)
        g.write('1300(30.000)') # even parity bit - 0
        data_append(1300,30.000)
        g.write('1200(30.000)') # Stop bit
        data_append(1200,30.000)

# Function which appends a sin wave to existing data.
# Inputs frequency of sine wave, Duration of the sine wave
def data_append(freq1,duration):
    global tx, next_point, g_uspersample, g_fudge, g_twopioverrate, g_theta, g_scale
    # tx ----> g_fudge
    # duration ----> tonedur
    # freq1 ----> tonefreq
    duration *= 1000.0 #converting ms to us

    duration += tx;
    tonesamples = (duration/g_uspersample) + 0.5 # NOTE why this 0.5???
    deltatheta = g_twopioverrate * freq1
    samp_range = int(tonesamples)
    if (tonesamples - samp_range) > 0.5 :
        samp_range += 1

    for i in range(samp_range):
        if(freq1 == 0):
            data.append(32767)
        else :
            sample = int(math.sin(g_theta)*g_scale)
            data.append(sample)
            g_theta += deltatheta

    tx = duration - (samp_range * g_uspersample)


def calculate_phase(freq2,numSamplesPerCyc,next_point):
    error = 0.01
    l = len(data)
    amplitude = data[l-1] / 32767.0
    slope = (next_point - data[l-1])/32767.0
    phase = 0

    for k in range(0,numSamplesPerCyc*1000):
        k = k/1000.0
        a = math.sin(math.pi * 2 * k / numSamplesPerCyc)
        s = math.sin(math.pi * 2 * (k+1) / numSamplesPerCyc) - a

        if(amplitude > 0 and slope > 0 and a > 0 and s > 0):
            if (abs(a-amplitude) <= error):
                break
        if(amplitude > 0 and slope < 0 and a > 0 and s < 0):
            if (abs(a-amplitude ) <= error):
                break
        if(amplitude < 0 and slope < 0 and a < 0 and s < 0):
            if (abs(a-amplitude ) <= error):
                break
        if(amplitude < 0 and slope > 0 and a < 0 and s > 0):
            if (abs(a-amplitude) <= error):
                break

        phase = math.pi * 2 * k / numSamplesPerCyc
    return phase

#-------------------------------------------------------------------------------
# Read the image in colour scale
data = array.array('h') # signed short integer (-32768 to 32767) data
sampleRate = 44100 # of samples per second (standard)
numChan = 1 # of channels (1: mono, 2: stereo)
dataSize = 2 # 2 bytes because of using signed short integers => bit depth = 16
volume = 100 # percent
tx = 0;
next_point = 0;
g_uspersample = 1000000.0/sampleRate
g_twopioverrate = 2.0 * math.pi / sampleRate
g_theta = 0.0
temp1 = (float)(1 << (16-1))
temp2 = 80.0/100.0
g_scale = (int)(temp1*temp2)
print(g_scale)
g_theta = 0.0

img = cv2.imread('320x256.png', 1);
shape = img.shape
print(" The size of the input image is \n")
print(shape[0] , "x" , shape[1])
print("\n")
print("Writing the PD90 values in PD90.txt and PD90_freq.txt")

f = open('PD90.txt','w')
g = open('PD90_freq.txt','w')

data.append(int(0))
data.append(int(0))
data.append(int(0))

VIS_code("PD90")

for i in range(0,shape[0],2):
#for i in range(0,20,2):
    g.write('1200(20.000) ') # sync word
    data_append(1200,20.000)
    g.write('1500(2.080) ') # porch
    data_append(1500,2.080)
    for j in range(0,shape[1]):
        f.write(str(luma(img[i,j,0],img[i,j,1],img[i,j,2]))) # blue pixel
        g.write(str(freq(luma(img[i,j,0],img[i,j,1],img[i,j,2]))))
        g.write('(0.532)')
        data_append(freq(luma(img[i,j,0],img[i,j,1],img[i,j,2])),0.532)
        f.write(' ')
        g.write(' ')
    f.write('\n')
    g.write('\n')
    for j in range(0,shape[1]):
        avg_ry = (RY(img[i,j,0],img[i,j,1],img[i,j,2]) + RY(img[i+1,j,0],img[i+1,j,1],img[i+1,j,2]))/2.0
        f.write(str(avg_ry))
        g.write(str(freq(avg_ry)))
        g.write('(0.532)')
        data_append(freq(avg_ry),0.532)
        f.write(' ')
        g.write(' ')
    f.write('\n')
    g.write('\n')
    for j in range(0,shape[1]):
        avg_by = (BY(img[i,j,0],img[i,j,1],img[i,j,2]) + BY(img[i+1,j,0],img[i+1,j,1],img[i+1,j,2]))/2.0
        f.write(str(avg_by))
        g.write(str(freq(avg_by)))
        g.write('(0.532)')
        data_append(freq(avg_by),0.532)
        f.write(' ')
        g.write(' ')
    f.write('\n')
    g.write('\n')
    for j in range(0,shape[1]):
        f.write(str(luma(img[i+1,j,0],img[i+1,j,1],img[i+1,j,2])))
        g.write(str(freq(luma(img[i+1,j,0],img[i+1,j,1],img[i+1,j,2]))))
        g.write('(0.532)')
        data_append(freq(luma(img[i+1,j,0],img[i+1,j,1],img[i+1,j,2])),0.532)
        f.write(' ')
        g.write(' ')
    f.write('\n')
    g.write('\n')
    f.write('\n')
    g.write('\n')

    print(i,",",j)

f.close()
g.close()

print(len(data))
f1 = wave.open('PD90_freq.wav', 'w')
f1.setparams((1, dataSize, 44100, len(data), "NONE", "Uncompressed"))
f1.writeframes(data.tostring())
f1.close()
