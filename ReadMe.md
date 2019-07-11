# h264EncodeInfoEditor

A script to edit H.264 encoder information.

* Before   
	```
	$ mediainfo input.h264

	General
	Complete name                            : input.h264
	Format                                   : AVC
	Format/Info                              : Advanced Video Codec
	File size                                : 103 MiB
	Writing library                          : x264 core 142 r2431+42 c69a006 tMod [8-bit@4:2:0 X86_64]
	Encoding settings                        : cabac=1 / ref=6 / deblock=1:0:-1 / analyse=0x3:0x133 / me=umh / subme=9 / psy=1 / fade_compensate=0.00 / psy_rd=1.00:0.10 / mixed_ref=1 / me_range=24 / chroma_me=1 / trellis=2 / 8x8dct=1 / cqm=0 / deadzone=21,11 / fast_pskip=0 / chroma_qp_offset=-3 / threads=84 / lookahead_threads=5 / sliced_threads=0 / nr=0 / decimate=1 / interlaced=0 / bluray_compat=0 / stitchable=1 / constrained_intra=0 / fgo=0 / bframes=5 / b_pyramid=2 / b_adapt=2 / b_bias=0 / direct=1 / weightb=1 / open_gop=0 / weightp=2 / keyint=250 / keyint_min=1 / scenecut=40 / intra_refresh=0 / rc_lookahead=70 / rc=crf / mbtree=1 / crf=23.0000 / qcomp=0.70 / qpmin=0:0:0 / qpmax=36:36:36 / qpstep=4 / vbv_maxrate=17500 / vbv_bufsize=17500 / crf_max=0.0 / nal_hrd=none / filler=0 / ip_ratio=1.40 / aq=3:0.80 / aq-sensitivity=10.00 / aq-factor=1.00:1.00:1.00 / aq2=0 / aq3=0

	Video
	Format                                   : AVC
	Format/Info                              : Advanced Video Codec
	Format profile                           : High@L4
	Format settings                          : CABAC / 6 Ref Frames
	Format settings, CABAC                   : Yes
	Format settings, ReFrames                : 6 frames
	Width                                    : 1 280 pixels
	Height                                   : 720 pixels
	Display aspect ratio                     : 16:9
	Frame rate                               : 23.976 (24000/1001) FPS
	Color space                              : YUV
	Chroma subsampling                       : 4:2:0
	Bit depth                                : 8 bits
	Scan type                                : Progressive
	Writing library                          : x264 core 142 r2431+42 c69a006 tMod [8-bit@4:2:0 X86_64]
	Encoding settings                        : cabac=1 / ref=6 / deblock=1:0:-1 / analyse=0x3:0x133 / me=umh / subme=9 / psy=1 / fade_compensate=0.00 / psy_rd=1.00:0.10 / mixed_ref=1 / me_range=24 / chroma_me=1 / trellis=2 / 8x8dct=1 / cqm=0 / deadzone=21,11 / fast_pskip=0 / chroma_qp_offset=-3 / threads=84 / lookahead_threads=5 / sliced_threads=0 / nr=0 / decimate=1 / interlaced=0 / bluray_compat=0 / stitchable=1 / constrained_intra=0 / fgo=0 / bframes=5 / b_pyramid=2 / b_adapt=2 / b_bias=0 / direct=1 / weightb=1 / open_gop=0 / weightp=2 / keyint=250 / keyint_min=1 / scenecut=40 / intra_refresh=0 / rc_lookahead=70 / rc=crf / mbtree=1 / crf=23.0000 / qcomp=0.70 / qpmin=0:0:0 / qpmax=36:36:36 / qpstep=4 / vbv_maxrate=17500 / vbv_bufsize=17500 / crf_max=0.0 / nal_hrd=none / filler=0 / ip_ratio=1.40 / aq=3:0.80 / aq-sensitivity=10.00 / aq-factor=1.00:1.00:1.00 / aq2=0 / aq3=0
	```
	
* After
	```
	$ mediainfo output.h264

	General
	Complete name                            : output.h264
	Format                                   : AVC
	Format/Info                              : Advanced Video Codec
	File size                                : 103 MiB
	Writing library                          : Chigusa H264 Encoder Info Test

	Video
	Format                                   : AVC
	Format/Info                              : Advanced Video Codec
	Format profile                           : High@L4
	Format settings                          : CABAC / 6 Ref Frames
	Format settings, CABAC                   : Yes
	Format settings, ReFrames                : 6 frames
	Width                                    : 1 280 pixels
	Height                                   : 720 pixels
	Display aspect ratio                     : 16:9
	Frame rate                               : 23.976 (24000/1001) FPS
	Color space                              : YUV
	Chroma subsampling                       : 4:2:0
	Bit depth                                : 8 bits
	Scan type                                : Progressive
	Writing library                          : Chigusa H264 Encoder Info Test
	```
## Some Example

* Input h264 file, output h264 file.
	```
	python h264EncodeInfoEditor.py -i <input.h264> -o <output.h264> -s "Chigusa H264 Encoder Info Test"
	```

* Demux MP4 file to h264 stream by ffmpeg, and pipe to stdin, output h264 file.
	```
	ffmpeg -i <input.mp4> -c:v copy -an -bsf:v h264_mp4toannexb -f h264 - | python h264EncodeInfoEditor.py -i - -o <output.h264> -s "Chigusa H264 Encoder Info Test"
	```

* Input h264 file, pipe h264 stream to ffmpeg, and mux to mp4 file.

	```
	python h264EncodeInfoEditor.py -i <input.h264> -o - -s "Chigusa H264 Encoder Info Test" | ffmpeg -f h264 -i - -c:v copy <output.mp4>
	```

* Demux MP4 file to h264 stream by ffmpeg, and pipe to stdin, pipe h264 stream to ffmpeg, and mux to mp4 file.
	```
	ffmpeg -i <input.mp4> -c:v copy -an -map_metadata -1 -f h264 - | python h264EncodeInfoEditor.py -i - -o - -s "Chigusa H264 Encoder Info Test" | ffmpeg -f h264 -i - -i <input.mp4> -map 0 -map 1:a -c copy <output.mp4>
	```

## Usage

```
usage: h264EncodeInfoEditor [-h] -i INPUT -o OUTPUT -s STRING

A script to edit H.264 encoder information

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input h264 bit stream, ' - ' will read stream from
                        stdin
  -o OUTPUT, --output OUTPUT
                        output h264 bit stream, ' - ' will write stream from
                        stdout
  -s STRING, --string STRING
                        info what you want write

```