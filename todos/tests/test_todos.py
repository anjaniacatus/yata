import pytest

from django.urls import reverse
from playwright.sync_api import Page, expect
from todos.models import TodoItem

def reverse_url(
    live_server, viewname, urlconf=None, args=None, kwargs=None, current_app=None
):
    end = reverse(viewname, urlconf, args, kwargs, current_app)
    return f"{live_server.url}{end}"


def test_display_empty_list_on_first_load(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)
    page.wait_for_selector("text=Nothing to see here")

def test_create_todo_item_gets_rid_of_nothing_to_see(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)
    page.get_by_label("Title").click()
    page.get_by_label("Title").fill("foo")
    page.get_by_role("button", name="Add").click()
    expect(page.get_by_text("Nothing to see here...")).to_be_hidden()


def test_create_todo_item_shows_new_item(live_server, page: Page):
    url = reverse_url(live_server, "index")

    page.goto(url)
    page.get_by_label("Title").click()
    page.get_by_label("Title").fill("foo")
    page.get_by_role("button", name="Add").click()
    page.wait_for_selector("text=foo")


def test_display_one_item_on_first_load(live_server, page: Page):
    TodoItem.objects.create(title="read Nicolas Machiavel book : The Prince")
    page.goto(reverse_url(live_server, "index"))
    page.wait_for_selector("text=read Nicolas Machiavel book : The Prince")
    expect(page.get_by_text("Nothing to see here...")).to_be_hidden()


def test_checkbox(live_server, page: Page):
    items = [TodoItem.objects.create(title=f"Test item {i}") for i in range(3)]
    page.goto(reverse_url(live_server, "index"))

    middle_item = items[1]
    middle_id = f"toggle_item_{middle_item.id}"
    page.get_by_test_id(middle_id).check()
    expect(page.get_by_test_id(middle_id)).to_be_checked()

    middle_item.refresh_from_db()
    assert middle_item.completed is True

    items[0].refresh_from_db()
    assert items[0].completed is False

    items[2].refresh_from_db()
    assert items[2].completed is False


def test_checkbox_loads_correctly(live_server, page: Page):
    item = TodoItem.objects.create(title="Test item", completed=True)
    page.goto(reverse_url(live_server, "index"))
    checkbox_id = f"toggle_item_{item.id}"
    expect(page.get_by_test_id(checkbox_id)).to_be_checked()

def test_delete_item(live_server, page: Page):
    item = TodoItem.objects.create(title="Awesome task", completed=True)
    print(item.id)
    page.goto(reverse_url(live_server, "index"))

    delete_id = f"delete_item_{item.id}"
    page.get_by_test_id(delete_id).click()
    expect(page.get_by_test_id("todo_items")).not_to_contain_text("Awesome task")

    with pytest.raises(TodoItem.DoesNotExist):
        TodoItem.objects.get(id=item.id)
