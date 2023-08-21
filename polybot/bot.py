import telebot
from loguru import logger
import os
import time
from telebot.types import InputFile
from polybot import img_proc
from polybot.img_proc import Img


class Bot:

    def __init__(self, token, telegram_chat_url):
        # create a new instance of the TeleBot class.
        # all communication with Telegram servers are done using self.telegram_bot_client
        self.telegram_bot_client = telebot.TeleBot(token)

        # remove any existing webhooks configured in Telegram servers
        self.telegram_bot_client.remove_webhook()
        time.sleep(0.5)

        # set the webhook URL
        self.telegram_bot_client.set_webhook(url=f'{telegram_chat_url}/{token}/', timeout=60)

        logger.info(f'Telegram Bot information\n\n{self.telegram_bot_client.get_me()}')

    def send_text(self, chat_id, text):
        self.telegram_bot_client.send_message(chat_id, text)

    def send_text_with_quote(self, chat_id, text, quoted_msg_id):
        self.telegram_bot_client.send_message(chat_id, text, reply_to_message_id=quoted_msg_id)

    def is_current_msg_photo(self, msg):
        return 'photo' in msg

    def download_user_photo(self, msg):
        """
        Downloads the photos that sent to the Bot to `photos` directory (should be existed)
        :return:
        """
        if not self.is_current_msg_photo(msg):
            raise RuntimeError(f'Message content of type \'photo\' expected')


        file_info = self.telegram_bot_client.get_file(msg['photo'][-1]['file_id'])
        data = self.telegram_bot_client.download_file(file_info.file_path)
        folder_name = file_info.file_path.split('/')[0]

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        with open(file_info.file_path, 'wb') as photo:
            photo.write(data)

        return file_info.file_path

    def send_photo(self, chat_id, img_path):
        if not os.path.exists(img_path):
            raise RuntimeError("Image path doesn't exist")

        self.telegram_bot_client.send_photo(
            chat_id,
            InputFile(img_path)
        )

    def handle_message(self, msg):
        """Bot Main message handler"""
        logger.info(f'Incoming message: {msg}')
        self.send_text(msg['chat']['id'], f'Your original message: {msg["text"]}')


class QuoteBot(Bot):
    def handle_message(self, msg):
        logger.info(f'Incoming message: {msg}')

        if msg["text"] != 'Please don\'t quote me':
            self.send_text_with_quote(msg['chat']['id'], msg["text"], quoted_msg_id=msg["message_id"])


class ImageProcessingBot(Bot):
    def imag_filters(self, path, msg):
            other_img= Img(path)
            img = Img(path)

            if 'caption' in msg:
                if msg['caption'] == 'Salt and paper':
                    img.salt_n_pepper()
                    new_path = img.save_img()
                    time.sleep(0.5)
                    Bot.send_photo(self, msg['chat']['id'], img_path=new_path)
                    time.sleep(2)
                    #self.delet_content()
                elif msg['caption'] == 'Concat':
                    if 'media_group_id' in msg:
                        img.concat(other_img)
                        new_path = img.save_img()
                        time.sleep(0.5)
                        Bot.send_photo(self, msg['chat']['id'], img_path=new_path)
                        time.sleep(2)
                        pass
                    else:
                        self.send_text(msg['chat']['id'], text='there is one image, try with another image')
                    #self.delet_content()
                elif msg['caption'] == 'Segment':
                    img.segment()
                    new_path = img.save_img()
                    time.sleep(1)
                    Bot.send_photo(self, msg['chat']['id'], img_path=new_path)
                    time.sleep(3)
                    #self.delet_content()
                elif msg['caption'] == 'Blur':
                    img.blur()
                    new_path = img.save_img()
                    time.sleep(0.5)
                    Bot.send_photo(self, msg['chat']['id'], img_path= new_path)
                    time.sleep(2)
                    #self.delet_content()
                elif msg['caption'] == 'Contour':
                    img.contour()
                    new_path = img.save_img()
                    time.sleep(0.5)
                    Bot.send_photo(self, msg['chat']['id'], img_path=new_path)
                    time.sleep(2)
                    #self.delet_content()
                else:
                    self.send_text(msg['chat']['id'], text='I don`t know this filter, try these one: Salt and paper, Concat, Segment, Blur, contour' )



    def handle_message(self, msg):

        if self.is_current_msg_photo(msg) == True:
            if 'caption' in msg:
                self.send_text(msg['chat']['id'], text='thank you')
                self.send_text(msg['chat']['id'], text='a few moment')
                time.sleep(1.0)
                logger.info(f'Incoming message: {msg} ')
                filename = self.download_user_photo(msg)
                #self.imag_filters('/home/orb/Ex_Course/ImageProcessingService/polybot/{filename}'.format(filename= filename), msg)
                self.imag_filters(
                    filename, msg)
            else:
                logger.info(f'Incoming message: {msg} ')
                self.send_text(msg['chat']['id'], text='Please send me again, this time try this filters: salt_n_paper, concat, segment, Blur')

        else:
            self.send_text(msg['chat']['id'], text='Hi, send me a photo please')



    def delet_content(self):

        dir = '/home/orb/Ex_Course/ImageProcessingService/polybot/photos'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))













