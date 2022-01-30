import json

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "reprJSON"):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)