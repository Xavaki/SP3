import subprocess
import os
import sys
from ffprobe import FFProbe


class VideoManipulator():

    outdir = "output_files/"

    def choose_file(self, message="Choose input file"):

        allowed_formats = ['mp4', 'mov', 'avi', 'gif']

        print(message)
        i = 1
        files = {}
        for f in os.listdir():
            if f.split('.')[-1] in allowed_formats:
                print(f'{i} ····· {f}')
                files[i] = f
                i += 1

        if os.listdir(self.outdir):
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

    def convert_to(self, infile, outcodec):

        outfile = f'{infile.split(".")[0]}_{outcodec}.mp4'
        if self.outdir not in outfile:
            outfile = self.outdir + outfile
        if (outcodec == "vp8") or (outcodec == "vp9"):
            outfile = outfile.replace("mp4", "webm")

        commands = {
            "av1": f'ffmpeg -i {infile} -c:v libaom-av1 -c:a copy {outfile}',
            "h265": f'ffmpeg -i {infile} -c:v libx265 -c:a copy {outfile}',
            "vp8": f'ffmpeg -i {infile} -c:v libvpx -c:a libopus {outfile}',
            "vp9": f'ffmpeg -i {infile} -c:v libvpx-vp9 -c:a libopus {outfile}',
        }

        # check if file has already been converted
        if outfile.split("/")[-1] not in os.listdir("output_files") and outfile.split("/")[-1] not in os.listdir():
            subprocess.call(commands[outcodec].split(" "))
            print(f'Video outputted to {outfile}')
        else:
            print("Converted video already exists")
        
        return outfile

    def choose_codec(self, message="Choose codec"):

        print(message)
        print("1 ···· av1 (may take a long time)")
        print("2 ···· h.265")
        print("3 ···· vp8")
        print("4 ···· vp9")
        outcodecs = {"1": "av1", "2": "h265", "3": "vp8", "4": "vp9"}

        try:
            choice = input()
            outcodec = outcodecs[choice]
            return outcodec
        except:
            print("Outcodec choice error")
            exit()

    def convert_video(self):
        infile = self.choose_file()
        outcodec = self.choose_codec()
        self.convert_to(infile, outcodec)

    def codec_comparison(self):

        infile = self.choose_file("Choose input file")
        outcodec1 = self.choose_codec("Choose codec 1")
        outcodec2 = self.choose_codec("Choose codec 1")

        outfile1 = self.convert_to(infile, outcodec1)
        outfile2 = self.convert_to(infile, outcodec2)

        outfile = f'{infile.split(".")[0]}_{outcodec1}_{outcodec2}_COMPARISON.mp4'
        if self.outdir not in outfile:
            outfile = self.outdir + outfile

        command = f'ffmpeg -i {outfile1} -i {outfile2} -filter_complex hstack {outfile}'
        subprocess.call(command.split(" "))
        print(f'Video outputted to {outfile}')


    def stream_video(self):
        infile = self.choose_file("Choose video to stream at udp://127.0.0.1:23000")
        command = f'ffmpeg -i {infile} -f mpegts udp://127.0.0.1:23000'
        subprocess.call(command.split(" "))

        # to watch --> ffplay udp://127.0.0.1:23000
        # on VLC --> udp://@:23000


if __name__ == "__main__":

    if len(sys.argv) == 1:
        print("Please call any of the following functions:")
        print("··· shorten_video")
        print("··· convert_video")
        print("··· codec_comparison")
        print("··· stream_video")
        exit()

    elif len(sys.argv) == 2:
        function = sys.argv[1]
        vm = VideoManipulator()
        if function == "shorten_video":
            vm.shorten_video()
            exit()
        elif function == "convert_video":
            vm.convert_video()
            exit()
        elif function == "codec_comparison":
            vm.codec_comparison()
            exit()
        elif function == "stream_video":
            vm.stream_video()
            exit()

    print("Please call any of the following functions")
    print("··· shorten_video")
    print("··· convert_video")
    print("··· codec_comparison")
    print("··· stream_video")
    exit()
