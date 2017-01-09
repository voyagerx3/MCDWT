# MRVT (MultiResolution Video Transform)

## Input

A sequence I of images I[t], where each I[t] is a 2D array of pixels I[t][y][x]. "t" denotes time. "x" and "y" denote space. 

```
+---------------+  +---------------+     +---------------+   +--------------+
|               |  |               |     |               |   |              |
|               |  |               |     |            O<-+---+ I[T-1][y][x] |
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
                             ^      +---+---+-------+
                             |      |   |   |       |        A = approximation coefficients for the 1-th level of spatial decomposition
                             +----- +---+---+       |        B = horizontal detail coefficients at the 1-th level
                                    |   |   |       |        C = vertical detail coefficients at the 1-th level
                                    +---+---+-------+ l = 1  D = diagonal detail coefficients at the 1-th level
                                    |       |       |        E = horizontal detail coefficients at the 0-th level
                                    |       |       |        F = vertical detail coefficients at the 0-th level
                                    |       |       |        G = diagonal detail coefficients at the 0-th level
      t = 0                         +-------+-------+                          t = 1
+---+---+-------+                                                        +---+---+-------+
|   |   |       |                                                        |   |   |       |
+---+---+       |                                                        +---+---+       |
|   |   |       |                                                        |   |   |       |
+---+---+-------+                                                        +---+---+-------+  l = 2
|       |       |                                                        |       |       |
|       |       |                                                        |       |       |
|       |       |                                                        |       |       |
+-------+-------+                                                        +-------+-------+

I[2][0] = approximation frame for the 2-th level of temporal decomposition, first GOP
I[2][1] = approximation frame for the 2-th level of temporal decomposition, second GOP
I[1][0] = detail frame for the 1-th level of temporal decomposition, first GOP
I[0][0] = detail frame for the 0-th level of temporal decomposition, first GOP
I[0][1] = detail frame for the 0-th level of temporal decomposition, first GOP
```

## Algorithm

1. Perform spatial decomposition.
2. Perform temporal decomposition.



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

