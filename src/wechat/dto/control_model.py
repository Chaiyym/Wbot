"""
会话项 DTO

定义微信会话的数据传输对象
"""

from dataclasses import dataclass
from typing import Optional, Any

from uiautomation import ListItemControl, Control


@dataclass
class ControlProps:
    index: int
    name: str
    automation_id: Optional[str]
    control_type: str
    process_id: int
    is_focus: bool
    is_selected: bool
    is_enable: bool
    is_offscreen: bool
    help: Optional[str]
    origin: Control  # 原始控件对象


@dataclass
class MessageItem(ControlProps):
    """消息数据对象"""


@dataclass
class ConversationItem(ControlProps):
    """会话数据对象"""
