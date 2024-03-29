import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    TASKTYPES = ['Meeting', 'Investigation/Organization', 'Chat/Tell/Talk', 'Admin', 'Output/Documentation',
                 '1on1', 'Preparation', 'MailCheck']
