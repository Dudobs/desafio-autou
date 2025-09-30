import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

from .config import Config

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)
  app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

  UPLOAD_FOLDER = Config.UPLOAD_FOLDER
  ALLOWED_EXTENSIONS = Config.ALLOWED_EXTENSIONS

  CORS(app)

  if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


  def allowed_file(filename):
    return '.' in  filename and \
      filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


  @app.route("/", methods=["POST"])
  def classifies_content():
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


  return app