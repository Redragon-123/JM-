'''
The task is to create a to-do list application

Specification:
You should design an appropriate data structure for the to-do list.
You should use functions where appropriate.
You should create an appropriate programming structure to "drive" the application.

Good programming practice:
Functions should have one purpose (single responsibility principle).
Meaningful names for variables and functions.
Document your functions.
'''
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
To-Do List with JSON persistence
'''
from datetime import datetime
from typing import List, Dict, Any
import json, os, tempfile, shutil

DATA_FILE = r"D:\unverisity of Leeds\programming\week_05_classwork\week_05\session_2\tasks\to_do_list_data.json"

PRIORITY_SCORE = {"AAA": 5, "AA": 4, "A": 3, "B": 2, "C": 1}

def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _normalize_date(s: str) -> str:
    s = s.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            d = datetime.strptime(s, fmt)
            return d.strftime("%Y-%m-%d")
        except ValueError:
            pass
    raise ValueError("invaild date, please try YYYY-MM-DD or DD/MM/YYYY")

def _priority_value(p: str) -> int:
    return PRIORITY_SCORE.get(p.upper(), 0)

def _display_task(t: Dict[str, Any]) -> str:
    return (f"[#{t['id']:04d}] "
            f"[{t['category']}] "
            f"Pri:{t['priority']} "
            f"Due:{t['deadline']} "
            f"{'(DONE)' if t['done'] else ''}\n"
            f"    {t['description']}"
            f"{'  Tags:'+','.join(t['tags']) if t.get('tags') else ''}")

def _save_data_atomic(data: Dict[str, Any], path: str) -> None:
    dir_ = os.path.dirname(os.path.abspath(path)) or "."
    os.makedirs(dir_, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(prefix=".todo_tmp_", dir=dir_)
    os.close(fd)
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        shutil.move(tmp_path, path)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def _load_data(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"tasks": [], "next_id": 1}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("data root is not dict")
        data.setdefault("tasks", [])
        data.setdefault("next_id", 1)
        for t in data["tasks"]:
            t.setdefault("category", "work")
            t.setdefault("priority", "C")
            t.setdefault("deadline", "2099-12-31")
            t.setdefault("description", "")
            t.setdefault("created_at", _now_str())
            t.setdefault("done", False)
            t.setdefault("tags", [])
        return data
    except Exception:
        bak = path + ".corrupt.bak"
        try:
            shutil.copy2(path, bak)
            print(f"! warning: JSON damaged, a backup is saved at {bak}. Reinitializing...")
        except Exception:
            print("! warning: JSON damaged and backup failed. Reinitializing...")
        return {"tasks": [], "next_id": 1}

def _autosave(func):
    def wrapper(data: Dict[str, Any], *args, **kwargs):
        result = func(data, *args, **kwargs)
        try:
            _save_data_atomic(data, DATA_FILE)
        except Exception as e:
            print(f"! autosave failed: {e}")
        return result
    return wrapper

todo_data: Dict[str, Any] = _load_data(DATA_FILE)

def add_task(data: Dict[str, Any]) -> None:
    print("\n--- Add Task ---")
    category = input("category (work/personal/shopping): ").strip().lower()
    if category not in {"work", "personal", "shopping"}:
        print("✗ invalid category.")
        return

    priority = input("priority (AAA/AA/A/B/C): ").strip().upper()
    if priority not in PRIORITY_SCORE:
        print("✗ invalid priority.")
        return

    try:
        deadline = _normalize_date(input("deadline (YYYY-MM-DD or DD/MM/YYYY): "))
    except ValueError as e:
        print("✗", e)
        return

    description = input("description: ").strip()
    tags = [t.strip() for t in input("tags (comma, space is allowed): ").split(",") if t.strip()]

    t = {
        "id": data["next_id"],
        "category": category,
        "priority": priority,
        "deadline": deadline,
        "description": description,
        "created_at": _now_str(),
        "done": False,
        "tags": tags,
    }
    data["tasks"].append(t)
    data["next_id"] += 1
    print("✓ added:\n" + _display_task(t))

# add @ _autosave to changable functions
add_task = _autosave(add_task)

def edit_task(data: Dict[str, Any]) -> None:
    print("\n--- Edit Task ---")
    try:
        tid = int(input("task id: ").strip())
    except ValueError:
        print("✗ invalid id")
        return

    t = next((x for x in data["tasks"] if x["id"] == tid), None)
    if not t:
        print("✗ task not found")
        return

    print("current: \n" + _display_task(t))
    new_desc = input("new description (press enter to skip): ").strip()
    new_pri  = input("new priority (AAA/AA/A/B/C, enter to skip): ").strip().upper()
    new_cat  = input("new category (work/personal/shopping, enter to skip): ").strip().lower()
    new_due  = input("new deadline (YYYY-MM-DD/ DD/MM/YYYY, enter to skip): ").strip()
    new_tags = input("new tags (comma seperate, enter skip): ").strip()

    if new_desc:
        t["description"] = new_desc
    if new_pri:
        if new_pri in PRIORITY_SCORE:
            t["priority"] = new_pri
        else:
            print("! priority not update: invaild input")
    if new_cat:
        if new_cat in {"work", "personal", "shopping"}:
            t["category"] = new_cat
        else:
            print("! category not update: invaild input")
    if new_due:
        try:
            t["deadline"] = _normalize_date(new_due)
        except ValueError as e:
            print("! deadline not update: ", e)
    if new_tags:
        t["tags"] = [x.strip() for x in new_tags.split(",") if x.strip()]

    print("✓ updated:\n" + _display_task(t))

edit_task = _autosave(edit_task)

def delete_task(data: Dict[str, Any]) -> None:
    print("\n--- Delete Task ---")
    try:
        tid = int(input("task id: ").strip())
    except ValueError:
        print("✗ invalid id")
        return

    for i, t in enumerate(data["tasks"]):
        if t["id"] == tid:
            removed = data["tasks"].pop(i)
            print("✓ removed:\n" + _display_task(removed))
            return
    print("✗ task not found")

delete_task = _autosave(delete_task)

def change_status(data: Dict[str, Any]) -> None:
    print("\n--- Change Status ---")
    try:
        tid = int(input("task id: ").strip())
    except ValueError:
        print("✗ invalid id")
        return

    t = next((x for x in data["tasks"] if x["id"] == tid), None)
    if not t:
        print("✗ task not found")
        return
    t["done"] = not t["done"]
    print("✓ status toggled:\n" + _display_task(t))

change_status = _autosave(change_status)

def clear_completed(data: Dict[str, Any]) -> None:
    before = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if not t["done"]]
    print(f"✓ cleared {before - len(data['tasks'])} completed task(s)")

clear_completed = _autosave(clear_completed)

def display_tasks(tasks: List[Dict[str, Any]]) -> None:
    if not tasks:
        print("(no tasks)")
        return
    for t in tasks:
        print(_display_task(t))

def sort_all_tasks(data: Dict[str, Any], by="priority", descending=False) -> List[Dict[str, Any]]:
    arr = list(data["tasks"])
    if by == "priority":
        arr.sort(key=lambda x: _priority_value(x["priority"]), reverse=descending)
    elif by == "deadline":
        arr.sort(key=lambda x: x["deadline"], reverse=descending)
    elif by == "created_at":
        arr.sort(
            key=lambda x: datetime.strptime(x["created_at"], "%Y-%m-%d %H:%M:%S"),
            reverse=descending
        )
    else:
        print("! unsupported sort key")
    return arr

def search_tasks(data: Dict[str, Any], keyword: str, case_sensitive=False) -> List[Dict[str, Any]]:
    if not case_sensitive:
        keyword = keyword.lower()
    results = []
    for t in data["tasks"]:
        blob = f"{t['id']} {t['category']} {t['priority']} {t['deadline']} {t['description']} {' '.join(t['tags'])}"
        if not case_sensitive:
            blob = blob.lower()
        if keyword in blob:
            results.append(t)
    return results

def edit_tags(data: Dict[str, Any]) -> None:
    print("\n--- Edit Tags ---")
    try:
        tid = int(input("task id: ").strip())
    except ValueError:
        print("✗ invalid id")
        return
    t = next((x for x in data["tasks"] if x["id"] == tid), None)
    if not t:
        print("✗ task not found")
        return
    print("current tags:", t.get("tags", []))
    new_tags = [x.strip() for x in input("new tags (comma): ").split(",") if x.strip()]
    t["tags"] = new_tags
    print("✓ tags updated:", t["tags"])

edit_tags = _autosave(edit_tags)

def view_all_tags(data: Dict[str, Any]) -> None:
    tag_count: Dict[str, int] = {}
    for t in data["tasks"]:
        for tg in t.get("tags", []):
            tag_count[tg] = tag_count.get(tg, 0) + 1
    if not tag_count:
        print("(no tags)")
        return
    print("--- All Tags ---")
    for k, v in sorted(tag_count.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{k}: {v}")

def view_tasks_menu(data: Dict[str, Any], only_pending=False) -> None:
    while True:
        base = [t for t in data["tasks"] if (not only_pending) or (not t["done"])]
        print(
            "\n===== View Tasks =====\n"
            "1) direct display\n"
            "2) priority high to low\n"
            "3) priority low to high\n"
            "4) deadline soon to late\n"
            "5) deadline late to soon\n"
            "6) time of creating previous to latest\n"
            "7) time of creating latest to previous\n"
            "8) category\n"
            "0) back to main menu\n"
            "======================"
        )
        sub = input("choice: ").strip()
        if sub == "0":
            return
        elif sub == "1":
            display_tasks(base)
        elif sub == "2":
            display_tasks(sorted(base, key=lambda x: _priority_value(x["priority"]), reverse=True))
        elif sub == "3":
            display_tasks(sorted(base, key=lambda x: _priority_value(x["priority"])))
        elif sub == "4":
            display_tasks(sorted(base, key=lambda x: x["deadline"]))
        elif sub == "5":
            display_tasks(sorted(base, key=lambda x: x["deadline"], reverse=True))
        elif sub == "6":
            display_tasks(sorted(base, key=lambda x: x["created_at"]))
        elif sub == "7":
            display_tasks(sorted(base, key=lambda x: x["created_at"], reverse=True))
        elif sub == "8":
            cat = input("category (work/personal/shopping): ").strip().lower()
            display_tasks([t for t in base if t["category"] == cat])
        else:
            print("invalid choice")

def menu():
    actions = {
        "1": ("add task",             lambda: add_task(todo_data)),
        "2": ("view incompleted",     lambda: view_tasks_menu(todo_data, only_pending=True)),
        "3": ("view all",             lambda: view_tasks_menu(todo_data, only_pending=False)),
        "4": ("change status",        lambda: change_status(todo_data)),
        "5": ("edit task",            lambda: edit_task(todo_data)),
        "6": ("delete task",          lambda: delete_task(todo_data)),
        "7": ("clear completed",      lambda: clear_completed(todo_data)),
        "8": ("search",               lambda: _menu_search()),
        "9": ("edit tags",            lambda: edit_tags(todo_data)),
        "0": ("view all tags",        lambda: view_all_tags(todo_data)),
        "10":("exit",                 None),
    }

    while True:
        print(
            "\n====== To-Do List ======\n"
            "1) add task\n"
            "2) view incompleted tasks\n"
            "3) view all tasks\n"
            "4) change tasks status\n"
            "5) edit task\n"
            "6) delete task\n"
            "7) clear complete\n"
            "8) search\n"
            "9) edit tags\n"
            "0) view all tags\n"
            "10) exit\n"
            "========================"
        )
        choice = input("please input your demand: ").strip()
        act = actions.get(choice)
        if not act:
            print("invaild choice, please try again.")
            continue
        if choice == "10":
            # save again on exit 
            try:
                _save_data_atomic(todo_data, DATA_FILE)
            except Exception as e:
                print(f"! save on exit failed: {e}")
            print("Bye~")
            break
        act[1]()

def _menu_search():
    kw = input("keyword: ").strip()
    if not kw:
        print("✗ empty keyword")
        return
    res = search_tasks(todo_data, kw, case_sensitive=False)
    print(f"--- search results ({len(res)}) ---")
    display_tasks(res)

if __name__ == "__main__":
    menu()
