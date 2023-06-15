"""Simple function."""
from reactpy import component, html


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
def app():
    """Create the app."""
    return html.div(
        html.h1("Photo Gallery"),
        photo("Landscape", image_id=830),
        photo("City", image_id=274),
        photo("Puppy", image_id=237),
        todo_list(),
    )
