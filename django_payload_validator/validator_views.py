from django.views.generic import View


class BaseValidatorView(View):
    """
    Override necessary methods to implement payload validation.
    """
    required_class_attrs = ['payload_validator']

    def __init__(self, **kwargs):
        """
        Overriding django's base view to make sure that all necessary parameters are either set or provided.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
        self._check_attrs()

    def _check_attrs(self):
        for class_attr in self.required_class_attrs:
            if not self.hasattr(class_attr):
                raise ('{class_attr} is a required property for {class_name}'.
                       format(class_attr=class_attr, class_name=self.__class__.__name__))

    def post(self, request, *args, **kwargs):
        """
        Override post method to make calls to payload_validator.is_valid() of payload_validator instead of
        form.is_valid().
        :param request: WSGI Request
        :return: Json serialized object if validation passes
        errors as json if validation fails.
        """
        if self.payload_validator.is_valid():
            return self.payload_validator.json_valid()
        return self.payload_validator.json_invalid()
