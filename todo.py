import argparse
import json
import sys
import os
from typing import TypedDict

TODOS_FILE: str = "todos.json"


class Task(TypedDict):
    id: int
    title: str
    done: bool


def load_todos() -> list[Task]:
    if not os.path.exists(TODOS_FILE):
        return []
    try:
        with open(TODOS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"警告：{TODOS_FILE} 格式損壞，以空清單繼續。")
        return []
    except OSError as e:
        print(f"警告：無法讀取 {TODOS_FILE}（{e}），以空清單繼續。")
        return []


def save_todos(todos: list[Task]) -> None:
    try:
        with open(TODOS_FILE, "w", encoding="utf-8") as f:
            json.dump(todos, f, ensure_ascii=False, indent=2)
    except OSError as e:
        print(f"錯誤：無法儲存 {TODOS_FILE}（{e}）。")


def add_task(title: str) -> None:
    todos: list[Task] = load_todos()
    new_id: int = max((t["id"] for t in todos), default=0) + 1
    todos.append({"id": new_id, "title": title, "done": False})
    save_todos(todos)
    print(f"已新增任務 #{new_id}：{title}")


def list_tasks() -> None:
    todos: list[Task] = load_todos()
    if not todos:
        print("目前沒有任何任務。")
        return

    use_color: bool = sys.stdout.isatty()
    total: int = len(todos)
    done_count: int = sum(1 for t in todos if t["done"])

    print(f"\n  任務清單  （{done_count}/{total} 已完成）")
    print("  " + "─" * 36)
    for t in todos:
        if t["done"]:
            symbol: str = "✓"
            if use_color:
                line: str = f"  \033[32m{symbol}  {t['id']:>3}.  \033[9m{t['title']}\033[0m"
            else:
                line = f"  {symbol}  {t['id']:>3}.  {t['title']} [完成]"
        else:
            symbol = "○"
            if use_color:
                line = f"  \033[2m{symbol}\033[0m  {t['id']:>3}.  {t['title']}"
            else:
                line = f"  {symbol}  {t['id']:>3}.  {t['title']}"
        print(line)
    print()


def mark_done(task_id: int) -> None:
    todos: list[Task] = load_todos()
    for t in todos:
        if t["id"] == task_id:
            if t["done"]:
                print(f"任務 #{task_id} 已經是完成狀態。")
            else:
                t["done"] = True
                save_todos(todos)
                print(f"任務 #{task_id} 已標記為完成：{t['title']}")
            return
    print(f"找不到任務 #{task_id}。")


def delete_task(task_id: int) -> None:
    todos: list[Task] = load_todos()
    new_todos: list[Task] = [t for t in todos if t["id"] != task_id]
    if len(new_todos) == len(todos):
        print(f"找不到任務 #{task_id}。")
        return
    save_todos(new_todos)
    print(f"已刪除任務 #{task_id}。")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="todo.py",
        description="命令列待辦事項工具",
    )
    subparsers = parser.add_subparsers(dest="command", metavar="指令")
    subparsers.required = True

    sp_add = subparsers.add_parser("add", help="新增任務")
    sp_add.add_argument("title", nargs="+", help="任務內容")

    subparsers.add_parser("list", help="列出所有任務")

    sp_done = subparsers.add_parser("done", help="標記任務為完成")
    sp_done.add_argument("id", type=int, metavar="ID", help="任務編號")

    sp_delete = subparsers.add_parser("delete", help="刪除任務")
    sp_delete.add_argument("id", type=int, metavar="ID", help="任務編號")

    args = parser.parse_args()

    if args.command == "add":
        add_task(" ".join(args.title))
    elif args.command == "list":
        list_tasks()
    elif args.command == "done":
        mark_done(args.id)
    elif args.command == "delete":
        delete_task(args.id)
