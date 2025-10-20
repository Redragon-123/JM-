from datetime import datetime
def view_tasks(tasks, only_pending=False):
    base = [t for t in tasks if (not only_pending) or (not t.get("done"))]
    def parse_time(t):
        try:
            return datetime.strptime(t.get("created_at", ""), "%Y-%m-%d %H:%M:%S")
        except Exception:
            return datetime.min

    while True:
        print(
            "\n===== View Tasks =====\n"
            "1) directly display\n"
            "2) from high to low priority\n"
            "3) from low to high priority\n"
            "4) display by tags groups\n"
            "5) output by tags\n"
            "6) by created time (old → new)\n"
            "7) by created time (new → old)\n"
            "0) return to main menu\n"
            "======================"
        )
        sub = input("please input your choice:").strip()
        if sub == "0":
            return
        elif sub == "1":
            display_tasks(base)
        elif sub == "2":
            arr = sorted(base, key=_priority_value)  # high→low
            display_tasks(arr)
        elif sub == "3":
            arr = sorted(base, key=_priority_value, reverse=True)  # low→high
            display_tasks(arr)
        elif sub == "4":
            display_group_by_tag(base)
        elif sub == "5":
            tag = input("please input tags:").strip()
            if not tag:
                print("tag cannot be empty.")
                continue
            arr = [t for t in base if tag in (t.get("tags") or [])]
            display_tasks(arr)
        elif sub == "6":
            arr = sorted(base, key=parse_time)  # old→new
            display_tasks(arr)
        elif sub == "7":
            arr = sorted(base, key=parse_time, reverse=True)  # new→old
            display_tasks(arr)
        else:
            print("invalid choice, please try again.")


def menu():
    action={"1":("add task",todo_data) 
            "2": ("view incompleted tasks", lambda ts: view_tasks(ts, only_pending=True)),
            "3": ("view all tasks",       lambda ts: view_tasks(ts, only_pending=False)),
            "4":("change tasks status",)
            "5":("edit task",)
            "6":("delete task",)
            "7":("clear complete",)
            "8":("search",)
            "9":("edit tags",)
            "0":("view all tags",)
            "10":("exit",None)}
    while True:
        print(  "====== To-Do List ======\n"
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
        choice=input("please input your demand: ")
        if choice == "10":
            print("Bye~")
            break
        action = action.get(choice)
        if not action:
            print("invaild choice, please try again.")
            continue
        func = action[1]
        func(tasks)
