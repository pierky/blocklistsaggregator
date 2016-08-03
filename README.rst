IP Block Lists Aggregator
=========================

A Python tool that downloads IP block lists from various sources and builds configurations for network equipments and firewalls.

Installation
------------

Installation using ``pip``:

.. code:: bash

        $ pip install blocklistsaggregator

Editable Installation using your GitHub forked repository and ``virtualenv``:

.. code:: bash

        $ mkdir blocklistsaggregator
        $ cd blocklistsaggregator
        $ virtualenv venv
        $ source venv/bin/activate
        $ pip install -e git+https://github.com/YOUR_USERNAME/blocklistsaggregator.git#egg=blocklistsaggregator

Usage
-----

It's a command line tool, the ``--help`` is your friend! Some examples are worth a thousand words.

- Download and display entries from all the configured block lists:

  .. code:: bash

          $ blocklistsaggregator.py

- Only from `Ransomware Tracker RW_IPBL <https://ransomwaretracker.abuse.ch/blocklist/>`_ and `DROP <https://www.spamhaus.org/drop/>`_:

  .. code:: bash

          $ blocklistsaggregator.py --lists rw_ipbl drop

- Download entries from all the configured lists and save them in JSON format into ``all.json``:

  .. code:: bash

          $ blocklistsaggregator.py -f json -o all.json

- Read the previously saved entries from ``all.json`` and display them in a Cisco IOS prefix-list style:

  .. code:: bash

          $ blocklistsaggregator.py -i all.json -f cisco-ios

- From the previously saved entries, filter out those falling in 6.0.0.0/8 and those with a prefix-len shorter than /24 and save them into ``cisco.acl`` in a Cisco ACL style with name *BADGUYS*:

  .. code:: bash

          $ blocklistsaggregator.py -i all.json --exclude 6.0.0.0/8 --exclude-ipv4-shorter-than 24 -o cisco.acl -f cisco-ios --cisco-cfg-element acl_source --cisco-cfg-element-name BADGUYS

- Prepare an ``ip route <network> <mask> null0`` command for each IPv4 entry in `DROP <https://www.spamhaus.org/drop/>`_:

  .. code:: bash

          $ blocklistsaggregator.py --lists drop -4 --lines-format "ip route {network} {netmask} null0"

- Download standard block lists and output them in a Mikrotik address-list format into ``addMalwareIPs.rsc``; save lists into ``/tmp`` and, in case of failure during one of the next executions, reuse them to build the output:

  .. code:: bash

          $ blocklistsaggregator --output addMalwareIPs.rsc --output-format mikrotik --mikrotik-address-list-name addressListMalware --lists-storage-dir /tmp/ --recover-from-file

Logging
+++++++

Error logging and reporting can be configured in order to have feedback about BlockListsAggregator's activity. The ``--logging-config-file`` option can be set to the path of a configuration file in `Python's logging.fileConfig() format <https://docs.python.org/2/library/logging.config.html#configuration-file-format>`_. An example is provided within the ``distrib/log.ini`` file (`here the file hosted on GitHub <https://github.com/pierky/blocklistsaggregator/blob/master/distrib/log.ini>`_).

Source block lists
++++++++++++++++++

The following block lists are currenly implemented:

- rw_ipbl, `Ransomware Tracker RW_IPBL <https://ransomwaretracker.abuse.ch/blocklist/>`_
- rw_dombl, `Ransomware Tracker RW_DOMBL <https://ransomwaretracker.abuse.ch/blocklist/>`_ (please read below)
- rw_urlbl, `Ransomware Tracker RW_URLBL <https://ransomwaretracker.abuse.ch/blocklist/>`_ (please read below)
- drop, `Spamhaus DROP <https://www.spamhaus.org/drop/>`_
- drop_v6, `Spamhaus DROPv6 <https://www.spamhaus.org/drop/>`_
- edrop, `Spamhaus EDROP <https://www.spamhaus.org/drop/>`_
- feodo_badip, `Feodo BadIP <https://feodotracker.abuse.ch/blocklist/>`_
- feodo_ip, `Feodo IP <https://feodotracker.abuse.ch/blocklist/>`_
- palevo, `Palevo C&C <https://palevotracker.abuse.ch/blocklists.php>`_
- zeus, `ZeuS <https://zeustracker.abuse.ch/blocklist.php>`_
- bambenek_c2, `Bambenek Consulting C2 master feed <http://osint.bambenekconsulting.com/feeds/>`_

**Warning for RW_DOMBL and RW_URLBL**: the program extracts the domain names reported into these lists to resolve the IP addresses and uses them for the output. This may result in an overblocking behaviour because these filters should be applied with a more granular level than layer-3 addresses. These lists are not used by default unless explicitly given via the command line `--lists` or `--lists-include` arguments.

A list of block-lists can be found on http://iplists.firehol.org/

Output options
++++++++++++++

The following output formats are currenly implemented:

- JSON
- lines (with macros)
- Cisco IOS prefix-list
- Cisco IOS ACL (source-based, destination-based, permit/deny actions)
- Mikrotik RouterOS address-list

Status
------

This tool is currently in **beta**: some field tests have been done but it needs to be tested deeply and on more scenarios.

Moreover, contributions (fixes to code and to grammatical errors, typos, new features) are very much appreciated. 

Bug? Issues?
------------

But also suggestions? New ideas?

Please create an issue on GitHub at https://github.com/pierky/blocklistsaggregator/issues

Author
------

Pier Carlo Chiodi - https://pierky.com

Blog: https://blog.pierky.com Twitter: `@pierky <https://twitter.com/pierky>`_
