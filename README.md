# SVC (Symmetric Video Coding)

Video Codec = Video Encoder + Video Decoder

```
   I   +----+   I   +----+   I
 ----> | VE | ----> | VD | ---->
       +----+       +----+
```

Video Encoder = Spatio-Temporal Transform + Entropy Compressor

```
  I   +-----+   I   +----+   I
----> | STT | ----> | EC | ---->
      +-----+       +----+
```

Video Decoder = Entroy Decompressor + Inverse Spatio-Temporal Transform

```
  I   +----+   I   +------+   I
----> | ED | ----> | ISTT | ---->
      +----+       +------+
```

Spatio-Temporal Transform = Spatial Transform + Temporal Transform

```
  I   +----+   I   +----+   I
----> | ST | ----> | TT | ----->
      +----+       +----+
```

Inverse Spatio-Temporal Transform = Inverse Temporal Transform + Inverse Spatial Transform

```
  I   +-----+   I   +-----+  I
----> | ITT | ----> | IST | ---->
      +-----+       +-----+
```
