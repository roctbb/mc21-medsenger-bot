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

    if info or not info.get('phone') or not data.get('params', {}).get('message'):
        alert = Alert(contract_id=contract_id, name=info.get('name'), birthday=info.get('birthday'),
                             phone=info.get('phone'), message=data.get('params').get('message'))
        db.session.add(alert)
        db.session.commit()

        medsenger_api.send_message(is_urgent=True, contract_id=contract_id, only_patient=True, text="В течение нескольких минут с Вами свяжется врач контакт-центра МЦ 21 век по телефону {}.".format(info.get('phone')))
        medsenger_api.send_message(is_urgent=True, need_answer=True, contract_id=contract_id, only_doctor=True, text="Отправлен запрос в контакт центр для экстренной связи с пациентом.")
    else:
        abort(422)


# contract management api

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


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(HOST, PORT, debug=API_DEBUG)
