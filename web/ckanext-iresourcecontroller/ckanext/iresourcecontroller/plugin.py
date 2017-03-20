# encoding: utf-8
import hmac
from hashlib import sha1
from time import time
import ckan.plugins as plugins
from urlparse import urlparse


class ExampleIResourceControllerPlugin(plugins.SingletonPlugin):

    plugins.implements(plugins.IResourceController)

    def before_show(self, resource):
        """
        Set the url to a tempurl
        :param resource:
        :return:
        """
        duration_in_seconds = 60*10
        expires = int(time() + duration_in_seconds)
        parsed_url = urlparse(resource['url'])

        if parsed_url.netloc == 'data.amsterdam.nl':
            object_store_url = 'https://e85bcf2124fb4437b1bc6eb75dfc3abf.objectstore.eu'

            key = 'my_secret_seed'
            hmac_body = '%s\n%s\n%s' % ('GET', expires, parsed_url.path)
            sig = hmac.new(key, hmac_body, sha1).hexdigest()

            resource['url'] = '{}{}?{}&tempurl_sig={}&tempurl_expires={}'.format(
                object_store_url, parsed_url.path, parsed_url.query, sig, expires)
