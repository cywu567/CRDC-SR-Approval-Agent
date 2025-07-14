from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from fedlead_agent_crewai.utils.session_manager import get_page
from fedlead_agent_crewai.utils.log_utils import log_tool_execution

class ApproveSRToolInput(BaseModel):
    pass

class ApproveSRTool(BaseTool):
    name: str = "approve_sr_tool"
    description: str = "Approves the submission request"
    args_schema: Type[BaseModel] = ApproveSRToolInput

    def _run(self) -> str:
        input_data = {}
        try:
            page = get_page()
            all_results = []

            while True:
                next_button = page.query_selector("button:has-text('Next')")
                if next_button and next_button.is_enabled():
                    next_button.click()
                    page.wait_for_timeout(1000)
                else:
                    break
            
            approve_button = page.query_selector("button:has-text('Approve')")
            approve_button.click()
            page.wait_for_timeout(1000)
            
            reason_box = page.query_selector('div[data-testid="review-comment"] textarea:not([aria-hidden="true"])')
            if not reason_box:
                return "Could not find the text box to give a reason for approval."
            reason_box.fill("testing")

            approve_button = page.query_selector("button:has-text('Confirm to Approve')")
            approve_button.click()
            page.wait_for_timeout(1500)
            
            popup = page.query_selector("div[role='dialog'], .MuiDialog-paper")
            if popup:
                modal_text = popup.inner_text().strip()

                log_tool_execution(
                    tool_name="approve_sr_tool",
                    input_data=input_data,
                    output_data={"modal_text": modal_text},
                    status="error",
                    error_message="Approval blocked by rejection modal"
                )
                return f"Approval failed with message: {modal_text}"

            return "Submission request approved"
        
        except Exception as e:
            log_tool_execution(
                tool_name="approve_sr_tool",
                input_data=input_data,
                output_data=None,
                status="error",
                error_message=str(e)
            )
            return f"ApproveSRTool error: {str(e)}"
