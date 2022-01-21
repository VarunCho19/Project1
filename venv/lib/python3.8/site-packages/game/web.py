# -*- coding: utf-8 -*-
# @author: leesoar

"""web.py"""
import argparse
import os
import platform

from flask import request, Flask, jsonify, make_response
from game import __version__

app = Flask(__name__)


@app.route('/', methods=["GET"])
def load_emulator():
    return app.send_static_file('game.html')


@app.route('/api/file', methods=['GET', 'POST'])
def find_game():
    try:
        path = request.args.get("p")
        resp = make_response(open(path, mode="rb").read())
        resp.headers["Content-type"] = "application/octet-stream"
        return resp
    except FileNotFoundError:
        return jsonify(dict(code=0, msg="File not exist.")), 202


@app.errorhandler(404)
def not_found(e):
    return jsonify(dict(code=0, msg="not found")), 404


@app.errorhandler(500)
def svc_error(e):
    return jsonify(dict(code=0, msg="error")), 500


def run_web(args):
    try:
        app.run(host='0.0.0.0', port=2345, debug=False)
    except Exception:
        pass


def open_game(args):
    os_type = platform.system()
    url = f"http://localhost:2345?p={args.src}"
    if os_type == "Windows":
        return os.system(f"start {url}")
    return os.system(f"open {url}")


def run():
    parser = argparse.ArgumentParser(
        description=f"A web game emulator, not only can play games. Welcome to explore.",
        prog="game", add_help=False)

    subparsers = parser.add_subparsers(dest='cmd', title='Available commands')
    parser.add_argument('-v', '--version', action='version', version=__version__, help='Get version of game')
    parser.add_argument('-h', '--help', action='help', help='Show help message')

    p_web = subparsers.add_parser('web')
    p_web.set_defaults(func=run_web)

    p_play = subparsers.add_parser('play')
    p_play.set_defaults(func=open_game)
    p_play.add_argument('src', type=str, help="game absolute path")

    try:
        args = parser.parse_args()
        args.func(args)
    except Exception:
        print("Error, check logs.")
