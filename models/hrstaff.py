from init import db, ma

class Hrstaff(db.Model):
    __tablename__ = 'hrstaffs'
    
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    
class HrstaffSchema(ma.Schema):
    class Meta:
        fields = ('id', 'is_admin')
    