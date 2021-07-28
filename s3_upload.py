from flask import Flask, request, jsonify
import boto3
from werkzeug.utils import secure_filename, redirect
import logging


logger=logging.getLogger(__name__)
app = Flask(__name__)


s3 = boto3.client('s3',
                  aws_access_key_id='AKIAQ5RARCW7R3SCI4NM',
                  aws_secret_access_key= '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',
                  )
BUCKET_NAME='itgluetest'

@app.route('/',methods=['GET'])
def index():
    return 'upload  only  allowed have a good  day!!'




@app.route('/upload',methods=['POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            resp = jsonify({'message' : 'No file part in the request'})
            resp.status_code = 400
            return resp
        print('got  the file buddy!!')
        logger.info('got  the file buddy!!')
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print(f'filename:{filename}')
            logger.info(f'filename:{filename}')
            file_path=filename
            file.save(file_path)
            s3.upload_file(
                Bucket = BUCKET_NAME,
                Filename=file_path,
                Key = filename
            )
            print(f'uploaded:{filename}')
            logger.info(f'uploaded:{filename}')
            link='https://{0}.s3.amazonaws.com/{1}'.format(BUCKET_NAME,filename)
            print(f'link:{link}')
            logger.info(f'link:{link}')
            resp = jsonify({'message' : 'uploaded  successfully  here is  the link {0}'.format(link)})
            resp.status_code = 201
    return resp


if __name__ == "__main__":
        app.run(host='0.0.0.0',port=5000,debug=True)