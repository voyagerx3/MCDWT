def MCDWT(input = 'input', output = 'output', n=5, l=2) -> None :
    ''' A Motion Compensated Discrete Wavelet Transform.

    Compute the 1D-DWT along motion trajectories. The input video (as a sequence of images) must be stored in disk (<input> directory) and the output (as a sequence of DWT coefficients that are called pyramids) will be stored in disk (<output> directory). So, this MCDWT implementation does not transform the video on the fly.

    Arguments:
        <input>: directory of the input images that must be named 000.png, 001.png, etc.
        <output>: directory fo the output (transformed) pyramids (named 000.png, 001.png, etc.).
        <n>: number of images of the input.
        <l>: number of leves of the MCDWT (temporal scales). Controls the GOP size. Examples: l=0 -> GOP_size = 1, l=1 -> GOP_size = 2, l=2 -> GOP_size = 4. etc.
    '''

    x = 2
    for j in range(l): # Number of temporal scales
        i = 0
        while i < (n//x):
            print('A = ', x*i)
            print('B = ', x*i+x//2)
            print('C = ', x*i+x)
            i += 1
            print('i = ', i)
        x *= 2
