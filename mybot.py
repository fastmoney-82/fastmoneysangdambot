import asyncio
import logging
import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# 오류 발생 시 기록을 남기기 위한 설정
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

WELCOME_TEMPLATE = (
    "✨ 패스트머니 방문을 감사드립니다! ✨\n\n"
    "📌 [아래 양식을 채워서 채팅 남겨주시면 확인 후 빠르게 답변 드리겠습니다.]\n"
    "----------------------------------------\n"
    "1. 이름: \n"
    "2. 연락처: \n"
    "3. 신청희망금액: \n"
    "----------------------------------------\n"
    "✍️ 위 양식을 복사하여 @Fastmoney8282 여기로 보내주세요!.\n"
    "문의 사항이 있으시면 언제든 말씀해 주세요!"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_name = update.effective_user.first_name
  greeting = f"안녕하세요, {user_name}님!\n\n{WELCOME_TEMPLATE}"
  await update.message.reply_text(greeting)


async def group_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
  new_members = update.message.new_chat_members
  for member in new_members:
    if member.id != context.bot.id:
      member_name = member.first_name
      greeting = (
          f"👋 {member_name}님이 그룹에 입장하셨습니다!\n\n{WELCOME_TEMPLATE}"
      )
      await update.message.reply_text(greeting)


# --- 1. Render 포트 에러를 막기 위한 가짜 웹 서버 설정 (백그라운드 실행용) ---
app = Flask("")


@app.route("/")
def home():
  return "Bot is running!"


def run_web():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


if __name__ == "__main__":
  # 웹 서버를 별도 스레드로 먼저 띄워서 포트 응답을 즉시 보장합니다.
  threading.Thread(target=run_web).start()

  TOKEN = "8918867103:AAE9_L3UWshp-AHn5nlRZAuF_miWfm5pBC4"

  application = Application.builder().token(TOKEN).build()

  application.add_handler(CommandHandler("start", start_command))
  application.add_handler(
      MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, group_welcome)
  )

  print("환영 인사 자동 발송 봇이 시작되었습니다! 검은 창을 끄지 마세요.")
  application.run_polling()
