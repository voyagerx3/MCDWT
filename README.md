# Motion Compensated Discrete Wavelet Transform (MCDWT)

## MCDWT and video scalabilty
**MCDWT inputs a [video][video] and outputs a video**, in a way that when using only a portion of the data of the transformed video, a video with a lower temporal resolution ([temporal scalability][Scalability]), lower spatial resolution ([spatial scalability][Scalability]) or/and lower quality ([quality scalability][Scalability]) can be generated. If all the transformed data is used, then the original video is obtained (MCDWT es is a lossless transform). The video output has exactly the same number of elements than the input video (for example, no extra motion fields are produced). At this moment, we will focuse only on spatial scalability.

[Scalability]: http://eeweb.poly.edu/~yao/EL6123/scalablecoding.pdf
[video]: https://en.wikipedia.org/wiki/Video

## The 's'-levels 2D Discrete Wavelet Transform
A<sup>[1](#myfootnote1)</sup> [2D-DWT][2D-DWT] (2 Dimensions - Discrete Wavelet Transform) generates a scalable representation of an image and by extension, of a video if we apply the DWT on all the images of the video. This is done, for example, in [the JPEG2000 image and video compression standard][J2K]. Notice that only the spatial redundancy is exploited. All the temporal redundancy is still in the video.

[J2K]: https://en.wikipedia.org/wiki/JPEG_2000
[2D-DWT]: https://en.wikipedia.org/wiki/Discrete_wavelet_transform

### Input
A sequebce `V` of `n` images:
```
                                                         x
+---------------+  +---------------+     +---------------+
|               |  |               |     |            |  |
|               |  |               |   y |----------- O <---- V[n-1][y][x]
|               |  |               | ... |               |
|               |  |               |     |               |
|               |  |               |     |               |
|               |  |               |     |               |
+---------------+  +---------------+     +---------------+
      V[0]               V[1]                 V[n-1]
```

### Output
A sequence `S` of `n` "pyramids". For example, a 2-levels 2D-DWT looks like:
```
+---+---+-------+  +---+---+-------+     +---+---+-------+
|LL2|HL2|       |  |   |   |       |     |   |   |       |
+---+---+  HL1  |  +---+---+       |     +---+---+       |
|LH2|HH2|       |  |   |   |       |     |   |   |       |
+---+---+-------+  +---+---+-------+ ... +---+---+-------+
|       |       |  |       |       |     |       |       |
|  LH1  |  HH1  |  |       |       |     |       |       |
|       |       |  |       |       |     |       |       |        
+-------+-------+  +-------+-------+     +-------+-------+
       S[0]               S[1]                  S[2]
```

### Algorithm
```python
S = []
for image in V:
  S.append(2D_DWT(image))
```

### Scalability
The 2D-DWT applied to a video produces a representation scalable in the space (we can extract different videos with different spatial scales or resolutions), in the time (we can extract diferent videos with different number of frames) and in quality (we can get the DWT coefficients with different quantization steps to reconstruct videos of different quality).

### Inverse 's'-levels inverse 2D-DWT
In the last example, subbands `V2={S[0].LL2, S[1].LL2, ..., S[n-1].LL2}` represent the scale (number) 2 of the original video (the spatial resolution of this `V2` is the resolution of `V` divided by 4 in each spatial dimension).

To reconstruct the scale 1, we apply the iDWT (1-level inverse DWT) in place (this means that the output of the transform replaces all or a part of the input data):
```python
for pyramid in S:
  2D_iDWT(pyramid)
```

And finally, to get the original video, we need to apply again the previous code.

### Redundancy and compression
The 2D DWT provides an interesting feature to `S`: `S` usually has a lower entropy than `V`. This means that if we apply to `S` an entropy encoder, we can get a shorter representation of the video than if we encode `V` directly. This is a consequence of 2D-DWT exploits the spatial redudancy of the images of the video: neighboring pixels tend to have similar values and when they are substracted, they tend to produce zeros.

## MCDWT
As we have said, the 2D-DWT does not exploit the temporal redundancy of a video. This means that we can achieve higher compression ratios if we apply a 1D-DWT along the temporal domain. This is exactly what MCDWT does. However, due to the temporal redundancy is generated mainly by the presence of objects in the scene of the video which are moving with respect to the camera, some sort of motion estimation and compensation must be used.

### Input
A sequence `S` of `n` pyramids.

### Output
A sequence `T` of `n` pyramids organized in `l` temporal subbands, where each subband is a sequence of pyramids.

For example, if `l=2` and `n=5`:

```
      Spatial
      scale 0 1 2       t = 1                               t = 3
            ^ ^ ^ +---+---+-------+                   +---+---+-------+                                ^
            | | | |   |   |       |                   |   |   |       |                                |
            | | v +---+---+       |                   +---+---+    O <---- T[3][y][x]                  |
            | |   |   |   |       |                   |   |   |       |                                |
            | v   +---+---+-------+                   +---+---+-------+ l = 0                          |
            |     |       |       |                   |       |       |                                |
            |     |       |       |                   |       |       |                                |
            |     |       |       |                   |       |       |                                |
            v     +-------+-------+       t = 2       +-------+-------+                                |
                      |       |     +---+---+-------+     |        |                                 ^ |
                      |       |     |   |   |       |     |        |                                 | |
                      |       +---->+---+---+       |<----+        |                                 | |
                      |             |   |   |       |              |                                 | |
                      |             +---+---+-------+ l = 1        |                                 | |
                      |             |       |       |              |                                 | |
                      |             |       |       |              |                                 | |
                      |             |       |       |              |                                 | |
      t = 0           |             +-------+-------+              |           t = 4                 | |
+---+---+-------+     |                 |       |                  |     +---+---+-------+         ^ | |
|   |   |       |     |                 |       |                  |     |   |   |       |         | | |
+---+---+       |<----+                 |       |                  +---->+---+---+       |         | | |
|   |   |       |                       |       |                        |   |   |       |         | | |
+---+---+-------+                       |       |                        +---+---+-------+  l = 2  | | |
|       |       |                       |       |                        |       |       |         | | |
|       |       |<----------------------+       +----------------------->|       |       |         | | |
|       |       |                                                        |       |       |         | | |
+-------+-------+                                                        +-------+-------+         v v v
      GOP 0                                       GOP 1                             Temporal scale 2 1 0
<---------------><----------------------------------------------------------------------->

(X --> Y) = X depends on Y (X has been encoded using Y)
```

### Algorithm of the direct (forward) transform (MCDWT)
![MCDWT](forward.png)

### Algorithm of the inverse (backward) transform (iMCDWT)
![MCDWT](backward.png)

### Data extraction

#### Spatial scalability

Scale 1:

[A.L] = iDWT(A.L,0); [B.L] = iDWT(B.L,0); [C.L] = iDWT(C.L,0);
[A.H] = iDWT(0,A.H); [\tilde{B}.H] = iDWT(0,\tilde{B}.H); [C.H] = iDWT(0,C.H);
A = [A.L] + [A.H]; C = [C.L] + [C.H];
[B_A.H] = P([A.H], [B.L] -> [A.L]); [C_A.H] = P()

tmp1 = DWT(V[1])
tmp2 = iDWT(tmp1.L, 0)
tmp2 -= (P(V[0].0, tmp2 -> V[0].0) + P(V[2].0, tmp2 -> V[2].0)/2
tmp2 = DWT(tmp2)
V[1] = {tmp1.L, tmp2.H}

tmp = iDWT(V[1].L, 0)
V[1] += 


### Inverse SVT (examples)

#### Spatial scalability

Scale 2:

V[0].2 = T[0].L2,
V[4].2 = T[4].L2,
V[2].2 = T[2].L2 + (V[0].2 + V[4].2)/2,
V[1].2 = T[1].L2 + (V[0].2 + V[2].2)/2,
V[3].2 = T[3].L2 + (V[2].2 + V[4].2)/2

Scale 1:

(note A.Hx = {A.HLx, A.LHx, A.HHx})

V[0].1 = 2D_iDWT(V[0].2, T[0].H2),
V[4].1 = 2D_iDWT(V[4].2, T[4].H2),
(tmp = 2D_iDWT(V[2].2, 0))
V[2].1 = tmp + ( 
  P(V[0].1, tmp -> V[0].1) +
  P(V[4].1, tmp -> V[4].1)
)/2,
(tmp = 2D_iDWT(V[1].2, 0))
V[1].1 = tmp + (
  P(V[0].1, tmp -> V[0].1) +
  P(V[2].1, tmp -> V[2].1)
)/2,
(tmp = 2D_iDWT(V[3].2, 0))
V[3].1 = tmp + (
  P(V[2].1, tmp -> V[2].1) +
  P(V[4].1, tmp -> V[4].1)
)/2

Scale = 0

V[0].0 = V[0] = 2D_iDWT(V[0].1, T[0].H1),

V[4].0 = 2D_iDWT(V[4].1, T[4].H1),

(tmp = 2D_iDWT(V[2].1, 0))
V[2].0 = tmp + (
  P(V[0].0, tmp -> V[0].0) +
  P(V[4].0, tmp -> V[4].0)
)/2,

(tmp = 2D_iDWT(V[1].1, 0)
V[1].1 = tmp + (
  P(V[0].0, tmp -> V[0].0) +
  P(V[2].0, tmp -> V[2].0)
)/2,

(tmp = 2D_iDWT(V[3].1, 0)
V[3].1 = tmp + (
  P(V[2].0, tmp -> V[2].0) +
  P(V[4].0, tmp -> V[4].0)
)/2.

Scale = -1

V[0].-1 = 2D_iDWT(V[0].0, 0),

V[4].-1 = 2D_iDWT(V[4].0, 0),

(tmp = 2D_iDWT(V[2].0, 0))
v[2].-1 = tmp + (
  P(V[0].-1, tmp -> V[0].-1) +
  P(V[4].-1, tmp -> V[4].-1)
)/2,

(tmp = 2D_iDWT(V[1].0, 0))
v[1].-1 = tmp +

#### Temporal scalability

Scale 2:

V[0].0 = V[0] = 2D_iDWT<l>(T[0]),
V[4].0 = 2D_iDWT<l>(T[4])

Scale 1:

Scale 2,
(V[2].2 = T[2].L2 + (V[0].2 + V[4].2)/2)
((tmp = 2D_iDWT(V[2].2, 0))
(V[2].1 = tmp + ( 
  P(V[0].1, tmp -> V[0].1) +
  P(V[4].1, tmp -> V[4].1)
)/2)
(tmp = 2D_iDWT(V[2].1, 0))
V[2].0 = tmp + (
  P(V[0].0, tmp -> V[0].0) +
  P(V[4].0, tmp -> V[4].0)
)/2

Scale 0:

Scale2, Scale 1,

V[1].2 = T[1].L2 + (V[0].2 + V[2].2)/2,
((tmp = 2D_iDWT(V[1].1, 0)
V[1].1 = tmp + (
  P(V[0].0, tmp -> V[0].0) +
  P(V[2].0, tmp -> V[2].0)
)/2)

V[3].2 = T[3].L2 + (V[2].2 + V[4].2)/2


2D_iDWT(T[0]), 2D_iDWT(T[4]), 2D_iDWT(T[

```python
for pyramid in T:
  2D_iDWT(pyramid)
```

#### Quality scalability

##### In a intra-image

Design a "sorting" algorithm that, bit-plane by bit-plane, in function of the content of the LLl subband (or the requested WOI of this) dedides the ordering in which the locations at the rest of subbands should be checked to determine if the wavelet coefficients that are in those locations are significant or not, depending on the contribution of these locations to the energy of the inverse transform. LH, HL and HH subbands can be "melt" in only one (the H subband to distinguish they from the L subband). This should generate basically a collection of quadtrees (one for each L coefficient).


Sort the wavelet coefficients by magnitude (supposing an orthogonal transform)

### Algorithm



## Wavelets and pyramids
The <sup>[1](#myfootnote1)</sup> DWT (Discrete Wavelet Transform)][DWT] allows to get a scalable representation of a image and by extension, of a video if we apply the DWT on all the images of the video. However, this can be also done with [Gaussian and Laplacian pyramids][Pyramids]. Image pyramids are interesting because they are shift invariant and therefore, one can operate within the scales as they are *normal* images.

[DWT]: https://en.wikipedia.org/wiki/Discrete_wavelet_transform

Image pyramids representations need more memory than DWT ones and this is a drawback when compressing. Luckily, it is very fast to convert a laplacian pyramid representation into a DWT representation and viceversa. For this reason, even if we use the DWT to work with our images, we can suppose at any moment that we can also working with the pyramid of those images.

[Pyramids]: https://en.wikipedia.org/wiki/Pyramid_(image_processing)



## Video transforming choices
To obtain a multiresolution version or a video (a sequence of images), [the<sup>[1](#myfootnote1)</sup> DWT (Discrete Wavelet Transform)][DWT] is applied along temporal (`t`) and spatial domains (`2D`). At this point, two alternatives arise: (1) a `t+2D` transform or (2) a `2D+t` transform. In a `t+2D` transform, the video is first analyzed over the time domain and next, over the spatial domain. A `2D+t` transform does just the opposite.


Each choice has a number of pros and cons. For example, in a `t+2D` transform we can apply directly any image predictor based on motion estimation because the input is a normal video. However, if we implement a `2D+t` transform, the input to the motion estimator is a sequence of images in the DWT domain. [The overwhelming majority of DWT's are not shift invariant][Friendly Guide], which basically means that DWT(`s(t)`) `!=` DWT(`s(t+x)`), where `x` is a displacement of the signal `s(t)` along the time domain. Therefore, motion estimators which compare pixel values will not work on the DWT domain. On the other hand, if we want to provide true spatial scalability (processing only those spatial resolutions (scales) necessary to get a spatially scaled of our video), a `t+2D` transformed video could be unsuitable because the first step of the forward transform (`t`) should be reversed at full resolution in the backward transform (as the forward transform did).

[Friendly Guide]: http://www.polyvalens.com/blog/wavelets/theory

<!--That said, this project implements a t+2D version for its simplicity at the t stage.-->

## Input of SVT

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
```python
tmp = Spatial_Analysis(I)
S = Temporal_Analysis(tmp)
```

# Spatial Analysis

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

See [pywt.wavedec2()](https://pywavelets.readthedocs.io/en/latest/ref/2d-dwt-and-idwt.html#d-multilevel-decomposition-using-wavedec2) at [PyWavelets](https://pywavelets.readthedocs.io/en/latest/index.html).

# Temporal Analysis

A motion-driven `L` temporal-levels (`L+1` temporal scales) lifted 1D-DWT.

## Input

A sequence `I` of images in the wavelet domain.

## Output

A sequence `S` of temporal subbands, where each subband `S[l]` is a sequence of images in the wavelet domain.

## Algorithm

First, an example of a generation of 3 temporal scales (two iterations or levels of the transform) with 5 images:

```
I[0] I[1] I[2] I[3] I[4]
I[0] D[1] I[2] D[3] I[4] (predict step)
I[0]      I[2]      I[4] (update step)
I[0]      D[2]      I[4] (predict step)
I[0]                I[4] (update step)
---- -------------------
GOP0        GOP1

S[2] = {I[0], I[4]}
S[1] = {D[2]}
S[0] = {D[1], D[3]}

To generate Prediction(D[2]) we search (I[2].2).0 into (I[0].2).0 and (I[4].2).0.

```

Next, an algorithm. Notice that `O` is computed in-place (of `I`,  for this reason,`I` is returned).
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

<!-- Footnotes -->
<a name="myfootnote1">1</a>: there are infinite transforms. 
