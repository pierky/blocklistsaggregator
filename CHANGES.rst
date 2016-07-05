Changelog
=========

0.4.0
-----

- Add `drop_v6` list (`Spamhaus DROPv6 <https://www.spamhaus.org/drop/>`_).

0.3.0
-----

- Add `--lists-storage-dir` and `--recover-from-file` arguments to save lists into files and reuse them in case of failure of next updates.

0.2.0
-----

Please note: JSON files saved with the previous version are not compatible with this one; blocklists must be downloaded and saved again to work.

- Keep track of source blocklist for each entry.
- Add `bl_ids` and `bl_names` macros to the `lines` formatter.
- Add a comment containing the source blocklist to each Mikrotik RouterOS address-list entry.

0.1.0
-----

First release (beta)
