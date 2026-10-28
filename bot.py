import asyncio
import logging
import os
import random
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl import types
from fastapi import FastAPI
import httpx

API_ID = 38036402
API_HASH = "c11ba405e629262a728eadce550b94f8"

client = TelegramClient('session_upravlyalka', API_ID, API_HASH)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "🚀 Управлялка активна!"}

async def send_ping():
    await asyncio.sleep(10)
    render_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')}.onrender.com"
    async with httpx.AsyncClient() as client_http:
        while True:
            if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
                try:
                    response = await client_http.get(render_url)
                    logging.info(f"📟 Автопинг: {response.status_code}")
                except: pass
            await asyncio.sleep(300)

muted_users = set()
antimute_enabled = True
afk_enabled = False
afk_reason = ""
autoresponder_enabled = False
autoresponder_text = ""

@client.on(events.NewMessage(outgoing=True, pattern=r'\.help'))
async def help_cmd(event):
    await event.edit(
        "**Навигация по командам бота-автоматизации**\n\n"
        "▫️ **Работа с сообщениями**\n"
        "  • `.check` — анализ файла\n"
        "  • `.spam <кол-во> <текст>` — спам\n"
        "  • `.help` — список команд\n"
        "  • `.love` — ❤️\n"
        "  • `.mute` — мут (в ответе)\n"
        "  • `.unmute` — снять мут (в ответе)\n"
        "  • `.antimute` — обход мута\n"
        "  • `.sw` — раскладка (в ответе)\n"
        "  • `.troll` — оскорбление\n"
        "  • `.type <текст>` — анимация хакера\n"
        "  • `.zaebu <текст>` — по одной букве\n\n"
        "▫️ **Форматирование**\n"
        "  • `.bold` | `.italic` | `.monospace` | `.underline`\n"
        "  • `.leet` | `.kawaii` | `.tsundere` | `.yandere`\n\n"
        "▫️ **Игры**\n"
        "  • `.bw` | `.dice` | `.duel` | `.flip` | `.chk` | `.ttt`\n\n"
        "▫️ **Обработка и Пробив**\n"
        "  • `.clone` | `.dox` | `.doxp` | `.fv` | `.afk` | `.autoresponder`\n"
        "  • `.gifts` | `.info` | `.nk` | `.short` | `.status`\n"
        "  • `.story` | `.time` | `.yars` | `.gif` | `.gosu` | `.gp` | `.lq`"
    )

@client.on(events.NewMessage(outgoing=True, pattern=r'\.check'))
async def check_cmd(event):
    if not event.is_reply: return await event.edit("⚠️ Ответь на файл!")
    await event.edit("🔍 **Анализ...**")
    await asyncio.sleep(0.5)
    await event.edit("🛡 **Чисто!**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.spam (\d+) (.+)'))
async def spam_cmd(event):
    count, text = int(event.pattern_match.group(1)), event.pattern_match.group(2)
    await event.delete()
    for _ in range(min(count, 50)):
        await event.respond(text)
        await asyncio.sleep(0.08)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.love'))
async def love_cmd(event):
    for f in ["❤️", "🧡", "💛", "💚", "💙", "💜", "💖", "💝", "💕"]:
        try: await event.edit(f); await asyncio.sleep(0.1)
        except: pass
    await event.edit("**Люблю тебя! ✨**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.mute'))
async def mute_cmd(event):
    if not event.is_reply: return await event.edit("⚠️ Ответь на смс!")
    reply = await event.get_reply_message()
    muted_users.add(reply.sender_id)
    await event.edit("🤫 Замучен.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.unmute'))
async def unmute_cmd(event):
    if not event.is_reply: return await event.edit("⚠️ Ответь на смс!")
    reply = await event.get_reply_message()
    if reply.sender_id in muted_users: muted_users.remove(reply.sender_id)
    await event.edit("🔊 Размучен!")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.antimute'))
async def antimute_cmd(event):
    global antimute_enabled
    antimute_enabled = not antimute_enabled
    await event.edit(f"🛡 Anti-Mute: **{'ВКЛ' if antimute_enabled else 'ВЫКЛ'}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.sw'))
async def sw_cmd(event):
    if not event.is_reply: return await event.edit("⚠️ Ответь на смс!")
    reply = await event.get_reply_message()
    ru = "йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"
    en = "qwertyuiopasdfghjkl;'zxcvbnm,.QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>"
    t = reply.text
    tr = t.translate(str.maketrans(ru, en)) if any(c in ru for c in t) else t.translate(str.maketrans(en, ru))
    await event.edit(tr)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.troll'))
async def troll_cmd(event):
    phrases = ["🤡 Чего зенки вылупил?", "🤫 Слит, нищ.", "Иди уроки учи, клоун.", "Потеряйся, чушпан."]
    await event.edit(random.choice(phrases))

@client.on(events.NewMessage(outgoing=True, pattern=r'\.type (.+)'))
async def type_cmd(event):
    text = event.pattern_match.group(1)
    current = ""
    for char in text:
        current += char
        try: await event.edit(current + "▒"); await asyncio.sleep(0.04)
        except: pass
    await event.edit(text)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.zaebu (.+)'))
async def zaebu_cmd(event):
    text = event.pattern_match.group(1)
    await event.delete()
    for char in text:
        if char.strip(): await event.respond(char); await asyncio.sleep(0.1)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.bold (.+)'))
async def bold_h(event): await event.edit(f"**{event.pattern_match.group(1)}**")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.italic (.+)'))
async def italic_h(event): await event.edit(f"__{event.pattern_match.group(1)}__")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.monospace (.+)'))
async def mono_h(event): await event.edit(f"`{event.pattern_match.group(1)}`")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.underline (.+)'))
async def under_h(event): await event.edit(f"<u>{event.pattern_match.group(1)}</u>")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.leet (.+)'))
async def leet_cmd(event):
    t = event.pattern_match.group(1).lower()
    dic = {'а':'4','е':'3','и':'1','о':'0','т':'7','с':'c','в':'8'}
    await event.edit("".join([dic[c] if c in dic else c for c in t]))
@client.on(events.NewMessage(outgoing=True, pattern=r'\.kawaii (.+)'))
async def kaw_h(event): await event.edit(f"✨ {event.pattern_match.group(1)} (о´∀`о) 💕")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.tsundere (.+)'))
async def tsun_h(event): await event.edit(f"💢 {event.pattern_match.group(1)}... Б-бака! 🙄")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.yandere (.+)'))
async def yan_h(event): await event.edit(f"👁‍🗨 {event.pattern_match.group(1)}... Ты же только мой? 🔪")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.bw'))
async def bw_cmd(event):
    frames = ["⬜️⬜️⬜️⬜️⬜️\n⬜️⬛️⬜️⬛️⬜️\n⬜️⬜️⬜️⬜️⬜️", "⬛️⬛️⬛️⬛️⬛️\n⬛️⬜️⬛️⬜️⬛️\n⬛️⬛️⬛️⬛️⬛️"]
    for f in frames: await event.edit(f"🎮 **Закрась поле:**\n\n{f}"); await asyncio.sleep(0.3)
@client.on(events.NewMessage(outgoing=True, pattern=r'\.dice'))
async def dice_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file=types.InputMediaDice(emoticon="🎲"))
@client.on(events.NewMessage(outgoing=True, pattern=r'\.duel'))
async def duel_cmd(event):
    if not event.is_reply: return await event.edit("⚠️ Ответь на смс!")
    reply = await event.get_reply_message()
    await event.edit("⚔️ **Вызов брошен! Заряжаем револьверы...**")
    await asyncio.sleep(0.8)
    await event.edit(f"👑 Ты развалил @{reply.sender.username or reply.sender_id} и забрал {random.randint(10,100)} звёзд! 😎" if random.choice([True, False]) else "💀 Ты проиграл дуэль...")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.flip'))
async def flip_cmd(event): await event.edit(f"🪙 Выпало: **{random.choice(['🌕 ОРЁЛ', '🟤 РЕШКА'])}**")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.chk'))
async def chk_cmd(event): await event.edit("🏁 **[ШАШКИ]**\n\n🔴🟪🔴🟪🔴\n🟪⬜️🟪⬜️🟪\n⚪️🟪⚪️🟪⚪️\n\nТвой ход!")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ttt'))
async def ttt_cmd(event): await event.edit("❌⭕️ **КРЕСТИКИ-НОЛИКИ**\n\n❌ ｜ ⬜️ ｜ ⬜️\n———————\n⬜️ ｜ ⭕️ ｜ ⬜️")

async def make_dox(event):
    if not event.is_reply: return "⚠️ Ответь на смс цели!"
    reply = await event.get_reply_message()
    u = reply.sender
    try:
        full = await client(GetFullUserRequest(u.id))
        bio = full.full_user.about or "Не указано"
    except: bio = "Скрыто приватностью"
    ips, cities = ["195.211.193.", "91.243.102.", "178.92.24."], ["Киев", "Харьков", "Одесса", "Днепр", "Львов"]
    return f"🚨 **ПОЛНЫЙ ДОКС** 🚨\n👤 **Имя:** {u.first_name or 'Нет'}\n🆔 **ID:** `{u.id}`\n🏷 **Юзернейм:** @{u.username or 'нет'}\n📝 **БИО:** {bio}\n🌐 **IP:** `{random.choice(ips)}{random.randint(1,254)}`\n📍 **Город:** г. {random.choice(cities)}\n🔐 **Порт:** `8080 open [Vulnerable]`"

@client.on(events.NewMessage(outgoing=True, pattern=r'\.dox$'))
async def dox_cmd(event): await event.edit(await make_dox(event))
@client.on(events.NewMessage(outgoing=True, pattern=r'\.doxp$'))
async def doxp_cmd(event):
    res = await make_dox(event); await event.delete()
    await client.send_message("me", res)
@client.on(events.NewMessage(outgoing=True, pattern=r'\.clone$'))
async def clone_cmd(event):
    if not event.is_reply: return await event.edit("⚠️ Ответь на смс жертвы!")
    reply = await event.get_reply_message()
    u = reply.sender
    await event.edit("👥 **Клонирую аккаунт...**")
    try:
        full = await client(GetFullUserRequest(u.id))
        await client(UpdateProfileRequest(first_name=u.first_name or "", last_name=u.last_name or "", about=full.full_user.about or ""))
        await event.edit("👑 **Готово! Профиль скопирован.**")
    except Exception as e: await event.edit(f"❌ Ошибка: {e}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.fv'))
async def fv_cmd(event): await event.edit("🔊 **Усиление голосового...**\nБассы: +24dB [Успешно].")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.afk (.*)'))
async def afk_cmd(event):
    global afk_enabled, afk_reason
    afk_enabled = True
    afk_reason = event.pattern_match.group(1) or "Отошел"
    await event.edit(f"💤 **Режим AFK активирован:** *{afk_reason}*")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.autoresponder (.*)'))
async def autoresponder_cmd(event):
    global autoresponder_enabled, autoresponder_text
    t = event.pattern_match.group(1)
    autoresponder_enabled = bool(t)
    autoresponder_text = t
    await event.edit(f"🤖 **Автоответчик запущен:** `{t}`" if t else "❌ **Автоответчик выключен.**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.gifts'))
async def gifts_cmd(event): await event.edit("🎁 **Сканирование подарков...**\nНайдено: 12 уникальных кастомных подарков, 3 Premium дропа.")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.info'))
async def info_cmd(event):
    if not event.is_reply: return await event.edit("⚠️ Ответь на смс!")
    reply = await event.get_reply_message()
    await event.edit(f"📊 **ИНФО:**\nID: `{reply.sender_id}`\nБот: {reply.sender.bot}")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.nk'))
async def nk_cmd(event): await event.edit("🐾 **Ня! Отправляю неко-тян...** 🐾")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.short'))
async def short_cmd(event): await event.edit("📝 **Краткий пересказ:**\nСобеседник пытается оправдаться, ты доминируешь в споре. Слив.")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.status (.+)'))
async def status_cmd(event):
    await client(UpdateProfileRequest(about=event.pattern_match.group(1)))
    await event.edit("📝 **Статус в БИО изменен!**")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.story'))
async def story_cmd(event): await event.edit("📸 **Нарезка медиа под формат Stories...** [100%]")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.time'))
async def time_cmd(event): await event.edit(f"🕒 **Точное время:** `{datetime.now().strftime('%H:%M:%S')}`")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.yars'))
async def yars_cmd(event): await event.edit("👁‍🗨 **Запуск поиска по фото...**\nСовпадений в сети: 4.")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.gif'))
async def gif_cmd(event): await event.edit("📹 **Конвертация в анимированный GIF...** [Успешно]")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.gosu'))
async def gosu_cmd(event): await event.edit("⚡️ **[GOSU MODE ACTIVATED]** ⚡️\nСистема взломана. 💻")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.gp'))
async def gp_cmd(event): await event.edit("💣 **[BIG SURPRISE PACK]** 💣\nВсе файлы зашифрованы алгоритмом AES-256. 😉")
@client.on(events.NewMessage(outgoing=True, pattern=r'\.lq (.+)'))
async def lq_cmd(event): await event.edit(f"⚠️ [LQ]: {''.join([c.upper() if random.choice([True, False]) else c.lower() for c in event.pattern_match.group(1)])}")

@client.on(events.NewMessage(incoming=True))
async def background_handlers(event):
    global afk_enabled, afk_reason, autoresponder_enabled, autoresponder_text
    if event.sender_id in muted_users:
        try: await event.delete()
        except: pass
        return
    if event.is_private:
        if afk_enabled: await event.respond(f"💤 AFK. Причина: {afk_reason}")
        elif autoresponder_enabled: await event.respond(autoresponder_text)

@client.on(events.NewMessage(outgoing=True))
async def afk_reset(event):
    global afk_enabled
    if afk_enabled and not event.text.startswith(r'.afk'):
        afk_enabled = False
        msg = await event.respond("⚡️ **Режим AFK автоматически отключен.**")
        await asyncio.sleep(2); await msg.delete()

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(client.start())
    asyncio.create_task(send_ping())
    print("🚀 Управлялка успешно запущена!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
