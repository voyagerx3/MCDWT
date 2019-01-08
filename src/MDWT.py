from DWT import forward as DWT
from DWT import backward as iDWT
from io import image, pyramid

def forward(s = "/tmp/input/", S = "/tmp/output/", N = 5):
    ''' Motion 1-iteration forward 2D DWT of a sequence of images.

    Compute the 2D-DWT of each image of the sequence s.

    Input:
    -----

        s: the sequence of images to be transformed.

    Output:
    ------

        S: the sequence of pyramids (transformed images).

    '''
    for i in range(N):
        img = image.read("{}{:03d}".format(s, i))
        pyr = DWT(img)
        pyramid.write(pyr, "{}{:03d}".format(S, i))
#    S = Sequence()
#    for image in s:
#        S.append(DWT(image))
#    return S

def backward(S = "/tmp/input", s = "/tmp/output/", N = 5):
    ''' Motion 1-iteration forward 2D DWT of a sequence of pyramids.

    Compute the inverse 2D-DWT of each pyramid of the sequence S.

    Input:
    -----

        S: the sequence of pyramids to be transformed.

    Output:
    ------

        s: the sequence of images.

    '''

    for i in range(N):
        pyr = pyramid.read("{}{:03d}".format(S, i))
        img = iDWT(pyr)
        image.write("{}{:03d}".format(s, i))
    
#    s = []
#    for pyramid in S:
#        s.append(iDWT(pyramid))
#    return s
