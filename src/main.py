from views import MainPage, ShowAvisos,ShowAviso, CreateAviso, DeleteAviso, EditAviso, CreateOperacion, ShowOperaciones, DeleteOperacion, EditOperacion
import webapp2


app = webapp2.WSGIApplication([
        ('/', ShowAvisos),
        ('/show/([\d]+)', ShowAviso), 
        ('/create', CreateAviso), 
        ('/edit/([\d]+)', EditAviso),
        ('/delete/([\d]+)', DeleteAviso),
        ('/createOperacion/([\d]+)', CreateOperacion),
        ('/listOperaciones/([\d]+)', ShowOperaciones),
        ('/deleteOperacion/([\d]+)', DeleteOperacion),
        ('/editOperacion/([\d]+)', EditOperacion)
        ],
        debug=True)
