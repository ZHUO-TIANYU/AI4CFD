from ansys.aedt.core import Icepak
from openai import OpenAI
import json
import os
import sys

# =====================================================================
# 🌟 User Configuration
# Modify these settings to match your LLM provider.
# =====================================================================

# LLM API Settings (e.g., OpenAI, DeepSeek, Moonshot)
MY_API_KEY = "sk-your_api_key_here"  # Enter your real API Key here
MY_BASE_URL = "https://api.openai.com/v1" # Default is OpenAI format
MY_MODEL_NAME = "gpt-4o"                  # Enter your model name

# Quick Reference for Popular LLMs:
# - DeepSeek:  MY_BASE_URL = "https://api.deepseek.com", MY_MODEL_NAME = "deepseek-chat"
# - Moonshot:  MY_BASE_URL = "https://api.moonshot.cn/v1", MY_MODEL_NAME = "moonshot-v1-8k"
# - Aliyun:    MY_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1", MY_MODEL_NAME = "qwen-plus"
# - OpenAI:    MY_BASE_URL = "https://api.openai.com/v1", MY_MODEL_NAME = "gpt-4o"
# =====================================================================

def main():
    # Get file path (prompt if user runs it directly)
    if len(sys.argv) > 1:
        project_path = sys.argv[1].strip('"').strip("'")
    else:
        print("=======================================")
        print("  Ansys Icepak AI Inspection Tool")
        print("=======================================")
        project_path = input("Enter the absolute path to your .aedt file (e.g., F:\\Icepack\\Project1.aedt):\n> ").strip('"').strip("'")

    if not project_path or not os.path.exists(project_path):
        print(f"❌ Error: File not found - {project_path}. Please check the path.")
        return

    # Check if the user has entered a real API Key
    if "your_api_key" in MY_API_KEY or MY_API_KEY == "":
        print("⚠️ Warning: You haven't set a real API Key in icepak.py. Skipping AI inspection.")

    print(f"\n=== Connecting to AEDT and opening project: {project_path} ===")

    # Connect to Ansys
    try:
        app = Icepak(
            project=project_path, 
            version="2025.2", 
            non_graphical=False, 
            new_desktop=False,
            close_on_exit=False
        )
    except Exception as e:
        print(f"❌ Failed to connect to Ansys. Ensure Ansys is running and the path is valid. Error: {e}")
        return

    # Extract component data
    report_data = []
    print("=== Extracting component data ===")
    for obj_name in app.modeler.object_names:
        if obj_name == "Region": 
            continue
        obj = app.modeler[obj_name]
        report_data.append({
            "object_name": obj_name,
            "material": obj.material_name
        })

    print(f"=== Extracted {len(report_data)} components ===")

    # Exit if no API key is provided
    if "your_api_key" in MY_API_KEY or MY_API_KEY == "":
        return

    # Call AI for inspection
    print(f"\n=== Calling AI expert ({MY_MODEL_NAME}) for review (Please wait) ===")
    client = OpenAI(api_key=MY_API_KEY, base_url=MY_BASE_URL)

    prompt = f"""
    You are an extremely strict thermal simulation engineer. Below is a JSON list of components exported from an Ansys Icepak model.
    Due to Icepak's default settings, if a user forgets to assign a material to an object, it is silently set to "air".

    Please analyze this list and identify any objects whose names are physically mismatched with the "air" material (e.g., objects named chip, block, pcb, heatsink, but assigned as air). Provide troubleshooting advice.
    Output the results directly by listing the component names that need attention and the reasons. Do not include unnecessary fluff.

    Component Data:
    {json.dumps(report_data, indent=4)}
    """

    try:
        response = client.chat.completions.create(
            model=MY_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an extremely strict CFD engineer. Point out engineering errors directly without providing emotional comfort."},
                {"role": "user", "content": prompt}
            ]
        )
        print("\n=== AI Inspection Report ===")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"❌ AI API call failed: {e}")

if __name__ == "__main__":
    main()
