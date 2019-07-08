# mycroft-webhook-inbound

This is a very hacky Mycroft webhook (written in flask and using (yes, I know *ugh*) and using `subprocess.call()`) that listens for REST requests with JSON payloads and hands them off to Mycroft's message bus.

## Endpoints

All of the follow pyaloads should These payloads should be sent as a HTTP `POST` request with the header `Content-Type: application/json`

### announcement

It listens on `/api/v1.0/announce` for a JSON payload in the format:

```json
{
  "announcement": "your announcement here"
}
```

It will verbally announce whatever the `announcement` text in the payload is. Honestly, though, I recommend installing https://github.com/ketudb/mycroft-announce and using the `say-to` endpoint to call that. It's a much nicer experience.

### say-to

It also listens for utterances (e.g. things you can say to it) on `/api/v1.0/say-to` in the format:

```json
{
 "input": "your utterance here"
}
```

It will process whatever the value of `input` is as an utterance (e.g. you could send `"input": "volume 5"` to adjust the volume of the Mycroft. **Note** that it will also verbally respond to the input as though you had verbally issused the command (e.g. given the last example, it might response with `Volume set to five.` out loud).

## Installation/startup

By default it listens on all interfaces on port `8080`.

To install:

```bash
sudo mkdir /opt/mycroft-webhook && sudo chmod 0777 /opt/mycroft-webhook
git clone https://github.com/ketudb/mycroft-webhook-inbound.git /opt/mycroft-webhook
pip install flask
```

To configure it to run at start (very very hacky!) add the following line to
your `~/custom_setup.sh` file:

```bash
python /opt/mycroft-webhook/webhook.py 2>&1 | logger -t mycroft-webhook &
```

To configure with hass.io, add this to your configuration.yaml:

```yaml
notify:
  - name: mycroft_name
    platform: rest
    resource: http://ip-address:8080/api/v1.0/announce
    method: POST_JSON
    message_param_name: announcement
```

## Issues/TODOs

* I need to add some kind of security to the endpoint. Right now, it's assumed that it's secured by the firewall on your local network, which isn't ideal - especially given the point of this is to _not_ have to expose the Mycroft MessageBus service.

* I want to switch from using `subprocess.call()` for calling the Mycroft python modules to importing and using them, or just talking directly to the MessageBus. I wrote this for a quick-fix to integrate with HomeAssistant, so it's not well thought through, but it gets the job done and I'll clean it up later 😛

* It should probably fail more gracefully. It doesn't _really_ check to see if the `subprocess` call exited cleanly or not. That's not great.

* It should also really run in it's own venv.
