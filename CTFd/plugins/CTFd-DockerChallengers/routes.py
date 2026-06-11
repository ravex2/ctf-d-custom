from flask import jsonify

def register_routes(bp):

    @bp.route("/api/dynamic_docker/ping", methods=["GET"])
    def ping():
        return jsonify({
            "status": "ok",
            "message": "dynamic_docker plugin funcionando"
        })