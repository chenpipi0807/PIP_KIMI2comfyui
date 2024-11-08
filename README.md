# ComfyUI-PIP-KIMI 节点

这是一个用于 ComfyUI 的自定义节点,集成了 Moonshot AI 的 KIMI 大语言模型。通过这个节点,你可以在 ComfyUI 工作流中直接与 KIMI AI 进行对话交互。

## 功能特点

- 支持与 KIMI AI 进行自然语言对话
- 保持对话历史记录,支持上下文理解
- 可以添加额外的输入信息
- 支持网络搜索功能
- 完整的错误处理和日志记录
![微信截图_20241108201940](https://github.com/user-attachments/assets/d5111c7a-430f-4fed-80c2-7ab3932a509d)

## 使用方法

1. 前往 https://platform.moonshot.cn/console/account 注册账号并获取 API 密钥（新用户可获得价值15元的免费额度，约可使用15万字的token）
2. 将获取到的 API 密钥保存在 `key.txt` 文件中
3. 在 ComfyUI 中添加 "PIP_KIMI" 节点
4. 配置以下输入参数:
   - `default_question`: 默认问题文本(必填)
   - `history_dialogue`: 对话历史记录(必填)
   - `additional_input`: 额外的输入信息(可选)

## 输出说明

节点有两个输出:
- `response`: 包含完整对话历史的 JSON 字符串
- `response_show`: KIMI 的当前回复文本

## 配置参数

- 模型: moonshot-v1-128k
- temperature: 0.7
- web_search: 启用
- top_p: 0.95
- presence_penalty: 0.6

## 注意事项

- 请确保 `key.txt` 文件存在且包含有效的 API 密钥
- API 请求超时时间设置为 40 秒
- 所有错误信息都会被记录到日志中

## 安装

1. 将项目文件复制到 ComfyUI 的 `custom_nodes` 目录下
2. 重启 ComfyUI
3. 在节点列表中即可找到 "PIP_KIMI Node"

## 依赖

- requests
- json
- logging
- os

## 错误处理

节点包含完整的错误处理机制:
- API 密钥文件不存在的处理
- 网络请求错误处理
- 通用异常处理

所有错误都会通过节点的输出端口返回,并同时记录到日志中。
