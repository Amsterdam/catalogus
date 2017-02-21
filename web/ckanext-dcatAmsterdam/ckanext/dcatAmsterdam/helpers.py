import ckan.model as model
import ckan.plugins.toolkit as tk
import db

from pylons import config

from ckan.common import request

import logging
log = logging.getLogger(__name__)

def get_tracking_summary(package):
    # page-view tracking summary data
    package['tracking_summary'] = (
        model.TrackingSummary.get_for_package(package['id']))

    return package['tracking_summary']
