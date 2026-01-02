import sublime
import sublime_plugin

class QueryKeyBindingCommand(sublime_plugin.WindowCommand):
    def run(self):
        # 调起底部面板
        self.window.show_input_panel("Miku 查询 (输入 :keys):", "", self.on_done, None, None)

    def on_done(self, text):
        if text.strip() == ":keys":
            self.opacity = 0.9  # 初始透明度调高一点，方便看清初音绿
            self.show_animated_popup()

    def get_content(self, opacity):
        # 核心配色：Miku Teal (#39C5BB), Miku Pink (#FF1694)
        return """
        <style>
            body {{ 
                background-color: rgba(26, 29, 30, {0}); 
                color: rgba(240, 240, 240, {0}); 
                padding: 15px;
                border: 1px solid rgba(57, 197, 187, {0});
            }}
            .title {{ 
                color: rgba(57, 197, 187, {0}); 
                font-weight: bold; 
                margin-bottom: 10px; 
                border-bottom: 1px solid rgba(255, 22, 148, {0});
            }}
            .key {{ color: rgba(255, 22, 148, {0}); font-family: monospace; font-weight: bold; }}
            .desc {{ color: rgba(57, 197, 187, {0}); }}
            .highlight {{ 
                background-color: rgba(57, 197, 187, {0}); 
                color: #1A1D1E; 
                padding: 0 4px; 
                border-radius: 3px;
            }}
        </style>
        <div class="title">MIKU 快捷键速查</div>
        <div class="row"><span class="highlight">f</span> <span class="key">[F5]</span>: <span class="desc">运行 Python</span></div>
        <div class="row"><span class="highlight">p</span> <span class="key">[F6]</span>: <span class="desc">Python 交互终端</span></div>
        <div class="row"><span class="highlight">q</span> <span class="key">[F10]</span>: <span class="desc">查询面板</span></div>
        <div class="row" style="margin-top:5px; font-size: 0.9em; color: #5C6370;">(10s 后消失或按 Esc)</div>
        """.format(opacity)

    def show_animated_popup(self):
        view = self.window.active_view()
        if not view: return

        view.show_popup(
            self.get_content(self.opacity),
            flags=sublime.HTML,
            location=-1,
            max_width=500
        )

        # 8秒后开始淡出
        sublime.set_timeout(self.fade_out, 8000)

    def fade_out(self):
        view = self.window.active_view()
        if not view or not view.is_popup_visible(): return

        if self.opacity > 0.1:
            self.opacity -= 0.1
            view.update_popup(self.get_content(self.opacity))
            sublime.set_timeout(self.fade_out, 100)
        else:
            view.hide_popup()

# miku

class MikuSimpleListener(sublime_plugin.EventListener):
    def on_activated(self, view):
        # 切换到文件时，状态栏显示 Miku 的问候
        sublime.status_message("MIKU: 欢迎回来，今天也要加油哦！ ♪")