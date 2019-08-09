from app import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectid = db.Column(db.String(64), index=True, unique=True)
    projectname = db.Column(db.String(120), index=True, unique=True)
    projectdesc = db.Column(db.String(120))
    projectstatus = db.Column(db.Boolean)
    projecthours = db.Column(db.Integer)
    projectcomsumedhours = db.Column(db.Integer)

    # この関数は、インタープリタ(コンソール)からこのクラス(からできたインスタンス)を呼んだ際に、
    # どのように表示されるかを定義している。ここではusernameを表示させている。
    def __repr__(self):
        return '<Projectid {}>'.format(self.projectid)


class TimeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectid = db.Column(db.String(64), index=True, unique=False)
    tasktype = db.Column(db.String(64), index=True, unique=False)
    starttime = db.Column(db.DateTime(timezone=False))
    endtime = db.Column(db.DateTime(timezone=False))
    minutes = db.Column(db.Integer)

    # この関数は、インタープリタ(コンソール)からこのクラス(からできたインスタンス)を呼んだ際に、
    # どのように表示されるかを定義している。ここではusernameを表示させている。
    def __repr__(self):
        return '<StartTime {}>'.format(self.starttime)