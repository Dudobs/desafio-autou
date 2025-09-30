import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './files'
ALLOWED_EXTENSION = {'txt', 'pdf'}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

CORS(app)

def allowed_file(filename):
   return '.' in  filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION


@app.route("/", methods=["POST"])
def classifies_email():
  if request.form:
    text = request.form['text']
    return jsonify({"text": text})

  if request.files:
    file = request.files['file']
    if not allowed_file(file.filename):
      return jsonify({"error": "Somente arquivos .txt ou .pdf são permitidos."}), 400
    
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # lógica para ler arquivo e classificá-lo

    os.remove(f"{app.config['UPLOAD_FOLDER']}/{filename}")

    return jsonify({"file": file.filename})
  
  return jsonify({"message": "Nenhum dado enviado"}), 400



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)