from flask import jsonify
from manage import *
from medsenger_api import AgentApiClient
from helpers import *
from models import *

medsenger_api = AgentApiClient(API_KEY, MAIN_HOST, AGENT_ID, API_DEBUG)

@app.route('/')
def index():
    return "Waiting for the thunder"


@app.route('/status', methods=['POST'])
@verify_json
def status(data):
    answer = {
        "is_tracking_data": False,
        "supported_scenarios": [],
        "tracked_contracts": []
    }

    return jsonify(answer)


@app.route('/order', methods=['POST'])
@verify_json
def order(data):
    print(data)
    contract_id = int(data.get('contract_id'))
    info = medsenger_api.get_patient_info(contract_id)

    if info and info.get('phone') and data.get('params', {}).get('message'):
        alert = Alert(contract_id=contract_id, name=info.get('name'), birthday=info.get('birthday'),
                             phone=info.get('phone'), message=data.get('params').get('message'))
        db.session.add(alert)
        db.session.commit()

        medsenger_api.send_message(is_urgent=True, contract_id=contract_id, only_patient=True, text="В течение нескольких минут с Вами свяжется врач контакт-центра МЦ 21 век по телефону {}.".format(info.get('phone')))
        medsenger_api.send_message(is_urgent=True, need_answer=True, contract_id=contract_id, only_doctor=True, text="Отправлен запрос в контакт центр для экстренной связи с пациентом.")
    else:
        abort(422)



@app.route('/init', methods=['POST'])
@verify_json
def init(data):
    return "ok"



@app.route('/remove', methods=['POST'])
@verify_json
def remove(data):
    return "ok"



# settings and views
@app.route('/settings', methods=['GET'])
@verify_args
def get_settings(args, form):
    return "Этот интеллектуальный агент не требует настройки"


@app.route('/api/alert', methods=['GET'])
@safe
def get_alert():
    key = request.args.get('key')

    workstation = Workstation.query.filter_by(access_key=key).first()

    if not workstation:
        abort(403)

    alerts = Alert.query.filter_by(sent_on=None).all()
    if not alerts:
        return jsonify({"state": "no alerts"})

    alert = alerts[0]
    alert.workstation_id = workstation.id
    alert.sent_on = datetime.now()

    db.session.commit()

    return jsonify({
        "state": "alert",
        "count": len(alerts),
        "alert": alert.as_dict()
    })

@app.route('/api/alert', methods=['POST'])
@safe
def process_alert():
    key = request.args.get('key')
    workstation = Workstation.query.filter_by(access_key=key).first()
    if not workstation:
        abort(403)

    data = request.json

    alert = Alert.query.filter_by(id=data.get('id')).first()

    if not alert:
        abort(404)

    if not data.get('result'):
        abort(422)

    alert.result = data.get('result')
    alert.comment = data.get('comment')
    alert.done_on = datetime.now()
    db.session.commit()

    message = f"<strong>Результат запроса в КЦ:</strong> {alert.result}"
    if alert.comment:
        message += f"<br><br><strong>Комментарий:</strong> {alert.comment}"

    medsenger_api.send_message(is_urgent=True, need_answer=True, contract_id=alert.contract_id, only_doctor=True,
                               text=message)

    return jsonify({
        "state": "done"
    })


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(HOST, PORT, debug=API_DEBUG)
