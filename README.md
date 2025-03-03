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

2025/3/3 增加了API调用的json模式，现在支持更加规范的json输出和读取了。

![微信截图_20250303182513](https://github.com/user-attachments/assets/218cbfbb-078f-452a-9d1b-c569698b1bbb)

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

### 示例2：漫画分镜设计（详细示例）

#### 步骤1：设置 PIP_KIMI（json）节点
1. 添加 PIP_KIMI（json）节点，并设置以下参数：
   - `default_question`: "作为专业漫画分镜师，请根据以下情节生成分镜方案：小明在学校参加篮球比赛投进了制胜球"
   - `json_format`: 
   ```json
   {
     "panels": [
       {"type": "scene_type", "description": "scene_description"},
       {"type": "scene_type", "description": "scene_description"},
       {"type": "scene_type", "description": "scene_description"},
       {"type": "scene_type", "description": "scene_description"},
       {"type": "dialogue", "character": "character_name", "text": "dialogue_text"},
       {"type": "narration", "text": "narration_text"}
     ]
   }
   ```
   - `additional_input`: 
   ```
   请遵循以下规则：
   1. 生成4个场景分镜、1个对话和1个旁白
   2. 场景类型必须从以下选择：环境全景、人物全身、动作特写、表情特写
   3. 场景描述要生动且具体，包含动作和环境细节
   4. 对话必须由场景中的一个角色说出
   5. 旁白应总结整个情节并提升情感氛围
   ```

#### 步骤2：获取 JSON 响应
Kimi 将生成类似如下的 JSON 响应：
```json
{
  "panels": [
    {
      "type": "环境全景",
      "description": "学校体育馆内，篮球场上挤满了观众，计分牌显示比分98:98，比赛时间只剩5秒"
    },
    {
      "type": "人物全身",
      "description": "小明持球快速突破防守，身体前倾，步伐坚定，眼神专注地盯着篮筐"
    },
    {
      "type": "动作特写",
      "description": "小明纵身跃起，双手握球，在空中舒展身体，将球投向篮筐，球划出一道完美的弧线"
    },
    {
      "type": "表情特写",
      "description": "小明屏住呼吸，瞪大双眼，嘴唇紧闭，脸上混合着紧张和期待的表情"
    },
    {
      "type": "dialogue",
      "character": "小明",
      "text": "就是现在，这一球我等了整整一年！"
    },
    {
      "type": "narration",
      "text": "随着终场哨声响起，篮球穿过篮网，全场沸腾，这一刻不仅仅是一场比赛的胜利，更是小明无数次训练的完美回报"
    }
  ]
}
```

#### 步骤3：使用 PIP_KIMI（jsonload）节点提取信息

可以使用多个 PIP_KIMI（jsonload）节点从这个 JSON 中提取不同部分：

1. **提取特定场景描述**
   - 连接 PIP_KIMI（json）的 `json_response` 到 PIP_KIMI（jsonload）的 `json_data`
   - 设置 `key_pattern` 为 `{panels}{2}{description}`
   - 得到输出：`小明纵身跃起，双手握球，在空中舒展身体，将球投向篮筐，球划出一道完美的弧线`

2. **提取对话内容**
   - 设置 `key_pattern` 为 `{panels}{4}{text}`
   - 得到输出：`就是现在，这一球我等了整整一年！`

3. **提取对话角色和内容**
   - 设置 `key_pattern` 为 `{panels}{4}`
   - 得到输出：
   ```json
   {
     "type": "dialogue",
     "character": "小明",
     "text": "就是现在，这一球我等了整整一年！"
   }
   ```

4. **提取所有场景信息**
   - 设置 `key_pattern` 为 `{panels}`
   - 得到完整的面板数组

### 示例3：角色属性生成

#### 步骤1：设置 PIP_KIMI（json）节点
- `default_question`: "为一个名叫'赤影'的武侠小说男主角生成详细的角色属性"
- `json_format`:
```json
{
  "character": {
    "name": "角色名",
    "age": 0,
    "gender": "性别",
    "appearance": "外貌描述",
    "personality": "性格特点",
    "skills": ["技能1", "技能2", "技能3"],
    "background": "背景故事",
    "relationships": [
      {"name": "关系人物1", "relation": "关系", "description": "关系描述"},
      {"name": "关系人物2", "relation": "关系", "description": "关系描述"}
    ]
  }
}
```

#### 步骤2：使用 PIP_KIMI（jsonload）节点灵活提取信息
- 提取年龄：`{character}{age}`
- 提取所有技能：`{character}{skills}`
- 提取第一个关系描述：`{character}{relationships}{0}{description}`
- 提取外貌和性格：同时使用两个 PIP_KIMI（jsonload）节点分别设置 `{character}{appearance}` 和 `{character}{personality}`



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
