from pymodm import MongoModel, fields, EmbeddedMongoModel, ReferenceField


class User(MongoModel):
    id = fields.CharField(primary_key=True)
    username = fields.CharField()
    role = fields.CharField(choices=('USER', 'STAFF', "ADMIN"))
    first_name = fields.CharField(max_length=30)
    last_name = fields.CharField(max_length=30)
    blocked = fields.BooleanField(default=False)
    password = fields.CharField()


# feel free to change these models

class Comment(EmbeddedMongoModel):
    author = fields.ReferenceField(User, on_delete=ReferenceField.CASCADE)
    content = fields.CharField()


class StreamVideo(MongoModel):
    title = fields.CharField()
    owner = fields.ReferenceField(User, on_delete=ReferenceField.CASCADE)
    revised_on = fields.DateTimeField()
    resourceId = fields.CharField()
    description = fields.CharField()
    comments = fields.EmbeddedDocumentListField(Comment)


class Ticket(MongoModel):
    user = fields.ReferenceField(User, on_delete=ReferenceField.CASCADE)
    messages = fields.ListField()
    state = fields.CharField(choices=('NEW', 'WAITING', 'SOLVED', 'CLOSED'))
