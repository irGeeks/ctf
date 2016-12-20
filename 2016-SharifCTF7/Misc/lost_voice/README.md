# Lost Voice

The flag for this challenge is devided into two parts.

Finding the first part was as easy as just listening to the voice messgae (95cd605bea9065f44530).

The second part however was a bit more challenging. After checking the file in hex viewer, I found out that it was a mp4 video. So I decomposed the video frames and compared the two of the frames. It was obvious that it's the same old stegano challenge they give every year (very creative!). So I merged all the images together to get the second part of the flag (cb13b6659dde).

### Extract the frames 
```
 ffmpeg -i LS.mp4 images/%d.png
```

### To merge them together
```
cp images/1.png part2.png
for f in `ls -v images`; do compare part2.png images/$f part2.png; done
```

