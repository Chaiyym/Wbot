"""
微信自动化工具模块

提供微信窗口控制、会话列表获取等功能
"""

import orjson
import uiautomation as auto
from loguru import logger


def find_wechat_conversation_list():
    """
    查找微信窗口和会话列表控件

    Returns:
        ListControl: 会话列表控件对象，如果未找到返回 None
    """
    logger.info("开始查找微信会话列表")
    wechat = auto.WindowControl(searchDepth=1, Name="微信")
    if not wechat.Exists(maxSearchSeconds=3):
        logger.warning("未找到微信窗口")
        return None
    
    logger.info(f"找到微信窗口: {wechat.Name}")
    
    list_control = wechat.ListControl(Name="会话")
    if list_control.Exists(maxSearchSeconds=2):
        logger.success(f"找到会话列表: {list_control.Name}")
        return list_control
    else:
        logger.warning("未找到会话列表控件")
        return None


def get_conversation_items():
    """
    获取微信会话列表中的所有会话项

    Returns:
        list: 会话项列表，每个元素为包含 index, name, classname, control_type 的字典
    """
    list_control = find_wechat_conversation_list()
    if not list_control:
        return []
    
    logger.info("获取会话列表项")
    items = list_control.GetChildren()
    
    result = []
    for i, item in enumerate(items):
        if item.Name:
            result.append({
                "index": i,
                "name": item.Name,
                "classname": item.ClassName,
                "control_type": item.ControlTypeName
            })
            logger.debug(f"{i+1}. {item.Name} ({item.ControlTypeName})")
    
    logger.success(f"共找到 {len(result)} 个会话")
    return result


def get_conversation_items_detailed():
    """
    获取微信会话列表的详细信息，用于分析元素属性

    Returns:
        list: 包含完整控件属性的会话项列表
    """
    list_control = find_wechat_conversation_list()
    if not list_control:
        return []
    
    logger.info("获取会话列表详细信息")
    items = list_control.GetChildren()
    
    result = []
    for i, item in enumerate(items):
        if item.Name:
            item_info = {
                "index": i,
                "Name": item.Name,
                "ClassName": item.ClassName,
                "ControlTypeName": item.ControlTypeName,
                "ProcessId": item.ProcessId,
                "AutomationId": item.AutomationId if hasattr(item, 'AutomationId') else None,
            }
            
            try:
                item_info["BoundingRectangle"] = {
                    "left": item.BoundingRectangle.left,
                    "top": item.BoundingRectangle.top,
                    "right": item.BoundingRectangle.right,
                    "bottom": item.BoundingRectangle.bottom,
                }
            except Exception:
                pass
            
            try:
                item_info["Description"] = item.Description
            except Exception:
                pass
            
            try:
                item_info["HelpText"] = item.HelpText
            except Exception:
                pass
            
            result.append(item_info)
            logger.debug(f"{i+1}. {item.Name}")
    
    logger.success(f"共找到 {len(result)} 个会话")
    logger.info("详细信息 JSON:")
    print(orjson.dumps(result, option=orjson.OPT_INDENT_2 | orjson.OPT_NON_STR_KEYS).decode("utf-8"))
    
    return result


def analyze_conversation_types():
    """
    分析会话列表，尝试区分群聊、单聊和公众号

    Returns:
        dict: 分类统计结果
    """
    list_control = find_wechat_conversation_list()
    if not list_control:
        return {}
    
    logger.info("开始分析会话类型")
    items = list_control.GetChildren()
    
    groups = []
    individuals = []
    official_accounts = []
    unknown = []
    
    for i, item in enumerate(items):
        if not item.Name:
            continue
        
        name = item.Name
        classname = item.ClassName
        
        if "群" in name or "(" in name or classname == "mmui::GrpItem":
            groups.append(name)
        elif "公众号" in name or "视频号" in name:
            official_accounts.append(name)
        else:
            individuals.append(name)
    
    result = {
        "群聊": groups,
        "单聊": individuals,
        "公众号/视频号": official_accounts,
        "总计": len(items)
    }
    
    logger.success("分析完成")
    logger.info("分类结果 JSON:")
    print(orjson.dumps(result, option=orjson.OPT_INDENT_2).decode("utf-8"))
    
    return result


def tree_view_wechat(max_depth: int = 3):
    """
    遍历微信窗口的所有元素并打印树形结构

    Args:
        max_depth: 最大遍历深度，默认为 3
    """
    logger.info("开始遍历微信窗口元素")
    wechat = auto.WindowControl(searchDepth=1, Name="微信")
    if not wechat.Exists(maxSearchSeconds=3):
        logger.warning("未找到微信窗口")
        return
    
    logger.info(f"微信窗口: {wechat.Name} ({wechat.ClassName})")
    
    def walk(control, depth: int, max_depth: int):
        if depth > max_depth:
            return
        try:
            children = control.GetChildren()
            for child in children:
                if child.Name and len(child.Name.strip()) > 0:
                    indent = "  " * depth
                    logger.debug(f"{indent}{child.ControlTypeName}: {child.Name} ({child.ClassName})")
                walk(child, depth + 1, max_depth)
        except Exception as e:
            logger.error(f"遍历出错: {e}")
    
    walk(wechat, 0, max_depth)
    logger.success("遍历完成")


if __name__ == "__main__":
    get_conversation_items_detailed()
