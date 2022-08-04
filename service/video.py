import os

from werkzeug.utils import secure_filename

from config import Videos_Folder
from models import Videos

ALLOWED_EXTENSIONS = {'mp4', 'mkv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class VideoService:
    # code random, bayad avaz she
    @staticmethod
    def add(username, file):
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(Videos_Folder + username, filename))

    @staticmethod
    def get_list():
        return Videos.objects.all()
