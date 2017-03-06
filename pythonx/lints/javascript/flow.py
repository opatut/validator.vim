# -*- coding: utf-8 -*-

import os, json
from validator import Validator
from validator.utils import logging

class Flow(Validator):
    __filetype__ = "javascript"

    stdin = False
    checker = "flow"
    args = "--json --from vim --show-all-errors"

    def cmd(self, fname):
        cmd = "echo $({} status {})".format(self.binary, self.cmd_args)
        logging.warn("Flow command: {}".format(cmd))
        return ['bash', '-c', cmd]

    def parse_loclist(self, lines, bufnr):
        content = '\n'.join(lines)

        # parse the json
        try:
            result = json.loads(content)
        except:
            logging.warn("Flow command: {}".format(self.cmd('fname')))
            logging.warn("Failed to parse JSON from flow: {}".format(content))
            return '[]'

        lists = []
        for i, error in enumerate(result['errors']):
            msg = ' '.join([message['descr'] for message in error['message']])

            for message in error['message']:
                if message['path'] != self.filename:
                    continue

                text = "[{}] {}".format(self.checker, msg)

                lists.append(dict(
                    lnum=message['line'],
                    col=message['start'],
                    enum=i + 1,
                    bufnr=bufnr,
                    type='E' if error['level'] == 'error' else 'W',
                    text=text,
                ))

        return json.dumps(lists)
