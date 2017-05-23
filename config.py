import os
current_dir = os.path.dirname(os.path.abspath(__file__)) + os.path.sep

db = {
    "host": "localhost",
    "database": "mobile",
    "user": "postgres",
    "password": "postgres"
}
port = 8080

config = {
  'global' : {
    'server.socket_host' : '127.0.0.1',
    'server.socket_port' : 8080,
    'server.thread_pool' : 8,
    'server.environment' : "production",
    'engine.autoreload_on' : True,
    'engine.autoreload_frequency' : 60
  },
      '/':{
  'tools.staticdir.root' : current_dir
    },
    '/static':{
    'tools.staticdir.on' : True,
    'tools.staticdir.dir': 'static',
    },
}

