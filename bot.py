import telebot
from PIL import Image, ImageDraw, ImageFont
import os

# Bot token from BotFather
TOKEN = '8150984568:AAHTVHWojlGVdCskMANxKSQtkAljsamHJ2g'
bot = telebot.TeleBot(TOKEN)

# Define the template and font paths within the 'assets' folder
template_path = os.path.join(os.path.dirname(__file__), "assets", "template.png")
main_font_path = os.path.join(os.path.dirname(__file__), "assets", "Gagalin.otf")
bio_font_path = os.path.join(os.path.dirname(__file__), "assets", "Neon.ttf")

# High-resolution template dimensions (for example, 2x the original size)
output_resolution = (1200, 1200)  # Adjust to fit your design
main_font_size = 280  # Larger font size for higher resolution
bio_font_size = 50

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
        # Load the template and create a high-resolution canvas
        template_image = Image.open(template_path).convert("RGBA")
        template_image = template_image.resize(output_resolution, Image.LANCZOS)
        
        # Load fonts with increased size for higher resolution
        main_font = ImageFont.truetype(main_font_path, main_font_size)
        bio_font = ImageFont.truetype(bio_font_path, bio_font_size)

        # Define text properties
        draw = ImageDraw.Draw(template_image)

        # Main logo text
        main_text_position = (180, 160)  # Adjusted for larger image
        main_text_color = (173, 216, 230)
        draw.text(main_text_position, name, font=main_font, fill=main_text_color)

        # Bio text below main logo text
        bio_text_position = (300, 500)  # Adjusted position for bio
        bio_text_color = (255, 255, 255)
        draw.text(bio_text_position, bio, font=bio_font, fill=bio_text_color)

        # Resize down to original size to simulate anti-aliasing
        final_image = template_image.resize((600, 600), Image.LANCZOS)

        # Save the image temporarily
        output_path = os.path.join(os.path.dirname(__file__), "output.png")
        final_image.save(output_path, "PNG", dpi=(300, 300))  # Set DPI to 300 for quality

        # Send the image
        with open(output_path, "rb") as image_file:
            bot.send_photo(message.chat.id, image_file)

    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

# Start the bot
bot.polling()