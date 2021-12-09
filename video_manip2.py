import subprocess
import os
import sys
from ffprobe import FFProbe
import random
import requests
from zipfile import ZipFile


class Seminar2:

    outdir = "output_files/"

    def choose_file(self, message):

        allowed_formats = ['mp4', 'mov', 'avi', 'gif']

        print(message)
        i = 1
        files = {}
        for f in os.listdir():
            if f.split('.')[-1] in allowed_formats:
                print(f'{i} ····· {f}')
                files[i] = f
                i += 1
        print("output_files/")
        for f in os.listdir(self.outdir):
            if f.split('.')[-1] in allowed_formats:
                print(f'{i} ····· {f}')
                files[i] = self.outdir + f
                i += 1

        try:
            choice = int(input())
            filename = files[choice]
            return filename
        except BaseException:
            print("Wrong input")
            exit()

    def shorten_video(self):

        infile = self.choose_file("Choose input file")
        duration = float(FFProbe(infile).streams[0].duration_seconds())
        print(
            f'How long would you like the output file to be [s]? (please consider size of input video ({duration})) ')
        n = int(input())
        if n > duration:
            print("Specified duration is longer than input video")
            exit()

        outfile = f'{infile.split(".")[0]}_{n}.mp4'
        if self.outdir not in outfile:
            outfile = self.outdir + outfile

        subprocess.call(f'ffmpeg -y -i {infile} -t {n} {outfile}'.split(" "))
        print(f'Video outputted to {outfile}')

    def macro_motion(self):

        infile = self.choose_file("Choose input file")

        outfile = f'{infile.split(".")[0]}_macromotion.mp4'
        if self.outdir not in outfile:
            outfile = self.outdir + outfile

        command = f'ffmpeg -flags2 +export_mvs -i {infile} -vf codecview=mv=pf+bf+bb {outfile}'
        subprocess.call(command.split(" "))
        print(f'Video outputted to {outfile}')

    def new_container(self):

        infile = self.choose_file("Choose input file")
        duration = float(FFProbe(infile).streams[0].duration_seconds())
        print(
            f'How long would you like the output file to be [s]? (please consider size of input video ({duration})) ')
        n = int(input())
        if n > duration:
            print("Specified duration is longer than input video")
            exit()

        outfile = f'{infile.split(".")[0]}_{n}_new_container.mp4'
        if self.outdir not in outfile:
            outfile = self.outdir + outfile

        command = f'ffmpeg -y -i {infile} -t {n} -map 0:v -c:v copy -map 0:1 -map 0:1 -c:a:0 aac -c:a:1 mp3 -b:a:0 96k {outfile}'
        subprocess.call(command.split(" "))
        print(f'Video outputted to {outfile}')

    def broadcasting_standard_test(self):

        b_standards = {
            "video": {
                "h264": ["DBV", "ISDB", "ISDB-Tb", "ATSC", "DTMB"],
                "mpeg2": ["DBV", "ISDB", "ATSC", "DTMB"],
                "avs": ["DTMB"],
                "avs+": ["DTMB"],
            },
            "audio": {
                "aac": ["DBV", "ISDB", "ISDB-Tb", "DTMB"],
                "ac-3": ["DBV", "ATSC", "DTMB"],
                "mp3": ["DBV", "DTMB"],
                "mp2": ["DTMB"],
                "dra": ["DTMB"],
            }
        }

        print("How would you like to test the function?")
        print("1 ···· by specifying an input file")
        print("2 ···· by simulating a random list of mock codecs")
        mode = input()

        if mode == "1":
            infile = self.choose_file("Choose input file")
            metadata = FFProbe(infile)
            codecs = [(stream.codec_type, stream.codec())
                      for stream in metadata.streams]
        elif mode == "2":
            codecs = [
                ("video", c) for c in random.sample(
                    list(
                        b_standards["video"].keys()), random.randint(
                        1, 4))] + [
                ("audio", c) for c in random.sample(
                    list(
                        b_standards["audio"].keys()), random.randint(
                        1, 5))]

        else:
            print("Mode choice error")
            exit()

        print("\nCodecs: ")
        for c in codecs:
            print(f'··· {c[0]} ··· {c[1]}')

        video = []
        audio = []
        for (codec_type, codec) in codecs:
            if codec_type == "video":
                for c in b_standards[codec_type][codec]:
                    if c not in video:
                        video.append(c)
            elif codec_type == "audio":
                for c in b_standards[codec_type][codec]:
                    if c not in audio:
                        audio.append(c)

        suitable_standards = [s for s in video if s in audio]

        if suitable_standards:
            print("\nSuitable broadcast standards:")
            for s in suitable_standards:
                print(s)
        else:
            print("\nERROR, no suitable standards for the specified codec set")

    def subtitles(self):

        infile = self.choose_file(
            "To which file would you like to add subtitles to?")

        if 'subs' in infile:
            print(
                "This video already contains a subtitle track, add new one anyways? [y/n]")
            x = input()
            if x == "y":
                pass
            else:
                print("Operation aborted.")
                exit()

        print("Which subtitle track would you like to add?")
        print("1 ···· BBB")
        print("2 ···· The Fellowship of the Ring")
        print("3 ···· Akira")

        subtitles = {
            "1": [
                "BBB",
                "https://www.opensubtitles.org/en/subtitleserve/sub/5833874"],
            "2": [
                "lotr1",
                "https://www.opensubtitles.org/en/subtitleserve/sub/4493239"],
            "3": [
                "akira",
                "https://www.opensubtitles.org/en/subtitleserve/sub/8683843"],
        }

        choice = input()

        if choice not in subtitles.keys():
            print("Subtitle track choice error")
            exit()

        track = subtitles[choice][0]
        link = subtitles[choice][1]

        try:
            if track not in os.listdir("downloads"):
                os.mkdir(f'downloads/{track}')
                # download zipfile
                r = requests.get(link, allow_redirects=True)
                open(f'downloads/{track}/{track}.zip', 'wb').write(r.content)
                print("Downoaded subtitles track")

                # extract zipfile contents
                with ZipFile(f'downloads/{track}/{track}.zip', 'r') as zo:
                    zo.extractall(f'downloads/{track}')
                print("Extracted track from zip file")

                # clean extracted directory
                for file in os.listdir(f'downloads/{track}'):
                    file = f'downloads/{track}/' + file
                    if file.split(".")[-1] != 'srt':
                        subprocess.call(['rm', file])
                    else:
                        subprocess.call(
                            ['mv', file, f'downloads/{track}/{track}.srt'])
                print("Cleaned subtitles directory")

            else:
                print("Subtitle track file already in repository")

        except BaseException:
            print("File download error, try with a different link")
            exit()

        # modify time stamps so that some text is actually displayed on the
        # output video
        if f'{track}_offset.srt' not in os.listdir('downloads/' + track):
            with open(f'downloads/{track}/{track}.srt') as file:
                lines = file.readlines()
                first_time_stamp = lines[1].split(" --> ")[0].split(":")
                offset = int(first_time_stamp[0]) * 3600 + int(
                    first_time_stamp[1]) * 60 + int(first_time_stamp[2].split(",")[0])

            try:
                subprocess.call(
                    f'ffmpeg -itsoffset -{offset} -y -i downloads/{track}/{track}.srt -c copy downloads/{track}/{track}_offset.srt'.split(" "))
                print("Subtitles offsetted correctly.")
            except BaseException:
                print("Offset operation failed, please try with a different link")
                exit()

        # combine input video with subtitles
        try:
            outfile = f'{infile.split(".")[0]}_{track}_subs.mp4'
            if self.outdir not in outfile:
                outfile = self.outdir + outfile
            command = f'ffmpeg -y -i {infile} -vf subtitles=downloads/{track}/{track}_offset.srt {outfile}'
            subprocess.call(command.split(" "))
            print(f'Video outputted to {outfile}')
        except BaseException:
            print(
                "Video and subtitle combination failed. Please try with a different file")
            exit()


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Please call any of the following functions:")
        print("··· shorten_video")
        print("··· macro_motion")
        print("··· new_container")
        print("··· broadcasting_standard_test")
        print("··· subtitles")
        exit()

    elif len(sys.argv) == 2:
        function = sys.argv[1]
        sem2 = Seminar2()

        if function == "shorten_video":
            sem2.shorten_video()
            exit()
        elif function == "macro_motion":
            sem2.macro_motion()
            exit()
        elif function == "new_container":
            sem2.new_container()
            exit()
        elif function == "broadcasting_standard_test":
            sem2.broadcasting_standard_test()
            exit()
        elif function == "subtitles":
            sem2.subtitles()
            exit()

    print("Please call any of the following functions")
    print("··· shorten_video")
    print("··· macro_motion")
    print("··· new_container")
    print("··· broadcasting_standard_test")
    print("··· subtitles")
    exit()
