import uuid
import datetime

from common.database import Database



class Post(object):

    def __init__(self, author, blog_id, title, content, date=datetime.datetime.utcnow(), _id=None):
        self.author = author
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.date = date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection="posts", data=self.json())

    def json(self):
        return {
            "author": self.author,
            "blog_id": self.blog_id,
            "title": self.title,
            "content": self.content,
            "date": self.date,
            "_id": self._id,
        }

    @classmethod
    def from_mongo(cls, id):
        post = Database.find_one('posts', {'id': id})
        return cls(**post)

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find('posts', {"blog_id": id})]

    @staticmethod
    def from_date(date):
        return [post for post in Database.find('posts', {"date": date})]


