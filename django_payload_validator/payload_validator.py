from base_payload_validator import BasePayloadValidator


class CreateTeamValidator(BasePayloadValidator):

    validation_rule = {
        'fields': {
         'name': {'type': str, 'required': True},
         'description': {'type': str, 'required': True},
         'team_type': {'type': str, 'required': True, 'allowed_values': ['tech', 'management', 'business', 'marketing']},
         'members': {'type': list}
         },
        'auto_populate_fields': {'created_by': 'request.user', 'last_updated_by': 'request.user'},
        'excluded_fields': ['members']
        }
