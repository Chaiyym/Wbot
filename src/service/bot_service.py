"""
微信业务服务模块

整合数据库和微信操作，实现业务逻辑：
- 初始化数据库
- 黑白名单管理
- 会话过滤
"""

from typing import List, Dict, Tuple

import orjson
from loguru import logger
from uiautomation import ListControl, WindowControl

from src.data import db
from src.data import whitelist
from src.data import blacklist
from src.wechat import wechat_core
from src.wechat.dto.control_model import ConversationItem
from src.wechat.wechat_core import get_session_list_control

automation_id_prefix = "session_item_"


def init_database():
    """
    初始化数据库
    """
    db.init_tables()


def add_to_whitelist(name: str, class_name: str = None, description: str = "") -> int:
    """
    添加会话到白名单

    Args:
        name: 会话名称
        class_name: 类名
        description: 描述

    Returns:
        记录 ID
    """
    return whitelist.add(name, class_name, description)


def add_to_blacklist(name: str, class_name: str = None, description: str = "") -> int:
    """
    添加会话到黑名单

    Args:
        name: 会话名称
        class_name: 类名
        description: 描述

    Returns:
        记录 ID
    """
    return blacklist.add(name, class_name, description)


def get_whitelist() -> List[Dict]:
    """
    获取白名单

    Returns:
        白名单列表
    """
    return whitelist.get_all()


def get_blacklist() -> List[Dict]:
    """
    获取黑名单

    Returns:
        黑名单列表
    """
    return blacklist.get_all()



# 提取消息内容
def handle_msg_by_control(session_item: Dict):
    return


def get_filtered_conversations(session_control: ListControl) -> List[ConversationItem]:
    """
    获取过滤后的微信会话

    Returns:
        (白名单会话, 黑名单会话, 未分类会话)
    """
    if not session_control:
        return []

    # 获取会话列表
    sessions = get_session_list_control(session_control)

    # 获取白名单转换为集合便于快速查找
    whitelist_names = {automation_id_prefix + item["name"] for item in get_whitelist()}
    logger.info(f"白名单: {whitelist_names}")

    target_sessions = []
    block_sessions = []

    # 遍历会话，按黑白名单分类
    for session in sessions:
        # 使用 DTO 的 automation_id 属性
        automation_id = session.automation_id
        if automation_id in whitelist_names:
            target_sessions.append(session)
            logger.success(f"[监听目标id] {automation_id}")

    logger.success(f"统计: 目标数={len(target_sessions)}")

    return target_sessions


def focus_session(session_item):
    session_item.origin.SetFocus()


def click_session(session_item):
    session_item.origin.Click()


def read_message_by_focus(wechat:WindowControl)-> List[ConversationItem]:
    message_list_control = wechat_core.get_wechat_chat_message_control(wechat)
    messages= wechat_core.get_message_list(message_list_control)
    #todo 过滤消息通过黑名单
    return messages


