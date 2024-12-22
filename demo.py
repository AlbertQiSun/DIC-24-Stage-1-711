import tkinter as tk
import json
from openai import OpenAI
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import PhotoImage
import base64
from io import BytesIO

class Pet:
    def __init__(self):
        self.root = self.main_stream()
        self.Image = None
        self.add_drag_functionality(self.root)
        self.client = OpenAI()
        self.gpt_window_open = False
        self.img = None
        self.default_prompt = 'You are a very helpful personalized learning helper to help student to learn better. Since I provide you with the previous chat for the context conversation, please use the informatino I provided to make more clear and responsible answers'

    def main_stream(self):
        root = tk.Tk()
        root.overrideredirect(True)
        root.wm_attributes("-topmost", 1)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width, window_height = 150, 150
        x = screen_width - window_width * 2
        y = screen_height - window_height * 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.bind("<Button-3>", self.show_menu)
        return root

    def show_menu(self, event):
        if hasattr(self, "menu_window") and self.menu_window.winfo_exists():
            self.menu_window.destroy()
        self.menu_window = tk.Toplevel(self.root)
        self.menu_window.overrideredirect(True)
        menu_x = event.x_root
        menu_y = event.y_root - 150
        menu_width = 100
        self.menu_window.geometry(f"{menu_width}x150+{menu_x}+{menu_y}")
        self.menu_window.wm_attributes("-topmost", 1)
        button_names = ["Ask GPT", "Function2", "Setting", "Exit"]
        menu_height = len(button_names) * 50
        self.menu_window.geometry(f"{menu_width}x{menu_height}+{menu_x}+{menu_y}")
        def on_enter(event, button):
            button.config(bg="#ddd", fg="black")  # 鼠标悬停时改变背景和文字颜色
        def on_leave(event, button):
            button.config(bg="#f0f0f0", fg="black")  # 鼠标离开时恢复背景颜色
        for name in button_names:
            btn = tk.Button(
                self.menu_window,
                text=name,
                command=lambda n=name: self.button_action(n, self.menu_window),
                relief="flat",
                bd=0,
                bg="#f0f0f0",
                fg="black",
                height=2
            )
            btn.pack(fill="both", pady=0, padx=0, expand=True)  # 使按钮填满菜单并紧密排列
            btn.bind("<Enter>", lambda e, b=btn: on_enter(e, b))  # 鼠标进入事件
            btn.bind("<Leave>", lambda e, b=btn: on_leave(e, b))  # 鼠标离开事件
        def start_drag(event):
            self.menu_window.x = event.x
            self.menu_window.y = event.y
        def drag_window(event):
            dx = event.x - self.menu_window.x
            dy = event.y - self.menu_window.y
            self.menu_window.geometry(f"+{self.menu_window.winfo_x() + dx}+{self.menu_window.winfo_y() + dy}")
        self.menu_window.bind("<Button-1>", start_drag)
        self.menu_window.bind("<B1-Motion>", drag_window)
        def close_menu(event):
            if self.menu_window.winfo_exists():
                self.menu_window.destroy()
        self.root.bind("<Button-1>", close_menu, add="+")

    def add_drag_functionality(self, window):
        def start_drag(event):
            window.x = event.x
            window.y = event.y
        def drag_window(event):
            dx = event.x - window.x
            dy = event.y - window.y
            window.geometry(f"+{window.winfo_x() + dx}+{window.winfo_y() + dy}")
        window.bind("<Button-1>", start_drag)
        window.bind("<B1-Motion>", drag_window)

    def read_setting(self):
        with open('setting.json', 'r', encoding='utf-8') as setting_file:
            setting = json.load(setting_file)
        return setting['Username'], setting['Custom']

    def log_in(self):
        try:
            with open('setting.json', 'r', encoding='utf-8') as setting_file:
                setting = json.load(setting_file)
            username = setting.get('Username')
            custom = setting.get('Custom', 'Default.png')
            if not username:
                raise ValueError("Username is missing in the setting file.")
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            self.sign_up()
            with open('setting.json', 'r', encoding='utf-8') as setting_file:
                setting = json.load(setting_file)
            username = setting.get('Username')
            custom = setting.get('Custom', 'Default.png')
        return username, custom

    def show(self):
        not_first_time, Username = self.log_in()
        if not_first_time:
            self.root.mainloop()

    def sign_up(self):
        self.signing = tk.Tk()
        self.signing.overrideredirect(True)
        window_width, window_height = 300, 200
        screen_width = self.signing.winfo_screenwidth()
        screen_height = self.signing.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.signing.geometry(f"{window_width}x{window_height}+{x}+{y}")
        def start_drag(event):
            self.signing.x = event.x
            self.signing.y = event.y
        def drag_window(event):
            dx = event.x - self.signing.x
            dy = event.y - self.signing.y
            self.signing.geometry(f"+{self.signing.winfo_x() + dx}+{self.signing.winfo_y() + dy}")
        self.signing.bind("<Button-1>", start_drag)
        self.signing.bind("<B1-Motion>", drag_window)
        title_label = tk.Label(self.signing, text='Please sign up to the environment')
        title_label.pack()
        user_info_entry = tk.Entry(self.signing, width=30)
        user_info_entry.pack()
        error_label = tk.Label(self.signing, text="", fg="red")
        error_label.pack()
        def on_sign_up():
            user_info = user_info_entry.get().strip()
            if user_info:
                with open('setting.json', 'w', encoding='utf-8') as setting_file:
                    json.dump({'Username': user_info, 'Custom': 'Default.png'}, setting_file)
                self.signing.destroy()
            else:
                error_label.config(text="Invalid username: cannot be empty or just spaces.")
        sign_up_button = tk.Button(self.signing, text='Sign Up', command=on_sign_up)
        sign_up_button.pack(pady=10)
        self.signing.bind('<Return>', lambda event: on_sign_up())
        self.signing.mainloop()

    def button_action(self, button_name, event):
        if button_name == "Exit":
            exit()
        if button_name == "Ask GPT":
            if not self.gpt_window_open:
                self.history = ''
                # 打开 GPT 窗口
                menu_x = self.menu_window.winfo_x()
                menu_y = self.menu_window.winfo_y()
                self.menu_window.destroy()
                self.gpt = tk.Toplevel(self.root)
                self.gpt.overrideredirect(True)
                self.gpt.wm_attributes("-topmost", 1)
                gpt_width = 700
                gpt_height = 300
                gpt_x = menu_x - gpt_width
                gpt_y = menu_y - gpt_height
                self.gpt.geometry(f"{gpt_width}x{gpt_height}+{gpt_x}+{gpt_y}")
                self.add_drag_functionality(self.gpt)

                # 聊天框
                frame = tk.Frame(self.gpt)
                frame.pack(fill="both", expand=True, padx=5, pady=5)
                self.chat_display = tk.Text(frame, wrap="word", state="disabled", height=15)
                scrollbar = tk.Scrollbar(frame, command=self.chat_display.yview)
                self.chat_display.config(yscrollcommand=scrollbar.set)
                self.chat_display.grid(row=0, column=0, sticky="nsew")
                scrollbar.grid(row=0, column=1, sticky="ns")
                frame.grid_rowconfigure(0, weight=1)
                frame.grid_columnconfigure(0, weight=1)

                # 输入框与按钮
                input_frame = tk.Frame(self.gpt)
                input_frame.pack(fill="x", padx=5, pady=5)
                self.input_box = tk.Entry(input_frame, width=50)
                self.input_box.pack(side="left", fill="x", expand=True, padx=5)
                submit_button = tk.Button(input_frame, text="Close", command=self.close_chat)
                submit_button.pack(side="right", padx=5)
                upload_button = tk.Button(input_frame, text="Upload Image", command=self.upload_image)
                upload_button.pack(side="left", padx=5)
                screen_shot = tk.Button(input_frame, text="Screenshot", command=self.get_screen_shot)
                screen_shot.pack(side="right", padx=5)
                close_btn = tk.Button(input_frame, text="Send", command=self.send_message)
                close_btn.pack(side="right", padx=5)
                self.gpt.bind('<Return>', lambda event: self.send_message())
                self.gpt_window_open = True

    def close_chat(self):
        self.gpt.destroy()
        self.history = ''
        self.gpt_window_open = False

    def encode_image(self):
        buffer = BytesIO()
        self.img.save(buffer, format="PNG")
        buffer.seek(0)
        self.encoded_image = base64.b64encode(buffer.read()).decode('utf-8')
        self.img = None
    def send_message(self):
        if self.img is None:
            self.chat_without_image()
        else:
            self.chat_with_image()

    def chat_without_image(self):
        self.chat_display.config(state="normal")
        new_prompt = self.input_box.get().strip()
        self.input_box.delete(0, tk.END)
        self.chat_display.insert('end', f"\nUser:\n{new_prompt}\n\n")
        self.history += new_prompt + '\n'
        if new_prompt != '':
            message_to_send = f"Here is the history for the previous chats:\n{self.history}\n{new_prompt}"
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                    "role": "user",
                    "content": self.default_prompt,
                },
                    {
                        "role": "system",
                        "content": message_to_send
                    }
                ],
                stream=True,
            )
            self.chat_display.insert('end', "GPT response:\n")
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    response_content = chunk.choices[0].delta.content
                    self.history += f"{response_content}"
                    self.chat_display.insert("end", f"{response_content}")
            self.chat_display.insert('end', "\n")
            self.history += '\n'
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def chat_with_image(self):
        self.chat_display.config(state="normal")
        new_prompt = self.input_box.get().strip()
        self.input_box.delete(0, tk.END)
        self.encode_image()
        encoded_image = self.encoded_image
        self.chat_display.insert('end', f"\nUser:\n{new_prompt}\n\n")
        self.history += new_prompt + '\n'
        print(self.history)
        if new_prompt != "":
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": self.default_prompt
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": new_prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{encoded_image}"
                                },
                            },
                        ],
                    }
                ],
            )
            response_content = response.choices[0].message.content
            self.history += f"{response_content}"
            self.chat_display.insert("end", f"{response_content}")
            self.chat_display.insert('end', "\n")
            self.history += '\n'
            print(self.history)
        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def get_screen_shot(self):
        pass

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if file_path:
            self.load_image(file_path)

    def load_image(self, file_path):
        self.img = Image.open(file_path)

    def update_chat(self, sender, message, is_image=False):
        self.chat_display.config(state="normal")
        if is_image:
            try:
                img = PhotoImage(file=message)
                self.chat_display.image_create("end", image=img)
                self.chat_display.insert("end", f"\n")
                self.chat_display.image = img  # 保持对图片的引用
            except Exception as e:
                self.chat_display.insert("end", f"{sender}: {message} (Error: {str(e)})\n")
        else:
            self.chat_display.insert("end", f"{sender}: {message}\n")

        self.chat_display.config(state="disabled")
        self.chat_display.see("end")


# 初始化并运行
if __name__ == "__main__":
    Pet = Pet()
    Pet.show()

