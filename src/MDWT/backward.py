import DWT.backward as iDWT

def backward(S, K):
    ''' Backward Motion 2D DWT.

    Compute the inverse 2D-DWT of a sequence of pyramids.

    Input:
    -----

        S: []

            A list of pyramids.

        K: int

            Number of levels of the inverse 2D-DWT.

    Output:
    ------

        s: []

            A list of images.
    '''
    s = []
    for pyramid in S:
        s.append(iDWT(pyramid, K))
    return s
