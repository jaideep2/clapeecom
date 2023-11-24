# clapeecom
Testing Vid2Vid

## To automate

1. ffmpeg convert mp4 to png

    ```bash
    docker exec -it ffmpeg-api ffmpeg -y -hwaccel cuvid -c:v h264_cuvid -resize 576x1024 -i /output/Dancing.mp4 -vf "scale_npp=format=yuv420p,hwdownload,format=yuv420p" -pix_fmt yuvj420p -color_range 2 /output/vid2vid_darkSushiMixMix_colorful_input/frame_%03d.png
    ```

2. Copy pngs to comfy

    ```bash
    cp -r workspace/ffmpeg/vid2vid_darkSushiMixMix_colorful_input workspace/ComfyUI/input/vid2vid_darkSushiMixMix_colorful_input
    ```

3. RUN COMFYUI WORKFLOW

4. Copy pngs back to ffmpeg
    
    ```bash
    cp -r workspace/ComfyUI/output/vid2vid_darkSushiMixMix_colorful workspace/ffmpeg/vid2vid_darkSushiMixMix_colorful_output
    ```

5. Convert png to jpg

    ```bash
    docker exec -it ffmpeg-api /bin/bash -c 'for image in /output/vid2vid_darkSushiMixMix_colorful_output/*.png; do ffmpeg -loglevel error -i "$image" "${image%.png}.jpg"; rm "$image"; echo "image $image converted to ${image%.png}.jpg "; done'
    ```

6. Convert to final mp4

    ```bash
    # h264_nvenc
    docker exec -it ffmpeg-api ffmpeg -y -loglevel error -i '/output/vid2vid_darkSushiMixMix_colorful_output/frame_%03d.jpg' -c:v h264_nvenc -preset fast -fps_mode passthrough /output/vid2vid_darkSushiMixMix_colorful_output/final.mp4
    # hevc_nvenc
    docker exec -it ffmpeg-api ffmpeg -y -loglevel error -i '/output/vid2vid_darkSushiMixMix_colorful_output/frame_%03d.jpg' -r 30 -c:v hevc_nvenc -pix_fmt yuv420p -preset fast /output/vid2vid_darkSushiMixMix_colorful_output/final2.mp4
    ```