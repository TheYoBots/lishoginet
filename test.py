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
            "position": "lnsg1gsnl/1r4kb1/ppppppppp/7P1/9/9/PPPPPPP1P/1B5R1/LNSGKGSNL w - 1",
            "moves": "b8f8",
        }

        response = self.worker.bestmove(job)
        self.assertEqual(response["move"]["bestmove"], "h6h7+")

    def test_minishogi_bestmove(self):
        job = {
            "work": {
                "type": "move",
                "id": "hihihihi",
                "level": 1,
            },
            "game_id": "ihihihih",
            "variant": "minishogi",
            "position": "r3k/2r2/KB1Ps/P4/2s2 b BGg 1",
            "moves": "b3a4",
        }

        response = self.worker.bestmove(job)
        self.assertEqual(response["move"]["bestmove"], "G*e8") # only move

    def test_analysis(self):
        job = {
            "work": {
                "type": "analysis",
                "id": "12345678",
            },
            "game_id": "87654321",
            "variant": "standard",
            "position": STARTPOS,
            "moves": "h3h4 e9f8 h4h5 f8g8 h5h6 b8f8",
            "skipPositions": [1],
        }

        response = self.worker.analysis(job)
        result = response["analysis"]

        self.assertTrue(0 <= result[0]["score"]["cp"] <= 90)

        self.assertTrue(result[1]["skipped"])

        self.assertTrue(0 <= result[0]["score"]["cp"] <= 90)
        self.assertFalse(result[3]["pv"].startswith("h5h7+"))

        self.assertTrue(result[4]["score"]["cp"] >= 0)


class UnitTests(unittest.TestCase):

    def test_parse_bool(self):
        self.assertEqual(lishoginet.parse_bool("yes"), True)
        self.assertEqual(lishoginet.parse_bool("no"), False)
        self.assertEqual(lishoginet.parse_bool(""), False)
        self.assertEqual(lishoginet.parse_bool("", default=True), True)

    def test_parse_duration(self):
        self.assertEqual(lishoginet.parse_duration("1m"), 60)
        self.assertEqual(lishoginet.parse_duration("2 s"), 2)


if __name__ == "__main__":
    if "-v" in sys.argv or "--verbose" in sys.argv:
        lishoginet.setup_logging(3)
    else:
        lishoginet.setup_logging(0)

    unittest.main()