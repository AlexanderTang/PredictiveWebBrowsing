#!python3
# encoding: utf-8
"""
urlStreamHandler.py
"""

import sys
import argparse
import json
import http.server
import socketserver
import datetime
import atexit
import signal
from subprocess import call

import csv

date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
filename = "urls_{}.csv".format(date)
logfile = open(filename, "w")
print('Writing to {}'.format(filename))

def at_exit():
    print("Closing logfile")
    logfile.close()
atexit.register(at_exit)

def do_exit(sig, frame):
    print("\nShutting down")
    sys.exit(0)
signal.signal(signal.SIGINT, do_exit)

class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        """The GreaseMonkey script sends json data containing the url,
        timestamp, and html. We capture all POST requests irrespective of the
        path.
        """
        length = int(self.headers['Content-Length'])
        content = self.rfile.read(length)
        data = json.loads(content.decode(encoding='UTF-8'))
        url = data['url']
        ts = data['ts']
        action = data['action']
        if action == 'load':
            toppage = data['top']
            html = data['html']
            if toppage:
                action_str = 'load'
            else:
                action_str = 'bg'
            target = ''
            print('{:<15}: {}'.format(action_str, url))
        elif 'target' in data:
            action_str = action
            target = data['target']
            print('{:<15}: {} -> {}'.format(action_str, url, target))
        else:
            action_str = action
            target = ''
            print('{:<15}: {}'.format(action_str, url))
        print('"'+ts+'", "'+action_str+'", "'+url+'", "'+target+'"',
              file=logfile)
        # TODO: Call your model to learn from url and build up a list of next
        # guesses guesses = myModel.get_guesses(url, html)
        if(action == "click" or action == "load"):
            command = "python run_prediction.py "
            command += url
            call(command)
            f = open('../actual_run_data/prediction.txt', 'r')
            guess = f.readline()
            print("LOOK HERE")
            print(guess)
            if guess[:-2] == "\n":
                guess = guess[:-2]
            f.close()

            response = {
                'success': True,
                'guesses': [[guess, 1]]
            }
        else:
            response = {
                'success': False,
                'guesses': []
            }
        jsonstr = bytes(json.dumps(response), "UTF-8")
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Content-length", len(jsonstr))
        self.end_headers()
        self.wfile.write(jsonstr)


def start_from_csv(filenames):
    """List of csv files that contain a url stream as if they were comming
    from the GreaseMonkey script."""
    """
    for filename in filenames:
        with open(filename, 'r') as csv_file:
            # TODO: Incrementally train your model based on these files
            print('Processing {}'.format(filename))
    """
    command = "python run_training.py"
    for fn in filenames:
        command += " " + fn
    call(command)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Record and suggest urls')
    parser.add_argument('--verbose', '-v', action='count',
                        help='Verbose output')
    parser.add_argument('--port', '-p', default=8000,
                        help='Server port')
    parser.add_argument('--csv', nargs='*',
                        help='CSV files with a url stream to start from')
    args = parser.parse_args(argv)

    if args.csv is not None:
        start_from_csv(args.csv)

    server = socketserver.TCPServer(("", args.port), MyRequestHandler)
    print("Serving at port {}".format(args.port))
    print("CTRL-C to exit")
    server.serve_forever()


if __name__ == "__main__":
    sys.exit(main())

print("ok")
