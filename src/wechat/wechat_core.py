"""
微信核心操作模块

提供微信窗口和会话列表的操作
"""
import time
from typing import Optional, List

import uiautomation as auto
from loguru import logger
from uiautomation import ListControl, WindowControl, Control

from src.wechat.dto.control_model import ConversationItem
from src.wechat.dto.control_model import MessageItem

WECHAT_WINDOW_NAME = "微信"
WECHAT_SESSION_UI_ID = "session_list"
WECHAT_CHAT_MESSAGE_UI_ID = "chat_message_list"
WECHAT_CHAT_EDIT_UI_ID = "chat_input_field"
WECHAT_CHAT_TOOL_BAR_UI_ID = "tool_bar_accessible"


def print_control_info(control: Control) -> bool:
    if control.Exists(maxSearchSeconds=3):
        logger.success(f"控件类型: {control.ControlTypeName}")
        logger.success(f"控件名称: {control.Name}")
        logger.success(f"AutomationId: {control.AutomationId}")
        return True
    logger.warning("未找到控件")
    return False


# 查找微信窗口控件
def get_wechat_window_control() -> Optional[auto.WindowControl]:
    logger.info(f"查找微信窗口控件: {WECHAT_WINDOW_NAME}")
    wechat = auto.WindowControl(searchDepth=1, Name=WECHAT_WINDOW_NAME)
    if print_control_info(wechat):
        return wechat
    return None


# 查找会话列表控件
def get_session_control(wechat_window: WindowControl) -> Optional[auto.ListControl]:
    if not wechat_window:
        return None

    logger.debug("查找会话列表控件")
    list_control = wechat_window.ListControl(AutomationId=WECHAT_SESSION_UI_ID)
    if print_control_info(list_control):
        return list_control
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
                name=item.Name,
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


# 查找消息列表控件
def get_wechat_chat_message_control(wechat_window: WindowControl) -> Optional[auto.ListControl]:
    logger.debug("查找消息列表控件")
    message_list_control = wechat_window.ListControl(AutomationId=WECHAT_CHAT_MESSAGE_UI_ID)
    if print_control_info(message_list_control):
        return message_list_control
    return None


def get_message_list(message_list_control: ListControl) -> List[ConversationItem]:
    if not message_list_control:
        return []
    items = message_list_control.GetChildren()
    result = []

    for i, item in enumerate(items):
        # 构建 DTO 对象
        try:
            dto = MessageItem(
                index=i,
                name=item.Name,
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
        except Exception as e:
            logger.warning(f"跳过第 {i} 个控件，原因: {e}")
            continue
        result.append(dto)
    logger.success(f"共获取 {len(result)} 个消息")
    return result
