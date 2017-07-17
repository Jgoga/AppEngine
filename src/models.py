from google.appengine.ext import db

class Aviso(db.Model):
    calle = db.StringProperty()
    numero = db.StringProperty()
    cod_postal = db.StringProperty()
    email = db.StringProperty()
    descripcion = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    tag = db.StringProperty()
    
class Operacion(db.Model):
    aviso = db.ReferenceProperty(Aviso)
    descripcion = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
