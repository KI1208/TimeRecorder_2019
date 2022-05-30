from flask import render_template, request, redirect, url_for, flash
from app import app, db
from app.models import Project, TimeRecord
from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
from config import Config

from dashapp import dashapp
from dashappq import dashapp

JST = timezone(timedelta(hours=+9), 'JST')
TASKTYPES = Config.TASKTYPES


@app.route('/', methods=['GET'])
def toppage():
    if request.args.get('date') is not None:
        requesteddate = parse(request.args.get('date')).date()
    else:
        requesteddate = datetime.now(JST).date()

    # Retrieve project list
    existingprojects = [project for project in Project.query.filter_by(projectstatus=True)]
    today_record = [record for record in TimeRecord.query.filter(TimeRecord.starttime > requesteddate,
                                                                 TimeRecord.starttime < requesteddate + timedelta(
                                                                     1)).order_by(TimeRecord.starttime).all()]

    # today_recordはTimeRecordクラスで、projectnameがない、かつキーの追加もできないので、別のdictに移す
    timerecords = []
    for record in today_record:
        timerecords.append({'projectname': Project.query.filter_by(projectid=record.projectid).first().projectname,
                            'tasktype': record.tasktype,
                            'starttime': record.starttime.time(),
                            'endtime': record.endtime.time(), # 11:00:00
                            'hours': record.minutes/60.0
                            })

    # その日の一番最後の終了時刻を取得しておく(10時 -> 600のような変換が必要)
    try:
        parsed_lasttime = timerecords[-1]['endtime']
        lasttime = parsed_lasttime.hour * 60 + parsed_lasttime.minute
    except IndexError as e:
        lasttime = 600

    return render_template('toppage.html', date=requesteddate, tasktypes=TASKTYPES, projects=existingprojects,
                           timerecords=timerecords, lasttime=lasttime)


@app.route('/changedate', methods=['POST', 'GET'])
def change_date():
    requestdata = request.values
    date = requestdata['date']

    return redirect(url_for('toppage', date=date))


@app.route('/projects', methods=['GET', 'POST'])
def projects():
    existingprojects = [project for project in Project.query.all()]
    # existingprojects = [project for project in Project.query.order_by(Project.projectstatus.desc(), Project.id).all()]
    # sorted_existingprojects = sorted(existingprojects, key=lambda x: (x['id'], x['projectstatus']))

    return render_template('projects.html', projects=existingprojects)


@app.route('/add_project', methods=['POST'])
def add_project():
    requestdata = request.values
    existingprojectids = [project.projectid for project in Project.query.all()]
    if requestdata['projectid'] in existingprojectids:
        flash('This project id is already registerd.')
    else:
        project = Project(projectid=requestdata['projectid'],
                          projectname=requestdata['projectname'],
                          projectdesc=requestdata['projectdesc'],
                          projecthours=requestdata['projecthours'],
                          projectstatus=True if requestdata['projectstatus'] == 'active' else False)
        db.session.add(project)
        db.session.commit()
        flash('Project Added.')

    return redirect(url_for('projects'))


@app.route('/update_project', methods=['POST'])
def update_project():
    requestdata = request.values
    projectname = requestdata.getlist('projectname[]')
    projectid = requestdata.getlist('projectid[]')
    projectdesc = requestdata.getlist('projectdesc[]')
    projecthours = requestdata.getlist('projecthours[]')
    projectstatus = requestdata.getlist('projectstatus[]')
    projectstatus2 = requestdata.getlist('projectstatus2[]')
    ids = requestdata.getlist('id[]')
    # flash(projectname)
    # flash(ids)
    # flash(projectstatus)
    # flash(projectstatus2)

    for id in [int(id) - 1 for id in ids]:
        project = Project.query.filter_by(id=id + 1).first()
        expected_projectstatus = projectstatus_changer(projectstatus2[id])
        changed = 'no'
        if projectname[id] != '':
            project.projectname = projectname[id]
            changed = 'yes'
        if projectid[id] != '':
            project.projectid = projectid[id]
            changed = 'yes'
        if projectdesc[id] != '':
            project.projectdesc = projectdesc[id]
            changed = 'yes'
        if projecthours[id] != '':
            project.projecthours = projecthours[id]
            changed = 'yes'
        if expected_projectstatus != project.projectstatus:
            project.projectstatus = expected_projectstatus
            changed = 'yes'
        if changed == 'yes':
            db.session.add(project)
            db.session.commit()
            flash(f'{projectname[id]} Updated.')

    return redirect(url_for('projects'))


@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    requestdata = request.values
    # Adjust for culumn
    starttime = parse(requestdata['date'] + 'T' + requestdata['starttime'])
    endtime = parse(requestdata['date'] + 'T' + requestdata['endtime'])
    diff = endtime - starttime
    projectid = Project.query.filter_by(projectname=requestdata['projectname']).first().projectid

    timerecord = TimeRecord(projectid=projectid,
                            tasktype=requestdata['tasktype'],
                            starttime=starttime,
                            endtime=endtime,
                            minutes=diff.seconds // 60
                            )
    db.session.add(timerecord)
    # db.session.commit()
    flash('Time Record Added.')

    # Update Project Consumed Hours
    project = Project.query.filter_by(projectid=projectid).first()
    if project.projectcomsumedhours is None:
        current_time = 0
    else:
        current_time = project.projectcomsumedhours

    project.projectcomsumedhours = diff.seconds // 3600 + current_time
    db.session.add(project)
    db.session.commit()
    flash(f'{projectid} Updated.')

    return redirect(url_for('toppage', date=requestdata['date']))


@app.route('/update_record', methods=['GET', 'POST'])
def update_record():
    return redirect(url_for('toppage'))


@app.route("/dummy")
def dummy():
    return dashapp.index()


@app.route('/weekly_report', methods=['GET', 'POST'])
def weekly_report():
    return render_template('report.html')


@app.route('/quarterly_report', methods=['GET', 'POST'])
def quarterly_report():
    return render_template('quarterly_report.html')


def projectstatus_changer(status):
    if status == 'active':
        return True
    else:
        return False
