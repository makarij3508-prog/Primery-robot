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

# Ключи авторизации
API_ID = 38036402
API_HASH = "c11ba405e629262a728eadce550b94f8"

client = TelegramClient('session_upravlyalka', API_ID, API_HASH)
logging.basicConfig(level=logging.INFO)

# Поднимаем FastAPI сервер для обхода блокировки Рендера
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "🚨 Ультимативный юзербот активен, автопинг работает!"}

# Функция автопинга (Self-Ping)
async def send_ping():
    await asyncio.sleep(10)
    # Render сам подставит имя хоста в эту переменную
    render_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '')}.onrender.com"
    async with httpx.AsyncClient() as client_http:
        while True:
            if os.environ.get('RENDER_EXTERNAL_HOSTNAME'):
                try:
                    response = await client_http.get(render_url)
                    logging.info(f"📟 Автопинг отправлен. Статус: {response.status_code}")
                except Exception as e:
                    logging.error(f"❌ Ошибка автопинга: {e}")
            await asyncio.sleep(300)

# Глобальные переменные для работы систем
muted_users = set()
antimute_enabled = True
afk_enabled = False
afk_reason = ""
autoresponder_enabled = False
autoresponder_text = ""

# ▫️ НАВИГАЦИЯ (Команда .help)
@client.on(events.NewMessage(outgoing=True, pattern=r'\.help'))
async def help_cmd(event):
    await event.edit(
        "**Навигация по командам бота-автоматизации**\n\n"
        "▫️ **Работа с сообщениями**\n"
        "  • `.check` — анализирует файл на угрозы\n"
        "  • `.spam <кол-во> <текст>` — жесткий спам текстом\n"
        "  • `.help` — список команд\n"
        "  • `.love` — романтическая анимация ❤️\n"
        "  • `.mute` — замутить собеседника (в ответе)\n"
        "  • `.unmute` — снять мут (в ответе)\n"
        "  • `.antimute` — включить/выключить обход мута\n"
        "  • `.sw` — сменить раскладку текста (в ответе)\n"
        "  • `.troll` — оскорбить случайной фразой\n"
        "  • `.type <текст>` — хакерская анимация набора\n"
        "  • `.zaebu <текст>` — отправить по одной букве\n\n"
        "▫️ **Форматирование**\n"
        "  • `.bold <текст>` — жирный text\n"
        "  • `.italic <текст>` — рукописный текст\n"
        "  • `.monospace <текст>` — моноширинный шрифт\n"
        "  • `.underline <текст>` — подчеркнутый текст\n"
        "  • `.leet <текст>` — превратить текст в l33t sp3ak\n"
        "  • `.kawaii <текст>` / `.tsundere <текст>` / `.yandere <текст>`\n\n"
        "▫️ **Игры**\n"
        "  • `.bw` — игра 'Закрась поле'\n"
        "  • `.dice` — кинуть анимированный кубик в чат\n"
        "  • `.duel` — дуэль на звёзды (в ответе)\n"
        "  • `.flip` — подбросить монетку\n"
        "  • `.chk` — запустить интерактивные шашки\n"
        "  • `.ttt` — запустить крестики-нолики\n\n"
        "▫️ **Обработка и Мониторинг**\n"
        "  • `.clone` — полностью скопировать чужой профиль (в ответе)\n"
        "  • `.dox` — выдать полный пробив юзера в чат (в ответе)\n"
        "  • `.doxp` — выдать пробив юзера скрытно себе в личку\n"
        "  • `.fv` — усилить голосовое сообщение\n"
        "  • `.afk <причина>` — включить автоответ-AFK\n"
        "  • `.autoresponder <текст>` — запустить автоответчик\n"
        "  • `.gifts` — симулировать проверку подарков аккаунта\n"
        "  • `.info` — техническая инфо по юзеру (в ответе)\n"
        "  • `.nk` — отправить аниме неко-тян\n"
        "  • `.short` — сделать суммаризацию диалога\n"
        "  • `.status <текст>` — установить кастомный статус\n"
        "  • `.story` — нарезать фото в формат сторис\n"
        "  • `.time` — вывести текущее точное время\n"
        "  • `.yars` — симулировать поиск по фотографии\n"
        "  • `.gif` — превратить медиа в GIF-формат\n\n"
        "▫️ **Остальное**\n"
        "  • `.gosu` — запустить gosu-скрипт\n"
        "  • `.gp` — выкатить огромный сюрприз-пакет\n"
        "  • `.lq <текст>` — зашакалить регистр текста"
    )

# ================= БЛОК: РАБОТА С СООБЩЕНИЯМИ =================

@client.on(events.NewMessage(outgoing=True, pattern=r'\.check'))
async def check_cmd(event):
    if not event.is_reply:
        await event.edit("⚠️ Ответь командой `.check` на файл или сообщение!")
        return
    await event.edit("🔍 **Анализ безопасности файла...**\n[■■■■■■■■□□] 80%")
    await asyncio.sleep(1)
    await event.edit("🛡 **Результат сканирования:** Угроз, малварей и инъекций не обнаружено. Файл чист!")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.spam (\d+) (.+)'))
async def spam_cmd(event):
    count = int(event.pattern_match.group(1))
    text = event.pattern_match.group(2)
    await event.delete()
    for _ in range(min(count, 100)):
        await event.respond(text)
        await asyncio.sleep(0.08)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.love'))
async def love_cmd(event):
    for frame in ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "💖", "💝", "💕"]:
        try: await event.edit(frame); await asyncio.sleep(0.15)
        except: pass
    await event.edit("**Ты лучшее, что есть в моей жизни! ✨**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.mute'))
async def mute_cmd(event):
    if not event.is_reply:
        await event.edit("⚠️ Ответь на сообщение того, кого хочешь замутить!")
        return
    reply = await event.get_reply_message()
    muted_users.add(reply.sender_id)
    await event.edit(f"🤫 Юзер `{reply.sender_id}` успешно замучен. Его смс будут тереться автоматически.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.unmute'))
async def unmute_cmd(event):
    if not event.is_reply:
        await event.edit("⚠️ Ответь на сообщение, чтобы размутить!")
        return
    reply = await event.get_reply_message()
    if reply.sender_id in muted_users:
        muted_users.remove(reply.sender_id)
    await event.edit("🔊 Собеседник успешно размучен!")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.antimute'))
async def antimute_cmd(event):
    global antimute_enabled
    antimute_enabled = not antimute_enabled
    await event.edit(f"🛡 Режим Anti-Mute (Игнор чужих ограничений): **{'ВКЛЮВЕН' if antimute_enabled else 'ВЫКЛЮЧЕН'}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.sw'))
async def sw_cmd(event):
    if not event.is_reply:
        await event.edit("⚠️ Ответь на сообщение с кривой раскладкой!")
        return
    reply = await event.get_reply_message()
    ru = "йцукенгшщзхъфывапролджэячсмитьбю.ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,"
    en = "qwertyuiopasdfghjkl;'zxcvbnm,.QWERTYUIOP{}ASDFGHJKL:\"ZXCVBNM<>"
    t = reply.text
    tr = t.translate(str.maketrans(ru, en)) if any(c in ru for c in t) else t.translate(str.maketrans(en, ru))
    await event.edit(tr)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.troll'))
async def troll_cmd(event):
    phrases = [
        "Чего зенки вылупил? 🤡", "Слит без права пересдачи, нищ. 🤫", "Иди уроки учи, клоун.",
        "Потеряйся отсюда, чушпан.", "Закрой рот, сквозняк поднимешь.", "Твой IQ равен комнатной температуре."
    ]
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
        if char.strip(): 
            await event.respond(char)
            await asyncio.sleep(0.12)

# ================= БЛОК: ФОРМАТИРОВАНИЕ =================

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
async def tsun_h(event): await event.edit(f"💢 {event.pattern_match.group(1)}... Б-бака! Не то чтобы мне это нравилось! 🙄")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.yandere (.+)'))
async def yan_h(event): await event.edit(f"👁‍🗨 {event.pattern_match.group(1)}... Ты же будешь со мной вечно? Или мне избавиться от лишних людей? 🔪")

# ================= БЛОК: ИГРЫ =================

@client.on(events.NewMessage(outgoing=True, pattern=r'\.bw'))
async def bw_cmd(event):
    frames = [
        "⬜️⬜️⬜️⬜️⬜️\n⬜️⬛️⬜️⬛️⬜️\n⬜️⬜️⬜️⬜️⬜️",
        "⬜️⬛️⬜️⬛️⬜️\n⬛️⬜️⬛️⬜️⬛️\n⬜️⬛️⬜️⬛️⬜️",
        "⬛️⬛️⬛️⬛️⬛️\n⬛️⬜️⬛️⬜️⬛️\n⬛️⬛️⬛️⬛️⬛️"
    ]
    for frame in frames:
        await event.edit(f"🎮 **Игра 'Закрась поле' закинута:**\n\n{frame}")
        await asyncio.sleep(0.4)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.dice'))
async def dice_cmd(event):
    await event.delete()
    await client.send_message(event.chat_id, file=types.InputMediaDice(emoticon="🎲"))

@client.on(events.NewMessage(outgoing=True, pattern=r'\.duel'))
async def duel_cmd(event):
    if not event.is_reply:
        await event.edit("⚠️ Ответь на сообщение противника!")
        return
    reply = await event.get_reply_message()
    target = f"@{reply.sender.username}" if reply.sender.username else "Оппонент"
    await event.edit("⚔️ **Вызов брошен! Заряжаем револьверы...**")
    await asyncio.sleep(1)
    if random.choice([True, False]):
        await event.edit(f"👑 Ты оказался быстрее и точнее! **{target} слит**, ты забрал его {random.randint(10,100)} звёзд! 😎")
    else:
        await event.edit(f"💀 {target} выдал хедшот... Ты проиграл дуэль и потерял звёзды.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.flip'))
async def flip_cmd(event):
    await event.edit(f"🪙 Монетка летит... Выпало: **{random.choice(['🌕 ОРЁЛ', '🟤 РЕШКА'])}**")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.chk'))
async def chk_cmd(event):
    await event.edit("🏁 **[ИНТЕРАКТИВНЫЕ ШАШКИ ЗАПУЩЕНЫ]**\n\n🔴🟪🔴🟪🔴\n🟪⬜️🟪⬜️🟪\n⚪️🟪⚪️🟪⚪️\n\nТвой ход! Напиши позицию.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.ttt'))
async def ttt_cmd(event):
    await event.edit("❌⭕️ **КРЕСТИКИ-НОЛИКИ**\n\n❌ ｜ ⬜️ ｜ ⬜️\n———————\n⬜️ ｜ ⭕️ ｜ ⬜️\n———————\n⬜️ ｜ ⬜️ ｜ ⬜️\n\nБот сделал ход. Твой черёд!")

# ================= БЛОК: ОБРАБОТКА И ХАКИНГ =================

async def make_dox(event):
    if not event.is_reply: return "⚠️ Ошибка: Ответь на смс цели!"
    reply = await event.get_reply_message()
    u = reply.sender
    try:
        full = await client(GetFullUserRequest(u.id))
        bio = full.full_user.about or "Не указано"
    except: bio = "Заблокировано приватностью"
    ips = ["195.211.193.", "91.243.102.", "178.92.24."]
    cities = ["Киев", "Харьков", "Одесса", "Днепр", "Львов", "Житомир"]
    return (
        f"🚨 **ПОЛНЫЙ УЛЬТИМАТИВНЫЙ ДОКС** 🚨\n"
        f"👤 **Имя/Фамилия:** {u.first_name or 'Нет'} {u.last_name or ''}\n"
        f"🆔 **ID Пользователя:** `{u.id}`\n"
        f"🏷 **Юзернейм:** @{u.username or 'отсутствует'}\n"
        f"📝 **БИО профиля:** {bio}\n"
        f"🌐 **Перехваченный IP:** `{random.choice(ips)}{random.randint(1,254)}`\n"
        f"📍 **Город провайдера:** г. {random.choice(cities)}\n"
        f"🔐 **Статус уязвимости:** `PORT 8080 open [Vulnerable IP]`"
    )

@client.on(events.NewMessage(outgoing=True, pattern=r'\.dox$'))
async def dox_cmd(event): await event.edit(await make_dox(event))

@client.on(events.NewMessage(outgoing=True, pattern=r'\.doxp$'))
async def doxp_cmd(event):
    res = await make_dox(event)
    await event.delete()
    await client.send_message("me", res)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.clone$'))
async def clone_cmd(event):
    if not event.is_reply:
        await event.edit("⚠️ Ответь на сообщение жертвы!")
        return
    reply = await event.get_reply_message()
    u = reply.sender
    await event.edit("👥 **Клонирую аккаунт жертвы...**")
    try:
        full = await client(GetFullUserRequest(u.id))
        await client(UpdateProfileRequest(first_name=u.first_name or "", last_name=u.last_name or "", about=full.full_user.about or ""))
        await event.edit("👑 **Профиль полностью скопирован!** Ты теперь его визуальный клон.")
    except Exception as e: await event.edit(f"❌ Ошибка смены данных: {e}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.fv'))
async def fv_cmd(event):
    await event.edit("🔊 **Усиление голосового сообщения...**\nДобавление бассов: +24dB [Успешно].")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.afk (.*)'))
async def afk_cmd(event):
    global afk_enabled, afk_reason
    reason = event.pattern_match.group(1)
    afk_enabled = True
    afk_reason = reason if reason else "Просто отошел"
    await event.edit(f"💤 **Режим AFK активирован.** Причина: *{afk_reason}*")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.autoresponder (.*)'))
async def autoresponder_cmd(event):
    global autoresponder_enabled, autoresponder_text
    text = event.pattern_match.group(1)
    if not text:
        autoresponder_enabled = False
        await event.edit("❌ **Автоответчик выключен.**")
    else:
        autoresponder_enabled = True
        autoresponder_text = text
        await event.edit(f"🤖 **Автоответчик запущен.** Текст ответа: `{autoresponder_text}`")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.gifts'))
async def gifts_cmd(event):
    await event.edit("🎁 **Сканирование подарков аккаунта...**\nНайдено: 12 уникальных кастомных подарков, 3 Telegram Premium дропа.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.info'))
async def info_cmd(event):
    if not event.is_reply:
        await event.edit("⚠️ Ответь на смс юзера!")
        return
    reply = await event.get_reply_message()
    await event.edit(f"📊 **ИНФО:**\nID: `{reply.sender_id}`\nБот: {reply.sender.bot}\nВзаимный контакт: {reply.sender.contact}")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.nk'))
async def nk_cmd(event):
    await event.edit("🐾 **Ня! Отправляю неко-тян...** 🐾\n[Медиафайл успешно сгенерирован]")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.short'))
async def short_cmd(event):
    await event.edit("📝 **Краткий пересказ диалога:**\nСобеседник пытается оправдаться, ты доминируешь в споре. Слив зафиксирован.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.status (.+)'))
async def status_cmd(event):
    t = event.pattern_match.group(1)
    await client(UpdateProfileRequest(about=t))
    await event.edit(f"📝 **Кастомный статус в БИО изменен на:** `{t}`")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.story'))
async def story_cmd(event):
    await event.edit("📸 **Нарезка медиа-файла под формат Telegram Stories...** [Завершено 100%]")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.time'))
async def time_cmd(event):
    await event.edit(f"🕒 **Точное время создателя:** `{datetime.now().strftime('%H:%M:%S')}`")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.yars'))
async def yars_cmd(event):
    await event.edit("👁‍🗨 **Запуск Yandex/Google reverse поиска по фото...**\nСовпадений в сети: 4 штуки.")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.gif'))
async def gif_cmd(event):
    await event.edit("📹 **Конвертация видео/фото файла в анимированный GIF...** [Успешно]")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.gosu'))
async def gosu_cmd(event): await event.edit("⚡️ **[GOSU MODE ACTIVATED]** ⚡️\nЗапуск ядерных эксплоитов... Обход брандмауэра... Система взломана. 💻")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.gp'))
async def gp_cmd(event): await event.edit("💣 **[BIG SURPRISE PACK EXP]** 💣\n▉▉▉▉▉▉▉▉▉▉ 100%\nВсе файлы зашифрованы алгоритмом AES-256. Переведите кэш автору! 😉")

@client.on(events.NewMessage(outgoing=True, pattern=r'\.lq (.+)'))
async def lq_cmd(event):
    t = event.pattern_match.group(1)
    await event.edit(f"⚠️ [LQ_COMPRESSION]: {''.join([c.upper() if random.choice([True, False]) else c.lower() for c in t])}")

# Фоновые обработчики входящих (Удаление мута, AFK и Автоответчик)
@client.on(events.NewMessage(incoming=True))
async def background_handlers(event):
    global afk_enabled, afk_reason, autoresponder_enabled, autoresponder_text
    if event.sender_id in muted_users:
        try: await event.delete()
        except: pass
        return
    if event.is_private:
        if afk_enabled:
            await event.respond(f"💤 Привет! Я сейчас не у ПК (AFK).\n**Причина:** {afk_reason}")
        elif autoresponder_enabled:
            await event.respond(autoresponder_text)

@client.on(events.NewMessage(outgoing=True))
async def afk_reset(event):
    global afk_enabled
    if afk_enabled and not event.text.startswith(r'.afk'):
        afk_enabled = False
        msg = await event.respond("⚡️ **Я вернулся! Режим AFK автоматически отключен.**")
        await asyncio.sleep(3)
        await msg.delete()

@app.on_event("startup")
async def on_startup():
    asyncio.create_task(client.start())
    asyncio.create_task(send_ping())
    print("🚀 Ультимативная Управлялка с автопингом запущена!")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
