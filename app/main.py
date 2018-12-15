import os
import flask 
import stagger
import json
app = flask.Flask(__name__)
tagcycle = ["album", "artist", "track", "year", "title"]

@app.route("/upload", methods=["POST"])
def upload():
    user_file = flask.request.files.getlist("user_file")[0]
    new_metadata = flask.request.form.to_dict()
    new_file = handlefile(user_file, new_metadata)
    return new_file

def handlefile(filey, tags):
    print(tags)
    tag = stagger.read_tag(filey)
    # doe iets met metadata
    # {"Edit":"Submit Query","song_album":"albumpje","song_artist":"artiest",
    # "song_number":"nummertje","song_releasedate":"","song_title":"titel"}
    path = "/app/mam.mp3"
    with open(path, "wb") as f:
        f.write(filey.read())
    for item in tagcycle:
        setattr(tag, item, tags[f"song_{item}"])
    tag.write(path)
    return flask.send_file(path)
    
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

