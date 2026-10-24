# Web Scraping Ethics and Legality Guidelines

1. **Respect `robots.txt`** – ตรวจ `https://<domain>/robots.txt` ก่อนเสมอ ถ้า path ไหนถูก Disallow ห้าม scrape
2. **Review Terms of Service** – หลายเว็บห้าม scraping ใน ToS การฝ่าฝืนอาจนำไปสู่ Cease and Desist หรือการฟ้องร้อง การที่ไม่ได้ห้ามไว้ก็ไม่ได้แปลว่าอนุญาต
3. **Rate limiting** – ใส่ delay ระหว่าง request (โปรเจกต์นี้ใช้ `delay_between_pages: 2`) และจำกัดจำนวนหน้า (`max_pages`) ไม่ส่ง request พร้อมกันจำนวนมาก
4. **Identify yourself** – ควรใช้ User-Agent ที่บอกตัวตนและช่องทางติดต่อได้ เมื่อใช้งานจริง
5. **Selenium กับเจ้าของเว็บ** – การเปิดเบราว์เซอร์จริงโหลดทั้ง JS/รูปภาพ ทำให้กินทรัพยากรเซิร์ฟเวอร์มากกว่า `requests` จึงควรใช้เมื่อจำเป็นเท่านั้น
6. **Data usage & copyright** – ข้อมูลที่ดึงมาอาจมีลิขสิทธิ์ ห้ามนำไปเผยแพร่ซ้ำหรือใช้เชิงพาณิชย์โดยไม่ได้รับอนุญาต และห้ามเก็บข้อมูลส่วนบุคคล (PII) โดยไม่ได้รับความยินยอม (สอดคล้องกับ PDPA)
7. **Legal risks** – ความเสี่ยงหลักคือการละเมิดสัญญา (ToS), trespass to chattels, ละเมิดลิขสิทธิ์ และละเมิดข้อมูลส่วนบุคคล

> โปรเจกต์นี้ใช้ `books.toscrape.com` ซึ่งเป็นเว็บที่สร้างขึ้นเพื่อฝึก scraping โดยเฉพาะ และใช้เพื่อการศึกษาเท่านั้น
