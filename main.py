import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time
from PIL import Image, ImageTk


class ColorPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("实时屏幕颜色拾取器")
        self.root.geometry("300x300") #窗口大小
        self.root.resizable(False, False)

        # 创建界面元素
        self.create_widgets()

        # 控制线程运行的标志
        self.running = False
        self.thread = None

        # 开始监控
        self.start_monitoring()

        # 窗口关闭事件处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # 坐标显示
        self.coord_label = ttk.Label(self.root, text="坐标: (0, 0)", font=("Arial", 12))
        self.coord_label.pack(pady=10)

        # 颜色显示区域
        self.color_frame = tk.Frame(self.root, width=100, height=100, relief="solid", borderwidth=2)
        self.color_frame.pack(pady=10)
        self.color_frame.pack_propagate(False)  # 防止框架被内部元素撑大

        # 颜色值显示
        self.color_label = ttk.Label(self.root, text="RGB: (0, 0, 0)", font=("Arial", 10))
        self.color_label.pack(pady=5)

        # 十六进制颜色值显示
        self.hex_label = ttk.Label(self.root, text="HEX: #000000", font=("Arial", 10))
        self.hex_label.pack(pady=5)

    def start_monitoring(self):
        """开始监控鼠标位置和颜色"""
        self.running = True
        self.thread = threading.Thread(target=self.monitor_mouse, daemon=True)
        self.thread.start()

    def monitor_mouse(self):
        """监控鼠标位置并获取颜色"""
        while self.running:
            try:
                # 获取鼠标位置
                x, y = pyautogui.position()

                # 获取屏幕截图（1x1像素）
                screenshot = pyautogui.screenshot(region=(x, y, 1, 1))

                # 获取RGB颜色值
                r, g, b = screenshot.getpixel((0, 0))

                # 更新UI（需要在主线程中执行）
                self.root.after(0, self.update_ui, x, y, r, g, b)

                # 短暂休眠以减少CPU使用率
                time.sleep(0.05)
            except Exception as e:
                print(f"错误: {e}")
                break

    def update_ui(self, x, y, r, g, b):
        """更新UI显示"""
        # 更新坐标
        self.coord_label.config(text=f"坐标: ({x}, {y})")

        # 更新颜色显示区域
        self.color_frame.config(bg=self.rgb_to_hex(r, g, b))

        # 更新RGB值
        self.color_label.config(text=f"RGB: ({r}, {g}, {b})")

        # 更新十六进制值
        self.hex_label.config(text=f"HEX: {self.rgb_to_hex(r, g, b)}")

    def rgb_to_hex(self, r, g, b):
        """将RGB颜色转换为十六进制格式"""
        return f"#{r:02x}{g:02x}{b:02x}".upper()

    def on_closing(self):
        """窗口关闭时的清理工作"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1)
        self.root.destroy()


if __name__ == "__main__":
    # 检查依赖库是否已安装
    try:
        import pyautogui
        from PIL import Image, ImageTk
    except ImportError as e:
        print(f"缺少必要的依赖库: {e}")
        print("请使用以下命令安装:")
        print("pip install pyautogui pillow")
        exit(1)

    # 创建主窗口
    root = tk.Tk()
    app = ColorPicker(root)
    root.mainloop()