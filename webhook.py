from flask import Flask, jsonify, abort, request
import subprocess
app = Flask(__name__)

# TODO: Add some kind of security to this!

@app.route('/')
def index():
        return "This service provides a REST API for the local mycroft-* commands. See <a href='https://github.com/ketudb/mycroft-webhook-inbound'>GitHub</a> for info!"

# Route the POST request
@app.route('/api/v1.0/announce', methods=['POST'])
def post_announcement():
        # Make sure the request is coming in as JSON.
        if not request.json:
                abort(400)

        # TODO: Check exit code & fail gracefully.
        announcement = "{\"utterance\": \"Announcement: " + request.json['announcement'] + "\"}"
        subprocess.call(["python", "-m", "mycroft.messagebus.send", "speak", announcement])

        # Return success if we've managed it.
        return jsonify({'success': "true"})

@app.route('/api/v1.0/say-to', methods=['POST'])
def post_say_to():
        # Make sure the request is coming in as JSON
        if not request.json:
                about(400)

        # TODO: Check exit code & fail gracefully.
        utterance_json = "{\"utterances\": [\"" + request.json['input'] + "\"], \"lang\": \"en-us\"}"
        subprocess.call(["python", "-m", "mycroft.messagebus.send", "recognizer_loop:utterance", utterance_json])                                                                             

        # Return success if we've managed it.
        return jsonify({'success': "true"})

if __name__ == '__main__':
        app.run(host='0.0.0.0', port='8080')
