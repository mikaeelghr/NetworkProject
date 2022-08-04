import os

from werkzeug.utils import secure_filename

from config import Videos_Folder
from models import Videos
import os

ALLOWED_EXTENSIONS = {'mp4', 'mkv'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class VideoService:
    # code random, bayad avaz she
    @staticmethod
    def add(user_id, name, title, file):
        if file and allowed_file(file.filename):
            filename = secure_filename(name) + '.' + secure_filename(file.filename).split('.')[-1]
            os.makedirs(Videos_Folder + user_id, exist_ok=True)
            file.save(os.path.join(Videos_Folder + user_id, filename))
            Videos.objects.create(title=title, owner=user_id, filename=filename)

    @staticmethod
    def get_list():
        return Videos.objects.all()
