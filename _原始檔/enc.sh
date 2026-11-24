#!/bin/zsh
# 用法：enc.sh <區塊> <格率>：secframes → GIF（600 寬、10fps、160 色 bayer）＋ MP4（1080 寬）
W=/private/tmp/claude-501/-Users-ningchang--claude-spares-spare-83sWsf/8be7a878-1d74-40b6-a934-3282ef5f9fed/scratchpad/work/gif
cd $W; s=$1; f=${2:-15}; mkdir -p enc
ffmpeg -v error -y -framerate $f -i secframes/$s/%03d.png -vf "crop=iw:ih-4:0:0,fps=10,scale=600:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=160[p];[b][p]paletteuse=dither=bayer:bayer_scale=3" enc/$s.gif
ffmpeg -v error -y -framerate $f -i secframes/$s/%03d.png -vf "crop=iw:ih-4:0:0,scale=1080:-2:flags=lanczos,format=yuv420p" -c:v libx264 -crf 20 -movflags +faststart enc/$s.mp4
echo $s $(stat -f %z enc/$s.gif) $(stat -f %z enc/$s.mp4)
