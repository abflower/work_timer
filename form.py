from wtforms import Form, validators, StringField


class TimerForm(Form):
    time_start=StringField(
        label='Start time', default='08:00',
        validators=[validators.InputRequired()])
    time_end=StringField(
        label='Finish time', default='16:30',
        validators=[validators.InputRequired()])
