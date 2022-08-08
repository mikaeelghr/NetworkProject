from bson import ObjectId
from pymodm.errors import DoesNotExist
from werkzeug.utils import secure_filename

from config import Videos_Folder
from models import Videos, Comment
import os

from util.thumb import generate_thumbnail

ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'webm'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class VideoService:
    @staticmethod
    def add(user_id, name, title, file):
        if file and allowed_file(file.filename):
            filename = secure_filename(name) + '.' + secure_filename(file.filename).split('.')[-1]
            thumbnail_name = secure_filename(name) + '.jpg'
            os.makedirs(Videos_Folder + user_id, exist_ok=True)
            file_path = os.path.join(Videos_Folder + user_id, filename)
            thumbnail_path = os.path.join(Videos_Folder + user_id, thumbnail_name)
            file.save(file_path)
            generate_thumbnail(file_path, thumbnail_path)
            Videos.objects.create(title=title, owner=user_id, filename=filename, thumbnail_name=thumbnail_name)
        else:
            raise Exception("invalid file type")

    @staticmethod
    def get_list():
        return Videos.objects.raw({"deleted": {"$ne": True}})

    @staticmethod
    def get(_id):
        try:
            return Videos.objects.get({"_id": ObjectId(_id)})
        except DoesNotExist:
            return None

    @staticmethod
    def add_comment(_id, user_id, message):
        video = Videos.objects.get({"_id": ObjectId(_id)})
        comment = Comment()
        comment.author = user_id
        comment.content = message
        video.comments.append(comment)
        video.save()

    @staticmethod
    def like(_id, user_id):
        video = Videos.objects.get({"_id": ObjectId(_id)})
        if user_id not in video.likes:
            video.likes.append(user_id)
        else:
            video.likes.remove(user_id)
        video.save()

    @staticmethod
    def delete(_id):
        video = Videos.objects.get({"_id": ObjectId(_id)})
        video: Videos
        user = video.owner
        user.deleted_videos += 1
        user.save()
        video.deleted = True
        video.save()

    @staticmethod
    def add_tag(_id, tag):
        video = Videos.objects.get({"_id": ObjectId(_id)})
        if tag not in video.tags:
            video.tags.append(tag)
        video.save()

    @staticmethod
    def dislike(_id, user_id):
        video = Videos.objects.get({"_id": ObjectId(_id)})
        if user_id not in video.dislikes:
            video.dislikes.append(user_id)
        else:
            video.dislikes.remove(user_id)
        video.save()
