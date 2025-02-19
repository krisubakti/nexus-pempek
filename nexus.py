import asyncio
import os
from playwright.async_api import async_playwright

def check_if_disconnected(page):
    try:
        return page.locator("text=CONNECT TO NEXUS").is_visible()
    except:
        return False

async def nexus_bot(wallet_address):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        await page.goto("https://app.nexus.xyz")
        
        # Login menggunakan wallet
        await page.click("button:has-text('Connect Wallet')")
        await asyncio.sleep(2)  # Tunggu tampilan wallet
        
        await page.fill("input[type='text']", wallet_address)
        await page.click("button:has-text('Continue')")
        await asyncio.sleep(5)
        
        while True:
            if check_if_disconnected(page):
                print(f"[{wallet_address}] Terputus! Menghubungkan kembali...")
                await page.click("text=CONNECT TO NEXUS")
                await asyncio.sleep(5)
            
            await asyncio.sleep(10)  # Mengecek status setiap 10 detik
        
        await browser.close()

async def main():
    print("\n==============================")
    print("  🚀 Pempek Lahat Nexus Bot  ")
    print("==============================\n")
    
    accounts = []
    with open("wallets.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            wallet_address = line.strip()
            accounts.append(wallet_address)
    
    tasks = [nexus_bot(wallet) for wallet in accounts]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())