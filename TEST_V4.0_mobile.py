# -*- coding: utf-8 -*-
# 填空题练习软件 - 移动版 (基于TEST_V4.0)
# 适配安卓手机的填空题练习应用，支持中文字体显示

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.utils import platform
from kivy.core.text import LabelBase

from docx import Document
import random
import os

# 注册中文字体
if platform == 'android':
    # 安卓系统中文字体路径
    LabelBase.register(name='NotoSansCJK', 
                      fn_regular='/system/fonts/NotoSansCJK-Regular.ttc')
else:
    # Windows系统中文字体
    try:
        LabelBase.register(name='NotoSansCJK', 
                          fn_regular='C:/Windows/Fonts/msyh.ttc')  # 微软雅黑
    except:
        pass  # 如果字体不存在，使用默认字体

# 设置窗口大小（仅在桌面环境下有效）
if platform != 'android':
    Window.size = (400, 700)

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 标题
        title = Label(
            text='📚 填空题练习 - 精简版',
            size_hint_y=None,
            height=dp(60),
            font_size=dp(20),
            font_name='NotoSansCJK',
            bold=True,
            color=(0.2, 0.6, 1, 1)
        )
        main_layout.add_widget(title)
        
        # 按钮区域
        button_layout = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))
        
        # 创建按钮
        buttons = [
            ('📁 打开Word文档', self.select_document),
            ('🔀 随机练习', self.shuffle_questions),
            ('🔄 重新开始', self.restart_practice),
            ('🎯 开始练习', self.start_practice)
        ]
        
        for text, callback in buttons:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=dp(50),
                font_size=dp(16),
                font_name='NotoSansCJK',
                background_color=(0.2, 0.6, 1, 1)
            )
            btn.bind(on_press=callback)
            button_layout.add_widget(btn)
        
        # 状态显示
        self.status_label = Label(
            text='请选择Word文档开始练习',
            size_hint_y=None,
            height=dp(40),
            font_size=dp(14),
            font_name='NotoSansCJK',
            color=(0.5, 0.5, 0.5, 1)
        )
        button_layout.add_widget(self.status_label)
        
        main_layout.add_widget(button_layout)
        self.add_widget(main_layout)
    
    def select_document(self, instance):
        """选择文档"""
        app = App.get_running_app()
        app.show_file_chooser()
    
    def shuffle_questions(self, instance):
        """随机打乱题目"""
        app = App.get_running_app()
        app.shuffle_questions()
    
    def restart_practice(self, instance):
        """重新开始练习"""
        app = App.get_running_app()
        app.restart_practice()
    
    def start_practice(self, instance):
        """开始练习"""
        app = App.get_running_app()
        if app.questions:
            app.screen_manager.current = 'practice'
            practice_screen = app.screen_manager.get_screen('practice')
            practice_screen.show_question()
        else:
            self.show_popup('提示', '请先选择Word文档')
    
    def show_popup(self, title, message):
        """显示弹窗"""
        content = Label(
            text=message, 
            text_size=(dp(250), None), 
            halign='center',
            font_name='NotoSansCJK'
        )
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()

class PracticeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'practice'
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # 顶部导航
        nav_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.back_btn = Button(
            text='⬅️ 返回',
            size_hint_x=None,
            width=dp(80),
            font_name='NotoSansCJK',
            background_color=(0.5, 0.5, 0.5, 1)
        )
        self.back_btn.bind(on_press=self.go_back)
        nav_layout.add_widget(self.back_btn)
        
        self.progress_label = Label(
            text='第 1 / 1 题',
            font_size=dp(16),
            font_name='NotoSansCJK',
            bold=True
        )
        nav_layout.add_widget(self.progress_label)
        
        main_layout.add_widget(nav_layout)
        
        # 题目显示区域
        scroll = ScrollView()
        self.question_label = Label(
            text='',
            text_size=(None, None),
            font_size=dp(16),
            font_name='NotoSansCJK',
            size_hint_y=None,
            valign='top'
        )
        self.question_label.bind(texture_size=self.question_label.setter('size'))
        scroll.add_widget(self.question_label)
        main_layout.add_widget(scroll)
        
        # 答案输入区域
        input_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), spacing=dp(10))
        
        input_label = Label(
            text='请输入答案（多个答案用逗号分隔）：',
            size_hint_y=None,
            height=dp(30),
            font_size=dp(14),
            font_name='NotoSansCJK'
        )
        input_layout.add_widget(input_label)
        
        self.answer_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            font_size=dp(16),
            font_name='NotoSansCJK'
        )
        input_layout.add_widget(self.answer_input)
        
        # 按钮区域
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.hint_btn = Button(
            text='💡 提示',
            size_hint_x=0.3,
            font_name='NotoSansCJK',
            background_color=(1, 0.6, 0, 1)
        )
        self.hint_btn.bind(on_press=self.show_hint)
        button_layout.add_widget(self.hint_btn)
        
        self.submit_btn = Button(
            text='✅ 提交',
            size_hint_x=0.7,
            font_name='NotoSansCJK',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        self.submit_btn.bind(on_press=self.check_answer)
        button_layout.add_widget(self.submit_btn)
        
        input_layout.add_widget(button_layout)
        main_layout.add_widget(input_layout)
        
        # 导航按钮
        nav_button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        self.prev_btn = Button(
            text='⬅️ 上一题',
            font_name='NotoSansCJK',
            background_color=(0.6, 0.6, 0.6, 1)
        )
        self.prev_btn.bind(on_press=self.prev_question)
        nav_button_layout.add_widget(self.prev_btn)
        
        self.next_btn = Button(
            text='下一题 ➡️',
            font_name='NotoSansCJK',
            background_color=(0.6, 0.6, 0.6, 1)
        )
        self.next_btn.bind(on_press=self.next_question)
        nav_button_layout.add_widget(self.next_btn)
        
        main_layout.add_widget(nav_button_layout)
        
        # 结果显示
        self.result_label = Label(
            text='',
            size_hint_y=None,
            height=dp(60),
            font_size=dp(14),
            font_name='NotoSansCJK',
            text_size=(None, None)
        )
        main_layout.add_widget(self.result_label)
        
        # 统计信息
        self.stats_label = Label(
            text='准备开始练习...',
            size_hint_y=None,
            height=dp(40),
            font_size=dp(12),
            font_name='NotoSansCJK',
            color=(0.2, 0.7, 0.2, 1)
        )
        main_layout.add_widget(self.stats_label)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        """返回主界面"""
        app = App.get_running_app()
        app.screen_manager.current = 'main'
    
    def show_question(self):
        """显示当前题目"""
        app = App.get_running_app()
        if not app.questions:
            return
        
        question = app.questions[app.current_index]
        
        # 更新进度
        self.progress_label.text = f'第 {app.current_index + 1} / {len(app.questions)} 题'
        
        # 显示题目
        self.question_label.text = question["question"]
        self.question_label.text_size = (Window.width - dp(40), None)
        
        # 清空答案输入框和结果
        self.answer_input.text = ''
        self.result_label.text = ''
        
        # 更新按钮状态
        self.prev_btn.disabled = (app.current_index == 0)
        self.next_btn.disabled = (app.current_index == len(app.questions) - 1)
        
        # 聚焦到输入框
        self.answer_input.focus = True
        
        # 更新统计信息
        app.update_stats()
    
    def check_answer(self, instance):
        """检查答案"""
        app = App.get_running_app()
        if not app.questions:
            return
        
        user_answer = self.answer_input.text.strip()
        if not user_answer:
            self.show_popup('提示', '请输入答案')
            return
        
        # 处理用户输入（支持中英文逗号分隔）
        user_answers = [ans.strip() for ans in user_answer.replace(',', '，').split('，')]
        correct_answers = app.questions[app.current_index]["answers"]
        
        app.answered += 1
        
        # 简单的答案匹配
        is_correct = set(user_answers) == set(correct_answers)
        
        if is_correct:
            app.score += 1
            self.result_label.text = '✅ 正确！'
            self.result_label.color = (0, 1, 0, 1)
        else:
            self.result_label.text = f'❌ 错误！正确答案：{", ".join(correct_answers)}'
            self.result_label.color = (1, 0, 0, 1)
        
        app.update_stats()
        
        # 1秒后自动跳转到下一题
        Clock.schedule_once(self.auto_next, 1)
    
    def auto_next(self, dt):
        """自动跳转到下一题"""
        app = App.get_running_app()
        if app.current_index < len(app.questions) - 1:
            self.next_question(None)
        else:
            # 练习完成
            self.show_completion_dialog()
    
    def show_hint(self, instance):
        """显示答案提示"""
        app = App.get_running_app()
        if not app.questions:
            return
        
        correct_answers = app.questions[app.current_index]["answers"]
        
        # 直接显示完整答案
        hint_text = f'💡 答案: {", ".join(correct_answers)}'
        self.result_label.text = hint_text
        self.result_label.color = (1, 0.6, 0, 1)
        
        app.hints_used += 1
        app.update_stats()
    
    def prev_question(self, instance):
        """上一题"""
        app = App.get_running_app()
        if app.current_index > 0:
            app.current_index -= 1
            self.show_question()
    
    def next_question(self, instance):
        """下一题"""
        app = App.get_running_app()
        if app.current_index < len(app.questions) - 1:
            app.current_index += 1
            self.show_question()
    
    def show_completion_dialog(self):
        """显示完成对话框"""
        app = App.get_running_app()
        accuracy = (app.score / app.answered * 100) if app.answered > 0 else 0
        
        completion_msg = f"""🎉 恭喜完成练习！

总题数：{len(app.questions)}
正确：{app.score}
错误：{app.answered - app.score}
正确率：{accuracy:.1f}%"""
        
        content = BoxLayout(orientation='vertical', spacing=dp(10))
        
        content.add_widget(Label(
            text=completion_msg,
            text_size=(dp(300), None),
            halign='center',
            valign='center',
            font_name='NotoSansCJK'
        ))
        
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        restart_btn = Button(
            text='重新开始', 
            font_name='NotoSansCJK',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        close_btn = Button(
            text='返回主界面', 
            font_name='NotoSansCJK',
            background_color=(0.6, 0.6, 0.6, 1)
        )
        
        button_layout.add_widget(restart_btn)
        button_layout.add_widget(close_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='练习完成',
            content=content,
            size_hint=(0.8, 0.6)
        )
        
        def restart(instance):
            popup.dismiss()
            app.restart_practice()
            self.show_question()
        
        def go_main(instance):
            popup.dismiss()
            app.screen_manager.current = 'main'
        
        restart_btn.bind(on_press=restart)
        close_btn.bind(on_press=go_main)
        
        popup.open()
    
    def show_popup(self, title, message):
        """显示弹窗"""
        content = Label(
            text=message, 
            text_size=(dp(250), None), 
            halign='center',
            font_name='NotoSansCJK'
        )
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()

class PracticeApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # 数据
        self.questions = []
        self.current_index = 0
        self.score = 0
        self.answered = 0
        self.hints_used = 0  # 记录使用提示的次数
    
    def build(self):
        """构建应用"""
        self.screen_manager = ScreenManager()
        
        # 添加屏幕
        self.screen_manager.add_widget(MainScreen())
        self.screen_manager.add_widget(PracticeScreen())
        
        return self.screen_manager
    
    def show_file_chooser(self):
        """显示文件选择器"""
        content = BoxLayout(orientation='vertical')
        
        if platform == 'android':
            # 安卓平台的文件路径
            filechooser = FileChooserIconView(
                path='/storage/emulated/0/Download',
                filters=['*.docx']
            )
        else:
            # 桌面平台的文件路径
            filechooser = FileChooserIconView(
                filters=['*.docx']
            )
        
        content.add_widget(filechooser)
        
        button_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        
        select_btn = Button(
            text='选择',
            font_name='NotoSansCJK',
            background_color=(0.2, 0.8, 0.2, 1)
        )
        cancel_btn = Button(
            text='取消',
            font_name='NotoSansCJK',
            background_color=(0.6, 0.6, 0.6, 1)
        )
        
        button_layout.add_widget(select_btn)
        button_layout.add_widget(cancel_btn)
        content.add_widget(button_layout)
        
        popup = Popup(
            title='选择Word文档',
            content=content,
            size_hint=(0.9, 0.8)
        )
        
        def select_file(instance):
            if filechooser.selection:
                file_path = filechooser.selection[0]
                popup.dismiss()
                self.load_document(file_path)
        
        def cancel(instance):
            popup.dismiss()
        
        select_btn.bind(on_press=select_file)
        cancel_btn.bind(on_press=cancel)
        
        popup.open()
    
    def load_document(self, file_path):
        """加载Word文档"""
        try:
            self.questions = self.parse_docx(file_path)
            if not self.questions:
                self.show_popup("提示", "未找到红色字体内容，请检查文档格式")
                return
            
            self.current_index = 0
            self.score = 0
            self.answered = 0
            self.hints_used = 0
            
            # 更新主界面状态
            main_screen = self.screen_manager.get_screen('main')
            main_screen.status_label.text = f'已加载 {len(self.questions)} 道题目'
            
            self.show_popup("成功", f"已加载 {len(self.questions)} 道题目")
            
        except Exception as e:
            self.show_popup("错误", f"加载文档失败：{str(e)}")
    
    def parse_docx(self, file_path):
        """解析Word文档，提取红色字体作为答案"""
        doc = Document(file_path)
        questions = []
        
        for para in doc.paragraphs:
            if not para.text.strip():
                continue
            
            question_text = ""
            answers = []
            has_red = False
            
            for run in para.runs:
                # 检查字体颜色
                if run.font.color and run.font.color.rgb:
                    color = str(run.font.color.rgb).lower()
                    if color == "ff0000" or "red" in color:
                        # 红色字体作为答案
                        has_red = True
                        answers.append(run.text)
                        question_text += "______"  # 用下划线替换
                    else:
                        question_text += run.text
                else:
                    question_text += run.text
            
            if has_red and answers:
                questions.append({
                    "question": question_text,
                    "answers": answers
                })
        
        return questions
    
    def shuffle_questions(self):
        """随机打乱题目顺序"""
        if not self.questions:
            self.show_popup("提示", "请先加载题库")
            return
        
        random.shuffle(self.questions)
        self.current_index = 0
        
        # 如果在练习界面，更新显示
        if self.screen_manager.current == 'practice':
            practice_screen = self.screen_manager.get_screen('practice')
            practice_screen.show_question()
        
        self.show_popup("提示", "题目顺序已打乱")
    
    def restart_practice(self):
        """重新开始"""
        if not self.questions:
            self.show_popup("提示", "请先加载题库")
            return
        
        self.current_index = 0
        self.score = 0
        self.answered = 0
        self.hints_used = 0
        
        # 如果在练习界面，更新显示
        if self.screen_manager.current == 'practice':
            practice_screen = self.screen_manager.get_screen('practice')
            practice_screen.show_question()
        
        self.show_popup("提示", "已重新开始")
    
    def update_stats(self):
        """更新统计信息"""
        if self.screen_manager.current == 'practice':
            practice_screen = self.screen_manager.get_screen('practice')
            if self.answered > 0:
                accuracy = self.score / self.answered * 100
                practice_screen.stats_label.text = f'已答 {self.answered} 题 | 正确 {self.score} 题 | 正确率 {accuracy:.1f}% | 提示 {self.hints_used} 次'
            else:
                practice_screen.stats_label.text = '准备开始练习...'
    
    def show_popup(self, title, message):
        """显示弹窗"""
        content = Label(
            text=message, 
            text_size=(dp(250), None), 
            halign='center',
            font_name='NotoSansCJK'
        )
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == '__main__':
    PracticeApp().run()