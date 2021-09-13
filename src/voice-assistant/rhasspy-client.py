"""
Command-line interface to RhasspyClient.
For more information on Rhasspy, please see:
https://rhasspy.readthedocs.io/
"""
import argparse
import asyncio
import json
import logging
import errno 
import sys
import os
import subprocess
from typing import Any, Text, TextIO
from pathlib import Path

import aiohttp
import attr
import jsonlines

from rhasspyclient import RhasspyClient

APP_DIRECTORY = "./"
DOWNLOADS_DIRECTORY = os.path.join(APP_DIRECTORY, "FilesAudios")
_LOGGER = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


async def main():
    """Main method"""
    parser = argparse.ArgumentParser(prog="rhasspyclient")
    parser.add_argument(
        "--debug", action="store_true", help="Print DEBUG messages to console"
    )
    parser.add_argument(
        "--api-url",
        default="http://localhost:12101/api",
        help="URL of Rhasspy server (with /api)",
    )

    sub_parsers = parser.add_subparsers()
    sub_parsers.required = True
    sub_parsers.dest = "command"

    # version
    version_parser = sub_parsers.add_parser("version", help="Get Rhasspy version")
    version_parser.set_defaults(func=version)

    # restart
    restart_parser = sub_parsers.add_parser(
        "restart", help="Restart the Rhasspy server"
    )
    restart_parser.set_defaults(func=restart)

    # train
    train_parser = sub_parsers.add_parser("train-profile", help="Train Rhasspy profile")
    train_parser.add_argument(
        "--no-cache", action="store_true", help="Clear cache before training"
    )
    train_parser.set_defaults(func=train)

    # speech-to-text
    speech_to_text_parser = sub_parsers.add_parser(
        "speech-to-text", help="Transcribe WAV file(s)"
    )
    speech_to_text_parser.add_argument("wavs", nargs="*", help="WAV file paths")
    speech_to_text_parser.set_defaults(func=speech_to_text)

    # text-to-intent
    text_to_intent_parser = sub_parsers.add_parser(
        "text-to-intent", help="Recognize intent from text"
    )
    text_to_intent_parser.add_argument("text", nargs="*", help="Sentences to recognize")
    text_to_intent_parser.add_argument(
        "--handle", action="store_true", help="Handle intent"
    )
    text_to_intent_parser.set_defaults(func=text_to_intent)

    #intent-handle
    intent_handle_parser = sub_parsers.add_parser("intent-handle", help="Run handle intent")
    intent_handle_parser.add_argument("handle", nargs="*", help="Handle intent")
    intent_handle_parser.set_defaults(func=intent_handle)

    #record
    record_parser = sub_parsers.add_parser("record", help="Record audio from webcam")
    record_parser.set_defaults(func=record)

    # Parse args
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    _LOGGER.debug(args)

    # Begin client session
    async with aiohttp.ClientSession() as session:
        client = RhasspyClient(args.api_url, session)

        # Call sub-commmand
        await args.func(args, client)


# -----------------------------------------------------------------------------


async def version(args, client):
    """Get Rhasspy server version"""
    result = await client.version()
    print(result)

async def restart(args, client):
    """Restart Rhasspy server"""
    result = await client.restart()
    print(result)


async def train(args, client):
    """Generate speech/intent artifacts for profile"""
    result = await client.train(no_cache=args.no_cache)
    print_json(attr.asdict(result))


async def speech_to_text(wav_audio, client):
    """Transcribe WAV file to text"""
    if len(wav_audio) > 0:
            with open(wav_audio, "rb") as wav_file:
                result = await client.speech_to_text(wav_file.read())
                print(result)
                await text_to_intent(result, client)


async def text_to_intent(args, client):
    """Recognize intent from sentence(s)"""
    if len(args.text) > 0:
        sentences = args.text
    else:
        sentences = sys.stdin

    result = await client.text_to_intent(sentences)
    intent = json.dumps(result)
    print(intent)
    await intent_handle(result)
    

async def intent_handle(result):
    intent = result["intent"]["name"]
    contact_name = result["tokens"][len(result["tokens"])-1].capitalize()
    print(contact_name)
    
    if intent == 'GetCall':
        subprocess.run(["bash", "intent-handle.sh", contact_name])
    else:
        print('Sorry. You must ask for a call to be made.')

async def record(args, client):
    try:
        os.mkdir(DOWNLOADS_DIRECTORY)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    os.system("arecord -f S16_LE -d 3 -r 16000 --device='plughw:1,0' ./FilesAudios/call.wav")
    wav_path = os.path.join(DOWNLOADS_DIRECTORY, 'call.wav')
    await speech_to_text(wav_path, client)

#-----------------------------------------------------------------------------


def print_json(obj: Any, out_file: TextIO = sys.stdout) -> None:
    """Prints a JSON value as a single line"""
    with jsonlines.Writer(out_file) as writer:
        writer.write(obj)  # pylint: disable=E1101

    out_file.flush()


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
