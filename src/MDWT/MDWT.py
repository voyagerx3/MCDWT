import DWT_2D.forward as DWT_2D

def sequence_DWT_2D(s, K):
    ''' Motion DWT_2D.

    Compute the 2D-DWT of a sequence of images.

    Arguments
    ---------
        s : str

            Prefix of the input/output images. Example: "/tmp/".

        K : int

            Number of levels of the 2D-DWT.

    Returns
    -------

        S : str

            Prefix of the output pyramids. Eample: "/tmp".
    '''
    

    for image in s:
        DWT_2D(image, K) # In-place computation
    return s
def sequence_2D_iDWT(S, K):
    for pyramid in S:
        _2D_iDWT(pyramid, K) # In-place computation
    return S
