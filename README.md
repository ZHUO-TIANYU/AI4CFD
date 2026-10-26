# AI4CFD
# Ansys Icepak AI Inspection Tool

A Python tool that connects to Ansys Icepak, extracts component materials, and uses an LLM (Large Language Model) to perform an engineering sanity check. It catches common human errors, like forgetting to assign a solid material to a component (which Icepak silently defaults to "air").

## Features
- Automatically connects to your currently running Ansys AEDT session.
- Extracts component names and their assigned materials.
- Uses an LLM of your choice to flag components that physically shouldn't be assigned as "air" (e.g., objects named `chip`, `heatsink`, `pcb`).
- Easy to run via command line or `.bat` file.

## Prerequisites
- **Ansys AEDT** installed and running.
- **Python 3.10+** installed on your system.
- An **API Key** from any OpenAI-compatible LLM provider (e.g., DeepSeek, OpenAI, Moonshot, Aliyun).

## 🚀 How to Use

### Step 1: Install Required Libraries！！！！！！！！！！
Open Command Prompt (CMD) or terminal and run:
```bash
pip install pyaedt openai -i https://pypi.tuna.tsinghua.edu.cn/simple
Step 2: Configure Your LLM API
Open icepak.py with any text editor (VS Code, Notepad, etc.).

Scroll to the top and find the User Configuration section.

Enter your API details:
# Fill in the API details of your chosen LLM provider
MY_API_KEY = "sk-your_api_key_here"
MY_BASE_URL = "https://api.openai.com/v1" # Change to your provider's base URL
MY_MODEL_NAME = "gpt-4o"                  # Change to your provider's model name
(Note: Most providers support the OpenAI format. For example, if using DeepSeek, use https://api.deepseek.com and deepseek-chat. For Kimi, use https://api.moonshot.cn/v1 and moonshot-v1-8k).
Step 3: Run the Tool
Double-click run_inspection.bat (Windows).

Paste the absolute path to your Icepak .aedt file when prompted.




### Quick Reference for Popular LLMs

| Provider | `MY_BASE_URL` | `MY_MODEL_NAME` |
| :--- | :--- | :--- |
| **OpenAI** | `https://api.openai.com/v1` | `gpt-4o` or `gpt-3.5-turbo` |
| **DeepSeek** | `https://api.deepseek.com` | `deepseek-chat` |
| **Moonshot (Kimi)** | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` |
| **Aliyun (Qwen)** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` |
Press Enter. The tool will connect to Ansys, extract the data, and print the AI inspection report in the terminal.
