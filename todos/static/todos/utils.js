function showOrHideEmptyMessage() {
    // use the id and class name you just set up
    const itemClass = "todo_item" 
    const emptyListId = "todo_items_empty"

    const itemCount = Array.from(document.getElementsByClassName(itemClass)).length;

    if (itemCount === 0) {
        document.getElementById(emptyListId).style.display = "block";
    } else {
        document.getElementById(emptyListId).style.display = "none";
    }
}


window.onload = function () {
    // note the ID here. It is the target from our form's htmx post
    const targetNode = document.getElementById("todo_items");

    const config = {
        childList: true,
    };

    const observer = new MutationObserver(showOrHideEmptyMessage);

    observer.observe(targetNode, config);
    showOrHideEmptyMessage();
};
