from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle

Window.clearcolor = (0.04, 0.06, 0.12, 1)


class RoundedButton(Button):
    fill_color = (0.09, 0.13, 0.22, 1)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)
        self.font_size = sp(23)
        self.bold = True
        self.bind(pos=self.draw_background, size=self.draw_background)

    def draw_background(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.fill_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])


class PhunganCalculator(App):
    def build(self):
        self.expression = ""
        self.just_calculated = False
        self.root_box = BoxLayout(orientation="vertical")
        self.show_welcome()
        return self.root_box

    def show_welcome(self, *args):
        self.root_box.clear_widgets()
        page = BoxLayout(
            orientation="vertical",
            padding=dp(28),
            spacing=dp(18)
        )
        page.add_widget(Label(text="", size_hint_y=0.8))

        title = Label(
            text="[b]Welcome to[/b]",
            markup=True,
            font_size=sp(25),
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(48)
        )
        page.add_widget(title)

        app_name = Label(
            text="[b]Phungan Calculator[/b]",
            markup=True,
            font_size=sp(30),
            color=(0.28, 0.62, 1, 1),
            size_hint_y=None,
            height=dp(58)
        )
        page.add_widget(app_name)

        tagline = Label(
            text="Simple. Smart. Powerful.",
            font_size=sp(16),
            color=(0.62, 0.69, 0.82, 1),
            size_hint_y=None,
            height=dp(35)
        )
        page.add_widget(tagline)

        start = RoundedButton(
            text="Let's Calculate",
            size_hint=(1, None),
            height=dp(54)
        )
        start.fill_color = (0.08, 0.40, 0.92, 1)
        start.bind(on_press=self.show_calculator)
        page.add_widget(start)
        page.add_widget(Label(text="", size_hint_y=0.8))
        self.root_box.add_widget(page)

        # Automatically open the calculator after 2.5 seconds.
        Clock.schedule_once(self.show_calculator, 2.5)

    def show_calculator(self, *args):
        self.root_box.clear_widgets()
        root = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(12)
        )

        header = BoxLayout(
            size_hint_y=None,
            height=dp(55),
            spacing=dp(10)
        )
        logo = Label(
            text="[b]P[/b]",
            markup=True,
            font_size=sp(28),
            color=(0.28, 0.62, 1, 1),
            size_hint_x=None,
            width=dp(45)
        )
        header.add_widget(logo)

        name_box = BoxLayout(orientation="vertical", spacing=0)
        name_box.add_widget(Label(
            text="[b]PHUNGAN[/b]",
            markup=True,
            font_size=sp(18),
            halign="left",
            color=(1, 1, 1, 1)
        ))
        name_box.add_widget(Label(
            text="SMART CALCULATOR",
            font_size=sp(10),
            color=(0.55, 0.65, 0.82, 1),
            halign="left"
        ))
        header.add_widget(name_box)
        root.add_widget(header)

        panel = BoxLayout(
            orientation="vertical",
            padding=dp(16),
            spacing=dp(5),
            size_hint_y=0.30
        )
        with panel.canvas.before:
            Color(0.08, 0.11, 0.19, 1)
            panel_bg = RoundedRectangle(
                pos=panel.pos, size=panel.size, radius=[dp(22)]
            )
        panel.bind(
            pos=lambda obj, pos: setattr(panel_bg, "pos", pos),
            size=lambda obj, size: setattr(panel_bg, "size", size)
        )

        self.history = Label(
            text="",
            font_size=sp(15),
            color=(0.55, 0.65, 0.82, 1),
            halign="right",
            valign="middle",
            size_hint_y=0.35
        )
        self.history.bind(
            size=lambda obj, size: setattr(obj, "text_size", size)
        )
        panel.add_widget(self.history)

        self.display = Label(
            text="0",
            font_size=sp(36),
            color=(1, 1, 1, 1),
            halign="right",
            valign="middle",
            size_hint_y=0.65
        )
        self.display.bind(
            size=lambda obj, size: setattr(obj, "text_size", size)
        )
        panel.add_widget(self.display)
        root.add_widget(panel)

        grid = GridLayout(cols=4, spacing=dp(9), size_hint_y=0.70)
        rows = [
            ["AC", "⌫", "%", "÷"],
            ["7", "8", "9", "×"],
            ["4", "5", "6", "−"],
            ["1", "2", "3", "+"],
            ["±", "0", ".", "="]
        ]

        for row in rows:
            for key in row:
                btn = RoundedButton(text=key)
                if key in ["÷", "×", "−", "+"]:
                    btn.fill_color = (0.08, 0.35, 0.78, 1)
                elif key == "=":
                    btn.fill_color = (0.0, 0.62, 0.53, 1)
                elif key in ["AC", "⌫", "%", "±"]:
                    btn.fill_color = (0.14, 0.20, 0.32, 1)
                    btn.color = (0.43, 0.72, 1, 1)
                else:
                    btn.fill_color = (0.09, 0.13, 0.22, 1)
                btn.bind(on_press=self.press)
                grid.add_widget(btn)

        root.add_widget(grid)
        self.root_box.add_widget(root)

    def press(self, button):
        key = button.text

        if key == "AC":
            self.expression = ""
            self.history.text = ""
            self.just_calculated = False

        elif key == "⌫":
            self.expression = self.expression[:-1]
            self.just_calculated = False

        elif key == "±":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            elif self.expression:
                self.expression = "-" + self.expression
            self.just_calculated = False

        elif key == "%":
            try:
                value = self.safe_calculate(self.expression)
                self.expression = str(value / 100)
            except Exception:
                return
            self.just_calculated = False

        elif key == "=":
            try:
                result = self.safe_calculate(self.expression)
                self.history.text = self.expression + " ="
                self.expression = self.format_result(result)
                self.just_calculated = True
            except Exception:
                self.display.text = "Invalid calculation"
                self.expression = ""
                self.just_calculated = False
                return

        else:
            if self.just_calculated and key in "0123456789.":
                self.expression = ""
                self.history.text = ""
            mapping = {"×": "*", "÷": "/", "−": "-"}
            self.expression += mapping.get(key, key)
            self.just_calculated = False

        self.display.text = self.expression.replace("*", "×").replace("/", "÷").replace("-", "−") or "0"

    @staticmethod
    def safe_calculate(expr):
        allowed = set("0123456789.+-*/()% ")
        if not expr or any(c not in allowed for c in expr):
            raise ValueError("Invalid expression")
        # Restrict evaluation to arithmetic expressions with no builtins.
        result = eval(expr, {"__builtins__": {}}, {})
        if not isinstance(result, (int, float)) or abs(result) == float("inf"):
            raise ValueError("Invalid result")
        return result

    @staticmethod
    def format_result(value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(round(value, 10))


if __name__ == "__main__":
    PhunganCalculator().run()
