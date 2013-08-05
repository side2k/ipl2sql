ipl2sql
=======

iptables log to SQL converter.

This utility converts iptables log to a series of SQL queries(MySQL-compatible) and outputs them to stdout(just like mysqldump).


Table structure
=======

<pre>
CREATE TABLE `packets` (
  `IN` varchar(6) DEFAULT NULL,
  `OUT` varchar(6) DEFAULT NULL,
  `SRC` varchar(15) DEFAULT NULL,
  `DST` varchar(15) DEFAULT NULL,
  `LEN` int(11) DEFAULT NULL,
  `SPT` int(11) DEFAULT NULL,
  `DPT` int(11) DEFAULT NULL,
  KEY `IN` (`IN`,`OUT`,`SRC`,`DST`),
  KEY `SPT` (`SPT`,`DPT`)
)
</pre>

Basic usage
=======

Syntax:

<pre>
python ipl2sql &lt;logfile&gt; &lt;table_name&gt;
</pre>

...where logfile is a iptables log file(see demo.log), and table_name is a name of table which will be used in DELETE and INSERT statements.

<pre>
python ipl2sql iptables.log packets &gt; packets.sql
mysql iptables &lt; packets.sql
</pre>

.. or a simpler way:
<pre>
python ipl2sql iptables.log packets | mysql iptables
</pre>
