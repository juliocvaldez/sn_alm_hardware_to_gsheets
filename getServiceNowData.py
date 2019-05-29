import os
import json
import pysnow as snow


def getServiceNowData(creds):
    # Takes care of refreshing the token storage if needed
    store = {'token': None}

    def updater(new_token):
        print("OAuth token refreshed!")
        store['token'] = new_token

    # Create the OAuthClient with the ServiceNow provided `client_id` and `client_secret`, and a `token_updater`
    # function which takes care of refreshing local token storage.
    CLIENT = snow.OAuthClient(
        client_id=creds['CLIENT_ID'],
        client_secret=creds['CLIENT_SECRET'],
        token_updater=updater,
        instance=creds['INSTANCE']
    )

    if not store['token']:
      # No previous token exists. Generate new.
        store['token'] = CLIENT.generate_token(
            creds['USERNAME'], creds['PASSWORD'])

    # Set the access / refresh tokens
    CLIENT.set_token(store['token'])

    # Define fields to pull from table
    FIELDS = [
        'asset_tag',
        'ci.host_name',
        'ci.mac_address',
        'company',
        'cost',
        'department',
        'display_name',
        # 'end_of_depreciation',
        # 'end_of_life_year',
        'install_date',
        'install_status',
        'invoice_number',
        'location',
        'model',
        'model.depreciation',
        'model.manufacturer',
        'model_category',
        'po_number',
        'purchase_date',
        'residual',
        'retired',
        'retirement_date',
        'serial_number',
        'substatus',
        'u_business_services',
        'u_uc_property_tag'
    ]

    # Build query
    qb = (
        snow.QueryBuilder()
            .field('company.name').equals('INFR')
            .OR()
            .field('company.name').equals('NCS')
            .OR()
            .field('company.name').equals('EUC')
            .AND()
            .field('company').order_ascending()
            .AND()
            .field('display_name').order_ascending()
    )

    # Define a resource, here we'll use the Hardware Assets table API
    assets = CLIENT.resource(api_path='/table/alm_hardware')

    # Set request paramaters
    assets.parameters.display_value = True
    assets.parameters.exclude_reference_link = True

    # Query for assets
    SNDATA = assets.get(query=qb, stream=True, fields=FIELDS)

    # Iterate over the result and
    SNDATALIST = []
    for record in SNDATA.all():
        SNDATALIST.append(record)

    return SNDATALIST
