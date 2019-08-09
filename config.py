import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    TASKTYPES = ['Meeting', 'Investigation', 'Communication', 'Admin', 'Training',
                 'Onsite', 'Knowledge Sharing', 'Lab', 'Design', 'Preparation']
