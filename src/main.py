try:
    import logging
    import colorlog
    import logging.config
    import os
    import sys
    if __debug__:
        logging.config.fileConfig('logging.conf')
        logger = colorlog.getLogger('loggingUser')
    from flask import Flask
    from flask import json
    from flask import request
    import cv2
    import numpy as np
    import face_recognition
    from googleImageDown import down
except Exception as e:
    logging.warning("Error while importing librearies {}".format(e))
    sys.exit()


app = Flask(__name__)

@app.route("/search", methods=['POST'])
def search():
    data = {
        "name": request.get_json()['name'],
        "user": "0",
        "success": False,
        "face": [],
        "telephone": "0",
    }
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    vectors = []
    down(data['name'])
    try:
        i = 0
        count_resp = []
        images_array = os.listdir('/root/tmp')
        for image in range(0,len(images_array)-1):
            imagearray = cv2.imread('/root/tmp/' + images_array[image])
            vectors.append(get_vector(imagearray))
        for image in range(0,len(images_array)):
            count = 0
            for image_compare in range(image+1,len(images_array)-1):
                print(image, image_compare)
                if image_compare == image:
                    continue
                if compare_faces(vectors[image],vectors[image_compare]):
                    count = count+1
            count_resp.append(count)
        print(count_resp)
    except Exception as e:
        logging.warning('Error {}'.format(e))
        response.status_code = (500)
    finally:
        response.response = json.dumps(data)
        return response


@app.route("/register", methods=['POST'])
def register():
    data = {
        "face": [],
        "telephone": 0,
    }
    response = app.response_class(
        response=json.dumps(data),
        mimetype='application/json'
    )
    imagefile = request.files['file']

    try:
        image = imagefile.read()
        face = get_vector(image)
        #logging.debug('face {} '.format(face[0].__dict__))
        data['face'] = str(face[0])
        data['telephone'] = 789
        logging.debug('data {} '.format(json.dumps(data)))

    except Exception as e:
        logging.warning('Error {}'.format(e))
        response.status_code = (500)
    else:
        response.response = json.dumps(data)
        response.status_code = (200)
    finally:
        return response


def get_vector(photo):
    logging.debug('Photo '.format(photo))
    try:
        small_frame = cv2.resize(photo, (0, 0), fx=0.5, fy=0.5)
        rgb_small_frame = small_frame[:, :, ::-1]
        face_location = face_recognition.face_locations(rgb_small_frame)
        face = face_recognition.face_encodings(rgb_small_frame, face_location)
    except Exception as e:
        logging.warning('Error {}'.format(e))
        faces = list()
    finally:
        logging.debug('faces '.format(face))
        return face

def compare_faces(face_vector1, face_vector2):
    logging.debug('compare user')
    if face_recognition.compare_faces(np.array(face_vector1), np.array(face_vector2), 0.75):
        return True
    else:
        return False

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=6666)
