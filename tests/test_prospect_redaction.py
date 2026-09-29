import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile, get_prospect


SENSITIVE_KEYS = {"billing_qualification", "tax_id", "date_of_birth", "card_on_file", "credit_check_ref"}


def keys_in(value):
    if isinstance(value, dict):
        return set(value) | {key for item in value.values() for key in keys_in(item)}
    if isinstance(value, list):
        return {key for item in value for key in keys_in(item)}
    return set()


def test_prospect_tools_exclude_billing_identity_fields_for_every_prospect():
    data_service._PROFILES.clear()

    for prospect_id in data_service.PROSPECTS:
        contact_result = get_prospect.invoke(prospect_id)
        profile_result = build_prospect_profile.invoke(prospect_id)

        assert SENSITIVE_KEYS.isdisjoint(keys_in(contact_result))
        assert SENSITIVE_KEYS.isdisjoint(keys_in(profile_result))
        assert SENSITIVE_KEYS.isdisjoint(keys_in(data_service._PROFILES[prospect_id]))
