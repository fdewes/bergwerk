# _send_message, send_text_message, and send_text_with_buttons functions 
# taken from
# https://github.com/RasaHQ/rasa/blob/main/rasa/core/channels/socketio.py.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use 
# this file except in compliance with the License. You may obtain a copy of the 
# License at
#
# http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#
# Rasa Technologies GmbH
# Copyright 2016-2022 Rasa Technologies GmbH

async def _send_message(sid, response, sio) -> None:
    await sio.emit("bot_uttered", response, room=sid)


async def send_text_message(sid, text, sio) -> None:
    for message_part in text.strip().split("\n\n"):
        await _send_message(sid, {"text": message_part}, sio)


async def send_text_with_buttons(sid, text, buttons, sio) -> None:
    message_parts = text.strip().split("\n\n") or [text]
    messages = [
        {"text": message, "quick_replies": []} for message in message_parts
    ]
    messages[-1]["quick_replies"] = [
        {
            "content_type": "text",
            "title": button["title"],
            "payload": button["payload"],
        }
        for button in buttons
    ]
    for message in messages:
        await _send_message(sid, message, sio)


def create_buttons(l, last_message=None):
    button_list =  [{"title": item['title'], "payload": f"/{item['link']}"} for item in l]
    if len(button_list) == 0:
        button_list = [{"title": "🏡", "payload": "/Home"}]
    if last_message is not None:
        button_list.append({"title": "↩️", "payload": last_message})
    return button_list
