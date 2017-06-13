import uuid
from models.post import Post
import datetime
from common.database import Database

class Blog(object):
    def __init__(self, author, title, description, author_id, _id=None):
        self.author = author
        self.title = title
        self.description = description
        self.author_id = author_id
        self._id = uuid.uuid4().hex if _id is None else _id



    def new_post(self, title, content, date=datetime.datetime.utcnow()):
        post = Post(blog_id=self._id,
                    title=title,
                    content=content,
                    author=self.author,
                    date = date)
        post.save_to_mongo()

    def get_posts(self):
        return Post.from_blog(self._id)

    def save_to_mongo(self):
        Database.insert(collection='blogs', data = self.json())

    def json(self):
        return {
            "author" : self.author,
            "title" : self.title,
            "description" : self.description,
            "author_id" : self.author_id,
            "_id" : self._id
        }

    @classmethod
    def get_from_mongo(cls, id):
        blog = Database.find_one(collection='blogs',
                                 query={'_id': id})
        return cls(author=blog["author"],
                   title=blog["title"],
                   description=blog["description"],
                   author_id=blog["author_id"],
                   _id=blog["_id"])

    @classmethod
    def find_by_author_id(cls, author_id):
        blogs = Database.find(collection='blogs',
                              query={'author_id': author_id})
        return [cls(**blog) for blog in blogs]





