def sequence_2D_iDWT(S, K):
    for pyramid in S:
        _2D_iDWT(pyramid, K) # In-place computation
    return S
