from flask import Flask, jsonify, request
import threading

app_8080 = Flask("node_8080")
app_8081 = Flask("node_8081")

@app_8080.route("/telemetry", methods=["GET", "POST"])
def telemetry_node():
    return jsonify({
        "status": "active",
        "port": 8080,
        "stream": "bci_rf_payload",
        "data": request.json if request.is_json else {}
    })

@app_8081.route("/settlement", methods=["GET", "POST"])
def settlement_node():
    return jsonify({
        "status": "secure",
        "port": 8081,
        "stream": "estate_capital_ledger",
        "data": request.json if request.is_json else {}
    })

def run_server(app, port):
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    t1 = threading.Thread(target=run_server, args=(app_8080, 8080))
    t2 = threading.Thread(target=run_server, args=(app_8081, 8081))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
