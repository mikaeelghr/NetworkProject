import subprocess


def generate_thumbnail(in_filename, out_filename):
    subprocess.call(['ffmpeg', '-i', in_filename, '-ss', '00:00:03.000', '-vframes', '1', out_filename])
