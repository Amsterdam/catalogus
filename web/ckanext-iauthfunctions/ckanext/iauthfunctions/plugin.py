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
    user = context.get('user')
    package = get_package_object(context, data_dict)

    # draft state indicates package is still in the creation process
    # so we need to check we have creation rights.
    if package.state.startswith('draft'):
        auth = authz.is_authorized('package_update',
                                   context, data_dict)
        authorized = auth.get('success')
    elif package.owner_org is None and package.state == 'active':
        return {'success': True}
    else:
        # anyone can see a public package
        if not package.private and package.state == 'active':
            return {'success': True}
        authorized = toolkit.c.user in ['employee', 'employee_plus']
    if not authorized:
        return {'success': False,
                'msg': _('User %s not authorized to read package %s') % (user, package.id)}
    else:
        return {'success': True}


class IauthfunctionsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IAuthenticator)
    plugins.implements(plugins.IAuthFunctions)

    def login(self):
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
            # when JWT can be decoded user is authenticated
            try:
                jwt_payload = jwt.decode(
                    pylons.session.get('Authorization'),
                    os.getenv('JWT_SHARED_SECRET_KEY', 'insecure'),
                    algorithms=['HS256']
                )
                if jwt_payload.get('authz') == authorization_levels.LEVEL_EMPLOYEE:
                    # dataclassificatie == 'Intern'
                    toolkit.c.user = 'employee'
                elif jwt_payload.get('authz') == authorization_levels.LEVEL_EMPLOYEE_PLUS:
                    # dataclassificatie == 'Intern + Intern, beperkt'
                    toolkit.c.user = 'employee_plus'
            except:
                pass

        return toolkit.c.user

    def get_auth_functions(self):
        """
        IAuthFunctions
        :return:
        """
        return {
            'package_show': authz_package_show
        }
