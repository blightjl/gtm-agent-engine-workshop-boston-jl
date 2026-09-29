from gtm_agent import data_service


def test_update_prospect_info_persists_technology_and_invalidates_profile():
    prospect_id = "LEAD-39002"
    data_service.save_profile_to_db(
        prospect_id,
        {"prospect_id": prospect_id, "tech_stack": data_service.fetch_tech_stack(prospect_id)},
    )

    data_service.update_prospect_info(prospect_id, "Terraform")

    assert "Terraform" in data_service.fetch_tech_stack(prospect_id)
    profile = data_service.get_profile_from_db(prospect_id)["prospect_profile"]
    assert profile is None or "Terraform" in profile["tech_stack"]
