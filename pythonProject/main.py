from pyrogram import Client, filters
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import asyncio

app = Client(
    "my_bot_session",
    api_id=29482943,
    api_hash="a773fdcc93373ff21122a164f23f51c2",
    bot_token="5454972460:AAGzSo4M51MjvfX7IREY8XOZMNiGYRqPfJY"
)


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())



def get_info_from_site(queue):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get("https://svitlo.oe.if.ua/")
        queue_field = driver.find_element(By.NAME, "accountNumber")
        queue_field.send_keys(queue)
        submit = driver.find_element(By.ID, "accountNumberReport")
        submit.click()


        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                        "text[x='38.5px'][y='56'][dy='-9.72'][text-anchor='middle'] > tspan[style='font-weight:bold;font-size: 30px']")))


        element = driver.find_element(By.CSS_SELECTOR,
                                      "text[x='38.5px'][y='56'][dy='-9.72'][text-anchor='middle'] > tspan[style='font-weight:bold;font-size: 30px']")
        info = element.text.strip()
        return info
    except NoSuchElementException as e:
        print("Помилка: Елемент не знайдено", e)
        return "Не знайдено інформацію для введеного номеру."
    except TimeoutException as e:
        print("Помилка: Час очікування вичерпано", e)
        return "Час очікування завантаження елемента вичерпано."
    except Exception as e:
        print("Інша помилка:", e)
        return str(e)
    finally:
        driver.quit()



@app.on_message(filters.command("getinfo"))
async def get_info(client, message):
    try:
        queue = message.text.split(" ", 1)[1]
        if not queue.isdigit():
            await message.reply_text("Номер рахунку повинен складатись тільки з цифр.")
            return
    except IndexError:
        await message.reply_text(
            "Не вказано номер рахунку. Використовуйте команду у форматі `/getinfo {номер_рахунку}`.")
        return

    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, get_info_from_site, queue)
    await message.reply_text(info)


if __name__ == "__main__":
    app.run()
