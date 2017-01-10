# SVT (Scalable Video Transform)

SVT represents an video in a way that a using only a portion of the transformed video, a video with a lower temporal resolution (temporal scalability), lower spatial resolution (spatial scalability) or/and lower quality (quality scalability) can be generated. If all the transformed data is used, the original video is obtained.

## Input

A sequence I of images I[t], where each I[t] is a 2D array of pixels I[t][y][x]. "t" denotes time. "x" and "y" denote space. 

```
+---------------+  +---------------+     +---------------+   +--------------+
|               |  |               |     |               |   |              |
|               |  |               |     |            O <----+ I[T-1][y][x] |
|      I[0]     |  |      I[1]     | ... |     I[T-1]    |   |              |
|               |  |               |     |               |   +--------------+
|               |  |               |     |               |
+---------------+  +---------------+     +---------------+
```

## Output

A sequence S of temporal subbands S[l], where each S[l] is a sequence of frames S[l][t] and where each frame S[l][t] is collection of spatial subbands.

```
                        t = 0                               t = 1
                  +---+---+-------+                   +---+---+-------+
                  | A | B |       |                   |   |   |       |
                  +---+---+   E   |                   +---+---+       |
                  | C | D |       |                   |   |   |       |
                  +---+---+-------+                   +---+---+-------+ l = 0
                  |       |       |                   |       |       |
                  |   F   |   G   |                   |       |       |
                  |       |       |                   |       |       |
                  +-------+-------+       t = 0       +-------+-------+
                      ^       ^     +---+---+-------+     ^        ^
                      |       |     |   |   |       |     |        |
                      |       +---- +---+---+       | ----+        |
                      |             |   |   |       |              |
                      |             +---+---+-------+ l = 1        |
                      |             |       |       |              |
                      |             |       |       |              |
                      |             |       |       |              |
      t = 0           |             +-------+-------+              |           t = 1
+---+---+-------+     |                 ^       ^                  |     +---+---+-------+
|   |   |       |     |                 |       |                  |     |   |   |       |
+---+---+       | ----+                 |       |                  +---- +---+---+       |
|   |   |       |                       |       |                        |   |   |       |
+---+---+-------+                       |       |                        +---+---+-------+  l = 2
|       |       |                       |       |                        |       |       |
|       |       | ----------------------+       +----------------------- |       |       |
|       |       |                                                        |       |       |
+-------+-------+                                                        +-------+-------+

A = approximation coefficients for the 1-th level of spatial decomposition
B = horizontal detail coefficients at the 1-th level
C = vertical detail coefficients at the 1-th level
D = diagonal detail coefficients at the 1-th level
E = horizontal detail coefficients at the 0-th level
F = vertical detail coefficients at the 0-th level
G = diagonal detail coefficients at the 0-th level

I[2][0] = approximation frame for the 2-th level of temporal decomposition, first GOP
I[2][1] = approximation frame for the 2-th level of temporal decomposition, second GOP
I[1][0] = detail frame for the 1-th level of temporal decomposition, first GOP
I[0][0] = detail frame for the 0-th level of temporal decomposition, first GOP
I[0][1] = detail frame for the 0-th level of temporal decomposition, first GOP

(X --> Y) = Y depends on X (Y has been encoded using X)
```

## Algorithm

1. tmp = Spatial_Decomposition(I)
2. S = Temporal_Decomposition(tmp)

# Spatial Decomposition

## Input

A sequence I of images.

## Output

A sequence O of transformed images.

## Algorithm

1. for each I[t] in I:
2. ~ O[t] = 2D_DWT(I[t])

# 2D DWT

## Input

A image I.

## Output

A transformed image O.

## Algorithm

See [pywt.wavedec2()](https://pywavelets.readthedocs.io/en/latest/ref/2d-dwt-and-idwt.html#d-multilevel-decomposition-using-wavedec2) at [PyWavelets](https://pywavelets.readthedocs.io/en/latest/index.html). [Discrete wavelet transform](https://en.wikipedia.org/wiki/Discrete_wavelet_transform).

# Temporal Decomposition

A motion-driven L-levels 1D-DWT.

## Input

A sequence I of images.

## Output

A sequence O of temporal subbands O[l], where each O[l] is a sequence of frames O[l][t].

## Algorithm
[Lifting scheme](https://en.wikipedia.org/wiki/Lifting_scheme)
[A Really Friendly Guide To Wavelets](http://www.polyvalens.com/blog/wavelets/theory/)
http://stackoverflow.com/questions/15802827/how-can-dwt-be-used-in-lsb-substitution-steganography

```
Temporal_Decomposition(I, N, L):
  for l in range(L):
    n = N
    N /= 2
    for i in range(n):
      DWT_Step(I, O, n)
```

# DWT Step

A motion-driven 1-levels 1D-DWT.

## Input

A sequence of images

```
function R=myDWT(sig, count)
 [Lo_D, Hi_D] = wfilter_bior44();
 input = sig;
 while(count ~= 0) % While count not equal to 0
     % Pass through filters by using convolution
     Ca = conv(input, Lo_D, 'same');
     Cd = conv(input, Hi_D, 'same');
     % Downsample by 2
     Ca = downsample(Ca, 2);
     Cd = downsample(Cd, 2);
     % TODO: Save Ca and Cd somewhere
     count = count - 1;
     input = Ca;
 end
 R = input;
end
```
# Optical Flow Estimation

## Input

Two images A and C.

## Output

A image B.

## Algorithm

See how to compute the [optical flow](http://docs.opencv.org/trunk/d7/d8b/tutorial_py_lucas_kanade.html) between to images using [OpenCV](http://opencv.org/).

# SVC (Symmetric Video Coding)

Video Codec = Video Encoder + Video Decoder

```
   I   +----+   I   +----+   I
 ----> | VE | ----> | VD | ---->
       +----+       +----+
```

Video Encoder = Spatio-Temporal Transform + Progressive Entropy Compressor

```
  I   +-----+   I   +-----+   I
----> | STT | ----> | PEC | ---->
      +-----+       +-----+
```

Video Decoder = Progressive Entropy Decompressor + Inverse Spatio-Temporal Transform

```
  I   +-----+   I   +------+   I
----> | PED | ----> | ISTT | ---->
      +-----+       +------+
```

Spatio-Temporal Transform = Spatial Transform + Temporal Transform

```
  I   +----+   I   +----+   I
----> | ST | ----> | TT | ----->
      +----+       +----+
```

Inverse Spatio-Temporal Transform = Inverse Temporal Transform + Inverse Spatial Transform

```
  I   +-----+   I   +-----+   I
----> | ITT | ----> | IST | ---->
      +-----+       +-----+
```

Spatial Transform = 2D Laplacian Pyramid Transform (LPT)
Inverse Spatial Transform = Inverse 2D LPT

Temporal Transform = Motion Compensation (MC) in the LPT
Inverse Temporal Transform = Inverse MC in the LPT

Progressive Entropy Compressor = [MSB](https://en.wikipedia.org/wiki/Most_significant_bit) to [LSB](https://en.wikipedia.org/wiki/Least_significant_bit) [bit-plane](https://en.wikipedia.org/wiki/Bit_plane) encoder. The top floor of the pyramid is compressed using 0-Order Binary Arithmetic Coding (0OBAC)

