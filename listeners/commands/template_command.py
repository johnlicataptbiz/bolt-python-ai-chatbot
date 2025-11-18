from slack_bolt import Ack, Say, BoltContext
from logging import Logger
from slack_sdk import WebClient

"""
Template for a slash command listener.

Copy this file to `listeners/commands/` as a starting point for new commands.
Follow the patterns used in `listeners/commands/ask_command.py`:
- call `ack()` early
- access `context['user_id']` and `context['channel_id']`
- use `client.chat_postEphemeral` for user-directed responses
"""


def template_callback(
    client: WebClient, ack: Ack, command, say: Say, logger: Logger, context: BoltContext
):
    try:
        ack()
        user_id = context.get("user_id")
        channel_id = context.get("channel_id")
        text = command.get("text", "").strip()

        if not text:
            client.chat_postEphemeral(
                channel=channel_id, user=user_id, text="Please provide input to this command."
            )
            return

        # Example response — replace with real logic (e.g., call get_provider_response)
        client.chat_postMessage(channel=channel_id, text=f"Template received: {text}")

    except Exception as e:
        logger.error(e)
        client.chat_postEphemeral(channel=channel_id, user=user_id, text=f"Error: {e}")
