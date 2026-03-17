"""
UIAutomation 基础操作模块

提供窗口和控件查找的基础操作
"""

from typing import Optional

import uiautomation as auto
from loguru import logger


def find_window(name: str, class_name: Optional[str] = None, search_depth: int = 1, timeout: float = 3):
    """
    查找窗口

    Args:
        name: 窗口名称
        class_name: 窗口类名
        search_depth: 搜索深度
        timeout: 超时时间（秒）

    Returns:
        WindowControl 或 None
    """
    logger.debug(f"查找窗口: {name}")
    
    if class_name:
        window = auto.WindowControl(searchDepth=search_depth, Name=name, ClassName=class_name)
    else:
        window = auto.WindowControl(searchDepth=search_depth, Name=name)
    
    if window.Exists(maxSearchSeconds=timeout):
        logger.success(f"找到窗口: {window.Name} ({window.ClassName})")
        return window
    
    logger.warning(f"未找到窗口: {name}")
    return None


def get_desktop():
    """
    获取桌面根控件

    Returns:
        Control: 桌面控件
    """
    return auto.GetRootControl()


def get_top_windows():
    """
    获取所有顶层窗口

    Returns:
        list: 窗口列表
    """
    desktop = get_desktop()
    return desktop.GetChildren()


def list_window_names(max_count: int = 20):
    """
    列出顶层窗口名称

    Args:
        max_count: 最大显示数量

    Returns:
        list: 窗口信息列表
    """
    windows = get_top_windows()
    result = []
    
    for i, win in enumerate(windows[:max_count]):
        if win.Name:
            result.append({
                "index": i,
                "name": win.Name,
                "classname": win.ClassName,
                "process_id": win.ProcessId
            })
    
    return result


def find_control_in_window(window, control_type, name: Optional[str] = None):
    """
    在窗口中查找控件

    Args:
        window: 窗口控件对象
        control_type: 控件类型（如 auto.EditControl, auto.ButtonControl）
        name: 控件名称

    Returns:
        控件对象或 None
    """
    if name:
        control = control_type(searchFromControl=window, Name=name)
    else:
        control = control_type(searchFromControl=window)
    
    if control.Exists(maxSearchSeconds=2):
        return control
    
    return None


def walk_controls(control, depth: int = 0, max_depth: int = 3):
    """
    递归遍历控件树

    Args:
        control: 起始控件
        depth: 当前深度
        max_depth: 最大深度
    """
    if depth > max_depth:
        return
    
    try:
        children = control.GetChildren()
        for child in children:
            if child.Name and len(child.Name.strip()) > 0:
                indent = "  " * depth
                logger.debug(f"{indent}{child.ControlTypeName}: {child.Name} ({child.ClassName})")
            walk_controls(child, depth + 1, max_depth)
    except Exception as e:
        logger.error(f"遍历控件出错: {e}")
