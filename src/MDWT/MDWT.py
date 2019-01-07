import DWT_2D.forward as DWT_2D
from DWT import forward as DWT
from DWT import backward as iDWT

def forward(s):
    ''' Motion 2D 1-iteration forward DWT of a sequence of images.

    Compute the 2D-DWT of each image of the sequence s.

    Input:
    -----

        s: list[], the sequence of images.

    Output:
    ------

        S: list[], the sequence of pyramids.

    '''
    
    S = []
    for image in s:
        S.append(DWT(image))
    return S

def backward(S):
    ''' Motion 2D 1-iteration forward DWT of a sequence of pyramids.

    Compute the inverse 2D-DWT of each pyramid of the sequence S.

    Input:
    -----

        S: list[], the sequence of pyramids.

    Output:
    ------

        s: list[], the sequence of images.

    '''
    
    s = []
    for pyramid in S:
        s.append(iDWT(pyramid))
    return s
