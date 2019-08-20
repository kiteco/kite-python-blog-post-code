from django.http import JsonResponse


class JsonResponseMixin(object):
    """
    JsonResponse that can be dropped into class-based views relying on render_to_response
    """
    response_class = JsonResponse
    response_parser_kwargs = {}

    def get_response_kwargs(self):
        """
        Override this in your child class if you need to add kwargs to your response_class

        :return: the keyword arguments for instantiating the response_class
        """
        return self.response_parser_kwargs

    def render_to_response(self, context):
        """
        Cache context on the instance and return the response through the response_class
        """
        self.context = context
        return self.response_class(self.get_response(), **self.get_response_kwargs())
