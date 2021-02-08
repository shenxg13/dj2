from abc import ABC

import haystack
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from elasticsearch import NotFoundError
from haystack.backends.elasticsearch2_backend import Elasticsearch2SearchBackend, Elasticsearch2SearchEngine


class ConfigurableElasticBackend(Elasticsearch2SearchBackend, ABC):
    """
    Extends the Haystack ElasticSearch backend to allow configuration of index
    mappings and field-by-field analyzers.
    """
    DEFAULT_ANALYZER = "snowball"
    DEFAULT_NGRAM_SEARCH_ANALYZER = None

    def __init__(self, connection_alias, **connection_options):
        super(ConfigurableElasticBackend, self).__init__(connection_alias, **connection_options)

        # user index settings

        global_settings_dict = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS', None)
        if global_settings_dict:
            if 'settings' in global_settings_dict and 'SETTINGS_NAME' in connection_options:
                raise ImproperlyConfigured("You cannot specify ELASTICSEARCH_INDEX_SETTINGS['settings'] in settings "
                                           "and also 'SETTINGS_NAME' in your index connection '%s'. "
                                           "Use only one configuration way." % connection_alias)

            user_settings = None
            if 'settings' in global_settings_dict:
                user_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS', None)
            if 'SETTINGS_NAME' in connection_options:
                settings_name = connection_options.get('SETTINGS_NAME', None)
                if settings_name not in global_settings_dict:
                    raise ImproperlyConfigured("'SETTINGS_NAME' '%s' is missing in ELASTICSEARCH_INDEX_SETTINGS dict."
                                               % settings_name)
                user_settings = global_settings_dict.get(settings_name)

            if user_settings:
                setattr(self, 'DEFAULT_SETTINGS', user_settings)

        # user settings of analyzers

        if hasattr(settings, 'ELASTICSEARCH_DEFAULT_ANALYZER') and 'DEFAULT_ANALYZER' in connection_options:
            raise ImproperlyConfigured("You cannot specify ELASTICSEARCH_DEFAULT_ANALYZER in settings "
                                       "and also 'DEFAULT_ANALYZER' in your index connection '%s'. "
                                       "Use only one configuration way." % connection_alias)

        if hasattr(settings, 'ELASTICSEARCH_DEFAULT_NGRAM_SEARCH_ANALYZER') \
                and 'DEFAULT_NGRAM_SEARCH_ANALYZER' in connection_options:
            raise ImproperlyConfigured("You cannot specify ELASTICSEARCH_DEFAULT_NGRAM_SEARCH_ANALYZER in settings "
                                       "and also 'DEFAULT_NGRAM_SEARCH_ANALYZER' in your index connection '%s'. "
                                       "Use only one configuration way." % connection_alias)

        user_analyzer = getattr(settings, 'ELASTICSEARCH_DEFAULT_ANALYZER', None) \
            or connection_options.get('DEFAULT_ANALYZER', None)
        ngram_search_analyzer = getattr(settings, 'ELASTICSEARCH_DEFAULT_NGRAM_SEARCH_ANALYZER', None) or \
            connection_options.get('DEFAULT_NGRAM_SEARCH_ANALYZER', None)
        if user_analyzer:
            setattr(self, 'DEFAULT_ANALYZER', user_analyzer)
        if ngram_search_analyzer:
            setattr(self, 'DEFAULT_NGRAM_SEARCH_ANALYZER', ngram_search_analyzer)

    def setup(self):
        try:
            self.existing_mapping = self.conn.indices.get_mapping(index=self.index_name)
        except NotFoundError:
            pass
        except Exception:
            if not self.silently_fail:
                raise

        unified_index = haystack.connections[self.connection_alias].get_unified_index()
        self.content_field_name, field_mapping = self.build_schema(unified_index.all_searchfields())
        current_mapping = {
            'modelresult': {
                "_source": {
                    "excludes": [
                        "text",
                    ]
                },
                "_all": {
                    "enabled": 'false'
                },
                'properties': field_mapping,
            }
        }

        if current_mapping != self.existing_mapping:
            try:
                # Make sure the index is there first.
                self.conn.indices.create(index=self.index_name, body=self.DEFAULT_SETTINGS, ignore=400)
                self.conn.indices.put_mapping(index=self.index_name, doc_type='modelresult', body=current_mapping)
                self.existing_mapping = current_mapping
            except Exception:
                if not self.silently_fail:
                    raise

        self.setup_complete = True

    def build_schema(self, fields):
        content_field_name, mapping = super(ConfigurableElasticBackend, self).build_schema(fields)

        for field_name, field_class in fields.items():
            field_mapping = mapping[field_class.index_fieldname]

            if field_mapping['type'] == 'string' and field_class.indexed:
                if not hasattr(field_class, 'facet_for') and field_class.field_type not in ('ngram', 'edge_ngram'):
                    field_mapping['analyzer'] = getattr(field_class, 'analyzer', self.DEFAULT_ANALYZER)
                if not hasattr(field_class, 'facet_for') \
                   and field_class.field_type in ('ngram', 'edge_ngram') \
                   and self.DEFAULT_NGRAM_SEARCH_ANALYZER:
                    field_mapping['search_analyzer'] = getattr(field_class, 'search_analyzer',
                                                               self.DEFAULT_NGRAM_SEARCH_ANALYZER)
            mapping.update({field_class.index_fieldname: field_mapping})
        return content_field_name, mapping


class ConfigurableElasticSearchEngine(Elasticsearch2SearchEngine):
    backend = ConfigurableElasticBackend
