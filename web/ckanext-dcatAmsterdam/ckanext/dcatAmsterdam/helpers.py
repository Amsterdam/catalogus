import logging

import ckan.model as model

log = logging.getLogger(__name__)


def get_tracking_summary(package):
    # page-view tracking summary data
    package['tracking_summary'] = (
        model.TrackingSummary.get_for_package(package['id']))

    return package['tracking_summary']
