import boto3
import uuid
from datetime import datetime, timezone

def log_tool_execution(tool_name, input_data, output_data, status="success", error_message=None, table="Approval-Agent-ToolFormLogs"):
    try:
        dynamodb = boto3.resource("dynamodb", region_name="us-east-2")
        table = dynamodb.Table(table)
        table.put_item(Item={
            "execution_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "tool_name": tool_name,
            "input_data": input_data,
            "output_data": output_data,
            "status": status,
            "error_message": error_message
        })
    except Exception as e:
        print(f"[log_tool_execution] Error logging tool run: {e}")
