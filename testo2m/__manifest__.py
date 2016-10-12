# -*- coding: utf-8 -*-

{
    'name': 'Test O2M Widget',
    'sequence': 120,
    'version': '1.0',
    'depends': ['base', 'sale'],
    'category': 'Sales',
    'summary': 'Test for nested O2M Relations',
    'description': """
This is a test module for relations.
================================
    """,
    'data': ['views/o2m_test.xml',
             'security/ir.model.access.csv'],
    'qweb': [],
    'installable': True,
}
