import requests as req
import json
import logging
import os

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PIPKimi:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "default_question": ("STRING", {"multiline": True, "default": "请问有什么可以帮助您的？"}),
                "history_dialogue": ("STRING", {"default": ""}),
            },
            "optional": {
                "additional_input": ("STRING", {"multiline": True, "default": ""}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("response", "response_show")

    FUNCTION = "call_kimi"

    def call_kimi(self, default_question="", additional_input="", history_dialogue=""):
        # 读取API密钥
        try:
            with open(os.path.join(os.path.dirname(__file__), 'key.txt'), 'r') as file:
                api_key = file.read().strip()
        except FileNotFoundError:
            logger.error("key.txt 文件未找到")
            return ("请求错误: key.txt 文件未找到", "请求错误: key.txt 文件未找到")
        except Exception as e:
            logger.error(f"读取 key.txt 文件时发生错误: {str(e)}")
            return (f"请求错误: {str(e)}", f"请求错误: {str(e)}")

        api_url = "https://api.moonshot.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # 将默认问题与额外输入连接
        question = f"{default_question}\n{additional_input}".strip()

        messages = json.loads(history_dialogue) if history_dialogue else []
        messages.append({"role": "user", "content": question})

        data = {
            "model": "moonshot-v1-128k",
            "messages": messages,
            "temperature": 0.7,
            "web_search": True,
            "top_p": 0.95,
            "presence_penalty": 0.6,
            "stream": False
        }
        
        try:
            response = req.post(api_url, headers=headers, json=data, timeout=40)
            response.raise_for_status()
            response_data = response.json()
            response_text = response_data['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": response_text})
            return (json.dumps(messages), response_text)
        except req.RequestException as e:
            logger.error(f"Request error: {str(e)}")
            return (f"请求错误: {str(e)}", f"请求错误: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return (f"发生未知错误: {str(e)}", f"发生未知错误: {str(e)}")

# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "PIP_KIMI": PIPKimi
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "PIP_KIMI": "PIP_KIMI Node"
}
