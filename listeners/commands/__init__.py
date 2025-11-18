from slack_bolt import App
from .ask_command import ask_callback
from .template_command import template_callback


def register(app: App):
    app.command("/ask-bolty")(ask_callback)
    # Register the template command for local testing. Ensure your app
    # manifest includes this slash command (manifest.json) and re-install
    # the app in your workspace if needed.
    app.command("/template-bolty")(template_callback)
