# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentcard.py:7
# Component id: at.source.a1_at_functions.testvalidateagentcard
from __future__ import annotations

__version__ = "0.1.0"

class TestValidateAgentCard:
    def test_valid_minimal_card(self) -> None:
        data = {"name": "TestAgent"}
        report = validate_agent_card(data)
        assert report.valid
        assert report.card is not None
        assert report.card.name == "TestAgent"

    def test_valid_full_card(self) -> None:
        data = {
            "name": "FullAgent",
            "description": "A complete agent",
            "url": "https://example.com",
            "version": "1.0.0",
            "provider": {"organization": "TestOrg", "url": "https://testorg.com"},
            "capabilities": {"streaming": True, "pushNotifications": False, "stateTransitionHistory": True},
            "authentication": {"schemes": ["bearer"]},
            "skills": [
                {"id": "skill1", "name": "Skill One", "description": "Does things"},
            ],
            "defaultInputModes": ["text/plain"],
            "defaultOutputModes": ["text/plain", "application/json"],
        }
        report = validate_agent_card(data)
        assert report.valid
        assert report.card is not None
        assert report.card.name == "FullAgent"
        assert report.card.capabilities.streaming is True
        assert len(report.card.skills) == 1
        assert report.card.skills[0].id == "skill1"

    def test_missing_name_is_error(self) -> None:
        data = {"description": "no name"}
        report = validate_agent_card(data)
        assert not report.valid
        assert any(i.severity == "error" for i in report.issues)

    def test_empty_name_is_error(self) -> None:
        data = {"name": "   "}
        report = validate_agent_card(data)
        assert not report.valid

    def test_missing_description_is_warning(self) -> None:
        data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0"}
        report = validate_agent_card(data)
        assert report.valid
        assert any(i.severity == "warning" and i.field == "description" for i in report.issues)

    def test_missing_url_is_warning(self) -> None:
        data = {"name": "TestAgent", "description": "desc"}
        report = validate_agent_card(data)
        assert report.valid
        assert any(i.severity == "warning" and i.field == "url" for i in report.issues)

    def test_invalid_url_scheme_is_error(self) -> None:
        data = {"name": "TestAgent", "url": "ftp://bad.com"}
        report = validate_agent_card(data)
        assert not report.valid
        assert any("scheme" in i.message for i in report.errors)

    def test_missing_version_is_warning(self) -> None:
        data = {"name": "TestAgent", "url": "https://example.com"}
        report = validate_agent_card(data)
        assert any(i.severity == "warning" and i.field == "version" for i in report.issues)

    def test_no_skills_is_warning(self) -> None:
        data = {"name": "TestAgent", "url": "https://example.com", "version": "1.0", "description": "desc"}
        report = validate_agent_card(data)
        assert any(i.severity == "warning" and i.field == "skills" for i in report.issues)

    def test_skill_missing_id_is_error(self) -> None:
        data = {
            "name": "TestAgent",
            "url": "https://example.com",
            "version": "1.0",
            "skills": [{"id": "", "name": "Skill One"}],
        }
        report = validate_agent_card(data)
        assert not report.valid

    def test_skill_missing_name_is_error(self) -> None:
        data = {
            "name": "TestAgent",
            "url": "https://example.com",
            "version": "1.0",
            "skills": [{"id": "s1", "name": ""}],
        }
        report = validate_agent_card(data)
        assert not report.valid

    def test_auth_no_schemes_is_warning(self) -> None:
        data = {"name": "TestAgent", "authentication": {"schemes": []}}
        report = validate_agent_card(data)
        assert any(i.severity == "warning" and "schemes" in i.field for i in report.issues)
