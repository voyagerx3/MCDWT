# t+2D Video Transform (t2DVT)

t2DVT represents an video in a way that a using only a portion of the transformed video, a video with a lower temporal resolution (temporal scalability), lower spatial resolution (spatial scalability) or/and lower quality (quality scalability) can be generated. If all the transformed data is used, the original video is obtained.

To obtain a multiresolution version or a video (a sequence of images), the DWT (Discrete Wavelet Transform) is used. A DWT (there are infinite transforms) is applied along temporal (t) and spatial domains (2D). At this point, two alternatives arise: (1) a t+2D transform or (2) a 2D+t transform.

In a t+2D transform, the video is first analyzed over the time domain and next, over the spatial domain. A 2D+t transform does just the opposite.

Each choice has a number of pros and cons. For example, in a t+2D transform we can apply directly any image predictor based on motion estimation because the input is a normal video. However, if we implement a 2D+t transform, the input to the motion estimator is a sequence of images in the DWT domain. The overwhelming majority of DWT are not shift invariant [1], which basically means that DWT(`s(t)`) `!=` DWT(`s(t+x)`), where `x` is a displacement of the signal `s(t)` along the time domain. Therefore, motion estimators which compare pixel values will not work on the DWT domain. On the other hand, if we want to provide true spatial scalability (processing only those spatial resolutions (scales) necessary to get a spatially scaled of our video), a t+2D transformed video could be unsuitable because the first step of the forward transform (t) should be reversed at full resolution in the backward transform (as the forward transform did).

That said, this project implements a t+2D version for its simplicity at the t stage.

## Input

A sequence `I` of images `I[t]`, where each `I[t]` is a 2D array of pixels I[t][y][x]. "t" denotes time. "x" and "y" denote space. 

```
                                                      x
+---------------+  +---------------+     +---------------+   +--------------+
|               |  |               |     |               |   |              |
|               |  |               |   y |            O <----+ I[T-1][y][x] |
|      I[0]     |  |      I[1]     | ... |     I[T-1]    |   |              |
|               |  |               |     |               |   +--------------+
|               |  |               |     |               |
+---------------+  +---------------+     +---------------+
```

## Output

A sequence `S` of temporal subbands `S[l]`, where each `S[l]` is a sequence of frames `S[l][t]` and where each frame `S[l][t]` is collection of spatial subbands (`A`, `B`, `C`, `D`, `E`, `F` an `G`, in the following example).

```
      Spatial
      scale 0 1 2       t = 0                               t = 1
            ^ ^ ^ +---+---+-------+                   +---+---+-------+                                ^
            | | | | A | B |       |                   |   |   |       |                                |
            | | v +---+---+   E   |                   +---+---+ (x,y) |                                |
            | |   | C | D |       |                   |   |   |       |                                |
            | v   +---+---+-------+                   +---+---+-------+ l = 0                          |
            |     |       |       |                   |       |       |                                |
            |     |   F   |   G   |                   |       |       |                                |
            |     |       |       |                   |       |       |                                |
            v     +-------+-------+       t = 0       +-------+-------+                                |
                      ^       ^     +---+---+-------+     ^        ^                                 ^ |
                      |       |     |   |   |       |     |        |                                 | |
                      |       +---- +---+---+       | ----+        |                                 | |
                      |             |   |   |       |              |                                 | |
                      |             +---+---+-------+ l = 1        |                                 | |
                      |             |       |       |              |                                 | |
                      |             |       |       |              |                                 | |
                      |             |       |       |              |                                 | |
      t = 0           |             +-------+-------+              |           t = 1                 | |
+---+---+-------+     |                 ^       ^                  |     +---+---+-------+         ^ | |
|   |   |       |     |                 |       |                  |     |   |   |       |         | | |
+---+---+       | ----+                 |       |                  +---- +---+---+       |         | | |
|   |   |       |                       |       |                        |   |   |       |         | | |
+---+---+-------+                       |       |                        +---+---+-------+  l = 2  | | |
|       |       |                       |       |                        |       |       |         | | |
|       |       | ----------------------+       +----------------------- |       |       |         | | |
|       |       |                                                        |       |       |         | | |
+-------+-------+                                                        +-------+-------+         v v v
      GOP 0                                       GOP 1                             Temporal scale 2 1 0
<---------------><----------------------------------------------------------------------->

                                                                                    
A = approximation coefficients for the 1-th level of spatial decomposition (LL2, L(ow), H(ight))
B = horizontal detail coefficients at the 1-th level (HL2)
C = vertical detail coefficients at the 1-th level (LH2)
D = diagonal detail coefficients at the 1-th level (HH2)
E = horizontal detail coefficients at the 0-th level (HL1)
F = vertical detail coefficients at the 0-th level (LH1)
G = diagonal detail coefficients at the 0-th level (HH1)

I[2][0] = approximation frame for the 2-th level of temporal decomposition, first GOP
I[2][1] = approximation frame for the 2-th level of temporal decomposition, second GOP
I[1][0] = detail frame for the 1-th level of temporal decomposition, first GOP
I[0][0] = detail frame for the 0-th level of temporal decomposition, first GOP
I[0][1] = detail frame for the 0-th level of temporal decomposition, first GOP

(X --> Y) = Y depends on X (Y has been encoded using X)

(x,y) = spatial translation (location) of a DWT coefficient in a spatial subband
t = temporal transpation (location) of a DWT frame in a temporal subband

The wavelets are generated from a single basic wavelet, the so-called mother wavelet, by scaling and translation [1]
```

## Algorithm
```
tmp = Temporal_Decomposition(I)
S = Spatial_Decomposition(tmp)
```

# Temporal Decomposition

A motion-driven `L` temporal-levels (`L+1` temporal scales) lifted 1D-DWT.

## Input

A sequence `I` of images.

## Output

A sequence `O` of temporal subbands `O[l]`, where each `O[l]` is a sequence of wavelet frames `O[l][t]`.

## Algorithm

First, an example for generating 3 temporal scales (two iterations or levels of the transform):

```
I[0] I[1] I[2] I[3] I[4]
I[0] D[1] I[2] D[3] I[4] (predict step)
I[0]      I[2]      I[4] (update step)
I[0]      D[2]      I[4] (predict step)
I[0]                I[4] (update step)
---- -------------------
GOP0        GOP1

O[2] = {I[0], I[4]}
O[1] = {D[2]}
O[0] = {D[1], D[3]}
```

Next, an algorithm. Notice that `O` is computed in-place (for this, `I` is returned).
```
x = 2 # An offset
for each temporal level:
  i = 0 # Image index
  while i < (T//x):
    D = DWT_Step(I[x*i+x//2-1], I[x*i+x//2], I[x*i+x//2+1])
    I[x*i+x//2] = D
    i += 1
  x *= 2
return I
```

[Lifting scheme](https://en.wikipedia.org/wiki/Lifting_scheme)
[1] [A Really Friendly Guide To Wavelets](http://www.polyvalens.com/blog/wavelets/theory/)
http://stackoverflow.com/questions/15802827/how-can-dwt-be-used-in-lsb-substitution-steganography
http://stat.columbia.edu/~jakulin/Wavelets/index.html
http://www.ual.es/~vruiz/Docencia/Apuntes/Coding/Image/00-Fundamentals/index.html#x1-2000012

# DWT Step

A motion-driven 1 temporal-level lifted 1D-DWT without update step, for 3 images.

## Input

A sequence `{I[0],I[1],I[2]}` of 3 images.

## Output

A frame `D`.

## Algorithm

`D = I[1] - (I[0] + I[2])/2`, where `(A+B)/2` represents the generation of a prediction image using the images `A` and `B`, and where `A - B` represents the pixel-to-pixel subtraction of image `B` to image `A`. 

# Image Prediction
We will use an optical flow estimation algorithm for creating the prediction image.

## Input

Two images `A` and `C`.

## Output

An image `B`.

## Algorithm

See how to compute the [optical flow](http://docs.opencv.org/trunk/d7/d8b/tutorial_py_lucas_kanade.html) between to images using [OpenCV](http://opencv.org/). The prediction is built dividing by 2 the vectors field and projecting the ...


# Spatial Decomposition

## Input

A sequence `I` of images.

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

