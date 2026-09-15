import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ChatMemberHandler, filters, ContextTypes

# 오류 발생 시 검은 창에 기록을 남기기 위한 기본 설정
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ========================================================
# 📢 여기에 내가 자동으로 보내고 싶은 양식 문구를 작성하세요!
# \n 은 줄바꿈(엔터)을 의미합니다. 자유롭게 수정해 보세요.
# ========================================================
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

# 상황 1: 사용자가 봇에게 처음 와서 [시작(/start)]을 눌렀을 때 작동하는 함수
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 메시지를 보낸 사람의 이름을 가져와 인사말에 섞어 보냅니다.
    user_name = update.effective_user.first_name
    greeting = f"안녕하세요, {user_name}님!\n\n{WELCOME_TEMPLATE}"
    await update.message.reply_text(greeting)

# 상황 2: 단톡방(그룹방)에 새로운 사람이 입장했을 때 감지하여 작동하는 함수
async def group_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 새롭게 들어온 멤버들의 목록을 가져옵니다.
    new_members = update.message.new_chat_members
    
    for member in new_members:
        # 새로 들어온 사람이 '봇 자신'이 아닐 때만 웰컴 메시지를 보냅니다.
        if member.id != context.bot.id:
            member_name = member.first_name
            greeting = f"👋 {member_name}님이 그룹에 입장하셨습니다!\n\n{WELCOME_TEMPLATE}"
            await update.message.reply_text(greeting)

if __name__ == '__main__':
    # ⚠️ 중요: 본인의 실제 텔레그램 봇 토큰을 입력하세요.
    TOKEN = "8918867103:AAE9_L3UWshp-AHn5nlRZAuF_miWfm5pBC4"
    
    # 봇 빌드 및 시작 설정
    application = Application.builder().token(TOKEN).build()
    
    # 1. 1:1 대화방용 /start 명령어 연결
    application.add_handler(CommandHandler("start", start_command))
    
    # 2. 단톡방용 새 멤버 입장 이벤트 연결
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, group_welcome))
    
    # 봇 가동
    print("환영 인사 자동 발송 봇이 시작되었습니다! 검은 창을 끄지 마세요.")
    application.run_polling()
