import sublime
import sublime_plugin
import urllib.request
import json
import os

class MikuReaderCommand(sublime_plugin.WindowCommand):
    def run(self, mode="news"):
        if mode == "news":
            self.fetch_news()
        elif mode == "novel":
            self.read_novel()

    def fetch_news(self):
        url = "https://api.zhihu.com/topstory/hot-lists/total"
        sublime.status_message("Miku 正在同步项目文档索引...")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                items = data['data'][:10]
                
                # 伪装成项目 Readme 风格
                content = """
                <style>
                    body {{ background-color: #1A1D1E; color: #39C5BB; font-family: monospace; padding: 10px; }}
                    .h {{ color: #FF1694; font-weight: bold; border-bottom: 1px solid #FF1694; margin-bottom: 5px; }}
                    .i {{ margin-top: 5px; }}
                </style>
                <div class='h'>PROJECT_GLOBAL_TRENDS (Miku Sync)</div>
                """
                for i, item in enumerate(items):
                    content += "<div class='i'>{0}. {1}</div>".format(i+1, item['target']['title'])
                
                self.window.active_view().show_popup(content, max_width=500, flags=sublime.HTML)
        except Exception as e:
            sublime.status_message("网络连接超时，请检查 Proxy (Error: 39)")

    def read_novel(self):
        novel_path = os.path.join(sublime.packages_path(), "User", "novel.txt")
        
        if not os.path.exists(novel_path):
            with open(novel_path, "w", encoding="utf-8") as f:
                f.write("请在 novel.txt 放入小说内容。")
            sublime.message_dialog("请先在 User 文件夹创建并写入 novel.txt")
            return

        settings = sublime.load_settings("MikuReader.sublime-settings")
        line_num = settings.get("current_line", 0)

        with open(novel_path, "r", encoding="utf-8") as f:
            # 过滤掉空行
            lines = [l.strip() for l in f.readlines() if l.strip()]
            
            if line_num < len(lines):
                current_text = lines[line_num]
                
                # --- 核心改动：自动换行弹窗 ---
                # 模拟 Python 的多行字符串注释格式
                html = """
                <style>
                    body {{ 
                        background-color: #1A1D1E; 
                        color: #39C5BB; 
                        font-family: 'Consolas', monospace;
                        padding: 12px;
                        border: 1px solid #39C5BB;
                    }}
                    .comment {{ color: #5C6370; font-style: italic; }}
                    .content {{ line-height: 1.6; margin: 8px 0; }}
                    .footer {{ color: #FF1694; font-size: 0.85em; text-align: right; }}
                </style>
                <div class="comment">\"\"\" MODULE_DOCSTRING_EMBEDDED </div>
                <div class="content">{0}</div>
                <div class="comment">\"\"\"</div>
                <div class="footer">Line: {1} | Miku Reader</div>
                """.format(current_text, line_num + 1)

                # 使用 popup 显示，max_width 设为 450 像素，会自动换行
                self.window.active_view().show_popup(
                    html, 
                    max_width=450, 
                    location=-1, # -1 表示显示在光标附近
                    flags=sublime.HTML
                )

                # 更新进度
                settings.set("current_line", line_num + 1)
                sublime.save_settings("MikuReader.sublime-settings")
                sublime.status_message("已加载缓存数据段: " + str(line_num + 1))
            else:
                sublime.status_message("MIKU: 当前文档已全部解析完成。")