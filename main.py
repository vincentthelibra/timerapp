import flet as ft
import time

PRIMARY_COLOR = "#3498db"  # A nice blue color
SECONDARY_COLOR = "#2980b9"  # A darker blue for gradient
TEXT_COLOR = "#ecf0f1"  # Light gray for text
BUTTON_COLOR = "#2ecc71"  # Green for buttons


def main(page: ft.Page):
    page.title = "A Beautiful Timer App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Set the background to a gradient
    page.bgcolor = ft.colors.TRANSPARENT
    page.window_bgcolor = ft.colors.TRANSPARENT

    # Create a container with gradient background
    main_container = ft.Container(gradient=ft.LinearGradient(
        begin=ft.alignment.top_center,
        end=ft.alignment.bottom_center,
        colors=[PRIMARY_COLOR, SECONDARY_COLOR]),
                                  expand=True)

    # Set the theme
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(primary=PRIMARY_COLOR,
                                    on_primary=TEXT_COLOR,
                                    secondary=SECONDARY_COLOR,
                                    on_secondary=TEXT_COLOR))

    selected_time_ref = ft.Ref[int]()
    txt_time = ft.Text(value="00:00:00", style=ft.TextStyle(size=40))
    is_running = ft.Ref[bool]()

    def handle_timer_picker_change(e):
        selected_time_ref.current = int(e.data)

    def refresh():
        if is_running.current and selected_time_ref.current is not None and selected_time_ref.current > 0:
            selected_time_ref.current -= 1
            mins, secs = divmod(selected_time_ref.current, 60)
            hours, mins = divmod(mins, 60)
            txt_time.value = f"{hours:02d}:{mins:02d}:{secs:02d}"
            page.update()
            page.add(
                ft.Text(f"Debug: Time left - {selected_time_ref.current}"))
        elif selected_time_ref.current is not None and selected_time_ref.current <= 0:
            is_running.current = False
            txt_time.value = "Time's Up!"
            page.update()

    def start_countdown(e):
        if selected_time_ref.current is not None:
            duration = selected_time_ref.current
            hours, remainder = divmod(duration, 3600)
            mins, secs = divmod(remainder, 60)
            txt_time.value = f"{hours:02d}:{mins:02d}:{secs:02d}"
            page.update()
            page.go("/timer")
        else:
            print("Please select a time duration.")

    def reset_timer(e):
        is_running.current = False
        selected_time_ref.current = None
        txt_time.value = "00:00:00"
        page.go("/")

    def add_timer(e):
        is_running.current = False
        page.go("/")

    cupertino_timer_picker = ft.CupertinoTimerPicker(
        value=0,
        second_interval=1,
        minute_interval=1,
        mode=ft.CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS,
        on_change=handle_timer_picker_change,
    )

    start_button = ft.ElevatedButton(text="START", on_click=start_countdown)

    def main_page():
        return [
            ft.Column([
                cupertino_timer_picker,
                ft.Row([start_button], alignment=ft.MainAxisAlignment.CENTER)
            ],
                      alignment=ft.MainAxisAlignment.CENTER,
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                      expand=True)
        ]

    def timer_page():
        reset_button = ft.ElevatedButton(text="RESET", on_click=reset_timer)
        add_button = ft.ElevatedButton(text="ADD", on_click=add_timer)
        return [
            ft.Column([
                txt_time,
                ft.Row([reset_button, add_button],
                       alignment=ft.MainAxisAlignment.CENTER)
            ],
                      alignment=ft.MainAxisAlignment.CENTER,
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        ]

    def route_change(route):
        page.views.clear()
        if page.route == "/timer":
            page.views.append(ft.View(route="/timer", controls=timer_page()))
            is_running.current = True
            page.update()
            while is_running.current:
                refresh()
                time.sleep(1)
        else:
            page.views.append(ft.View(route="/", controls=main_page()))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)


ft.app(target=main)
