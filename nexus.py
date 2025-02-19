import time
import asyncio
from playwright.async_api import async_playwright

def log(message):
    print(f"[LOG] {message}")

async def nexus_bot():
    while True:
        try:
            async with async_playwright() as p:
                log("Memulai browser...")
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()

                log("🔄 Membuka Nexus...")
                await page.goto("https://app.nexus.xyz/")
                
                # Klik tombol "Sign up to earn NEX" jika ada
                sign_up_button = await page.query_selector(".w-\\[45\\%\\] > div > .min-w-\\[200px\\] > div > .w-full")
                if sign_up_button:
                    log("✅ Tombol 'Sign up to earn NEX' ditemukan! Klik...")
                    await sign_up_button.click()
                    await page.wait_for_timeout(2000)
                else:
                    log("⚠️ Tombol 'Sign up to earn NEX' tidak ditemukan. Mungkin sudah login?")
                
                # Klik tombol "Continue with a wallet"
                connect_wallet = await page.query_selector("button:text('Continue with a wallet')")
                if connect_wallet:
                    log("✅ Tombol 'Continue with a wallet' ditemukan! Klik...")
                    await connect_wallet.click()
                    await page.wait_for_timeout(2000)
                else:
                    log("⚠️ Tombol 'Continue with a wallet' tidak ditemukan. Mungkin sudah connect?")
                
                log("✅ Login sukses! 🚀 Menunggu disconnect...")
                
                # Loop pengecekan status koneksi
                while True:
                    await page.wait_for_timeout(10000)  # Tunggu 10 detik sebelum cek
                    if await page.query_selector("button:text('Continue with a wallet')"):
                        log("⚠️ Terputus! Menghubungkan kembali...")
                        break
                
                log("🔄 Menutup browser dan restart bot...")
                await browser.close()
        
        except Exception as e:
            log(f"❌ ERROR: {e}")
        
        log("🔄 Restarting bot dalam 5 detik...")
        time.sleep(5)  # Tunggu 5 detik sebelum restart bot

if __name__ == "__main__":
    asyncio.run(nexus_bot())