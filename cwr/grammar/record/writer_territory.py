# -*- coding: utf-8 -*-

from data.accessor import CWRConfiguration
from cwr.grammar.field import special as field_special
from cwr.grammar.field import record as field_record
from cwr.grammar.field import society as field_society
from cwr.interested_party import IPTerritoryOfControlRecord
from cwr.grammar.factory.field import DefaultFieldFactory
from data.accessor import CWRTables


"""
CWR Writer Territory of Control (SWT) records grammar.
"""

__author__ = 'Bernardo Martínez Garrido'
__license__ = 'MIT'
__status__ = 'Development'

# Acquires data sources
_config = CWRConfiguration()
_lookup_factory = DefaultFieldFactory(_config.load_field_config('table'), CWRTables())
_common_factory = DefaultFieldFactory(_config.load_field_config('common'))

"""
General fields.
"""

"""
Patterns.
"""

territory = field_special.lineStart + \
            field_record.record_prefix(_config.record_type('writer_territory'), compulsory=True) + \
            _common_factory.get_field('ip_n') + \
            field_society.pr_share() + \
            field_society.mr_share() + \
            field_society.sr_share() + \
            _lookup_factory.get_field('ie_indicator') + \
            _lookup_factory.get_field('tis_code') + \
            _common_factory.get_field('shares_change') + \
            _common_factory.get_field('sequence_n') + \
            field_special.lineEnd

"""
Parsing actions for the patterns.
"""

territory.setParseAction(lambda p: _to_writerterritory(p))

"""
Parsing methods.

These are the methods which transform nodes into instances of classes.
"""


def _to_writerterritory(parsed):
    """
    Transforms the final parsing result into an IPTerritoryRecord instance.

    :param parsed: result of parsing the Territory record
    :return: an IPTerritoryRecord created from the parsed record
    """
    return IPTerritoryOfControlRecord(parsed.record_type, parsed.transaction_sequence_n, parsed.record_sequence_n,
                                      parsed.ip_n, parsed.ie_indicator, parsed.tis_code, parsed.sequence_n,
                                      parsed.pr_share, parsed.mr_share, parsed.sr_share, parsed.shares_change)