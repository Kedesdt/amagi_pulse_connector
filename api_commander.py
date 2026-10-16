import threading

from flask import Flask, jsonify, render_template, request


class ApiCommander(threading.Thread):
	def __init__(self, host="0.0.0.0", port=5000, callback=None, set_active=None, get_active=None):
		super().__init__(daemon=True)
		self.callback = callback
		self.host = host
		self.port = port
		self.set_active = set_active
		self.get_active = get_active
		self.pulse_filter = None
		self.app = Flask(__name__)
		self.app.add_url_rule("/", "status_page", self.status_page, methods=["GET"])
		self.app.add_url_rule("/action", "action", self.action, methods=["POST"])
		self.app.add_url_rule("/set_active", "set_active", self.set_active_route, methods=["POST"])
		self.app.add_url_rule("/get_active", "get_active", self.get_active_route, methods=["GET"])
		self.app.add_url_rule("/get_pulse_filter", "get_pulse_filter", self.get_pulse_filter_route, methods=["GET"])
		self.app.add_url_rule("/set_pulse_filter", "set_pulse_filter", self.set_pulse_filter_route, methods=["POST"])

	def set_pulse_filter_route(self):
		data = request.get_json(silent=True) or {}
		if "filters" not in data:
			return jsonify({"status": "error", "message": "Missing 'filters' parameter"}), 400
		if not self.pulse_filter:
			return jsonify({"status": "error", "message": "Pulse filter not set"}), 400

		try:
			filters = self.update_pulse_filters(data["filters"])
			return jsonify({"status": "ok", "filters": filters})
		except (TypeError, ValueError) as error:
			return jsonify({"status": "error", "message": str(error)}), 400

	def get_pulse_filter_route(self):
		if not self.pulse_filter:
			return jsonify({"status": "error", "message": "Pulse filter not set"}), 400
		return jsonify({"status": "ok", "filters": self.pulse_filter.filters})
	
	def set_pulse_filter(self, pulse_filter):
		self.pulse_filter = pulse_filter

	def update_pulse_filters(self, filters):
		return self.pulse_filter.replace_filters(filters)

	def status_page(self):
		return render_template("status.html")

	def action(self):

		if self.callback:
			self.callback()

		return jsonify({"status": "ok"})

	def set_active_route(self):
		data = request.get_json(silent=True) or {}
		if "active" in data:
			active = data["active"]
			if self.set_active:
				self.set_active(active)
			return jsonify({"status": "ok", "active": active})
		else:
			return jsonify({"status": "error", "message": "Missing 'active' parameter"}), 400

	def get_active_route(self):
		if self.get_active:
			active = self.get_active()
			return jsonify({"status": "ok", "active": active})
		else:
			return jsonify({"status": "error", "message": "No get_active function provided"}), 400

	def run(self):
		self.app.run(host=self.host, port=self.port, threaded=True, use_reloader=False)
