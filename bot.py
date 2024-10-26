import telebot
from PIL import Image, ImageDraw, ImageFont
import os

# Bot token from BotFather
TOKEN = '8150984568:AAHTVHWojlGVdCskMANxKSQtkAljsamHJ2g'
bot = telebot.TeleBot(TOKEN)

# Define the template and font paths within the 'assets' folder
template_path = os.path.join(os.path.dirname(__file__), "assets", "template.png")
main_font_path = os.path.join(os.path.dirname(__file__), "assets", "Gagalin.otf")  # Main text font
bio_font_path = os.path.join(os.path.dirname(__file__), "assets", "Neon.ttf")  # Bio text font
main_font_size = 100  # Main text font size
bio_font_size = 18  # Smaller font size for bio text

@bot.message_handler(commands=['logo'])
def send_logo(message):
    # Parse the name and bio from the command
    user_text = message.text.split(maxsplit=2)
    if len(user_text) < 3:
        bot.reply_to(message, "Please provide the name and bio. Usage: /logo [Name] [Bio]")
        return

    name = user_text[1]
    bio = user_text[2]

    try:
        # Load the image and fonts
        template_image = Image.open(template_path).convert("RGBA")
        main_font = ImageFont.truetype(main_font_path, main_font_size)
        bio_font = ImageFont.truetype(bio_font_path, bio_font_size)

        # Define text properties
        draw = ImageDraw.Draw(template_image)
        
        # Main logo text properties
        main_text_position = (50, 80)  # Adjust for main text position
        main_text_color = (173, 216, 230)  # Light blue color
        draw.text(main_text_position, name, font=main_font, fill=main_text_color)

        # Bio text properties
        bio_text_position = (95, 200)  # Adjust position below the main text
        bio_text_color = (255, 255, 255)  # White color for bio text
        draw.text(bio_text_position, bio, font=bio_font, fill=bio_text_color)

        # Save the image temporarily
        output_path = os.path.join(os.path.dirname(__file__), "output.png")
        template_image.save(output_path, "PNG")

        # Send the image
        with open(output_path, "rb") as image_file:
            bot.send_photo(message.chat.id, image_file)

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Start the bot
bot.polling()