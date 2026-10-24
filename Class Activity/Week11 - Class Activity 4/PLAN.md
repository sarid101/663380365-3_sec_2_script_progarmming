# Project Plan: Enhanced Task Manager CLI

**ผู้จัดทำ:** สาริษฐ์ บุตรช่วง (663380365-3) — CP352301 Script Programming 1/2569, Week 11

## 1. บทนำ

Task Manager จาก Week 7–8 ทำงานได้ แต่โค้ดรับ input, logic และการอ่าน/เขียนไฟล์ปนกันอยู่ใน `main.py` และ `TaskManager` ทำให้เพิ่มฟีเจอร์ยากและหาบั๊กยาก เอกสารนี้วางแผนเวอร์ชันใหม่ที่ **แยกหน้าที่ของแต่ละส่วนให้ชัด** ก่อนลงมือเขียน และเพิ่มฟีเจอร์ **tags, search, filter, sort**

## 2. Requirements

### 2.1 Functional Requirements (ระบบต้องทำอะไรได้)

| # | Requirement | สถานะ Week 11 |
|---|---|---|
| F1 | เพิ่มงาน 3 ประเภท: ทั่วไป (`Task`), มีวันกำหนดส่ง (`DueDateTask`, `YYYY-MM-DD`), มีลำดับความสำคัญ (`PriorityTask`, High/Medium/Low) | ✅ |
| F2 | ใส่ tag ได้หลายอันต่องาน (ไม่บังคับ) | ✅ |
| F3 | แสดงงานทั้งหมดพร้อมรายละเอียดตามประเภทและ tags | ✅ |
| F4 | ทำเครื่องหมายว่าเสร็จ / ลบงาน ตาม ID | ✅ |
| F5 | **Search:** ค้นหาคำใน description หรือ tags (ไม่สนตัวพิมพ์เล็ก/ใหญ่) | ✅ |
| F6 | **Filter:** กรองตามสถานะ, วันกำหนดส่ง (ก่อนวันที่กำหนด), priority, tag — ใช้หลายเงื่อนไขพร้อมกันได้ | ✅ |
| F7 | **Sort:** เรียงตาม ID, วันกำหนดส่ง, priority | ✅ |
| F8 | บันทึกลง `data/tasks.json` ทุกครั้งที่ข้อมูลเปลี่ยน และโหลดกลับเป็น class ที่ถูกต้อง | ✅ |

### 2.2 Non-Functional Requirements (ระบบต้องทำได้ดีแค่ไหน)

- **Usability:** เมนูชัดเจน บอกรูปแบบ input ที่ต้องการ และบอกวิธีแก้เมื่อใส่ผิด
- **Reliability:** input ผิด (วันที่, priority, ID ไม่ใช่ตัวเลข) และไฟล์ JSON เสีย ต้องไม่ทำให้โปรแกรม crash
- **Maintainability:** แต่ละโมดูลมีหน้าที่เดียว มี docstring
- **Extensibility:** เพิ่มประเภทงานใหม่หรือเปลี่ยนที่เก็บข้อมูล (เช่น SQLite) ได้โดยแก้แค่โมดูลเดียว
- **Performance:** งานหลักร้อยรายการต้องตอบสนองทันที (ใช้ list ใน memory ก็เพียงพอ)

## 3. High-Level Architecture

```
            ┌────────────┐
            │  main.py   │  orchestrator: สร้าง object แล้วเริ่มโปรแกรม
            └─────┬──────┘
                  ▼
        ┌──────────────────┐
        │ cli_interface.py │  UI layer: เมนู, input(), print(), ตรวจรูปแบบ input
        └────────┬─────────┘
                 │ เรียก method
                 ▼
        ┌──────────────────┐
        │ task_manager.py  │  business logic: add / complete / delete / search / filter / sort
        └───┬──────────┬───┘
            │          │ load / save
            ▼          ▼
     ┌──────────┐  ┌─────────────────────┐
     │ task.py  │  │ data_persistence.py │  data layer: JSON ↔ Task objects
     └──────────┘  └──────────┬──────────┘
      models                  ▼
                       data/tasks.json
```

### 3.1 หน้าที่ของแต่ละโมดูล (Separation of Concerns)

| โมดูล | ทำ | ไม่ทำ |
|---|---|---|
| `task.py` | เก็บข้อมูลงาน, `mark_complete`, `add_tag` / `remove_tag`, `to_dict`, `__str__` | ไม่รู้จักไฟล์หรือเมนู |
| `data_persistence.py` | อ่าน/เขียน JSON, แปลง dict ↔ object ตาม `_type` | ไม่มี logic ค้นหา/กรอง |
| `task_manager.py` | จัดการ list ของงาน, `next_id`, search / filter / sort | ไม่เรียก `input()` และไม่เปิดไฟล์เอง |
| `cli_interface.py` | แสดงเมนู, รับและตรวจ input, แสดงผล | ไม่มี logic ของงาน |
| `main.py` | สร้าง `TaskManager` + `CLIInterface` แล้ว `run()` | — |

ผลที่ได้: ถ้าเปลี่ยนจาก JSON เป็น SQLite แก้แค่ `data_persistence.py` / ถ้าเปลี่ยนจาก CLI เป็น GUI แก้แค่ `cli_interface.py`

## 4. Data Model

### 4.1 Class Diagram

```
Task
├─ id: int
├─ description: str
├─ completed: bool
├─ tags: list[str]          ← ใหม่ใน Week 11
├─ mark_complete()
├─ add_tag(tag) / remove_tag(tag)
├─ to_dict() -> dict
└─ details() -> str          ← subclass override เพื่อเพิ่มข้อมูลใน __str__
   ▲                    ▲
   │                    │
DueDateTask          PriorityTask
└─ due_date: date    └─ priority: "High" | "Medium" | "Low"
```

### 4.2 รูปแบบใน `tasks.json`

```json
{
    "id": 2,
    "description": "Submit enhanced Task Manager design",
    "completed": false,
    "tags": ["assignment", "university"],
    "due_date": "2026-10-30",
    "_type": "DueDateTask"
}
```

`_type` บอกว่าต้องสร้าง class ไหนตอนโหลด ถ้าไฟล์เก่าไม่มี `tags` จะใส่ `[]` ให้อัตโนมัติ

## 5. Interface Design (CLI)

```
1. Add Normal Task      4. List All Tasks     7. Search Tasks
2. Add Due Date Task    5. Complete Task      8. Filter Tasks
3. Add Priority Task    6. Delete Task        9. Sort Tasks
0. Exit
```

- Filter ถามทีละเงื่อนไข กด Enter เพื่อข้ามเงื่อนไขที่ไม่ใช้
- Sort ถามเกณฑ์ (`id` / `due_date` / `priority`) และถามว่าจะกลับลำดับไหม

## 6. Algorithm (Pseudocode)

```
search(keyword):
    keyword = lowercase(keyword)
    return งานที่ keyword อยู่ใน description หรืออยู่ใน tag ใด tag หนึ่ง

filter(status, due_before, priority, tag):
    result = งานทั้งหมด
    สำหรับแต่ละเงื่อนไขที่ผู้ใช้ใส่มา:
        result = เก็บเฉพาะงานใน result ที่ผ่านเงื่อนไขนั้น      # AND
    return result

sort(criterion, reverse):
    ถ้า criterion = id: เรียงตาม id
    มิฉะนั้น:
        แยกงานที่ "มีค่า" (DueDateTask / PriorityTask) กับงานที่ "ไม่มีค่า"
        เรียงเฉพาะกลุ่มที่มีค่า (priority: High=1, Medium=2, Low=3)
        ต่อกลุ่มที่ไม่มีค่าไว้ท้าย
```

## 7. Implementation Plan

| ขั้น | งาน | สถานะ |
|---|---|---|
| 1 | ย้าย `Task`, `DueDateTask`, `PriorityTask` ไป `src/task.py` และเพิ่ม `tags` | ✅ |
| 2 | สร้าง `data_persistence.py` แล้วให้ `TaskManager` เรียกใช้แทนการเปิดไฟล์เอง | ✅ |
| 3 | สร้าง `cli_interface.py` ย้าย `input()` / `print()` ทั้งหมดออกจาก `main.py` | ✅ |
| 4 | รับ tags ตอนเพิ่มงานและแสดงใน `__str__` | ✅ |
| 5 | `search_tasks` | ✅ |
| 6 | `filter_tasks` | ✅ |
| 7 | `sort_tasks` | ✅ |
| 8 | Week 12: ขยาย filter เป็นช่วงวันที่ (ก่อน/หลัง), หลาย tag, sort ตาม description / completed, เมนูแก้ไข tags, unit test | ⏳ |

## 8. Potential Challenges

- **Sort ข้ามประเภทงาน:** `Task` ธรรมดาไม่มี `due_date` / `priority` → ใช้วิธีแยกกลุ่มแล้วต่อท้าย (ข้อ 6) แทนการใส่ค่าหลอกอย่าง `date.max` ซึ่งจะขึ้นไปอยู่บนสุดเมื่อกลับลำดับ
- **เรียง priority:** ถ้าเรียงเป็น string จะได้ High, Low, Medium → ต้อง map เป็นตัวเลขก่อน
- **วันที่:** ต้องตรวจรูปแบบตอนรับ input และแปลงเป็น `datetime.date` ก่อนเปรียบเทียบ
- **CLI ซับซ้อนขึ้น:** ใช้ helper method (`get_due_date_input`, `get_task_id`, `show_tasks`) ลดโค้ดซ้ำ (DRY)

## 9. Future Enhancements

แจ้งเตือนงานใกล้ครบกำหนดตอนเปิดโปรแกรม, งานที่ทำซ้ำ, export CSV, undo, เปลี่ยนเป็น SQLite, GUI ด้วย Tkinter
