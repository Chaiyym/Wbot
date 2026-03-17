"""
会话项 DTO

定义微信会话的数据传输对象
"""

from dataclasses import dataclass
from typing import Optional, Any

from uiautomation import ListItemControl, Control


@dataclass
class ConversationItem:
    """微信会话项数据对象"""
    index: int
    automation_id: Optional[str]
    control_type: str
    process_id: int
    is_focus: bool
    is_selected: bool
    is_enable: bool
    is_offscreen: bool
    help: Optional[str]
    origin: Control  # 原始控件对象

    @property
    def name(self) -> str:
        """获取会话名称（从原始控件）"""
        return self.origin.Name if self.origin else ""

    @property
    def classname(self) -> str:
        """获取会话类名"""
        return self.origin.ClassName if self.origin else ""

    def to_dict(self) -> dict:
        """转换为字典（不含 origin）"""
        return {
            "index": self.index,
            "automation_id": self.automation_id,
            "control_type": self.control_type,
            "process_id": self.process_id,
            "is_focus": self.is_focus,
            "is_selected": self.is_selected,
            "is_enable": self.is_enable,
            "is_offscreen": self.is_offscreen,
            "help": self.help,
            "name": self.name,
            "classname": self.classname,
        }
