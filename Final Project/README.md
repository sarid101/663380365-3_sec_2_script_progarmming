# Final Project — ระบบแนะนำสีทาเล็บจากโทนผิว (Nail Color Recommender)

**งานกลุ่ม** — โค้ดและเอกสารทั้งหมดอยู่ใน repository ของกลุ่ม:

### 👉 [github.com/Kittynakaa/Final_project_ScriptProgrammingggg](https://github.com/Kittynakaa/Final_project_ScriptProgrammingggg)

## สรุปโปรเจกต์

แอปวิเคราะห์รูปมือ/เล็บด้วย Computer Vision เพื่อหาโทนผิว แล้วแนะนำพาเลตสีทาเล็บที่เข้ากับผู้ใช้ตามโทนผิว ทรงเล็บ และความยาวเล็บ

**หลักการทำงาน**
1. ตรวจจับผิวในภาพ (แปลงเป็น YCrCb แล้ว threshold + morphology)
2. ประเมิน undertone (cool / warm / neutral) จากค่า ITA ในพื้นที่สี CIE Lab
3. แนะนำสีแบบ rule-based จากกฎในไฟล์ `data/palette_rules.json` (แก้กฎได้โดยไม่ต้องแตะโค้ด)
4. วาดภาพพาเลตและบันทึกประวัติผลการวิเคราะห์

**ฟีเจอร์เด่น:** Smart Nail Advisory ที่อธิบายเหตุผลของคำแนะนำได้, ค้นหา / กรองตามแท็ก / เรียงลำดับคำแนะนำ, ดึงชื่อสีจาก TheColorAPI, จัดการ error โดยไม่ crash, รันได้ทั้ง CLI และ GUI บน Google Colab, มีเว็บเดโมบน GitHub Pages

**สถาปัตยกรรม 3 ชั้น (OOP):** Presentation (`cli.py`) → Business Logic (`skin_analyzer.py`, `recommender.py`, `advisory.py`, `api_client.py`, `models.py`) → Data Access (`data_store.py`, `palette_renderer.py`)

**เทคโนโลยี:** Python, OpenCV, NumPy, requests, Pillow / Matplotlib, pytest, GitHub Actions

**การพัฒนา:** แบ่งเป็น Sprint 1–4 มี snapshot ของแต่ละ Sprint ใน repository พร้อม `TEST.md`, `FLOWCHART.md` และแผน/บันทึกการเปลี่ยนแปลงของ Sprint 4

## สมาชิกและบทบาท (Role Rotation)

| สมาชิก | รหัสนักศึกษา | Sprint 1 | Sprint 2 | Sprint 3 | Final |
|---|---|---|---|---|---|
| **สาริษฐ์ บุตรช่วง** (ผู้จัดทำ repository นี้) | 663380365-3 | Debugger | Planner | Coder | Debugger |
| ชาคริต อ่วมอ่ำ | 663380555-8 | Planner | Coder | Debugger | Planner |
| อภิสรา นครสุข | 663380578-6 | Coder | Debugger | Planner | Coder |
| เมธาวี สิทธิชัยเนตร | 663380372-6 | Coder | Debugger | Planner | Coder |

ข้อมูลบทบาทอ้างอิงจาก README ของ repository กลุ่ม
