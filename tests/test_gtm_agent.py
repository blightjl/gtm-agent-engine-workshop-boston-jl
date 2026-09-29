import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from gtm_agent.gtm_agent import send_prospect_email
from gtm_agent.gtm_records import PROSPECTS


class SendProspectEmailTest(unittest.TestCase):
    def test_disqualified_prospects_are_blocked(self):
        for prospect_id in (
            "LEAD-50001",
            "LEAD-50002",
            "LEAD-50003",
            "LEAD-50004",
            "LEAD-50005",
        ):
            result = send_prospect_email.func(
                {"prospect_id": prospect_id, **PROSPECTS[prospect_id]},
                "Follow-up",
                "Hello",
                runtime=None,
                from_rep={},
            )
            self.assertEqual(
                result,
                {
                    "status": "blocked",
                    "reason": "prospect is disqualified",
                    "prospect_id": prospect_id,
                },
            )

    def test_non_disqualified_prospect_is_sent(self):
        prospect_id = "LEAD-15229"
        result = send_prospect_email.func(
            {"prospect_id": prospect_id, **PROSPECTS[prospect_id]},
            "Follow-up",
            "Hello",
            runtime=None,
            from_rep={},
        )
        self.assertEqual(result["status"], "sent")


if __name__ == "__main__":
    unittest.main()
