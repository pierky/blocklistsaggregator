Changelog
=========

0.5.1
-----

- Fix a bug in the packaging system.

0.5.0
-----

- Better empty lines detection for RW_IPBL.
- Add `--lists-include` and `--lists-exclude` arguments.
- Add `rw_dombl` and `rw_urlbl` lists (`Ransomware Tracker RW_DOMBL and RW_URLBL <https://ransomwaretracker.abuse.ch/>`_).

  Warning: the program extracts the domain names reported into these lists to resolve the IP addresses and uses them for the output. This may result in an overblocking behaviour because these filters should be applied with a more granular level than layer-3 addresses. These lists are not used by default unless explicitly given via the command line `--lists` or `--lists-include` arguments.

0.4.1
-----

- Fix issue with RW_IPBL entries counter.

  It seems that RW_IPBL is having some issues with the number of entries reported in the last line.
  If an empty line is found it's counted as an entry, so last line's counter reports a wrong number.
  Trying to mitigate this behaviour.

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
