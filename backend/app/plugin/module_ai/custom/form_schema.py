from typing import Any, Dict, List, Optional, Union, Literal, Annotated
from pydantic import BaseModel, Field



# ==================== 基础公共字段 ====================
class BaseRule(BaseModel):
    field: Optional[str] = Field(
        ..., 
        description="字段名：必须用英文、snake_case 或 camelCase，语义清晰、无空格、无特殊字符。示例：user_name、email_addres"
    )
    title: Optional[str] = Field(
        ..., 
        description="用户看到的中文标签/标题，保持文档中的原始表述，简洁准确"
    )
    info: Optional[str] = Field(
        ..., 
        description="组件的提示信息"
    )
    value: Optional[Any] = Field(
        ..., 
        description="组件的默认值"
    )
    style: Optional[Union[str, Dict[str, Any]]] = Field(
        ..., 
        description="组件的内联样式, 格式为 {'key': 'value', 'key': 'value'}。示例：{'height': '40px'}"
    )
    required: Optional[Union[bool, str]] = Field(
        default=None, 
        alias="$required", 
        description="是否必填"
    )

class InputRule(BaseRule):
    type: Literal["input", "textarea"] = "input"
    props: Optional[Dict[str, Any]] = Field(
        ..., 
        description="组件额外属性。可以包含合理的 placeholder（如果文档中有暗示）。其他根据上下文添加"
    )

class SelectOption(BaseModel):
    label: str = Field(..., description="选项显示的文本，例如 '男'")
    value: Union[str, int, float, bool] = Field(..., description="选项对应的值，例如 'male'")

class SelectRule(BaseRule):
    type: Literal["select", "radio"] = "select"
    options: List[SelectOption] = Field(..., description="选项列表")


RuleItem = Annotated[
    Union[
        InputRule,
        SelectRule
    ],
    Field(discriminator="type")   # 关键！根据 type 字段自动选择模型
]

class FormSchema(BaseModel):
    form_title: Optional[str] = Field(None, description="整个表单的标题，如果文档中有明显标题则提取")
    rules: List[RuleItem] = Field(..., description="字段列表")

'''
你是一位专业的UI表单重建专家，擅长从PDF、图片、Word或文本文档中精确提取表单元素并转换为前端可直接使用的JSON数组（兼容 Ant Design、Element Plus、Naive UI 等）。

任务要求（严格遵守）：
1. 严格按文档从上到下、从左到右的自然视觉顺序提取字段，使用 order 字段记录顺序。
2. field 必须是英文语义化命名（snake_case 优先），不要使用中文或特殊字符。
3. 根据标签语义精确推断 type：
   - 包含“密码”、“password” → "password"
   - 包含“邮箱”、“email” → "email"
   - 包含“数字”、“数量”、“age”、“price” → "number"
   - 包含“性别”、“选项”、“选择”且选项有限 → "select" 或 "radio"
   - 包含“多选”、“同意” → "checkbox"
   - 包含“日期” → "date"
   - 其他默认 "input"
4. props 中至少添加合理的 placeholder（如果文档中有占位符或暗示文字，直接使用或合理构造）。
5. 如果有下拉选项、默认值、校验规则等线索，必须提取到 props.options 或对应属性中。
6. 判断 required：文档中出现“*”、“必填”、“required”、“不能为空”等 → true。
7. 输出必须是合法的 JSON，完全符合提供的 Schema，不要添加任何解释、Markdown 或额外文字。

文档内容：
{document}

请直接输出 FormSchema 的完整 JSON。

优化技巧：加入明确的任务要求和类型映射规则（Few-shot 隐含在规则中）。
强调“严格按视觉顺序”和“不要添加额外文字”。
使用 temperature=0 或 0.1 提升稳定性。
'''