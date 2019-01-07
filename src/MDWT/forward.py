import DWT.forward as DWT

def forward(s, K):
    ''' Forward Motion 2D DWT.

    Compute the 2D-DWT of a sequence of images.

    Input:
    -----

        s: []

            A list of images. Example:
                                                      x 
            +---------------+  +---------------+     +---------------+
            |               |  |               |     |            |  |
            |               |  |               |   y |----------- o <---- s[N-1][y][x]
            |               |  |               | ... |               |
            |               |  |               |     |               |
            |               |  |               |     |               |
            |               |  |               |     |               |
            +---------------+  +---------------+     +---------------+
                  s[0]               s[1]                 s[N-1]


        K: int

            Number of levels of the 2D-DWT.

    Returns
    -------

        S: []

            A list of pyramids. Example:

            +---+---+-------+  +---+---+-------+     +---+---+-------+
            |LL2|HL2|       |  |   |   |       |     |   |   |       |
            +---+---+  HL1  |  +---+---+       |     +---+---+       |
            |LH2|HH2|       |  |   |   |       |     |   |   |       |
            +---+---+-------+  +---+---+-------+ ... +---+---+-------+
            |       |       |  |       |       |     |       |       |
            |  LH1  |  HH1  |  |       |       |     |       |       |
            |       |       |  |       |       |     |       |       |        
            +-------+-------+  +-------+-------+     +-------+-------+
                  S[0]               S[1]                  S[N-1]

    '''
    
    S = []
    for image in s:
        S.append(DWT(image, K))
    return S
