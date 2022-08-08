from models import Req
import datetime

class ReqService:
    @staticmethod
    def create_req(src):
        Req.objects.create(src=src, req_time=datetime.datetime.now())

    @staticmethod
    def get_user_recent_reqs(src):
        last_time = datetime.datetime.now() - datetime.timedelta(days=1)
        return len(list(Req.objects.raw({'req_time': {'$gte':last_time}})))