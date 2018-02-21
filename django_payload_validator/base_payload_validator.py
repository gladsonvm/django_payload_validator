from response.response import Response
from django.http import JsonResponse
from operator import attrgetter
import json


class BasePayloadValidator(object):
    """
    This class bounds all methods necessary to validate request data and provide a formatted output
    """
    error_dict = dict()

    def validate_request_data(self):
        """
        This method is the entry point for BasePayloadValidator and provided formatted data after successful validation.
        :return: None if validation passes if any one validation fails, then appropriate error msg.
        """
        validators = [self.validate_request_body, self.validate_mandatory_params, self.validate_allowed_params]
        if hasattr(self, 'validators'):
            if type(self.validators) is list:
                validators = validators + self.validators
            else:
                raise TypeError('Validators provided in %s must be a list', self.__class__.__name__)

        for validator in validators:
            validation_result = validator()
            if validation_result[0]:
                pass
            else:
                self.error_dict.update(validation_result[1])
                return False
        return True

    def validate_mandatory_params(self):
        """
        This method checks if all mandatory params are there in a given json.
        :return: False and error msg if validation fails else True.
        """
        mandatory_params = self.get_mandatory_param()
        if mandatory_params:
            if len([x for x in mandatory_params if x not in list(self.data)]):
                return False, {'error': 'mandatory params missing. mandatory parameters are {mandatory_params}'
                                        .format(mandatory_params=mandatory_params)}
        return True,

    def validate_request_body(self):
        """
        This method checks if a given request body is a valid json.
        :return: False and error msg if validation fails else True.
        """
        try:
            self.data = json.loads(self.request.body.decode('UTF-8'))
        except:
            return False, {'error': 'provide a valid json.'}
        return True,

    def validate_allowed_params(self):
        """
        check if any invalid params are in request body.
        :return: False and error msg if validation fails else True.
        """
        allowed_params = self.get_all_params()
        sorted_request_params = sorted(list(self.data))
        sorted_allowed_params = sorted(allowed_params)
        invalid_params = [x for x in sorted_request_params if x not in sorted_allowed_params]
        if invalid_params:
            return False, {'error': 'invalid params found in request body. invalid parameters are {invalid_params}'
                .format(invalid_params=invalid_params)}
        return True,

    def get_validation_rule(self):
        """
        return validation rule specified in inherited class.
        :return: self.validation rule, a json.
        """
        return self.validation_rule

    def is_valid(self):
        """
        check if json data in request is valid or not.
        :return: validation results
        """
        validation_response = self.validate_request_data()
        return validation_response

    def json_valid(self):
        """
        triggered if a json is validated successfully against a given rule.
        :return: json serialized object after saving it to database.
        """
        self.object = self.save()
        return JsonResponse(self.render_json(self.object, status_code=201))

    def json_invalid(self):
        """
        invoked if a json is not validated successfully against a given rule.
        :return: errors as json
        """
        return JsonResponse(self.error_dict, status=400)

    def get_mandatory_param(self):
        """
        Return mandatory parameters in validation rule.
        :return: all mandatory params in validation rule
        if rule have mandatory params else None.
        """
        mandatory_params = [k for k, v in self.validation_rule.get('fields').items()
                            if self.validation_rule.get(k).get('required') is not None]

        return mandatory_params if mandatory_params else None

    def get_all_params(self):
        """
        Returns all params given in a validation rule.
        :return: all params in a given validation rule
        """
        return list(self.validation_rule['fields'])

    def save(self, data=None):
        """
        Create an entry in database after successful validation.
        auto_populate_fields can be mentioned in inherited class.
        :param data: extra data if needed.
        :return: object corresponding to database entry.
        """
        data = data if data else self.data
        if hasattr(self, 'auto_populate_fields'):
            data.update({k: attrgetter(v)(self) for k, v in self.auto_populate_fields.items()})
        self.instance = self.model.objects.create(**data)
        return self.instance

    def render_json(self, obj, status_code):
        """
        returns json serialized objects
        :param obj: an object corresponding to a database entry.
        :return: json serialized objects.
        """

        return Response.get_formatted_response(Response(request=self.request, data=[obj]))

