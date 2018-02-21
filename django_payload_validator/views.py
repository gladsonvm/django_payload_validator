from validator_views import BaseValidatorView
from payload_validator import CreateTeamValidator


class CreateTeam(BaseValidatorView):
    payload_validator = CreateTeamValidator
