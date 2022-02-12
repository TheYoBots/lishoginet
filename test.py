#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the lishogi.org lishoginet client.
# Copyright (C) 2016-2020 Niklas Fiekas <niklas.fiekas@backscattering.de>
# Copyright (C) 2022- TheYoBots (for lishogi) <contact@lishogi.org>
# See LICENSE.txt for licensing information.

import lishoginet
import unittest
import sys
import multiprocessing

try:
    import configparser
except ImportError:
    import ConfigParser as configparser


STARTPOS = "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL b - 1"


class WorkerTest(unittest.TestCase):

    def setUp(self):
        conf = configparser.ConfigParser()
        conf.add_section("Lishoginet")
        conf.set("Lishoginet", "Key", "testkey")

        lishoginet.get_stockfish_command(conf, update=True)

        self.worker = lishoginet.Worker(conf,
            threads=multiprocessing.cpu_count(),
            memory=32,
            user_backlog=0,
            system_backlog=0,
            progress_reporter=None)
        self.worker.start_stockfish()

    def tearDown(self):
        self.worker.stop()

    def test_bestmove(self):
        job = {
            "work": {
                "type": "move",
                "id": "abcdefgh",
                "level": 8,
            },
            "game_id": "hgfedcba",
            "variant": "standard",
            "position": STARTPOS,
            "moves": "2g2f 5a4b 2f2e 4b3b 2e2d 8b4b",
        }

        response = self.worker.bestmove(job)
        self.assertEqual(response["move"]["bestmove"], "P*2c+")

    def test_minishogi_bestmove(self):
        job = {
            "work": {
                "type": "move",
                "id": "hihihihi",
                "level": 1,
            },
            "game_id": "ihihihih",
            "variant": "minishogi",
            "position": "rbsgk/4p/5/P4/KGSBR b - 1",
            "moves": "4e4d",
        }

        response = self.worker.bestmove(job)
        self.assertEqual(response["move"]["bestmove"], "4a3b") # only move

    def test_analysis(self):
        job = {
            "work": {
                "type": "analysis",
                "id": "12345678",
            },
            "game_id": "87654321",
            "variant": "standard",
            "position": STARTPOS,
            "moves": "2g2f 5a4b 2f2e 4b3b 2e2d 8b4b P*2c+",
            "skipPositions": [1],
        }

        response = self.worker.analysis(job)
        result = response["analysis"]

        self.assertTrue(0 <= result[0]["score"]["cp"] <= 90)

        self.assertTrue(result[1]["skipped"])

        self.assertEqual(result[3]["score"]["mate"], 1)
        self.assertTrue(result[3]["pv"].startswith("P*2c+"))

        self.assertEqual(result[4]["score"]["mate"], 0)


class UnitTests(unittest.TestCase):

    def test_parse_bool(self):
        self.assertEqual(lishoginet.parse_bool("yes"), True)
        self.assertEqual(lishoginet.parse_bool("no"), False)
        self.assertEqual(lishoginet.parse_bool(""), False)
        self.assertEqual(lishoginet.parse_bool("", default=True), True)

    def test_parse_duration(self):
        self.assertEqual(lishoginet.parse_duration("1m"), 60)
        self.assertEqual(lishoginet.parse_duration("2 s"), 2)

    def test_encode_score(self):
        self.assertEqual(lishoginet.decode_score(lishoginet.encode_score("cp", 42)), {"cp": 42})
        self.assertEqual(lishoginet.decode_score(lishoginet.encode_score("mate", -1)), {"mate": -1})
        self.assertEqual(lishoginet.decode_score(lishoginet.encode_score("mate", 0)), {"mate": 0})
        self.assertEqual(lishoginet.decode_score(lishoginet.encode_score("mate", 1)), {"mate": 1})


if __name__ == "__main__":
    if "-v" in sys.argv or "--verbose" in sys.argv:
        lishoginet.setup_logging(3)
    else:
        lishoginet.setup_logging(0)

    unittest.main()