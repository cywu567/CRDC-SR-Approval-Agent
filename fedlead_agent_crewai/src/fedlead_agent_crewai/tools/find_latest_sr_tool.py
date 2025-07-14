from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from fedlead_agent_crewai.utils.session_manager import get_page, set_page
from fedlead_agent_crewai.utils.smart_click import smart_click
from fedlead_agent_crewai.utils.log_utils import log_tool_execution


class FindLatestSubmissionInput(BaseModel):
    submitter_name: str = Field(..., description="Submitter name to search (e.g. 'crdc.cw4')")


class FindLatestSubmissionTool(BaseTool):
    name: str = "review_latest_submission"
    description: str = "Searches for the submitter and clicks the first 'Review' button for their latest submission."
    args_schema: Type[BaseModel] = FindLatestSubmissionInput

    def _run(self, submitter_name: str) -> str:
        input_data = {"submitter_name": submitter_name}

        try:
            page = get_page()
            page.wait_for_timeout(1000)

            search_box = page.query_selector("input[placeholder*='Minimum 3 characters required']")
            if not search_box:
                output = "Could not find the Submitter Name search input box."
                raise Exception(output)

            search_box.fill(submitter_name)
            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)

            goal = f"Click the Review button for the latest submission by {submitter_name}"
            click_result = smart_click(page, goal)

            set_page(page)
            return f"Attempted smart_click for '{submitter_name}' submission. Result: {click_result} | URL: {page.url}"

        except Exception as e:
            log_tool_execution(
                tool_name="review_latest_submission",
                input_data=input_data,
                output_data=None,
                status="error",
                error_message=str(e)
            )
            return f"ReviewLatestSubmissionTool error: {str(e)}"
