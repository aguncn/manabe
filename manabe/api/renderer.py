from rest_framework.renderers import JSONRenderer


class Utf8JSONRenderer(JSONRenderer):
    charset = 'utf-8'
