Changelog for fishnet
=====================

v1.17.2
-------

* Reduce maximum move time from 20s to 6s. Clients that frequently hit this
  limit should be stopped in favor of clients with better hardware.
* Support future proof constants `--user-backlog short` and
  `--system-backlog long` (to be used instead of hardcoded durations).
* Fix some ignored command line flags during `python -m fishnet configure`
  and on intial run.

v1.17.1
-------

* Bring back `--threads-per-process`. Most contributors should not use this.

v1.17.0
-------

* Option to join only if a backlog is building up. Added `--user-backlog`
  and `--system-backlog` to configure threshold for oldest item in queue.
  Run `python -m fishnet configure` to rerun the setup dialog.
* Slow clients no longer work on young user requested analysis jobs. The
  threshold is continuously adjusted based on performance on other jobs.

v1.16.1
-------

* Fix false positive slowness warning.

v1.16.0
-------

* Removed `--threads-per-process`.
* Warning if client is unsustainably slow.
