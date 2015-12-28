from optparse import OptionParser
from pymediainfo import MediaInfo
import subprocess
import os
import ntpath

parser = OptionParser()
parser.add_option("-i", "--input_dir", dest="input_dir", help="Input dir with mkv files to be encoded", metavar="FILE")
parser.add_option("-o", "--output_dir", dest="output_dir", help="Output dir for encoded video", metavar="FILE", default=".")

(options, args) = parser.parse_args()

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

def change_ext(filename, new_ext):
    return os.path.splitext(filename)[0]+new_ext

def encode_video(filename, output_dir):
    media_info = MediaInfo.parse(filename)

    for track in media_info.tracks:
        if track.track_type == 'Video':
            height = track.height
            width = track.width


    print "%s dimensions are %sx%s" % (filename, height, width)
    basename=path_leaf(filename)
    print("Filename is %s" % (basename))
    output_file=os.path.join(output_dir, change_ext(basename, ".mp4"))


    subprocess.call(["HandBrakeCLI",
                    "-N", "eng",
                    "-l", str(height),
                    "-w", str(width),
                    "-o", str(output_file),
                    "-i", str(filename),
                    "-e", "x264",
                    "-q", "20",
                    "--crop", "0:0:0:0",
                    "--loose-anamorphic",
                    "-O"])

output_dir_files = []

for filename in os.listdir(options.output_dir):
    if filename.endswith(".mp4"):
        output_dir_files.append(filename)

for filename in os.listdir(options.input_dir):
    if filename.endswith(".mkv"):
        if change_ext(filename, ".mp4") not in output_dir_files:
            print("Haven't yet encoded %s so doing so now" % (filename))
            encode_video(os.path.join(options.input_dir,filename), options.output_dir)