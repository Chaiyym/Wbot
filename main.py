"""
Wbot 入口文件
"""
from loguru import logger

from src.service import bot_service
from src.wechat import wechat_core



# 核心业务
def execute_biz() -> str:
    # 初始化数据库
    bot_service.init_database()
    # 查找微信窗口
    wechat = wechat_core.get_wechat_window_control()
    # 获取会话控件
    session_control = wechat_core.get_session_control(wechat)

    # 获取过滤后的会话列表
    target_sessions = bot_service.get_filtered_conversations(session_control)
    for session_item in target_sessions:
        # session_item.GetChildren()
        #获取目标焦点
        bot_service.focus_session(session_item)
        bot_service.click_session(session_item)
        # 读取焦点会话数据
        messages = bot_service.read_message_by_focus(wechat)
        for message in messages:
            logger.info(f": {message.control_type}:{message.automation_id}:{message.name}")
    return "ok"


if __name__ == '__main__':
    print(execute_biz())
