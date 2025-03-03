# ComfyUI-PIP-KIMI 节点

这是一个用于 ComfyUI 的自定义节点,集成了 Moonshot AI 的 KIMI 大语言模型。通过这个节点,你可以在 ComfyUI 工作流中直接与 KIMI AI 进行对话交互。

## 更新日志
1.春节后的版本支持多模态图像推理了，需要选择vision版本的模型；
2.此外，现在支持模型切换功能了
3.新增了如下模型："moonshot-v1-8k-vision-preview",
                "moonshot-v1-32k-vision-preview",
                "moonshot-v1-128k-vision-preview",
                "kimi-latest"], 
![微信截图_20250205164124](https://github.com/user-attachments/assets/dc4971a5-6e6c-49cc-afba-95ac485a3bb7)

2025/3/3 增加了API调用的json模式，现在支持更加规范的json输出和读取了。当然我也增加了使用示例的工作流；

![微信截图_20250303184605](https://github.com/user-attachments/assets/55a922ba-f36c-4f76-9973-873a61c710be)


## JSON模式使用方法

### PIP_KIMI（json）节点

配置以下输入参数:
- `default_question`: 默认问题文本(必填)
- `history_dialogue`: 对话历史记录(必填)
- `json_format`: 期望的 JSON 输出格式模板(必填)
- `additional_input`: 额外的输入信息(可选)
- `max_tokens`: 最大输出 token 数量(可选，默认 4096)

### PIP_KIMI（jsonload）节点

配置以下输入参数:
- `json_data`: 要处理的 JSON 数据(必填)
- `key_pattern`: 要提取的键路径，格式为 `{key1}{key2}` 等(必填)

## 输出说明

### PIP_KIMI 节点输出
- `response`: 包含完整对话历史的 JSON 字符串
- `response_show`: KIMI 的当前回复文本

### PIP_KIMI（json）节点输出
- `json_response`: 以 JSON 格式返回的回复
- `history_dialogue`: 包含完整对话历史的 JSON 字符串

### PIP_KIMI（jsonload）节点输出
- `extracted_value`: 从 JSON 中提取的值

## JSON 模式使用示例

### 示例1：文章分析
1. 使用 PIP_KIMI（json）节点，设置 `json_format` 为：
```json
{
  "title": "文章标题",
  "summary": "文章摘要",
  "key_points": ["要点1", "要点2", "要点3"]
}
```

2. 设置 `default_question` 为 "请总结这篇文章的要点"

3. 获取返回的 JSON 结果，然后使用 PIP_KIMI（jsonload）节点提取特定值:
   - 提取 "title"：设置 `key_pattern` 为 `{title}`
   - 提取 "key_points" 中的第一项：设置 `key_pattern` 为 `{key_points}{0}`

### 示例2：段子整理（详细示例）

#### 步骤1：设置 PIP_KIMI（json）节点
1. 添加 PIP_KIMI（json）节点，并设置以下参数：
   - `default_question`: "将以下段子整理成JSON格式，包含笑点1、笑点2、段子内容和段子梗概："
   - `json_format`: 
   ```json
   {
     "joke_summary": "段子梗概",
     "joke_content": "完整段子内容",
     "funny_points": [
       {
         "point_id": 1,
         "description": "笑点1描述"
       },
       {
         "point_id": 2,
         "description": "笑点2描述"
       }
     ]
   }
   ```
   - `additional_input`: 
   ```
   话说这年头，减肥都快成全民运动了。我身边有个朋友，下定决心要减肥，那架势，就跟要去征服珠穆朗玛峰似的。
   他制定了超级严格的计划，每天早上五点准时起床晨跑，那寒风呼呼吹，他跟个勇士一样冲出家门。可跑不到一半，就在路边的早餐摊前缴械投降了。那热气腾腾的包子、油条，仿佛有种魔力，把他那减肥的信念一下子就击得粉碎。他一边往嘴里塞着吃的，一边还念叨着："吃完这顿，我今天肯定能消耗更多热量。"
   到了晚上，他又开始折腾。在网上买了各种减肥器材，什么呼啦圈、哑铃，弄得家里跟个小健身房似的。刚开始还新鲜，呼啦圈转得挺欢，可没几分钟，就哎哟哎哟地喊累，一屁股坐在沙发上，拿起手机刷起美食视频，看得那叫一个津津有味，嘴里还不忘嘟囔："我就看看，又不会胖。"
   最搞笑的是，他加入了一个减肥群，天天在里面打卡。看着别人晒的减肥成果，他眼馋得不行，就问人家秘诀。人家说要管住嘴、迈开腿，他还特认真地说："我都知道，就是做不到啊！" 过了几天，他又在群里发消息，说自己要尝试新的减肥方法，结果没多久就有人问他效果咋样，他回了一句："别提了，我刚试了一天，就发现这方法不适合我，一饿肚子我就头晕眼花，还是吃点东西补充能量吧。"
   这减肥啊，对他来说，就像是一场永远打不完的仗，每次都雄心勃勃地开始，然后灰溜溜地放弃，不过他的这些减肥趣事，倒成了我们茶余饭后的开心果，给大家带来了不少欢乐。
   ```

#### 步骤2：获取 JSON 响应
Kimi 将生成类似如下的 JSON 响应：
```json
{
  "joke_summary": "一个朋友立志减肥却总是难以坚持，从早晨跑步到购买健身器材再到加入减肥群，每次都是信心满满开始但很快就放弃",
  "joke_content": "话说这年头，减肥都快成全民运动了。我身边有个朋友，下定决心要减肥，那架势，就跟要去征服珠穆朗玛峰似的。他制定了超级严格的计划，每天早上五点准时起床晨跑，那寒风呼呼吹，他跟个勇士一样冲出家门。可跑不到一半，就在路边的早餐摊前缴械投降了。那热气腾腾的包子、油条，仿佛有种魔力，把他那减肥的信念一下子就击得粉碎。他一边往嘴里塞着吃的，一边还念叨着："吃完这顿，我今天肯定能消耗更多热量。"到了晚上，他又开始折腾。在网上买了各种减肥器材，什么呼啦圈、哑铃，弄得家里跟个小健身房似的。刚开始还新鲜，呼啦圈转得挺欢，可没几分钟，就哎哟哎哟地喊累，一屁股坐在沙发上，拿起手机刷起美食视频，看得那叫一个津津有味，嘴里还不忘嘟囔："我就看看，又不会胖。"最搞笑的是，他加入了一个减肥群，天天在里面打卡。看着别人晒的减肥成果，他眼馋得不行，就问人家秘诀。人家说要管住嘴、迈开腿，他还特认真地说："我都知道，就是做不到啊！" 过了几天，他又在群里发消息，说自己要尝试新的减肥方法，结果没多久就有人问他效果咋样，他回了一句："别提了，我刚试了一天，就发现这方法不适合我，一饿肚子我就头晕眼花，还是吃点东西补充能量吧。"这减肥啊，对他来说，就像是一场永远打不完的仗，每次都雄心勃勃地开始，然后灰溜溜地放弃，不过他的这些减肥趣事，倒成了我们茶余饭后的开心果，给大家带来了不少欢乐。",
  "funny_points": [
    {
      "point_id": 1,
      "description": "朋友晨跑途中被早餐摊的美食诱惑，一边吃一边自我安慰说'吃完这顿，我今天肯定能消耗更多热量'"
    },
    {
      "point_id": 2,
      "description": "朋友购买各种减肥器材后，很快就放弃锻炼改看美食视频，还辩解说'我就看看，又不会胖'"
    }
  ]
}
```

#### 步骤3：使用 PIP_KIMI（jsonload）节点提取信息

可以使用多个 PIP_KIMI（jsonload）节点从这个 JSON 中提取不同部分：

1. **提取段子梗概**
   - 连接 PIP_KIMI（json）的 `json_response` 到 PIP_KIMI（jsonload）的 `json_data`
   - 设置 `key_pattern` 为 `{joke_summary}`
   - 得到输出：`一个朋友立志减肥却总是难以坚持，从早晨跑步到购买健身器材再到加入减肥群，每次都是信心满满开始但很快就放弃`

2. **提取笑点1**
   - 设置 `key_pattern` 为 `{funny_points}{0}{description}`
   - 得到输出：`朋友晨跑途中被早餐摊的美食诱惑，一边吃一边自我安慰说'吃完这顿，我今天肯定能消耗更多热量'`

3. **提取笑点2**
   - 设置 `key_pattern` 为 `{funny_points}{1}{description}`
   - 得到输出：`朋友购买各种减肥器材后，很快就放弃锻炼改看美食视频，还辩解说'我就看看，又不会胖'`

4. **提取所有笑点**
   - 设置 `key_pattern` 为 `{funny_points}`
   - 得到完整的笑点数组

### 示例3：通用问答转JSON

#### 步骤1：设置 PIP_KIMI（json）节点
- `default_question`: "请解释什么是人工智能，并以JSON格式回答"
- `json_format`:
```json
{
  "question": "用户提问",
  "answer": {
    "brief": "简短回答",
    "detailed": "详细解释",
    "examples": ["例子1", "例子2", "例子3"],
    "related_fields": ["相关领域1", "相关领域2"]
  },
  "references": [
    {"title": "参考资料1", "source": "来源"},
    {"title": "参考资料2", "source": "来源"}
  ]
}
```

#### 步骤2：使用 PIP_KIMI（jsonload）节点灵活提取信息
- 提取简短回答：`{answer}{brief}`
- 提取所有例子：`{answer}{examples}`
- 提取第一个参考资料：`{references}{0}{title}`
- 提取详细解释和相关领域：同时使用两个 PIP_KIMI（jsonload）节点分别设置 `{answer}{detailed}` 和 `{answer}{related_fields}`



## 功能特点

- 支持与 KIMI AI 进行自然语言对话
- 保持对话历史记录,支持上下文理解
- 可以添加额外的输入信息
- 支持网络搜索功能
- 完整的错误处理和日志记录
![微信截图_20241108201940](https://github.com/user-attachments/assets/d5111c7a-430f-4fed-80c2-7ab3932a509d)
![微信截图_20241112132729](https://github.com/user-attachments/assets/ec18da0d-58fa-4cdb-9ffd-fc4647ca8f21)

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
