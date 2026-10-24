# Project Plan: Enhanced Task Manager CLI (Final Version)

**ผู้จัดทำ:** สาริษฐ์ บุตรช่วง (663380365-3) — SP352301 Script Programming 1/2569

## 1. Introduction

เอกสารนี้ต่อจาก PLAN.md ของ Week 11 ใช้บันทึกว่าแผนถูกทำจริงอย่างไร ปัญหาที่เจอ และสิ่งที่ได้เรียนรู้ จากการพัฒนา Task Manager แบบหลายโมดูลจนเสร็จ

## 2. Requirements — สถานะ

### 2.1 Functional

| Requirement | สถานะ |
|---|---|
| เพิ่ม / แสดง / ทำเครื่องหมายเสร็จ / ลบงาน | ✅ |
| รองรับ `DueDateTask` และ `PriorityTask` | ✅ |
| Tags (list of strings) ใน Task ทุกประเภท + เพิ่ม/ลบ tag | ✅ |
| Search คำใน description และ tags (case-insensitive, partial match) | ✅ |
| Filter รวมหลายเงื่อนไข: สถานะ, ช่วงวันที่, priority, tags | ✅ |
| Sort: id, description, completed, due_date, priority | ✅ |
| บันทึก/โหลด `data/tasks.json` โดยคงประเภทงานและ tags | ✅ |

### 2.2 Non-Functional

- **Usability:** เมนูชัดเจน ข้อความแจ้งเตือนบอกวิธีแก้ (เช่นรูปแบบวันที่ที่ถูกต้อง) ถามยืนยันก่อนลบ
- **Reliability:** ดัก input ผิด, ไฟล์ JSON เสีย, งานเก่าที่ไม่มี `tags`, งานที่ข้อมูลผิดถูกข้ามทีละรายการ
- **Maintainability:** แยกหน้าที่ชัดเจนตามชั้น, มี docstring, ใช้ dict map ประเภทงานและเมนูแทน if/elif ยาว ๆ
- **Testability:** unit test 13 ข้อ ใช้ไฟล์ชั่วคราว

## 3. Architecture (As Implemented)

```
main.py ──> CLIInterface ──> TaskManager ──> DataPersistence ──> data/tasks.json
                                  │
                                  └── Task / DueDateTask / PriorityTask
```

| โมดูล | หน้าที่ |
|---|---|
| `task.py` | Data models, `to_dict`, `__str__`, `add_tag` / `remove_tag` — subclass override แค่ `_extra_info()` จึงไม่ต้อง split string ใน `__str__` |
| `data_persistence.py` | อ่าน/เขียน JSON, สร้าง object กลับตาม `_type` ผ่าน `TASK_TYPES` dict |
| `task_manager.py` | Business logic ทั้งหมด ไม่มี `input()` / เมนู |
| `cli_interface.py` | รับ input, ตรวจความถูกต้อง, แสดงผล — เรียก TaskManager เท่านั้น |
| `main.py` | ตั้งค่า logging, สร้าง TaskManager + CLIInterface แล้วเริ่มทำงาน |

## 4. Implementation Details & Challenges

### 4.1 Tags
- เก็บเป็น list ใน `Task` normalize เป็นตัวพิมพ์เล็กและตัดซ้ำตั้งแต่ constructor
- `load_tasks` ใช้ `setdefault("tags", [])` รองรับไฟล์จากเวอร์ชันก่อน

### 4.2 Search
- เทียบ `keyword in description.lower()` หรือ `any(keyword in tag ...)` จับคำบางส่วนได้ เช่น `shop` เจอ tag `shopping`

### 4.3 Filter
- กรองทีละเงื่อนไขต่อกัน (AND)
- วันที่และ priority ใช้ `isinstance()` เพื่อให้กรองเฉพาะงานประเภทที่มี attribute นั้น
- Tags ใช้ `set(wanted).issubset(task.tags)` = ต้องมีครบทุก tag

### 4.4 Sort (Polymorphic sorting)
- **ปัญหา:** โค้ดตัวอย่างให้งานที่ไม่มีวันที่ใช้ `datetime.date.max` ซึ่งตอน `reverse=True` งานพวกนี้จะขึ้นไปอยู่บนสุด
- **วิธีแก้:** แยกงานที่มีค่ากับไม่มีค่า เรียงเฉพาะกลุ่มที่มีค่า แล้วต่อกลุ่มที่ไม่มีค่าไว้ท้าย
- Priority ใช้ `PRIORITY_MAP = {"High": 1, "Medium": 2, "Low": 3}` เพราะถ้าเรียงเป็น string จะได้ High, Low, Medium
- เรียงตาม id ก่อน แล้วอาศัย stable sort ของ Python ทำให้งานที่ค่าเท่ากันเรียงตาม id เสมอ แม้เรียงแบบมากไปน้อย

### 4.5 Debugging
- **Integration bug:** `main.py` ตัวอย่างรันไม่ได้ (`ImportError: attempted relative import with no known parent package`) เพราะ import `task_manager` เป็นโมดูลเดี่ยวทั้งที่ข้างในใช้ relative import → แก้เป็น import ผ่าน package `src`
- **Logical bug:** ลำดับ sort ตอน reverse (ข้อ 4.4) เจอตอนรัน demo แล้วเพิ่ม unit test กันไม่ให้กลับมาอีก
- **Logging:** ใช้ `logging.getLogger(__name__)` ในแต่ละโมดูล เปิดดูด้วย `--debug` แทนการเพิ่ม/ลบ `print`
- **Edge cases ที่ทดสอบ:** ลิสต์ว่าง, keyword ว่าง, วันที่/priority ผิด, ID ไม่มีอยู่, complete ซ้ำ, JSON เสีย, JSON เก่าไม่มี tags

## 5. Lessons Learned

- การแยกชั้น (UI / logic / storage) ทำให้หาบั๊กได้ว่าอยู่ชั้นไหน และเขียน test ให้ `TaskManager` ได้โดยไม่ต้องจำลองการพิมพ์
- ทำทีละฟีเจอร์แล้วทดสอบก่อนไปต่อ ช่วยให้เจอปัญหาเร็วและแก้ง่าย
- ควรทดสอบกรณีขอบ (reverse, ค่าว่าง, ข้อมูลเก่า) ไม่ใช่แค่กรณีปกติ

## 6. Future Work

- GUI ด้วย Tkinter
- เปลี่ยนจาก JSON เป็น SQLite
- แจ้งเตือนงานใกล้ครบกำหนดตอนเปิดโปรแกรม
- Recurring tasks, export CSV, ระบบผู้ใช้หลายคน, เว็บด้วย Flask
