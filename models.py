from pymodm import MongoModel, fields, EmbeddedMongoModel, ReferenceField
import pymongo


class User(MongoModel):
    username = fields.CharField()
    role = fields.CharField(choices=('USER', 'STAFF', "ADMIN"))
    firstname = fields.CharField(max_length=30)
    lastname = fields.CharField(max_length=30)
    blocked = fields.BooleanField(default=False)
    password = fields.CharField()

    class Meta:
        indexes = [pymongo.IndexModel([('username', pymongo.ASCENDING)], unique=True)]


# feel free to change these models

class Comment(EmbeddedMongoModel):
    author = fields.ReferenceField(User, on_delete=ReferenceField.CASCADE)
    content = fields.CharField()


class Videos(MongoModel):
    title = fields.CharField()
    owner = fields.ReferenceField(User, on_delete=ReferenceField.CASCADE)
    revised_on = fields.DateTimeField()
    filename = fields.CharField()
    description = fields.CharField()
    comments = fields.EmbeddedDocumentListField(Comment)


class Ticket(MongoModel):
    user = fields.ReferenceField(User, on_delete=ReferenceField.CASCADE)
    messages = fields.ListField()
    state = fields.CharField(choices=('NEW', 'WAITING', 'SOLVED', 'CLOSED'))
    assignee_user_id = fields.ReferenceField(User, on_delete=ReferenceField.CASCADE)
