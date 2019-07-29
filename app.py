import time
from flask import Flask, make_response, render_template, request, redirect, session, url_for
from form import TimerForm
import json

app = Flask(__name__)

def convert_time_into_min(string):
    hour_and_min = string.split(':')
    total_min = (int(hour_and_min[0])*60) + int(hour_and_min[1])
    return total_min

def return_localtime():
    localtime = time.localtime(time.time())
    return (localtime.tm_hour * 60) + localtime.tm_min


time_start = ''
time_end = ''
job_day_min = ''
slots_nr = ''

def return_result():
    if return_localtime() < convert_time_into_min(time_start):
        return (['You should not be at work!', '', '--'])
    elif return_localtime() < convert_time_into_min(time_end):
        localtime_min = return_localtime()
        completed_slots = (localtime_min-convert_time_into_min(time_start))//15
        bar = '[{}{}]'.format ('▒'*completed_slots, '░'*(slots_nr-completed_slots))
        percent = (((localtime_min-convert_time_into_min(time_start))/job_day_min)*100)
        percent = round(percent, 1)
        percent_str = 'You are at: {}%'.format(percent)
        return [bar, percent_str, percent]
    else:
        return(['Thou didst it!','',100])


@app.route('/', methods=['GET', 'POST'])
def index():
    form1 = TimerForm(request.form)

    if request.method == 'POST' and form1.validate():
        global time_start, time_end, job_day_min, slots_nr
        time_start = form1.time_start.data
        time_end = form1.time_end.data
        job_day_min = convert_time_into_min(time_end) - convert_time_into_min(time_start)
        slots_nr = job_day_min//15
        print(time_start, time_end, job_day_min, slots_nr)
        return redirect(url_for('timer'))

    return render_template('first_page.html', form=form1)

@app.route('/timer', methods=['GET', 'POST'])
def timer():
    percent = return_result()[2]
    result_graph = return_result()[0]
    result_perc = return_result()[1]
    response = make_response(render_template("index.html", percent=percent, result_graph=result_graph, result_perc=result_perc))
    return response

if __name__ == '__main__':
    app.run(port=4000, debug=True)