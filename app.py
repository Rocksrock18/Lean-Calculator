from flask import Flask, request, jsonify
from LeanCalc import LeanCalc
import json 

app = Flask(__name__)


@app.route('/api', methods = ['GET', 'POST', 'DELETE'])
def api():
    if request.method == 'POST':
        #   form of the data:
        #   {   
        #       pole: {coordinates:[]}
        #       image: {fov: , yaw: , width: , height: , latitude: , longitude: , type: , azimuth: , heading: }     
        #       esri_data: {assets: {pole: , crossarm: , insulator: }}
        #       bounded_box: []
        #   }
        data = request.form.to_dict()
        image_data = json.loads(data["image"])
        lc = LeanCalc()
        offset = lc.calcOffsetFactor(image_data)
        distance = lc.calcDistance(json.loads(data["pole"])["coordinates"], image_data)
        lean_factor = lc.calcLeanFactor(offset, data["bounded_box"], image_data["height"], image_data["width"], distance)
        return jsonify(lean_factor)
    else:
        return jsonify("Request type not allowed")

# optional, auto-generated
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
