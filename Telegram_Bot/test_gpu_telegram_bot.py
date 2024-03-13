import subprocess
import psutil
import json
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

###################### INIT ######################
# Slack API token
SLACK_TOKEN = "YOUR_SLACK_TOKEN"
# Slack channel to send the message
SLACK_CHANNEL = "YOUR_SLACK_CHANNEL_ID"
# Lambda Labs API_KEY
LAMBDA_API_KEY = "YOUR_LAMBDALABS_API_KEY"
# Lambda Labs Instance ID
LAMBDA_INSTANCE_ID = "YOUR_LAMBDALABS_INSTANCE_ID"
# Get Slack client
client = WebClient(token=SLACK_TOKEN)

###################### GPU USAGE ######################
# 6秒間、平均GPU使用量を確認　
# Initialize the list for storing GPU usage
gpu_usages = []

# Loop for getting GPU usage for 6 times with 1-sec interval
for i in range(6):
    # Get GPU usage using nvidia-smi command
    gpu_usage = subprocess.check_output(
        ["nvidia-smi", "--query-gpu=utilization.gpu", "--format=csv"]
    ).decode("utf-8")
    # Extract GPU usage percentage from output
    gpu_usage = gpu_usage.split("\n")[1]
    # Append GPU usage to the list
    gpu_usages.append(float(gpu_usage[:-1]))
    # Sleep for 10 seconds before next check
    time.sleep(1)

# Get the average of GPU usage
avg_gpu_usage = sum(gpu_usages) / len(gpu_usages)

###################### TERMINATE INSTANCE ######################
try:
    # Send message(GPU Usage) to Slack channel
    message = f"Instace ID: {LAMBDA_INSTANCE_ID}\nGPU Usage: {avg_gpu_usage}"
    response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
    print("Message sent: ", message)

    # For Terminating the current Lambda labs instance
    if avg_gpu_usage == 0.0:
        # Send message(Terminate Lambda Labs instance) to Slack channel
        message = f"Terminating Lambda Labs instance {LAMBDA_INSTANCE_ID}"
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=message)
        print("Message sent: ", message)
        # Convert dictionary to JSON string
        _json = {"instance_ids": [f"{LAMBDA_INSTANCE_ID}"]}
        _json_str = json.dumps(_json)
        # Create Terminate Lambda Labs instance command
        command = [
            "curl",
            "-u",
            f"{LAMBDA_API_KEY}:",
            "https://cloud.lambdalabs.com/api/v1/instance-operations/terminate",
            "-d",
            _json_str,
            "-H",
            "Content-Type: application/json",
        ]
        # Terminate Lambda Labs instance
        output = subprocess.check_output(command).decode("utf-8")
        response = client.chat_postMessage(channel=SLACK_CHANNEL, text=output)
        print("Message sent: ", output)

except SlackApiError as e:
    print("Error sending message: {}".format(e))