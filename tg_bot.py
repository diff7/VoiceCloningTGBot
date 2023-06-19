import os
import uuid
import telebot
from artist import VoiceArtist
from omegaconf import OmegaConf as omg 


token = os.environ['TG_TOKEN']
bot = telebot.TeleBot(token)

cfg = omg.load('./config.yaml')
artist = VoiceArtist(cfg, CUDA=False, sample_rate=16000)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True, True)
keyboard1.row("случайный", "ввести текст","загрузить голос")

os.makedirs('./voice/', exist_ok=True)
os.makedirs('./ready/', exist_ok=True)

@bot.message_handler(commands = ['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Ты можешь сгенерировать голос из текста (только на английском) или поменять спикера. /start\n', reply_markup = keyboard1)

@bot.message_handler(content_types = ['text'])
def send_voice(message):
    if message.text == 'случайный':
        artist.set_random_speaker()
        generate_audio(message, duty=True)
        bot.send_message(message.chat.id, 'случайный голос сгененрирован, пример голоса выше', reply_markup = keyboard1)
        
    if message.text == "ввести текст":
        bot.send_message(message.chat.id, 'Введите текст на английском')
        bot.register_next_step_handler(message, generate_audio)
        
    
    if message.text == "загрузить голос":
        bot.send_message(message.chat.id, 'Запишите свой голос')
        bot.register_next_step_handler(message, voice_processing)
        
        
def generate_audio(message, duty=False):
    if duty:
        signal = artist.generate("That's how I sound now")
    else:        
        signal = artist.generate(message.text)
    artist.ap.save_wav(signal, './temp.wav')     
    with open('./temp.wav', 'rb') as f:
        audio = f.read()
        bot.send_audio(message.chat.id, audio,message.text )
    os.remove('./temp.wav')
    if not duty:
        bot.send_message(message.chat.id, 'готово' ,reply_markup = keyboard1)
    # bot.send_chat_action(message.from_user.id, 'upload_audio')
    # bot.send_audio(message.from_userid, audio)
    # audio.close()
    
    
@bot.message_handler(content_types=['voice'])
def voice_processing(message):
    filename = str(uuid.uuid4())
    file_name_full="./voice/"+filename+".ogg"
    file_name_full_converted="./ready/"+filename+".wav"
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name_full, 'wb') as new_file:
        new_file.write(downloaded_file)
    os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
    artist.set_speaker_identity(file_name_full_converted)
    os.remove(file_name_full)
    os.remove(file_name_full_converted)
    bot.send_message(message.chat.id, 'Используем ваш голос, можете вводить текст',reply_markup = keyboard1)


bot.polling()