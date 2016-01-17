from flask import Response
import json

def jsondumpwrapper(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		return None


def get_json(js):
	return json.dumps(js, default=jsondumpwrapper);

def get_json_response(js):
	return Response(get_json(js), mimetype='application/json')
