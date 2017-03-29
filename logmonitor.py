import cgi
import datetime
import webapp2
import uuid
import os
import jinja2

from google.appengine.ext import ndb
from google.appengine.api import users

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


class Project(ndb.Model):
  author    = ndb.UserProperty()
  title     = ndb.StringProperty()
  created   = ndb.DateTimeProperty(auto_now_add=True)
  completed = ndb.BooleanProperty(default=False)
  uuid      = ndb.StringProperty()
  password  = ndb.StringProperty()
  


class Entry(ndb.Model):
  project    = ndb.KeyProperty(kind=Project)
  created    = ndb.DateTimeProperty(auto_now_add=True)
  entry_type = ndb.StringProperty(choices=['info','success','fail','warning'])
  message    = ndb.StringProperty()




def create_project(title,password=''):
  p = Project()
  p.author = users.get_current_user()
  p.title = title
  p.password = password
  p.uuid = str(uuid.uuid4())
  return p.put()

def project_from_uuid(uuid,password=''):
  query = Project.query().filter(ndb.AND(Project.uuid == uuid))
  projects = query.fetch(1)
  return projects[0]

def my_projects():
  query = Project.query().filter(Project.author==users.get_current_user())
  projects = query.fetch()
  return projects


def create_entry(uuid,password,entry_type,message):
  project = project_from_uuid(uuid,password)  
  e = Entry()
  e.project = project.key
  e.entry_type = entry_type
  e.message = message
  return e.put()


def list_entries(project):
  return Entry.query().filter(Entry.project==project.key).order(-Entry.created).fetch()

def complete_project(uuid):
  query = Project.query().filter(ndb.AND(Project.uuid == uuid,  Project.completed==False))
  projects = query.fetch(1)
  p = projects[0]
  p.completed = True
  p.put()

def default_jinja_params():
  return { 'login' : users.create_login_url('/'), 'logout': users.create_logout_url('/') }


def is_logged_in():
  user = users.get_current_user()
  return user


class ListProjects(webapp2.RequestHandler):
  def get(self):
    if is_logged_in():
      t = jinja_env.get_template('listprojects.html')
      params = default_jinja_params()
      params['projects'] = my_projects()
      self.response.out.write(t.render(params))
    else:
      self.redirect(users.create_login_url('/'))

class ShowProject(webapp2.RequestHandler):
  def get(self):
    if is_logged_in():
      if self.request.get('project'):
        t = jinja_env.get_template('showproject.html')
        params = default_jinja_params()
        project = project_from_uuid(self.request.get('project'))
        params['project'] = project
        params['entries'] = list_entries(project)
        self.response.out.write(t.render(params))
      else:
        self.error(404)
        self.response.out.write('<Your 404 error html page>')        
    else:
      self.redirect(users.create_login_url('/'))


class RssProject(webapp2.RequestHandler):
  def get(self):
    if is_logged_in():
      if self.request.get('project'):
        t = jinja_env.get_template('rss.html')
        params = default_jinja_params()
        project = project_from_uuid(self.request.get('project'))
        params['project'] = project
        params['entries'] = list_entries(project)
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.out.write(t.render(params))
      else:
        self.error(404)
        self.response.out.write('<Your 404 error html page>')        
    else:
      self.redirect(users.create_login_url('/'))


class CompleteProject(webapp2.RequestHandler):
  def post(self):
    if is_logged_in():
      if self.request.get('project'):            
        complete_project(self.request.get('project'))    
        self.redirect('/')
      else:
        self.error(404)
        self.response.out.write('<Your 404 error html page>')        
    else:
      self.redirect(users.create_login_url('/'))

class CreateProject(webapp2.RequestHandler):
  def post(self):
    if is_logged_in():
      if self.request.get('title'):
        create_project(self.request.get('title'),self.request.get('password'))        
        self.redirect('/')
      else:
        self.error(404)
        self.response.out.write('<Your 404 error html page>')        
    else:
      self.redirect(users.create_login_url('/'))


class CreateEntry(webapp2.RequestHandler):
  def post(self):    
    if self.request.get('project') and self.request.get('message') and self.request.get('entry_type'):
      try:
        create_entry(self.request.get('project'),self.request.get('password'),self.request.get('entry_type'),self.request.get('message'))            
        self.redirect('/')
      except Exception as inst:
        self.response.out.write(inst)   
    else:
      self.error(404)
      self.response.out.write('<Your 404 error html page>')        
  



app = webapp2.WSGIApplication([
  ('/', ListProjects),
  ('/project/show', ShowProject),
  ('/project/rss', RssProject),
  ('/project/create', CreateProject),  
  ('/project/complete', CompleteProject),
  ('/entry/create', CreateEntry)
  
], debug=True)


