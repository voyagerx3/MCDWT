import DWT.forward as DWT

def forward(s, K):
    ''' Forward Motion 2D DWT.

    Compute the 2D-DWT of a sequence of images.
    Input:
    -----

        s: []

            A list of images.

        K: int

            Number of levels of the 2D-DWT.

    Returns
    -------

        S: []

            A list of pyramids.
    '''
    
    S = []
    for image in s:
        S.append(DWT(image, K))
    return S
