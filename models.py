from pymodm import MongoModel, fields, EmbeddedMongoModel, ReferenceField


class User(MongoModel):
    username = fields.CharField(primary_key=True)
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
