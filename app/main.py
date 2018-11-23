import os
import flask 
import stagger
import json
app = flask.Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload():
    user_file = flask.request.files.getlist("user_file")[0]
    new_metadata = flask.request.form
    new_file = handlefile(user_file, flask.jsonify(new_metadata))
    return new_file

def handlefile(filey, tags):
    print(tags)
    filey.read()
    tag = stagger.read_tag(filey)
    # doe iets met metadata
    # {"Edit":"Submit Query","song_album":"albumpje","song_artist":"artiest",
    # "song_number":"nummertje","song_releasedate":"","song_title":"titel"}

    return flask.send_file(filey, attachment_filename = "hi")
    
@app.route("/")
def main():
    index_path = os.path.join(app.static_folder, 'index.html')
    return flask.send_file(index_path)


# Everything not declared before (not a Flask route / API endpoint)...
@app.route('/<path:path>')
def route_frontend(path):
    # ...could be a static file needed by the front end that
    # doesn't use the `static` path (like in `<script src="bundle.js">`)
    file_path = os.path.join(app.static_folder, path)
    if os.path.isfile(file_path):
        return flask.send_file(file_path)
        # ...or should be handled by the SPA's "router" in front end
    else:
        index_path = os.path.join(app.static_folder, 'index.html')
        return flask.send_file(index_path)


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)

