from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property
from app import app


class User(BaseModel):
    username = pw.CharField(unique=True, null=False)
    email = pw.CharField(unique = True, null =False)
    password = pw.CharField(unique=False,null = False)
    profilepic = pw.CharField(null=True)
    bio = pw.CharField(null=True, max_length=600)

    @hybrid_property
    def profilepic_url(self):
        return f"{app.config['S3_LOCATION']}{self.profilepic}"
    
    
