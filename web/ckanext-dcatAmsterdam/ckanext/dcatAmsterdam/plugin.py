import logging

import ckan.lib.search as search
import ckan.plugins as p
import ckan.plugins.toolkit as tk

import helpers as helpers

log = logging.getLogger('ckan.logic')

# Uncomment for translations
try:
    from ckan.lib.plugins import DefaultTranslation
except ImportError:
    class DefaultTranslation():
        pass


class DCATAmsterdam(p.SingletonPlugin, DefaultTranslation, tk.DefaultDatasetForm):
    # Uncomment to activate the translations
    # TRANSLATIONS BUG: --> http://stackoverflow.com/questions/36038176/ckan-error-after-enabling-harvester-module-module-object-has-no-attribute-i
    if tk.check_ckan_version(min_version='2.5.0'):
        p.implements(p.ITranslation, inherit=False)
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.ITemplateHelpers)

    ######################################################################
    ############################ DATASET FORM ############################
    ######################################################################

    def __init__(self, name=None):
        self.name = 'dcatAmsterdam'
        self.indexer = search.PackageSearchIndex()

    def _modify_package_schema(self):
        # Add our metadata fields to the package schema
        schema = super(DCATAmsterdam, self).create_package_schema()
        schema.update({
            'language': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'publisher_uri': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'contact_email': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'contact_name': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'contact_uri': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'frequency': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'publisher_email': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'spatial': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'temporal': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'theme': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'version_notes': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'dataclassificatie': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'tijdseenheid': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')],
            'gebiedseenheid': [tk.get_validator('ignore_missing'), tk.get_converter('convert_to_extras')]
        })
        # Add our metadata fields to the resource schema
        schema['resources'].update({
            'type': [tk.get_validator('ignore_missing')]
        })
        return schema

    def create_package_schema(self):
        # grab the default schema in our plugin
        schema = super(DCATAmsterdam, self).create_package_schema()
        schema.update(self._modify_package_schema())
        return schema

    def update_package_schema(self):
        # grab the default schema in our plugin
        schema = super(DCATAmsterdam, self).update_package_schema()
        schema.update(self._modify_package_schema())
        return schema

    def show_package_schema(self):
        schema = super(DCATAmsterdam, self).show_package_schema()
        schema.update({
            'language': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'publisher_uri': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'contact_email': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'contact_name': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'contact_uri': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'frequency': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'publisher_email': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'spatial': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'temporal': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'theme': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'version_notes': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'dataclassificatie': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'tijdseenheid': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')],
            'gebiedseenheid': [tk.get_converter('convert_from_extras'), tk.get_validator('ignore_missing')]
        })

        schema['resources'].update({
            'type': [tk.get_validator('ignore_missing')]
        })

        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    ######################################################################
    ############################ ICONFIGURER #############################
    ######################################################################

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')

        # Register this plugin's fanstatic directory with CKAN.
        tk.add_resource('fanstatic', 'dcatAmsterdam')

    ######################################################################
    ######################### IPACKAGECONTROLLER #########################
    ######################################################################

    def before_index(self, pkg_dict):
        return pkg_dict

    def after_create(self, context, pkg_dict):
        return pkg_dict

    def after_update(self, context, pkg_dict):
        return self.after_create(context, pkg_dict)

    def after_show(self, context, pkg_dict):
        return pkg_dict

    def after_delete(self, context, pkg_dict):
        return pkg_dict

    def after_search(self, search_results, search_params):
        return search_results

    ######################################################################
    ######################### ITEMPLATESHELPER ###########################
    ######################################################################

    def get_helpers(self):
        return {
            'get_tracking_summary': helpers.get_tracking_summary
        }
