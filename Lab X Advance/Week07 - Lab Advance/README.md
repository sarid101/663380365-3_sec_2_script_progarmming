# LabX ADV: Advanced Web Scraping & Introduction to Automated Agents

**ชื่อ:** สาริษฐ์ บุตรช่วง  **รหัส:** 663380365-3  **วิชา:** SP352301 Script Programming 1/2569

Agentic Web Scraper ที่ใช้ **Selenium** ควบคุมเบราว์เซอร์จริง และทำงานตาม "แผน" ที่เขียนไว้ในไฟล์ config (`configs/example_site_config.json`)
ตัว agent จะ: อ่าน config → เปิด `start_url` → ดึงข้อมูลสินค้าทุกชิ้นในหน้า → คลิกปุ่ม Next → วนซ้ำจนครบ `max_pages` หรือไม่มีหน้าถัดไป → บันทึกเป็น `data/scraped_products.json`

เว็บเป้าหมาย: [books.toscrape.com](https://books.toscrape.com) (เว็บจำลองที่สร้างมาเพื่อฝึก scraping โดยเฉพาะ)

## ผลลัพธ์

![ผลลัพธ์](screenshot.png)

```
Scraping page 1...
Scraping page 2...
Successfully scraped 40 items and saved to data\scraped_products.json
```

---

## คู่มือการ Setup โปรเจกต์ Agentic Web Scraper ใน VS Code

**สิ่งที่ต้องมี:** Python 3.9+, Google Chrome, VS Code

1. **เปิดโฟลเดอร์** `agentic-web-scraper` ใน VS Code แล้วเปิด Terminal (`Ctrl + ~`)
2. **สร้างและเปิดใช้ virtual environment** (ถ้ามี `.venv` อยู่แล้วข้ามไปข้อ 3)
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1        # Windows PowerShell
   # source .venv/bin/activate       # macOS / Linux
   ```
   > ถ้า PowerShell ขึ้น error เรื่อง script execution ให้รัน `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` ก่อน
3. **ติดตั้ง library**
   ```powershell
   pip install -r requirements.txt
   ```
4. **รันโปรแกรม** (ต้องอยู่ในโฟลเดอร์ `agentic-web-scraper`)
   ```powershell
   cd agentic-web-scraper
   python main.py
   ```
5. เปิดไฟล์ `data/scraped_products.json` เพื่อดูผลลัพธ์

### ปรับแต่ง
- เปลี่ยนจำนวนหน้า: แก้ `max_pages` ใน config
- อยากเห็นเบราว์เซอร์ทำงาน: แก้ `headless=True` เป็น `False` ใน `main.py`
- ใช้กับเว็บอื่น: แก้ selector ใน config (ใช้ F12 → Inspect หา selector) โดยไม่ต้องแก้โค้ด

---

## โครงสร้างโปรเจกต์

```
agentic-web-scraper/
├── src/
│   ├── __init__.py
│   ├── scraper_agent.py     # loop หลักของ agent: ดึงข้อมูล + เปลี่ยนหน้า
│   ├── config_parser.py     # โหลดและตรวจสอบ config
│   ├── data_models.py       # dataclass Product
│   ├── utils.py             # save JSON, explicit wait, robust_click (retry)
│   └── driver_manager.py    # สร้าง/ปิด WebDriver (headless, user-agent)
├── configs/example_site_config.json
├── data/scraped_products.json
├── docs/ETHICS.md
├── main.py
├── requirements.txt
└── README.md
```

## สิ่งที่แก้จากโค้ดต้นฉบับ

| ปัญหาในต้นฉบับ | การแก้ไข |
|---|---|
| `main.py` เพิ่ม `src` เข้า path แล้ว import แบบ `from scraper_agent import ...` แต่ใน `scraper_agent.py` ใช้ relative import (`from .driver_manager`) → `ImportError` | import แบบ package: `from src.scraper_agent import ScraperAgent` |
| `utils.py` ใช้ `os.makedirs` แต่ไม่ได้ `import os` → `NameError` ตอนบันทึกไฟล์ | เพิ่ม `import os` |
| config มี `"description": null` แต่ validator บังคับให้ทุก selector เป็น string → `ValueError` | อนุญาตให้เป็น `null` และข้ามช่องนั้นตอนดึงข้อมูล |
| `robust_click` ใช้ `By.CSS_SELECTOR` ตายตัวแม้ selector เป็น XPath | เดาชนิด selector อัตโนมัติ (ขึ้นต้น `/` = XPath) |
| หลังคลิก Next ไม่รอให้หน้าใหม่โหลด อาจดึงข้อมูลหน้าเดิมซ้ำ | รอ `EC.url_changes` ก่อนดึงหน้าถัดไป |
| ChromeDriver ของ `webdriver-manager` บน Windows บางครั้งชี้ไฟล์ผิด | ใช้ Selenium Manager (ในตัว selenium 4.6+) ก่อน แล้วค่อย fallback |

## Ethics

ดู [docs/ETHICS.md](docs/ETHICS.md) — โปรเจกต์นี้ใช้เพื่อการศึกษาเท่านั้น มี delay ระหว่างหน้า และจำกัดจำนวนหน้า

---

> ย้ายมาจาก repository เดิม: [sarid101/LabX-ADV1-Advanced-Web-Scraping-Introduction-to-Automated-Agents](https://github.com/sarid101/LabX-ADV1-Advanced-Web-Scraping-Introduction-to-Automated-Agents)
