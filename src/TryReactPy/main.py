"""Simple function."""
import asyncio
import json
from pathlib import Path

from reactpy import component, event, html, use_state
from reactpy.core import hooks

HERE = Path(__file__)
DATA_PATH = HERE.parent / "data" / "data.json"
sculpture_data = json.loads(DATA_PATH.read_text())


@component
def chat():
    """Chat.

    State is a snapshot: Changing the recipient after clicking "Send"
    does not change the recipient of the message because the state is
    'snapshot' when the event is triggered.
    """
    recipient, set_recipient = use_state("Alice")
    message, set_message = use_state("")

    @event(prevent_default=True)
    async def handle_submit(_event):
        set_message("")
        print("About to send message...")
        await asyncio.sleep(5)
        print(f"Sent '{message}' to {recipient}")

    return html.form(
        {"on_submit": handle_submit, "style": {"display": "inline-grid"}},
        html.label(
            {},
            "To: ",
            html.select(
                {
                    "value": recipient,
                    "on_change": lambda event: set_recipient(
                        event["target"]["value"],
                    ),
                },
                html.option({"value": "Alice"}, "Alice"),
                html.option({"value": "Bob"}, "Bob"),
            ),
        ),
        html.input(
            {
                "type": "text",
                "placeholder": "Your message...",
                "value": message,
                "on_change": lambda event: set_message(
                    event["target"]["value"],
                ),
            },
        ),
        html.button({"type": "submit"}, "Send"),
    )


@component
def gallery():
    """Manage state."""
    index, set_index = use_state(0)

    def handle_click(_event):
        set_index(index + 1)

    bounded_index = index % len(sculpture_data)
    sculpture = sculpture_data[bounded_index]
    alt = sculpture["alt"]
    artist = sculpture["artist"]
    description = sculpture["description"]
    name = sculpture["name"]
    url = sculpture["url"]

    return html.div(
        html.button({"on_click": handle_click}, "Next"),
        html.h2(name, " by ", artist),
        html.p(f"({bounded_index + 1} of {len(sculpture_data)})"),
        html.img({"src": url, "alt": alt, "style": {"height": "200px"}}),
        html.p(description),
    )


@component
def photo(alt_text, image_id):
    """Photo."""
    return html.img(
        {
            "src": f"https://picsum.photos/id/{image_id}/500/200",
            "style": {"width": "50%"},
            "alt": alt_text,
        },
    )


@component
def todo_item(attrs, name, done):
    """Item to be done."""
    return html.li(attrs, name, " ✔" if done else "")


@component
def data_list(items, filter_by_priority=None, sort_by_priority=False):
    """Manage items to be done."""
    if filter_by_priority is not None:
        items = [i for i in items if i["priority"] <= filter_by_priority]
    if sort_by_priority:
        items = sorted(items, key=lambda i: i["priority"])
    list_item_elements = [
        todo_item(
            {
                "key": i["id"],
            },
            i["text"],
            i["done"],
        )
        for i in items
    ]
    return html.ul(list_item_elements)


@component
def todo_list():
    """Items to be done."""
    tasks = [
        {"id": 0, "text": "Make breakfast", "priority": 0, "done": True},
        {"id": 1, "text": "Feed the dog", "priority": 0, "done": False},
        {"id": 2, "text": "Do laundry", "priority": 2, "done": True},
        {"id": 3, "text": "Go on a run", "priority": 1, "done": False},
        {"id": 4, "text": "Clean the house", "priority": 2, "done": True},
        {
            "id": 5, "text": "Go to the grocery store", "priority": 2,
            "done": True,
        },
        {"id": 6, "text": "Do some coding", "priority": 1, "done": True},
        {"id": 7, "text": "Read a book", "priority": 1, "done": True},
    ]
    return html.section(
        html.h1("My Todo List"),
        data_list(tasks, filter_by_priority=1, sort_by_priority=True),
    )


@component
def print_button(display_text, message_text):
    """Manage simple event."""
    def handle_event(_event):
        print(message_text)

    return html.button({"on_click": handle_event}, display_text)


@component
def color_button():
    """Multiple state updates.

    State is updated 3 times but only the last one is applied.
    """
    color, set_color = use_state("gray")

    def handle_click(_event):
        set_color("orange")
        set_color("pink")
        set_color("blue")

    def handle_reset(_event):
        set_color("gray")

    return html.div(
        html.button(
            {"on_click": handle_click, "style": {"background_color": color}},
            "Set Color",
        ),
        html.button(
            {
                "on_click": handle_reset, "style": {
                    "background_color": color,
                },
            }, "Reset",
        ),
    )


@component
def counter():
    """Batched state updates.

    State is updated 3 times, and they are all applied because we are
    updating using an updater function.
    """
    number, set_number = use_state(0)

    def increment(old_number):
        new_number = old_number + 1
        return new_number

    def handle_click(_event):
        set_number(increment)
        set_number(increment)
        set_number(increment)

    return html.div(
        html.h1(number),
        html.button({"on_click": handle_click}, "Increment"),
    )


@component
def mutability():
    """Dangers of Mutability.

    With mutable objects, changing it does not trigger a re-render
    """
    person, set_person = use_state(
        {
            "first_name": "Barbara",
            "last_name": "Hepworth",
            "email": "bhepworth@sculpture.com",
        },
    )

    def handle_first_name_change(_event):
        set_person({**person, "first_name": _event["target"]["value"]})

    def handle_last_name_change(_event):
        set_person({**person, "last_name": _event["target"]["value"]})

    def handle_email_change(_event):
        set_person({**person, "email": _event["target"]["value"]})

    return html.div(
        html.label(
            "First name: ",
            html.input(
                {
                    "value": person["first_name"],
                    "on_change": handle_first_name_change,
                },
            ),
        ),
        html.label(
            "Last name: ",
            html.input(
                {
                    "value": person["last_name"],
                    "on_change": handle_last_name_change,
                },
            ),
        ),
        html.label(
            "Email: ",
            html.input({
                "value": person["email"],
                "on_change": handle_email_change,
            }),
        ),
        html.p(
            f"{person['first_name']} {person['last_name']} {person['email']}",
        ),
    )


@component
def button_with_delay(message, delay):
    """Async event management."""
    async def handle_event(_event):
        await asyncio.sleep(delay)
        print(message)

    return html.button(
        {
            "on_click": handle_event,
            "title": f"Check the log in {delay} seconds",
        }, message,
    )


@component
def play_dinosaur_sound():
    """When state is not serializable."""
    _event, set_event = hooks.use_state(None)
    return html.div(
        html.audio(
            {
                "controls": True,
                "on_time_update": set_event,
                "src": "https://interactive-examples.mdn.mozilla.net/"
                       "media/cc0-audio/t-rex-roar.mp3",
            },
        ),
        html.pre(json.dumps(_event, indent=2)),
    )


@component
def div_in_div():
    """Stop propagation of events."""
    stop_propagation, set_stop_propagation = hooks.use_state(True)
    inner_count, set_inner_count = hooks.use_state(0)
    outer_count, set_outer_count = hooks.use_state(0)

    inner_div = html.div({
        "on_click": event(
            lambda _event: set_inner_count(inner_count + 1),
            stop_propagation=stop_propagation, ),
        "style": {
            "height": "50px", "width": "50px",
            "background_color": "blue", }, })
    outer_div = html.div(
        {
            "on_click": lambda _event: set_outer_count(outer_count + 1),
            "style": {
                "height": "100px", "width": "100px", "background_color": "red",
            },
        },
        inner_div,
    )

    return html.div(
        html.button(
            {
                "on_click": lambda _event: set_stop_propagation(
                    not stop_propagation,
                ),
            },
            "Toggle Propagation",
        ),
        html.pre(f"Will propagate: {not stop_propagation}"),
        html.pre(f"Inner click count: {inner_count}"),
        html.pre(f"Outer click count: {outer_count}"),
        outer_div,
    )


@component
def app():
    """Create the app."""
    return html.div(
        "Hello ReactPy!",
        html.h1("Photo Gallery"),
        photo("Landscape", image_id=830),
        photo("City", image_id=274),
        photo("Puppy", image_id=237),
        print_button("Play", "Playing"),
        todo_list(),
        gallery(),
        chat(),
        color_button(),
        counter(),
        mutability(),
        button_with_delay("Hi", 2),
        play_dinosaur_sound(),
        div_in_div(),
    )
