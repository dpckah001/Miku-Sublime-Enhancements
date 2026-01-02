import sublime
import sublime_plugin

def plugin_loaded():
    # 稍微延迟，等待 UI 完全加载
    sublime.set_timeout_async(start_miku_ultra_boot, 500)

def start_miku_ultra_boot():
    window = sublime.active_window()
    if not window: return

    # 1. 创建并显示 Miku 专属控制台
    panel = window.create_output_panel("miku_boot")
    window.run_command("show_panel", {"panel": "output.miku_boot"})
    panel.set_read_only(False)
    
    # 状态栏闪烁序列：葱绿(39C5BB) 与 粉(FF1694) 的意象
    # 虽然不能直接改状态栏颜色，但我们可以通过字符切换模拟“警示灯”效果
    flash_msgs = [
        "MIKU-OS >>> [ SYSTEM START ]",
        "MIKU-OS >>> [ ■■■■■■■■■■ ]",
        "MIKU-OS >>> [ □□□□□□□□□□ ]"
    ]
    
    def flash_status(count):
        if count > 0:
            msg = flash_msgs[count % 3]
            sublime.status_message(msg)
            sublime.set_timeout_async(lambda: flash_status(count - 1), 200)

    # 2. 定义启动日志和进度条
    boot_sequence = [
        "MEM_CHECKING... [ OK ]",
        "VOCALOID_CORE... [ LOADING ]",
        "[██░░░░░░░░] 20%",
        "VOCALOID_CORE... [ SUCCESS ]",
        "CONNECTING TO HATSUNE_NET... [CONNECTED]",
        "[██████░░░░] 60%",
        "LOADING ASSETS: 'Leek_Sword.obj'...",
        "LOADING ASSETS: 'Teal_Hair_Texture'...",
        "[██████████] 100%",
        "STATUS: ALL SYSTEMS 39! (MIKU)",
        "",
        "       ━━━━━━━◥◣◆◢◤━━━━━━━",
        "          HATSUNE MIKU v3.9",
        "             ⊂ヽ(  ^ω^)つ",
        "              )   / ",
        "             (_ノ  ",
        "       ━━━━━━━◥◣◆◢◤━━━━━━━",
        "       READY TO WORK? LET'S GO!",
        ""
    ]

    def type_logs(index):
        if index < len(boot_sequence):
            panel.run_command("append", {"characters": boot_logs[index] + "\n"})
            # 每一行出现的频率，进度条部分快一点，文字部分慢一点
            delay = 50 if "█" in boot_sequence[index] else 150
            sublime.set_timeout_async(lambda: type_logs(index + 1), delay)
        else:
            # 播放完成，闪烁状态栏
            flash_status(15)
            # 4秒后自动关闭面板
            sublime.set_timeout_async(lambda: window.run_command("hide_panel", {"cancel": True}), 4000)

    boot_logs = boot_sequence
    type_logs(0)