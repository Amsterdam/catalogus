import logging
import os

import authorization_levels
import ckan.authz as authz
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import jwt
import pylons
from ckan.lib.base import _
from ckan.logic.auth import (
    get_package_object
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def authz_package_show(context, data_dict):
    """
    data_dict params
        id: the id or name of the dataset
        use_default_schema: use default package schema instead of
                            a custom schema defined with an IDatasetForm
                            plugin (default: False)

        include_tracking: add tracking information to dataset and
                          resources (default: False)
    :rtype: dictionary
    """


    user = context.get('user')
    package = get_package_object(context, data_dict)
    # draft state indicates package is still in the creation process
    # so we need to check we have creation rights.
    authorized = None
    if package.state.startswith('draft'):
        auth = authz.is_authorized('package_update', context, data_dict)
        authorized = auth.get('success')
    elif package.owner_org is None and package.state == 'active':
        return {'success': True}
    else:
        authorized = toolkit.c.user in ['employee', 'employee_plus']

    if package.private:
        if authorized and package.state == 'active':
            # Intern, beperkt
            # TC: Find out where to get to the field dataclassificatie
            # if authorized and package.dataclassificatie == 'Intern, beperkt' and package.state == 'active':
            #     if toolkit.c.user == 'employee_plus':
            #         return {'success': True}
            #     else:
            #         return {'success': False,
            #                 'msg': _('User %s not authorized to read package %s') % (user, package.id)}
            #
            # ## Intern
            # TC: Find out where to get to the field dataclassificatie
            # if authorized and package.dataclassificatie == 'Intern' and package.state == 'active':
            #     return {'success': True}
            #
            return {'success': True}
        else:
            return {'success': False,
                    'msg': _('User %s not authorized to read package %s') % (user, package.id)}

    else:
        # anyone can see a public package
        if package.state == 'active':
            return {'success': True}

    return {'success': False,
            'msg': _('User %s not authorized to read package %s') % (user, package.id)}


class IauthfunctionsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.IAuthFunctions)

    def login(self):
        """
        Implementation of IAuthenticator.login
        We don't need to do anything here as we provide a JWT token with all info
        """
        pass

    def logout(self):
        """
        Implementation of IAuthenticator.login
        We don't need to do anything here as we provide a JWT token with all info
        """
        pass

    def identify(self):
        """
        Implementiation of IAuthenticator.identify
        Identify which user (if any) is logged in via DatapuntAmsterdam / auth
        """
        toolkit.c.user = 'open'
        if pylons.request.headers.get('Authorization'):
            try:
                prefix, jwt_token = pylons.request.headers.get('Authorization').split()
            except ValueError:
                log.error('Authorization header must have format: Bearer [JWT]')

            if prefix != 'Bearer':
                log.error('Authorization header prefix must be Bearer')

            try:
                jwt_payload = jwt.decode(
                    jwt_token,
                    os.getenv('JWT_SHARED_SECRET_KEY'),
                    algorithms=['HS256'])

                if jwt_payload.get('authz') == authorization_levels.LEVEL_EMPLOYEE:
                    # dataclassificatie == 'Intern'
                    toolkit.c.user = 'employee'
                elif jwt_payload.get('authz') == authorization_levels.LEVEL_EMPLOYEE_PLUS:
                    # dataclassificatie == 'Intern + Intern, beperkt'
                    toolkit.c.user = 'employee_plus'
            except:
                log.error('Decode of authorization token failed, check secret key')

        return toolkit.c.user

    def get_auth_functions(self):
        """
        IAuthFunctions
        :return:
        """
        toolkit.c.user = 'employee_plus'
        return {
            'package_show': authz_package_show
        }
