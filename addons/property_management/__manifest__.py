{
    'name': 'Property Management',
    'version': '1.0',
    'summary': 'Simple property structure',
    'author': 'Keem',
    'category': 'Real Estate',

    'depends': [
        'base',
        'contacts'
    ],

    'data': [

        'security/ir.model.access.csv',

        'views/property_views.xml',
        'views/unit_views.xml',

        'views/contact_views.xml',

    ],

    'installable': True,
    'application': True,
}
