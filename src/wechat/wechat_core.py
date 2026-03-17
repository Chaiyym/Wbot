"""
微信核心操作模块

提供微信窗口和会话列表的操作
"""
import time
from typing import Optional, List

import uiautomation as auto
from loguru import logger
from uiautomation import ListControl, WindowControl

from src.wechat.dto.conversation_item import ConversationItem

WECHAT_WINDOW_NAME = "微信"


# 获取微信窗口控件
def get_wechat_window_control() -> Optional[auto.WindowControl]:
    """
    查找微信窗口

    Returns:
        WindowControl 或 None
    """
    logger.info(f"查找微信窗口: {WECHAT_WINDOW_NAME}")
    wechat = auto.WindowControl(searchDepth=1, Name=WECHAT_WINDOW_NAME)

    if wechat.Exists(maxSearchSeconds=3):
        logger.success(f"找到微信窗口: {wechat.Name}")
        return wechat

    logger.warning("未找到微信窗口")
    return None


# 获取会话列表控件
def get_session_control(wechat_window: WindowControl) -> Optional[auto.ListControl]:
    """
    查找会话列表控件

    Args:
        wechat_window: 微信窗口对象

    Returns:
        ListControl 或 None
    """

    logger.debug("查找会话列表控件")
    list_control = wechat_window.ButtonControl(Name="fa")
    time.sleep(3)
    target = auto.ControlFromCursor()
    print(f"控件类型: {target.ControlTypeName}")
    print(f"控件名称: {target.Name}")
    print(f"AutomationId: {target.AutomationId}")
    if list_control.Exists(maxSearchSeconds=2):
        logger.success(f"找到会话列表: {list_control.Name}")
        return list_control

    logger.warning("未找到会话列表控件")
    return None


# 获取会话列表中的所有会话项
def get_session_list_control(session_control: ListControl) -> List[ConversationItem]:
    if not session_control:
        return []

    items = session_control.GetChildren()
    result = []

    for i, item in enumerate(items):
        if item.AutomationId:
            # 构建 DTO 对象
            dto = ConversationItem(
                index=i,
                automation_id=item.AutomationId,
                control_type=item.ControlTypeName,
                process_id=item.ProcessId,
                is_focus=item.GetPropertyValue(auto.PropertyId.HasKeyboardFocusProperty),
                is_selected=item.GetPropertyValue(auto.PropertyId.SelectionItemIsSelectedProperty),
                is_enable=item.GetPropertyValue(auto.PropertyId.IsEnabledProperty),
                is_offscreen=item.GetPropertyValue(auto.PropertyId.IsOffscreenProperty),
                help=item.GetPropertyValue(auto.PropertyId.HelpTextProperty),
                origin=item,
            )
            result.append(dto)

    logger.success(f"共获取 {len(result)} 个会话")
    return result
