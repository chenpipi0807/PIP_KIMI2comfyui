import requests as req
import json
import logging
import os
import base64
import torch
from PIL import Image
import io
import re

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
                "model_name": (["moonshot-v1-8k",
                "moonshot-v1-32k",
                "moonshot-v1-128k",
                "moonshot-v1-8k-vision-preview",
                "moonshot-v1-32k-vision-preview",
                "moonshot-v1-128k-vision-preview",
                "kimi-latest"], {"default": "kimi-latest"}),
                "image_input": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("response", "response_show")

    FUNCTION = "call_kimi"

    def tensor_to_image(self, tensor):
        logger.debug("Converting tensor to PIL image...")
        tensor = tensor.cpu()
        if tensor.dim() == 4:
            tensor = tensor[0]
        image = tensor.clone().detach()
        image = image * 255
        image = image.numpy().astype('uint8')
        return Image.fromarray(image)

    def call_kimi(self, default_question="", additional_input="", history_dialogue="", model_name="moonshot-v1-128k-vision-preview", image_input=None):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'key.txt'), 'r') as file:
                api_key = file.read().strip()
        except FileNotFoundError:
            logger.error("API key file (key.txt) not found!")
            return ("请求错误: key.txt 文件未找到", "请求错误: key.txt 文件未找到")
        except Exception as e:
            logger.error(f"Failed to read key.txt: {str(e)}")
            return (f"请求错误: {str(e)}", f"请求错误: {str(e)}")

        api_url = "https://api.moonshot.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        question = f"{default_question}\n{additional_input}".strip()
        messages = json.loads(history_dialogue) if history_dialogue else []

        # Handle image input
        if image_input is not None:
            if not (model_name.endswith("-vision-preview") or model_name.startswith("kimi-latest")):
                logger.warning(f"Model {model_name} does not support image processing. Switching to 'kimi-latest'")
                model_name = "kimi-latest"

            try:
                pil_image = self.tensor_to_image(image_input)
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='PNG')
                image_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
                
                # Constructing the message content with image_url and text
                image_url = f"data:image/png;base64,{image_data}"
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url,
                                }
                            },
                            {
                                "type": "text",
                                "text": question
                            }
                        ]
                    }
                )
            except Exception as e:
                logger.error(f"Image processing failed: {str(e)}")
                return (f"图片处理错误: {str(e)}", f"图片处理错误: {str(e)}")
        else:
            messages.append({"role": "user", "content": question})

        data = {
            "model": model_name,
            "messages": messages,
            "temperature": 0.7,
            "web_search": True,
            "top_p": 0.95,
            "presence_penalty": 0.6,
            "stream": False
        }

        try:
            logger.debug(f"Making API request to {api_url}...")
            response = req.post(api_url, headers=headers, json=data, timeout=120)
            response.raise_for_status()
            response_data = response.json()

            if 'error' in response_data:
                logger.error(f"API Error: {response_data['error']}")
                return (f"请求错误: {response_data['error']}", f"请求错误: {response_data['error']}")

            response_text = response_data['choices'][0]['message']['content']
            messages.append({"role": "assistant", "content": response_text})
            logger.debug("API request successful!")
            return (json.dumps(messages), response_text)

        except req.RequestException as e:
            logger.error(f"Request Error: {str(e)}")
            return (f"请求错误: {str(e)}", f"请求错误: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return (f"发生未知错误: {str(e)}", f"发生未知错误: {str(e)}")


class PIPKimiJSON:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "default_question": ("STRING", {"multiline": True, "default": "请问有什么可以帮助您的？"}),
                "history_dialogue": ("STRING", {"default": ""}),
                "json_format": ("STRING", {"multiline": True, "default": "{\n  \"response\": \"您的回答\"\n}"}),
            },
            "optional": {
                "additional_input": ("STRING", {"multiline": True, "default": ""}),
                "model_name": (["moonshot-v1-8k",
                "moonshot-v1-32k",
                "moonshot-v1-128k",
                "moonshot-v1-8k-vision-preview",
                "moonshot-v1-32k-vision-preview",
                "moonshot-v1-128k-vision-preview",
                "kimi-latest"], {"default": "kimi-latest"}),
                "image_input": ("IMAGE",),
                "max_tokens": ("INT", {"default": 4096, "min": 1, "max": 128000}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("json_response", "history_dialogue")

    FUNCTION = "call_kimi_json"

    def tensor_to_image(self, tensor):
        logger.debug("Converting tensor to PIL image...")
        tensor = tensor.cpu()
        if tensor.dim() == 4:
            tensor = tensor[0]
        image = tensor.clone().detach()
        image = image * 255
        image = image.numpy().astype('uint8')
        return Image.fromarray(image)

    def call_kimi_json(self, default_question="", json_format="", additional_input="", history_dialogue="", 
                       model_name="moonshot-v1-128k-vision-preview", image_input=None, max_tokens=4096):
        try:
            with open(os.path.join(os.path.dirname(__file__), 'key.txt'), 'r') as file:
                api_key = file.read().strip()
        except FileNotFoundError:
            logger.error("API key file (key.txt) not found!")
            return ("请求错误: key.txt 文件未找到", "请求错误: key.txt 文件未找到")
        except Exception as e:
            logger.error(f"Failed to read key.txt: {str(e)}")
            return (f"请求错误: {str(e)}", f"请求错误: {str(e)}")

        api_url = "https://api.moonshot.cn/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Prepare system message to guide JSON format
        system_message = {
            "role": "system", 
            "content": f"请以JSON格式回答用户的问题，JSON格式如下：\n{json_format}\n请严格按照这个格式输出JSON，不要添加其他文字说明。"
        }

        question = f"{default_question}\n{additional_input}".strip()
        
        try:
            messages = json.loads(history_dialogue) if history_dialogue else []
            # Add system message if there isn't one already
            if not messages or messages[0].get("role") != "system":
                messages.insert(0, system_message)
        except json.JSONDecodeError:
            logger.warning("Invalid history_dialogue JSON, creating new history")
            messages = [system_message]

        # Handle image input
        if image_input is not None:
            if not (model_name.endswith("-vision-preview") or model_name.startswith("kimi-latest")):
                logger.warning(f"Model {model_name} does not support image processing. Switching to 'kimi-latest'")
                model_name = "kimi-latest"

            try:
                pil_image = self.tensor_to_image(image_input)
                img_byte_arr = io.BytesIO()
                pil_image.save(img_byte_arr, format='PNG')
                image_data = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')
                
                # Constructing the message content with image_url and text
                image_url = f"data:image/png;base64,{image_data}"
                messages.append(
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": image_url,
                                }
                            },
                            {
                                "type": "text",
                                "text": question
                            }
                        ]
                    }
                )
            except Exception as e:
                logger.error(f"Image processing failed: {str(e)}")
                return (f"图片处理错误: {str(e)}", f"图片处理错误: {str(e)}")
        else:
            messages.append({"role": "user", "content": question})

        data = {
            "model": model_name,
            "messages": messages,
            "temperature": 0.7,
            "web_search": True,
            "top_p": 0.95,
            "presence_penalty": 0.6,
            "stream": False,
            "max_tokens": max_tokens,
            "response_format": {"type": "json_object"}
        }

        try:
            logger.debug(f"Making API request to {api_url} with JSON mode...")
            response = req.post(api_url, headers=headers, json=data, timeout=180)
            response.raise_for_status()
            response_data = response.json()

            if 'error' in response_data:
                logger.error(f"API Error: {response_data['error']}")
                return (f"请求错误: {response_data['error']}", json.dumps(messages))

            # Extract JSON response
            json_response = response_data['choices'][0]['message']['content']
            # Validate it's proper JSON
            try:
                json_obj = json.loads(json_response)
                # Format it nicely
                json_response = json.dumps(json_obj, ensure_ascii=False, indent=2)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON returned: {e}")
                json_response = f"错误: API返回的JSON格式无效: {e}"

            # Add response to message history
            messages.append({"role": "assistant", "content": json_response})
            logger.debug("API JSON request successful!")
            
            return (json_response, json.dumps(messages))

        except req.RequestException as e:
            logger.error(f"Request Error: {str(e)}")
            return (f"请求错误: {str(e)}", json.dumps(messages))
        except Exception as e:
            logger.error(f"Unexpected Error: {str(e)}")
            return (f"发生未知错误: {str(e)}", json.dumps(messages))


class PIPKimiJSONLoad:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "json_data": ("STRING", {"multiline": True}),
                "key_pattern": ("STRING", {"default": "{key}"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("extracted_value",)

    FUNCTION = "extract_json_value"

    def extract_json_value(self, json_data, key_pattern):
        try:
            # Parse JSON data
            data = json.loads(json_data)
            
            # Extract keys enclosed in curly braces from the pattern
            keys = re.findall(r'\{([^{}]+)\}', key_pattern)
            
            if not keys:
                return (f"Error: No keys found in pattern '{key_pattern}'. Use format like '{{key}}'.",)
            
            # Navigate through nested JSON structure
            result = data
            path = []
            
            for key in keys:
                path.append(key)
                
                if isinstance(result, dict) and key in result:
                    result = result[key]
                elif isinstance(result, list) and key.isdigit() and int(key) < len(result):
                    result = result[int(key)]
                else:
                    path_str = ".".join(path)
                    return (f"Error: Key '{path_str}' not found in JSON data.",)
            
            # Convert result to string if it's not already
            if isinstance(result, (dict, list)):
                result = json.dumps(result, ensure_ascii=False, indent=2)
            else:
                result = str(result)
                
            return (result,)
            
        except json.JSONDecodeError as e:
            return (f"Error: Invalid JSON data - {str(e)}",)
        except Exception as e:
            return (f"Error: {str(e)}",)


# A dictionary that contains all nodes you want to export with their names
NODE_CLASS_MAPPINGS = {
    "PIP_KIMI": PIPKimi,
    "PIP_KIMI_JSON": PIPKimiJSON,
    "PIP_KIMI_JSONLOAD": PIPKimiJSONLoad
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "PIP_KIMI": "PIP_KIMI Node",
    "PIP_KIMI_JSON": "PIP_KIMI（json）",
    "PIP_KIMI_JSONLOAD": "PIP_KIMI（jsonload）"
}
