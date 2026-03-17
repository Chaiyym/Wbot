"""
Wbot 入口文件
"""
from orjson import orjson

from src.service import bot_service
from src.service.bot_service import init_database, get_filtered_conversations, focus_session, click_session
from src.wechat.wechat_core import get_wechat_window_control, get_session_control, get_session_list_control


# 核心业务
def execute_biz() -> str:
    # 初始化数据库
    init_database()
    # 查找微信窗口
    wechat = get_wechat_window_control()
    # 获取会话控件
    session_control = get_session_control(wechat)

    # 获取过滤后的会话列表
    target_sessions = get_filtered_conversations(session_control)
    for session_item in target_sessions:
        # session_item.GetChildren()
        focus_session(session_item)
        click_session(session_item)

    result = {
        # "whitelist": white,
        # "blacklist": black,
        # "unclassified": other,
        "summary": {
            "whitelist_count": len(white),
            "blacklist_count": len(black),
            "unclassified_count": len(other),
            "total": len(white) + len(black) + len(other)
        }
    }

    return orjson.dumps(result, option=orjson.OPT_INDENT_2).decode("utf-8")


if __name__ == '__main__':
    print(execute_biz())
