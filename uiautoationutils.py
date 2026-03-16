import uiautomation as auto


def demo_get_desktop():
    print("=== 获取桌面信息 ===")
    desktop = auto.GetRootControl()
    print(f"桌面控件名称: {desktop.Name}")
    print(f"桌面控件类名: {desktop.ClassName}")
    print(f"桌面控件进程ID: {desktop.ProcessId}")
    print()


def demo_find_window(title):
    print("=== 查找窗口示例 ===")
    notepad = auto.WindowControl(searchDepth=1, Name=title)
    if not notepad.Exists(maxSearchSeconds=1):
        print("未找到记事本窗口")
    else:
        print(f"找到窗口: {notepad.Name}")
        print(f"窗口类名: {notepad.ClassName}")
        print(f"窗口进程ID: {notepad.ProcessId}")
    print()


def demo_list_windows():
    print("=== 列出顶层窗口 ===")
    desktop = auto.GetRootControl()
    windows = desktop.GetChildren()
    for i, win in enumerate(windows[:10]):
        if win.Name:
            print(f"{i+1}. {win.Name} ({win.ClassName})")
    print(f"共找到 {len(windows)} 个顶层窗口，显示前10个")
    print()


def demo_get_control_info():
    print("=== 获取控件信息示例 ===")
    desktop = auto.GetRootControl()
    children = desktop.GetChildren()
    if children:
        first_window = children[0]
        print(f"第一个窗口名称: {first_window.Name}")
        print(f"第一个窗口类名: {first_window.ClassName}")
        window_children = first_window.GetChildren()
        print(f"该窗口下有 {len(window_children)} 个子控件")
        if window_children:
            print(f"第一个子控件: {window_children[0].Name} ({window_children[0].ClassName})")
    print()


def demo_search_control():
    print("=== 搜索控件示例 ===")
    desktop = auto.GetRootControl()
    button = auto.ButtonControl(searchFromControl=desktop, Name="确定")
    if button.Exists(maxSearchSeconds=1):
        print(f"找到按钮: {button.Name}")
    else:
        print("未找到名为'确定'的按钮")
    print()


def demo_write_to_notepad(title, text):
    print("=== 写入记事本示例 ===")
    notepad = auto.WindowControl(searchDepth=1, Name=title)
    if not notepad.Exists(maxSearchSeconds=2):
        print("未找到记事本窗口")
        return False
    
    print(f"找到窗口: {notepad.Name}")
    
    edit = notepad.EditControl()
    if edit.Exists(maxSearchSeconds=1):
        edit.SetFocus()
        auto.SendKeys(text)
        print(f"已写入内容: {text}")
        return True
    else:
        print("未找到编辑区域")
        return False


def demo_tree_view_window(title, max_depth=100):
    print(f"=== 遍历窗口元素: {title} ===")
    window = auto.WindowControl(searchDepth=1, Name=title)
    if not window.Exists(maxSearchSeconds=2):
        print("未找到窗口")
        return
    
    print(f"窗口: {window.Name} ({window.ClassName})\n")
    
    def walk_controls(control, depth, max_depth):
        if depth > max_depth:
            return
        try:
            children = control.GetChildren()
            for child in children:
                if child.Name:
                    indent = "  " * depth
                    print(f"{indent}{child.ControlTypeName}: {child.Name} ({child.ClassName})")
                walk_controls(child, depth + 1, max_depth)
        except Exception:
            pass
    
    walk_controls(window, 0, max_depth)
    print(f"\n遍历完成 (最大深度: {max_depth})")


if __name__ == "__main__":
    print("UIAutomation Demo 开始\n")
    print("=" * 50)

    demo_get_desktop()
    demo_list_windows()
    demo_find_window()
    demo_get_control_info()
    demo_search_control()

    print("=" * 50)
    print("Demo 执行完成")
