from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property
from app import app
from models.user import User


class Picture(BaseModel):
    name = pw.CharField(unique=False, null=True)
    category = pw.CharField(unique = False, null =False)
    description = pw.CharField(unique=False,null = True)
    image = pw.CharField(unique = False,null = True)
    price =pw.CharField(default=0)
    artist_id = pw.ForeignKeyField(User, backref="artists", null =True)
    bidder_id = pw.ForeignKeyField(User, backref="bidders", null =True)
    buyer_id = pw.ForeignKeyField(User, backref="buyers", null =True)
    sold = pw.BooleanField(default=False)

    @hybrid_property
    def profilepic_url(self):
        return f"{app.config['S3_LOCATION']}{self.image}"
