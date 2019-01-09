#import math
import cv2
import numpy as np
import os

class InputFileException(Exception):
    pass

def readL(file_name):
    fn = file_name + "_LL"
    LL = cv2.imread(fn, -1)
    if LL is None:
        raise InputFileException('{} not found'.format(fn))
    else:
        if __debug__:
            print("pyramid: read {}".format(fn))
    return LL.astype(np.float64)

def readH(file_name):
    fn = file_name + "_LH"
    LH = cv2.imread(fn, -1)
    if LH is None:
        raise InputFileException('{} not found'.format(fn))
    else:
        if __debug__:
            print("pyramid: read {}".format(fn))

    fn = file_name + "_HL"
    HL = cv2.imread(fn, -1)
    if HL is None:
        raise InputFileException('{} not found'.format(fn))
    else:
        if __debug__:
            print("pyramid: read {}".format(fn))

    fn = file_name + "_HH"
    HH = cv2.imread(fn, -1)
    if HH is None:
        raise InputFileException('{} not found'.format(fn))
    else:
        if __debug__:
            print("pyramid: read {}".format(fn))
    return LH.astype(np.float64), HL.astype(np.float64), HH.astype(np.float64)

def read(file_name):
    '''Read a pyramid from disk.

    Parameters
    ----------

        image : str.

            Pyramid in the file system, without extension.

    Returns
    -------

        (L, H) where L = [:,:,:] and H = (LH, HL, HH),
        where LH, HL, HH = [:,:,:].

            A color pyramid.

    '''

    #fn = file_name + "_LL"
    #LL = cv2.imread(fn, -1).astype(np.float64)
    #if LL is None:
    #    raise InputFileException('{} not found'.format(fn))
    #else:
    #    if __debug__:
    #        print("pyramid: read {}".format(fn))
    LL = readL(file_name)
    #LL -= 32768

    LH, HL, HH = readH(file_name)
    return (LL, (LH, HL, HH))

def writeH(H, file_name):
    print(len(H))
    LH = H[0]
    LH = np.rint(LH).astype(np.int16)
    cv2.imwrite(file_name + "_LH.png", LH)
    os.rename(file_name + "_LH.png", file_name + "_LH")
    if __debug__:
        print("pyramid: written {}".format(file_name + "_LH"))

    HL = H[1]
    HL = np.rint(HL).astype(np.int16)
    cv2.imwrite(file_name + "_HL.png", HL)
    os.rename(file_name + "_HL.png", file_name + "_HL")
    if __debug__:
        print("pyramid: written {}".format(file_name + "_HL"))

    HH = H[2]
    HH = np.rint(HH).astype(np.int16)
    cv2.imwrite(file_name + "_HH.png", HH)
    os.rename(file_name + "_HH.png", file_name + "_HH")
    if __debug__:
        print("pyramid: written {}".format(file_name + "_HH"))

def write(pyramid, file_name):
    '''Write a pyramid to disk.

    Parameters
    ----------

        L : [:,:,:].

            A LL subband.

        H : (LH, HL, HH), where LH, HL, HH = [:,:,:].

            H subbands.

        file_name : str.

            Pyramid in the file system.

    Returns
    -------

        None.

    '''

    #file_name = '{}L{:03d}.png'.format(path, number)
    #print(np.min(pyramid[0]))
    #LL = pyramid[0] + 32768
    LL = pyramid[0]
    #print(np.min(LL))
    #print(np.max(LL))
    #assert (np.amax(LL) < 65536), 'range overflow'
    #assert (np.amin(LL) >= 0), 'range underflow'

    LL = np.rint(LL).astype(np.uint16)
    cv2.imwrite(file_name + "_LL.png", LL)
    os.rename(file_name + "_LL.png", file_name + "_LL")
    if __debug__:
        print("pyramid: written {}".format(file_name + "_LL"))
    #y = pyramid[0].shape[0]
    #x = pyramid[0].shape[1]
    #buf = np.full((y*2, x*2, 3), 32768, np.uint16)
    #buf[0:y,x:x*2,:] = np.round(pyramid[1][0] + 128)
    #buf[y:y*2,0:x,:] = np.round(pyramid[1][1] + 128)
    #buf[y:y*2,x:x*2,:] = np.round(pyramid[1][2] + 128)
    #LH = pyramid[1][0] + 32768

    writeH(pyramid[1], file_name)
    #LH = pyramid[1][0]

    #assert (np.amax(LH) < 65536), 'range overflow'
    #assert (np.amin(LH) >= 0), 'range underflow'

    #LH = np.rint(LH).astype(np.uint16)
    #LH = np.rint(LH).astype(np.int16)
    #cv2.imwrite(file_name + "_LH.png", LH)
    #os.rename(file_name + "_LH.png", file_name + "_LH")
    #if __debug__:
    #    print("pyramid: written {}".format(file_name + "_LH"))

    #buf[0:y,x:x*2,:] = np.rint(LH).astype('uint16')

    #HL = pyramid[1][1] + 32768
    #HL = pyramid[1][1]
    
    #assert (np.amax(HL) < 65536), 'range overflow'
    #assert (np.amin(HL) >= 0), 'range underflow'

    #HL = np.rint(HL).astype(np.uint16)
    #HL = np.rint(HL).astype(np.int16)
    #cv2.imwrite(file_name + "_HL.png", HL)
    #os.rename(file_name + "_HL.png", file_name + "_HL")
    #if __debug__:
    #    print("pyramid: written {}".format(file_name + "_HL"))

    #buf[y:y*2,0:x,:]= np.rint(HL).astype('uint16')

    #HH = pyramid[1][2] + 32768
    #HH = pyramid[1][2]

    #assert (np.amax(HH) < 65536), 'range overflow'
    #assert (np.amin(HH) >= 0), 'range underflow'

    #HH = np.rint(HH).astype(np.uint16)
    #HH = np.rint(HH).astype(np.int16)
    #cv2.imwrite(file_name + "_HH.png", HH)
    #os.rename(file_name + "_HH.png", file_name + "_HH")
    #if __debug__:
    #    print("pyramid: written {}".format(file_name + "_HH"))

    #buf[y:y*2,x:x*2,:] = np.rint(HH).astype('uint16')
    #file_name = '{}H{:03d}.png'.format(path, number)

    #cv2.imwrite(file_name, buf)
