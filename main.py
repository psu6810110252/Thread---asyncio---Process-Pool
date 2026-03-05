import asyncio
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# ==========================================
# ส่วนที่ 1: Asyncio - งาน I/O (ดึงข้อมูลผ่าน Network)
# ==========================================
async def fetch_etf_data(ticker):
    print(f"[Asyncio] 📡 กำลังดึงข้อมูลราคา {ticker} จาก API...")
    await asyncio.sleep(1.5)  # จำลองการรอเซิร์ฟเวอร์ตอบกลับ (Network Latency)
    
    # จำลองการสุ่มราคาปิดย้อนหลัง 5 วัน
    prices = [round(random.uniform(300, 500), 2) for _ in range(5)]
    print(f"[Asyncio] ✅ ได้รับข้อมูล {ticker} เรียบร้อย: {prices}")
    return ticker, prices

async def main_async_fetch(tickers):
    print("\n--- ขั้นตอนที่ 1: ดึงข้อมูลด้วย Asyncio ---")
    # สั่งให้ดึงข้อมูลทุกกองทุนพร้อมๆ กันโดยไม่รอบล็อกกันเอง
    tasks = [fetch_etf_data(ticker) for ticker in tickers]
    results = await asyncio.gather(*tasks)
    return dict(results)

# ==========================================
# ส่วนที่ 2: Thread Pool - งาน I/O (บันทึกลงฮาร์ดดิสก์)
# ==========================================
def save_to_csv(item):
    ticker, prices = item
    print(f"[Thread] 💾 กำลังบันทึกข้อมูล {ticker} ลงไฟล์ {ticker}_history.csv... (Thread: {threading.current_thread().name})")
    time.sleep(1)  # จำลองความหน่วงของการเขียนไฟล์ลงฮาร์ดดิสก์
    print(f"[Thread] 📁 บันทึกไฟล์ {ticker} สำเร็จ")

def run_threading_save(data_dict):
    print("\n--- ขั้นตอนที่ 2: บันทึกไฟล์ด้วย Thread Pool ---")
    # ใช้ Thread Pool เพื่อสั่งเขียนไฟล์หลายๆ ไฟล์พร้อมกัน
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(save_to_csv, data_dict.items())

# ==========================================
# ส่วนที่ 3: Process Pool - งาน CPU (คำนวณสถิติ/คณิตศาสตร์)
# ==========================================
def calculate_volatility(ticker):
    print(f"[Process] ⚙️ กำลังคำนวณความผันผวน (Volatility) ของ {ticker}...")
    
    # จำลองการคำนวณทางคณิตศาสตร์ที่ซับซ้อนและกิน CPU หนักๆ
    _ = [x ** 2.5 for x in range(5_000_000)] 
    
    # สุ่มผลลัพธ์ค่าความผันผวน (เปอร์เซ็นต์)
    volatility = round(random.uniform(10, 25), 2)
    print(f"[Process] 📊 {ticker} มีค่าความผันผวน: {volatility}%")
    return ticker, volatility

def run_process_pool_compute(tickers):
    print("\n--- ขั้นตอนที่ 3: ประมวลผลข้อมูลด้วย Process Pool ---")
    # แตก Process ไปยัง CPU Core อื่นๆ เพื่อคำนวณเลขพร้อมกัน
    with ProcessPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(calculate_volatility, tickers))
    return results

# ==========================================
# Main Execution
# ==========================================
if __name__ == "__main__":
    etf_list = ["VOO", "QQQ", "VTI"] # รายชื่อกองทุนที่ต้องการวิเคราะห์
    
    start_time = time.time()
    
    # 1. ดึงข้อมูล
    etf_data = asyncio.run(main_async_fetch(etf_list))
    
    # 2. บันทึกข้อมูล
    run_threading_save(etf_data)
    
    # 3. คำนวณความผันผวน
    run_process_pool_compute(etf_list)
    
    print(f"\n✨ ทำงานเสร็จสิ้นทั้งหมดในเวลา: {time.time() - start_time:.2f} วินาที ✨")