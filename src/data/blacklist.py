"""
黑名单操作模块

提供黑名单的增删改查功能
"""

from datetime import datetime
from typing import Optional, List, Dict

import orjson
from loguru import logger

from src.data.db import get_connection


def add(name: str, class_name: Optional[str] = None, description: str = "") -> int:
    """
    添加窗口到黑名单

    Args:
        name: 窗口名称
        class_name: 窗口类名（可选）
        description: 描述信息

    Returns:
        int: 新增记录的 ID
    """
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    
    cursor.execute(
        "INSERT INTO window_blacklist (name, class_name, description, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (name, class_name, description, now, now)
    )
    
    row_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    logger.success(f"添加黑名单成功: {name} (ID: {row_id})")
    return row_id


def remove(id: int) -> bool:
    """
    从黑名单移除

    Args:
        id: 记录 ID

    Returns:
        bool: 是否成功删除
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM window_blacklist WHERE id = ?", (id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    if deleted:
        logger.success(f"从黑名单移除成功: ID {id}")
    else:
        logger.warning(f"黑名单中未找到 ID: {id}")
    
    return deleted


def get_all() -> List[Dict]:
    """
    获取黑名单所有记录

    Returns:
        list: 黑名单记录列表
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM window_blacklist ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def exists(name: str, class_name: Optional[str] = None) -> bool:
    """
    检查窗口是否在黑名单中

    Args:
        name: 窗口名称
        class_name: 窗口类名

    Returns:
        bool: 是否在黑名单中
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if class_name:
        cursor.execute(
            "SELECT id FROM window_blacklist WHERE name = ? OR class_name = ?",
            (name, class_name)
        )
    else:
        cursor.execute(
            "SELECT id FROM window_blacklist WHERE name = ?",
            (name,)
        )
    
    result = cursor.fetchone() is not None
    conn.close()
    
    return result


def to_json() -> str:
    """
    导出黑名单为 JSON 格式

    Returns:
        str: JSON 格式的黑名单数据
    """
    data = get_all()
    return orjson.dumps(data, option=orjson.OPT_INDENT_2).decode("utf-8")
