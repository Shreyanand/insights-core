"""
CatalinaOut - ``catalina.out`` logs for Tomcat
==============================================

"""

from .. import LogFileOutput, parser


@parser('catalina.out')
class CatalinaOut(LogFileOutput):
    """
    This parser reads all ``catalina.out`` files in the ``/var/log/tomcat*``
    directories.

    It uses the LogFileOutput base class.

    Note that the standard format of Catalina log lines spreads the information
    over two lines::

        Nov 10, 2015 8:52:38 AM org.apache.jk.common.MsgAjp processHeader
        SEVERE: BAD packet signature 18245
        Nov 10, 2015 8:52:38 AM org.apache.jk.common.ChannelSocket processConnection
        SEVERE: Error, processing connection
        SEVERE: BAD packet signature 18245
        Nov 10, 2015 8:52:38 AM org.apache.jk.common.ChannelSocket processConnection
        SEVERE: Error, processing connection
        Nov 10, 2015 4:55:48 PM org.apache.coyote.http11.Http11Protocol pause
        INFO: Pausing Coyote HTTP/1.1 on http-8080

    However, this parser only recognises single lines.

    When using this parser, consider using a filter or a scan method, e.g.::

        CatalinaOut.filters.append('BAD packet signature')
        CatalinaOut.keep_scan('bad_signatures', 'BAD packet signature')

    Example:
        >>> catalina = shared[CatalinaOut]
        >>> catalina.file_path
        '/var/log/tomcat/catalina.out'
        >>> catalina.file_name
        'catalina.out'
        >>> len(catalina.lines.get('SEVERE'))
        4
        >>> 'Http11Protocol pause' in catalina
        True
        >>> catalina.lines[0]
        'Nov 10, 2015 8:52:38 AM org.apache.jk.common.MsgAjp processHeader'
        >>> catalina.bad_signatures
        ['SEVERE: BAD packet signature 18245', 'SEVERE: BAD packet signature 18245']
        >>> from datetime import datetime
        >>> catalina.get_after(datetime(2015, 11, 10, 12, 00, 00))
        ['Nov 10, 2015 4:55:48 PM org.apache.coyote.http11.Http11Protocol pause',
         'INFO: Pausing Coyote HTTP/1.1 on http-8080']
    """
    def get_after(self, timestamp, lines=None):
        """
        Get a list of lines after the given time stamp.

        Parameters:
            timestamp(datetime.datetime): log lines after this time are
                returned.
            lines(list): the list of log lines to search (e.g. from a get).
                If not supplied, all available lines are searched.

        Returns:
            (list): The list of log lines with time stamps after the given
            date and time.  Lines after the time stamped lines are considered
            to be continuations of the previous line and are included if the
            previous line's timestamp is after the given timestamp.
        """
        return super(CatalinaOut, self).get_after(timestamp, lines, '%b %d, %Y %I:%M:%S %p')
