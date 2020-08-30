from os import system
import json
import glob
import argparse


class Video:  # Video Model
    url = str()
    cuts = list()

    def __init__(self, url: str, cuts: list):
        self.url = url
        self.cuts = cuts


def download_video(index: int, url: str):
    system(f"youtube-dl '{url}' -o 'sources/source_{index}'")


def cut_video(video_index: int, seconds_info: str):
    VIDEO_CNT = len(seconds_info)
    SOURCE_FILE_NAME = glob.glob(f'./sources/source_{video_index}*')[0]

    for i in range(0, VIDEO_CNT):
        start, end = seconds_info[i].split('-')
        system(
            f"ffmpeg -ss 00:{start} -to 00:{end} -i '{SOURCE_FILE_NAME}' 'outputs/{video_index}_{i}.{SOURCE_FILE_NAME.split('.')[-1]}' &"
        )


def info_reader(info: str) -> list():
    obj = json.loads(info)
    return [Video(video['url'], video['cuts']) for video in obj["clips"]]


def main():
    parser = argparse.ArgumentParser(
        description=
        'Download youtube videos, and cut them by scenes with given information.'
    )
    parser.add_argument('filename',
                        metavar='FILENAME',
                        type=str,
                        help='The file name of the video information file.')
    args = parser.parse_args()
    info_file = open(args.filename, 'r')
    videos = info_reader(info_file.read())
    info_file.close()

    VIDEO_CNT = len(videos)
    for i in range(0, VIDEO_CNT):  # this can be asynchronously
        print(f"{i+1}/{VIDEO_CNT}: {videos[i].url}")
        download_video(i, videos[i].url)
        print("Video downloaded.")
        cut_video(i, videos[i].cuts)

    print("Done!")


main()