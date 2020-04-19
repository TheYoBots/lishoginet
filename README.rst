fishnet: distributed Stockfish analysis for lichess.org
=======================================================

.. image:: https://badge.fury.io/py/fishnet.svg
    :target: https://pypi.python.org/pypi/fishnet
    :alt: pypi package

.. image:: https://travis-ci.org/niklasf/fishnet.svg?branch=master
    :target: https://travis-ci.org/niklasf/fishnet
    :alt: build

Installation
------------

1. Request your personal fishnet key: https://lichess.org/get-fishnet
2. Install the fishnet client.

   **Via pip**

   To install or upgrade to the latest version do:

   ::

       pip install --upgrade --user fishnet

   Example usage:

   ::

       python -m fishnet --auto-update

   Other useful commands:

   ::

       python -m fishnet configure  # Rerun the configuration dialog
       python -m fishnet systemd  # Generate a systemd service file
       python -m fishnet --help  # List all commands and options

   **Via Docker**

   There is a `Docker container <https://hub.docker.com/r/mklemenz/fishnet/>`_
   courtesy of `@mklemenz <https://github.com/mklemenz>`_. For example you can
   simply do:

   ::

       docker run mklemenz/fishnet --key MY_APIKEY --auto-update

Video tutorial
--------------

.. image:: https://img.youtube.com/vi/iPRNluVn22w/0.jpg
    :target: https://www.youtube.com/watch?v=iPRNluVn22w
    :alt: Introduction video

FAQ
---

Which engine does fishnet use?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

fishnet is using
`a fork of Stockfish <https://github.com/niklasf/Stockfish/tree/fishnet>`__
(hence the name) with multi-variant support
by `@ddugovic, @ianfab et al <https://github.com/ddugovic/Stockfish>`_.

You can build Stockfish yourself (for example with ``./build-stockfish.sh``)
and provide the path using ``python -m fishnet --stockfish-command``. Otherwise
a precompiled binary will be downloaded for you.

What are the requirements?
^^^^^^^^^^^^^^^^^^^^^^^^^^

* Precompiled Stockfish binaries available for Linux, Windows and OS X on
  Intel and AMD CPUs
* Python 3.3+ or 2.7
* Will max out the number of configured CPU cores
* Uses a default of 256 MiB RAM per engine process
* A small amount of disk space
* Low-bandwidth network communication with Lichess servers
  (only outgoing HTTP requests, so probably no firewall configuration
  required)

Is my CPU fast enough?
^^^^^^^^^^^^^^^^^^^^^^

Almost all processor will be able to meet the requirement of 4 meganodes in
6 seconds. Clients on the faster end will automatically be assigned
analysis jobs that have humans waiting for the result (the user queue, as
opposed to the system queue for slower clients).

What happens if I stop my client?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Feel free to turn your client on and off at any time. By default, the client
will try to finish any jobs it has already started. On immediate shutdown,
the client tries to inform Lichess that jobs should be reassigned.
If even that fails,
Lichess will reassign the jobs after a timeout.

Will fishnet use my GPU?
^^^^^^^^^^^^^^^^^^^^^^^^

No, Stockfish is a classical alpha-beta engine. (Supporting Lc0 analysis is
a future prospect.)

Is fishnet secure?
^^^^^^^^^^^^^^^^^^

To the best of our knowledge. All network communication uses modern TLS.
However you implicitly trust the authors, PyPI infrastructure when running with
``--auto-update``, the CI infrastructure when using precompiled Stockfish
binaries, and Lichess to not exploit potential vulnerabilities in Stockfish's
UCI implementation. You can mitigate all of these by running fishnet as an
unprivileged user.

Is there a Docker image?
^^^^^^^^^^^^^^^^^^^^^^^^

Yes, see the installation instructions above.

Can I autoscale fishnet in the cloud?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is currently no ready-made solution, but
`an API for monitoring the job queue status <https://github.com/niklasf/fishnet/blob/master/doc/protocol.md#status>`_
is provided.

Protocol
--------

.. image:: https://raw.githubusercontent.com/niklasf/fishnet/master/doc/sequence-diagram.png

See `protocol.md <https://github.com/niklasf/fishnet/blob/master/doc/protocol.md>`_ for details.

License
-------

fishnet is licensed under the GPLv3+ license. See LICENSE.txt for the full
license text.
