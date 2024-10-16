import flet as ft
from flet_timer.flet_timer import Timer


def main(page: ft.Page):
    page.title = "Countdown Timer App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Reference to store the selected time in seconds
    selected_time_ref = ft.Ref[int]()

    # Function to handle changes in the timer picker
    def handle_timer_picker_change(e):
        selected_time_ref.current = int(e.data)

    # Function to start the countdown
    def start_countdown(e):
        if selected_time_ref.current is not None:
            duration = selected_time_ref.current
            mins, secs = divmod(duration, 60)
            txt_time.value = f"{mins:02}:{secs:02}"
            page.update()
            countdown_timer.start()
            page.go("/timer")
        else:
            print("Please select a time duration.")

    # Function to update the countdown display
    def refresh():
        if selected_time_ref.current > 0:
            selected_time_ref.current -= 1
            mins, secs = divmod(selected_time_ref.current, 60)
            txt_time.value = f"{mins:02}:{secs:02}"
        else:
            countdown_timer.stop()
        page.update()

    # Function to reset the countdown timer
    def reset_timer(e):
        countdown_timer.stop()
        selected_time_ref.current = None
        txt_time.value = "00:00:00"
        page.go("/")

    # Function to add a new timer (navigate back to picker)
    def add_timer(e):
        countdown_timer.stop()
        page.go("/")

    # Create a text component for displaying the countdown time
    txt_time = ft.Text(value="00:00:00", style=ft.TextStyle(size=40))

    # Create a CupertinoTimerPicker for selecting the countdown duration
    cupertino_timer_picker = ft.CupertinoTimerPicker(
        value=0,
        second_interval=10,
        minute_interval=1,
        mode=ft.CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS,
        on_change=handle_timer_picker_change,
    )

    # Create a timer object for updating the countdown every second
    countdown_timer = Timer(name="countdown_timer",
                            interval_s=1,
                            callback=refresh)

    # Create a "START" button to initiate the countdown
    start_button = ft.ElevatedButton(text="START", on_click=start_countdown)

    # Define the main page with the time picker and start button
    def main_page():
        return [
            cupertino_timer_picker,
            ft.Row([start_button], alignment=ft.MainAxisAlignment.CENTER)
        ]

    # Define the timer display page with reset and add buttons
    def timer_page():
        reset_button = ft.ElevatedButton(text="RESET", on_click=reset_timer)
        add_button = ft.ElevatedButton(text="ADD", on_click=add_timer)
        return [txt_time, ft.Row([reset_button, add_button])]

    # Handle page routes
    def route_change(route):
        print(page.route)
        if page.route == "/timer":
            page.views.clear()
            page.views.append(ft.View(route="/timer", controls=timer_page()))
        else:
            page.views.clear()
            page.views.append(ft.View(route="/", controls=main_page()))
        page.update()

    # Set up initial route and route change handler
    page.on_route_change = route_change
    route_change(page.route)


ft.app(main)
