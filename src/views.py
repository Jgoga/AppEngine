from datetime import datetime
import os

from google.appengine.ext import db
import jinja2 
from models import Aviso
from models import Operacion
import webapp2
import urllib2
import json
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))
    
class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))


class MainPage(BaseHandler):
    def get(self):
        self.render_template('index.html', {})

class ShowAvisos(BaseHandler):
    def get(self):
        avisos = Aviso.all().order('date')
        self.render_template('avisos_index.html', {'avisos': avisos})

class ShowAviso(BaseHandler):
    def get(self, aviso_id):
        iden = int(aviso_id)
        aviso = db.get(db.Key.from_path('Aviso', iden))       
        address = "%s, %s ,%s"% (aviso.cod_postal,aviso.calle,aviso.numero)
        
        # HACER LA PETICION A LA API DE FLICKR
        url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&format=json&api_key=1002d4db6914f828ee4b6641b321b489&tags="+aviso.tag
        respuesta = urllib2.urlopen(url).read()[14:-1]
        respuesta = json.loads(respuesta)
        respuesta = respuesta["photos"]["photo"]
        self.render_template('show_aviso.html', {'aviso': aviso, 'address':address, 'respuesta':respuesta})

class CreateAviso(BaseHandler):
    def post(self):
        aviso = Aviso(calle = self.request.get('inputStreet'),
                      numero = self.request.get('inputNumber'),
                      cod_postal = self.request.get('inputZip'),
                      email = self.request.get('inputEmail'),
                      descripcion = self.request.get('inputDescription'),
                      tag = self.request.get('inputTag')
                      )
        aviso.put()
        return webapp2.redirect('/')
    def get(self):
        self.render_template('create.html', {})
        
class EditAviso(BaseHandler):
    def post(self, aviso_id):
        iden = int(aviso_id)
        aviso = db.get(db.Key.from_path('Aviso',iden))
        aviso.calle = self.request.get('inputStreet')
        aviso.numero = self.request.get('inputNumber')
        aviso.cod_postal = self.request.get('inputZip')
        aviso.email = self.request.get('inputEmail')
        aviso.descripcion = self.request.get('inputDescription')
        aviso.tag = self.request.get('inputTag')
        aviso.date = datetime.now()
        aviso.put()
        return webapp2.redirect('/')
        
    def get(self, aviso_id):
        iden = int(aviso_id)
        aviso = db.get(db.Key.from_path('Aviso', iden))
        self.render_template('edit.html', {'aviso' : aviso})
        


class DeleteAviso(BaseHandler):
    def get(self, aviso_id):
        iden = int(aviso_id)
        aviso = db.get(db.Key.from_path('Aviso',iden))
        db.delete(aviso)
        return webapp2.redirect('/')


class CreateOperacion(BaseHandler):
    def post(self, aviso_id):
        iden = int(aviso_id)
        aviso = db.get(db.Key.from_path('Aviso',iden))
        date_object = datetime.strptime(self.request.get('inputFecha')+" "+self.request.get('inputHora'), '%d-%m-%Y %I:%M%p')

        operacion = Operacion(descripcion = self.request.get('inputDescription'),
                                date = date_object,
                                aviso = aviso
                     )
        operacion.put() 
        return webapp2.redirect('/listOperaciones/'+aviso_id)
        
    def get(self, aviso_id):
        iden = int(aviso_id)
        self.render_template('createOperacion.html', {})


class ShowOperaciones(BaseHandler):
    def get(self,aviso_id):
        iden = int(aviso_id)
        aviso = db.get(db.Key.from_path('Aviso',iden))
        operaciones = Operacion.all().filter('aviso =', aviso)
        self.render_template('operaciones_index.html', {'operaciones': operaciones})
        
class EditOperacion(BaseHandler):
    def post(self, operacion_id):
        iden = int(operacion_id)
        operacion = db.get(db.Key.from_path('Operacion',iden))
        aviso_id = str(operacion.aviso.key().id_or_name())
        operacion.descripcion = self.request.get('inputDescription')
        date_object = datetime.strptime(self.request.get('inputFecha')+" "+self.request.get('inputHora'), '%d-%m-%Y %I:%M%p')
        operacion.date = date_object
        operacion.put()
        return webapp2.redirect('/listOperaciones/'+aviso_id)
        
    def get(self, operacion_id):
        iden = int(operacion_id)
        operacion = db.get(db.Key.from_path('Operacion', iden))
        descripcion = operacion.descripcion
        fecha = operacion.date.strftime("%d-%m-%Y")
        hora = operacion.date.strftime("%I:%M%p")
        self.render_template('editOperacion.html', {'descripcion' : descripcion, 'fecha':fecha, 'hora':hora})
        


class DeleteOperacion(BaseHandler):
    def get(self, operacion_id):
        iden = int(operacion_id)
        operacion = db.get(db.Key.from_path('Operacion',iden))
        aviso_id = str(operacion.aviso.key().id_or_name())
        db.delete(operacion)
        return webapp2.redirect('/listOperaciones/'+aviso_id)