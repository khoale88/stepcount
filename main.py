import os
from flask import Flask, json, Response, request,render_template, url_for, redirect, send_file
import steppandas as stppd
# import unzip_and_parse as uap
# import stepcount as stpcnt
# import model

app = Flask(__name__)
app.config["APP_HOST"] = "0.0.0.0"
app.config["APP_PORT"] = 5000
# app.config["CLASS_JAR"] = "./parser/parser.jar"
app.config["UPLOAD_FOLDER"] = "./uploads/"
app.config["OUTPUT_FOLDER"] = "./static/"


@app.route('/uploadXML', methods=['POST'])
def upload_xml():
    xmlfile = request.files['xmlFile']
    # filename = xmlfile.filename
    filename = "export.xml"

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    xmlfile.save(save_path)

    outputlink = stppd.process(input_path=app.config["UPLOAD_FOLDER"], 
                               filename=filename)
    body = {"link":outputlink}
    return Response(response=json.dumps(body), status=200)

@app.route('/return_files/')
def return_files():
    try:
        outputlink = os.path.abspath(app.config["UPLOAD_FOLDER"])
        outputlink = os.path.join(outputlink, 'export.csv')
        return send_file(outputlink, as_attachment=True, attachment_filename='export.csv')
    except Exception as e:
        return str(e)

@app.route("/stepcount",methods=['GET'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host=app.config["APP_HOST"], port=app.config["APP_PORT"])
