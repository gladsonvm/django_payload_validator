# Django payload validator
This package can validate data provided as payload in request body. This is similar to django forms, but only different being this works on json data provided throuogh body of a request rather than HTML forms.

### Usage

```
class TeamCreateView(JsonCreateView):
    model = <model>
    validation_rule = <validation_rule>
```

### Example

```
class TeamCreateView(JsonCreateView):
    model = Team
    validation_rule = create_team
```

### Concepts:

- ##### validation_rule
   - A validation rule defines all fields those are meant to be validated.
   - Validation rule is a dictionary which defines 
      * fields
        * all fields those are meant to be validated as a dict. Each fields must define its `type`. If a field is mandatory, then set `required` param to true in field declaration. 
      * auto populated fields
        * Fields those are not obtained from request data and must be updated in database.
      * excluded fields
        * Fields that should not be displayed in response. 
      
   example:
   ```
   create_team = {
    'fields': {
        'name': {'type': str, 'required': True},
        'description': {'type': str, 'required': True},
        'team_type': {'type': str, 'required': True, 'allowed_values': ['tech', 'management', 'business', 'marketing']},
        'members': {'type': list}
        },
    'auto_populate_fields': {'created_by': 'request.user', 'last_updated_by': 'request.user'},
    'excluded_fields': ['members']
    }
   ```
   
   
