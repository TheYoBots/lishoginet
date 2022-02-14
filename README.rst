lishoginet: distributed Fairy-Stockfish analysis for lishogi.org
================================================================

.. image:: https://badge.fury.io/py/lishoginet.svg
    :target: https://pypi.python.org/pypi/lishoginet
    :alt: pypi package

Based on `lichess-org/fishnet@824bfe4 <https://github.com/lichess-org/fishnet/commit/824bfe43e6096e908fd1bae3947b98df0f48b9df/>`_

Installation
------------

1. Install the lishoginet client.

   **Via pip**

   To install or upgrade to the latest version do:

   ::

       pip install --upgrade --user lishoginet

   Example usage:

   ::

       python -m lishoginet --auto-update

   Other useful commands:

   ::

       python -m lishoginet configure  # Rerun the configuration dialog
       python -m lishoignet systemd  # Generate a systemd service file
       python -m lishoginet --help  # List all commands and options

   **Via Docker**

   There is a `Docker container <https://github.com/TheYoBots/lishoginet/blob/master/Dockerfile/>`_
   courtesy of `@mklemenz <https://github.com/mklemenz>`_. For example you can
   simply do:

   ::

       docker build -t lishoginet:latest .
       docker run -it lishoginet:latest

Lichess' Video tutorial
-----------------------

.. image:: https://img.youtube.com/vi/iPRNluVn22w/0.jpg
    :target: https://www.youtube.com/watch?v=iPRNluVn22w
    :alt: Introduction video

FAQ
---

Which engine does lishoginet use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

lishoginet is using
`a fork of Stockfish called Fairy Stockfish <https://github.com/ianfab/Stockfish>`_
which supports both shogi and shogi variants
by `@ianfab <https://github.com/ianfab>`_.

You can build Fairy-Stockfish yourself (for example with ``./build-stockfish.sh``)
and provide the path using ``python -m lishoginet --stockfish-command``. Otherwise
a precompiled binary will be downloaded for you.

What are the requirements?
^^^^^^^^^^^^^^^^^^^^^^^^^^

* Precompiled Fairy-Stockfish binaries available for Linux, Windows and OS X on
  Intel and AMD CPUs
* Python 3.3+ or 2.7
* Will max out the number of configured CPU cores
* Uses a default of 256 MiB RAM per engine process, spawns one process for
  each group of ~3 cores
* A small amount of disk space
* Low-bandwidth network communication with Lishogi servers
  (only outgoing HTTP requests, so probably no firewall configuration
  required)

Is my CPU fast enough?
^^^^^^^^^^^^^^^^^^^^^^

Almost all processors will be able to meet the requirement of 4 meganodes in
6 seconds. Clients on the faster end will automatically be assigned
analysis jobs that have humans waiting for the result (the user queue, as
opposed to the system queue for slower clients).

What happens if I stop my client?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Feel free to turn your client on and off at any time. By default, the client
will try to finish any jobs it has already started. On immediate shutdown,
the client tries to inform Lishogi that jobs should be reassigned.
If even that fails,
Lishogi will reassign the jobs after a timeout.

Will lishoginet use my GPU?
^^^^^^^^^^^^^^^^^^^^^^^^^^^

No, Fairy-Stockfish is a classical alpha-beta engine.

Is lishoginet secure?
^^^^^^^^^^^^^^^^^^^^^

To the best of our knowledge. All network communication uses modern TLS.
However you implicitly trust the authors, PyPI infrastructure when running with
``--auto-update``, the CI infrastructure when using precompiled Fairy-Stockfish
binaries, and Lishogi to not exploit potential vulnerabilities in Fairy-Stockfish's
USI implementation. You can mitigate all of these by running lishoginet as an
unprivileged user.

Is there a leaderboard of contributors?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

No, sorry, not publically. It would incentivize gaming the metrics.

Is there a Docker image?
^^^^^^^^^^^^^^^^^^^^^^^^

Yes, see the installation instructions above.

Can I autoscale lishoginet in the cloud?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is currently no ready-made solution, but
`an API for monitoring the job queue status <https://github.com/TheYoBots/lishoginet/blob/master/doc/protocol.md#status>`_
is provided.

Protocol
--------

.. image:: https://raw.githubusercontent.com/TheYoBots/lishoginet/master/doc/sequence-diagram.png

See `protocol.md <https://github.com/TheYoBots/lishoginet/blob/master/doc/protocol.md>`_ for details.

License
-------

lishoginet is licensed under the GPLv3+. See LICENSE.txt for the full
license text.