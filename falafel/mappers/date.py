"""
date - Command
==============

This module provides processing for the output of the ``date`` command.
The specs handled by this command inlude::

    "date"                      : CommandSpec("/bin/date"),
    "date_utc"                  : CommandSpec("/bin/date --utc"),

Class ``Date`` parses the output of the ``date`` command.  Sample output of
this command looks like::

    Fri Jun 24 09:13:34 CST 2016

Class ``DateUTC`` parses the output of the ``date --utc`` command.  Output is
similar to the ``date`` command except that the `Timezone` column uses UTC.

All classes utilize the same base class ``DateMapper`` so the following
examples apply to all classes in this module.

Examples:
    >>> from falafel.mappers.date import Date, DateUTC
    >>> from falafel.tests import context_wrap
    >>> date_content = "Mon May 30 10:49:14 CST 2016"
    >>> shared = {Date: Date(context_wrap(date_content))}
    >>> date_info = shared[Date]
    >>> date_info.data
    'Mon May 30 10:49:14 CST 2016'
    >>> date_info.datetime is not None
    True
    >>> date_info.timezone
    'CST'

    >>> date_content = "Mon May 30 10:49:14 UTC 2016"
    >>> shared = {DateUTC: DateUTC(context_wrap(date_content))}
    >>> date_info = shared[DateUTC]
    >>> date_info.data
    'Mon May 30 10:49:14 UTC 2016'
    >>> date_info.datetime
    datetime.datetime(2016, 5, 30, 10, 49, 14)
    >>> date_info.timezone
    'UTC'
"""

import sys
from datetime import datetime

from .. import Mapper, mapper, get_active_lines


class DateParseException(Exception):
    pass


class DateMapper(Mapper):
    """Base class implementing shared code."""

    def parse_content(self, content):
        """
        Parses the output of the ``date`` and ``date --utc`` command.

        Sample: Fri Jun 24 09:13:34 CST 2016
        Sample: Fri Jun 24 09:13:34 UTC 2016

        Attributes
        ----------
        datetime: datetime.datetime
            A native datetime.datetime of the parsed date string
        timezone: str
            The string portion of the date string containing the timezone

        Raises:
            DateParseException: Raised if any exception occurs parsing the
            content.
        """
        self.data = get_active_lines(content, comment_char="COMMAND>")[0]
        parts = self.data.split()
        if not len(parts) == 6:
            msg = "Expected six date parts.  Got [%s]"
            raise DateParseException(msg % self.data)
        try:
            self.timezone = parts[4]
            no_tz = ' '.join(parts[:4]) + ' ' + parts[-1]
            self.datetime = datetime.strptime(no_tz, '%a %b %d %H:%M:%S %Y')
        except:
            raise DateParseException(self.data), None, sys.exc_info()[2]


@mapper("date")
class Date(DateMapper):
    """
    Class to parse ``date`` command output.

    Sample: Fri Jun 24 09:13:34 CST 2016
    """
    pass


@mapper("date_utc")
class DateUTC(DateMapper):
    """
    Class to parse ``date --utc`` command output.

    Sample: Fri Jun 24 09:13:34 UTC 2016
    """
    pass
