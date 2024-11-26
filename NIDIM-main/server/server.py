from flask import Flask, request, jsonify
from flask_cors import CORS
import query
import os


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/api/query/ocr", methods=['GET'])
def getOcrQuery():
    queries = request.args.to_dict(flat=False)
    ids = queries.get('queries[id]', [])
    values = queries.get('queries[value]', [])
    data = []
    for id, value in zip(ids, values):
        data.append({'id': id, 'value': value})
    resultQuery = query.ocrQuery(data)
    return jsonify(
        {
            "data": resultQuery
        }
    )
@app.route('/api/get-image-names', methods=['GET'])
def get_image_names():
    video = request.args.get('video')  
    frame = int(request.args.get('frame'))
    if not video:
        return jsonify({"error": "Missing video parameter"}), 400
    image_data = []  
    for i in range(-100, 201+1-100):
        if(i+frame<0):
            continue
        frame_idx = query.getData(video, frame+i)[3]
        image_data.append(frame_idx)
    return jsonify(image_data)

@app.route("/api/query/text", methods=['GET'])
def getTextQuery():

    queries = request.args.to_dict(flat=False)
    ids = queries.get('queries[id]', [])
    values = queries.get('queries[value]', [])
    
    rateNum = request.args.get('rateNum', None)
    # print(rateNum)

    data = []
    
    for id, value in zip(ids, values):
        data.append({'id': id, 'value': value})
    resultQuery = query.textQuery1(data,rateNum)
    # resultQuery = query.find_vector(data)
    return jsonify(
        {
            "data": resultQuery
        }
    )

@app.route("/api/query/image", methods=['POST'])
def postImageQuery():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        rate_num = request.form.get('rateNum', None)
        if file:
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            return jsonify({'message': 'File successfully uploaded', 'file_path': file_path}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route("/api/query/image", methods=['GET'])
def getImageQuery():
    # data=getText()
    # rate_num = request.args.get('rateNum', None)
    # if(rate_num):
    #     query.TUNGDO(rate_num)

    resultQuery = query.imageQuery()
    
    return jsonify(
        {
            "data": resultQuery
        }
    )


@app.route("/api/query/similar", methods=['GET'])
def getSimilarQuery():
    url_img = request.args.get('url_img')
    print(url_img)
    resultQuery = query.similarQuery(url_img)
    return jsonify(
        {
            "data": resultQuery
        }
    )



if  __name__ == "__main__":
    app.run(debug=True, port=8080,use_reloader=False)