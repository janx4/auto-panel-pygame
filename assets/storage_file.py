import pygame as pg
import pyautogui as pag
import webbrowser
import keyboard
import pyperclip as ppc
import time

# ****************************************
# * Author            : Cong Huy         *
# * Date of Execution : Dec 19th, 2020   *
# * Made with love and improving skills  *
# ****************************************

# Variable of window tool, FPS and border size button
WIDTH = 400
HEIGHT = 400
FPS = 60
BORDER_RECT = 3
text = ""

# Color RGB
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (15, 250, 35)
YELLOW = (255, 255, 36)
BLACK = (0, 0, 0)
PURPLE = (245, 17, 203)
color_button1 = (214, 28, 28)
color_button2 = (214, 28, 28)

# Variable of status loop, selection button event, running animations
running = True
action_click_mode = False
stop_click_mode = False
action_spam_mode = False
stop_spam_mode = False
select_button1 = False
select_button2 = False

clicked_run = False
confirmed_choosing = False
selected_button = False

pop_up_info = False
mouse_on_run = False
run_setting = False

i = 0
total_click = 0
mark_button = 0
index_frame = 0
index_bear = 0
index_header = 0
x_click_pos = 0
y_click_pos = 0

# Variable of the button
button1_x = WIDTH // 6
button1_y = HEIGHT // 3
button2_x = WIDTH // 6
button2_y = HEIGHT * 7 // 12
button_width = WIDTH * 4 // 6
button_height = HEIGHT // 6

# The smaller animation_velocity, The faster animation of object !
bear_velocity = 15
header_velocity = 20

pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

# Load icon and background images
icon_image = pg.image.load("assets/others/icon.png")
bg_image = pg.image.load("assets/others/bg.png")
about_us_image = pg.image.load("assets/others/about_us.png")
info_author_image = pg.image.load("assets/others/info_author.png")
button_run_image = pg.image.load("assets/others/button.png")
button_run_select_image = pg.image.load("assets/others/button_click.png")
tick_image = pg.image.load("assets/others/tick_mark.png")
x_image = pg.image.load("assets/others/x_mark.png")
notice_run = pg.image.load("assets/others/notice_run.png")

# Load bear images
animation_bear = []
for i in range(8):
    bear_image = pg.image.load("assets/bear-animation/bear_" + str(i) + ".png")
    animation_bear.append(bear_image)
# Load "Auto Panel" Title Images
animation_header = []
for i in range(3):
    header_image = pg.image.load("assets/header_animation/3d-text-" + str(i) + ".png")
    animation_header.append(header_image)

# Set caption and icon
pg.display.set_caption("Auto Panel by Janx4 v1.0")
pg.display.set_icon(icon_image)
pg.mouse.set_cursor(*pg.cursors.arrow)
# Initialize fonts to write
font = pg.font.SysFont('comicsansms', 35)
font_1 = pg.font.Font("assets/fonts/aloveofthunder.ttf", 22)
text_button1 = font.render("Auto Click", True, WHITE)
text_button2 = font.render("Auto Spam", True, WHITE)
new_text_button1 = font.render("Auto Click", True, RED)
new_text_button2 = font.render("Auto Spam", True, RED)


def draw_button(x, y, width, height, color, content):
    pg.draw.rect(screen, color, (x, y, width, height))
    screen.blit(content, (x + 50, y + 5))


def draw_border(x, y, width, height, color):
    pg.draw.rect(screen, color, (
        x - BORDER_RECT, y - BORDER_RECT, width + BORDER_RECT * 2, height + BORDER_RECT * 2))


def change_color_button(x_pos, y_pos, new_color):
    global color_button1, color_button2
    # If position of the mouse is on the button 1 / button 2, the button's color changes to new color
    if button1_x < x_pos < button1_x + button_width and button1_y < y_pos < button1_y + button_height:
        color_button1 = new_color
    else:
        color_button1 = (214, 28, 28)

    if button2_x < x_pos < button2_x + button_width and button2_y < y_pos < button2_y + button_height:
        color_button2 = new_color
    else:
        color_button2 = (214, 28, 28)
    return color_button1, color_button2


def processing_event(x_pos, y_pos):
    global select_button1, select_button2, running, clicked_run, mouse_on_run
    global confirmed_choosing, run_setting, selected_button, pop_up_info, action_spam_mode, stop_spam_mode

    for event in pg.event.get():
        # Check whether user want to exit the program
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Check whether user click the button to choose it !
                if not selected_button:
                    if button1_x < x_pos < button1_x + button_width and button1_y < y_pos < button1_y + button_height:
                        select_button1 = True
                        select_button2 = False
                    if button2_x < x_pos < button2_x + button_width and button2_y < y_pos < button2_y + button_height:
                        select_button1 = False
                        select_button2 = True
                # Click to open URL of author
                if 0 < x_pos < 40 and 0 < y_pos < 40:
                    webbrowser.open("https://www.facebook.com/janx4/")

                # When user click RUN button
                if 0.6 * WIDTH < x_pos < 0.6 * WIDTH + 150 and 0.7875 * WIDTH < y_pos < 0.7875 * WIDTH + 75 and not run_setting:
                    clicked_run = True
                # When user click X button to cancel mode
                if 0.73 * WIDTH < x_pos < 0.73 * WIDTH + 75 and 0.78 * HEIGHT < y_pos < 0.78 * HEIGHT + 75 and run_setting:
                    clicked_run = False
                    confirmed_choosing = False
                    run_setting = False
                    selected_button = False
                    action_spam_mode = False
                    stop_spam_mode = True

        # Check whether user press any key
        list_select_button = [select_button1, select_button2]
        if event.type == pg.KEYDOWN:
            # Press Space = Click RUN button
            if event.key == pg.K_SPACE and any(list_select_button) and not run_setting:
                clicked_run = True
            # Press ESC = Exit Auto Mode ~ Click X Button
            if event.key == pg.K_ESCAPE and run_setting:
                clicked_run = False
                confirmed_choosing = False
                run_setting = False
                selected_button = False

            # If user doesnt choose any button
            if not selected_button:
                if any(list_select_button):
                    if event.key == pg.K_UP or event.key == pg.K_DOWN:
                        select_button1 = not select_button1
                        select_button2 = not select_button2
                else:
                    # Select button 1 automatically when press any key
                    select_button1 = True

        # Check whether the position of mouse is on the RUN button
        if 0.6 * WIDTH < x_pos < 0.6 * WIDTH + 150 and 0.7875 * WIDTH < y_pos < 0.7875 * WIDTH + 75:
            mouse_on_run = True
        else:
            mouse_on_run = False
        # Check whether the position of mouse is on the About Us image
        if 0 < x_pos < 40 and 0 < y_pos < 40:
            pop_up_info = True
        else:
            pop_up_info = False

    # Draw border button which was selected
    if select_button1:
        draw_border(button1_x, button1_y, button_width, button_height, YELLOW)
        draw_button(button1_x, button1_y, button_width, button_height, GREEN, new_text_button1)
    if select_button2:
        draw_border(button2_x, button2_y, button_width, button_height, YELLOW)
        draw_button(button2_x, button2_y, button_width, button_height, GREEN, new_text_button2)
    return running, clicked_run, mouse_on_run, select_button1, select_button2, confirmed_choosing, run_setting, selected_button, pop_up_info, x_click_pos, y_click_pos, action_spam_mode, stop_spam_mode


def animations():
    global index_frame, index_header, index_bear
    # Increasing index frame and change animation of header, bear
    index_frame += 1
    if index_frame % bear_velocity == 0:
        index_bear += 1
    if index_frame % header_velocity == 0:
        index_header += 1
    # Blit image about us
    screen.blit(about_us_image, (0, 0))
    # Animations of "Auto Panel"
    screen.blit(animation_header[index_header], (WIDTH // 2 - 150, HEIGHT // 7))

    # Pop up when the mouse is on "ABOUT US" image
    if pop_up_info:
        screen.blit(info_author_image, (0.0675 * WIDTH, 0.015 * HEIGHT))
    # Animations of bear
    screen.blit(animation_bear[index_bear], (WIDTH // 2 - 25, HEIGHT * 19 // 24 + 10))
    screen.blit(animation_bear[index_bear], (WIDTH // 6 - 25, HEIGHT * 19 // 24 + 10))
    screen.blit(animation_bear[index_bear], (WIDTH // 3 - 25, HEIGHT * 19 // 24 + 10))
    return index_bear, index_header


def reset_animation_loop():
    global index_bear, index_header
    # If index bear/header equals last element, call back it and set 0 again
    if index_bear >= len(animation_bear) - 1:
        index_bear = 0
    if index_header >= len(animation_header) - 1:
        index_header = 0
    return index_bear, index_header


def execute_command():
    global clicked_run, confirmed_choosing, selected_button, run_setting, text, i
    global x_click_pos, y_click_pos, action_click_mode, stop_click_mode, action_spam_mode, stop_spam_mode

    # Event if user click RUN button
    if clicked_run:
        clicked_run = False
        # If the selected button was button 1
        if select_button1:
            confirmed_choosing = True
            selected_button = True
            run_setting = True
            pag.alert(title="➤ Hướng dẫn sử dụng AUTO CLICK :",
                      text="  Tốc độ phiên bản hiện tại : 15 CPS ( Clicks Per Second )\n  Di chuyển chuột của bạn đến vị trí cần auto và nhấn phím SHIFT để thao tác.\n\t\t( Nhấn ESC để huỷ AUTO CLICK )")
        # If the selected button was button 2
        if select_button2:
            text = pag.prompt(text="☻ Nhập vào text bạn cần spam ☻", title='INPUT', default='')
            if len(str(text)) == 0:
                pag.alert(title="✖ OOPS !!!",
                          text="(✖╭╮✖) Hình như bạn chưa nhập gì cả ! Bạn vui lòng thử lại nhé ! ❀")
            elif text is not None:
                confirmed_choosing = True
                selected_button = True
                run_setting = True
                pag.alert(title="➤ Hướng dẫn AUTO SPAM :",
                          text="Phần mềm sẽ tự động kết thúc mỗi lệnh spam bằng phím ENTER.\n"
                               "1. Di chuyển chuột của bạn vào ô nhập dữ liệu \n"
                               "2. Nhấn SHIFT để bắt đầu AUTO SPAM\n"
                               "➤ LƯU Ý :\n"
                               "\t◉ AUTO SPAM SẼ HOẠT ĐỘNG SAU 1 GIÂY TỪ KHI NHẤN SHIFT !\n"
                               "\t◉ HÃY ĐỊNH DẠNG /id/ ĐỂ ĐƯỢC HIỂU LÀ SỐ THỨ TỰ (1, 2, 3,...) !\n"
                               "\tVD: \"anh hôn em lần thứ /id/\" , \"/id/. Yêu sếp forever\", ...\n\n\t"
                               "      ( Nhấn ESC để huỷ AUTO SPAM )")
            else:
                pass

    # Starting mode by press SHIFT
    if keyboard.is_pressed("shift") and run_setting:
        if select_button1:
            action_click_mode = True
            stop_click_mode = False
            if action_click_mode:
                x_click_pos, y_click_pos = pag.position()
        if select_button2:
            # Time sleep 1 second before running AUTO SPAM
            time.sleep(1)
            action_spam_mode = True
            stop_spam_mode = False
    # Stopping spam mode by press ESC
    if keyboard.is_pressed("esc") and action_click_mode and select_button1:
        action_click_mode = False
        stop_click_mode = True
    if keyboard.is_pressed("esc") and action_spam_mode and select_button2:
        action_spam_mode = False
        stop_spam_mode = True
        i = 0

    # Click mode active !
    if action_click_mode and not stop_click_mode:
        pag.tripleClick(x_click_pos, y_click_pos)
        pag.moveTo(x_click_pos, y_click_pos)
        # Spam mode active !
    if action_spam_mode and not stop_spam_mode:
        time.sleep(0.05)
        temp = text
        text = text.replace("/id/", str(i-1))
        # Copy text and paste to input box automatically
        ppc.copy(text)
        time.sleep(0.1)
        pag.hotkey("ctrl", "v")
        pag.press("enter")
        #
        text = temp
        i += 1

    # If user confirmed then blit x_image on the screen (to turn off mode)
    if confirmed_choosing:
        screen.blit(x_image, (0.73 * WIDTH, 0.78 * HEIGHT))
    # or back to RUN button
    elif mouse_on_run:
        screen.blit(button_run_select_image, (0.6 * WIDTH, 0.7875 * HEIGHT))
        screen.blit(notice_run, (0.6 * WIDTH - 150, 0.7875 * HEIGHT - 45))
    else:
        screen.blit(button_run_image, (0.6 * WIDTH, 0.7875 * HEIGHT))
    return clicked_run, confirmed_choosing, selected_button, run_setting, x_click_pos, y_click_pos, action_click_mode, stop_click_mode, action_spam_mode, stop_spam_mode, text, i


def main_loop():
    # CHECK USER
    # global running
    # check_login = pag.password(text='Enter password !', title='Login as Administrator', default='', mask='*')
    # if check_login != "conghuy.tk":
    #     running = False
    pag.FAILSAFE = False
    while running:
        # Set FPS, get position of the cursor, initialize screen
        clock.tick(FPS)
        screen.fill(GRAY)
        screen.blit(bg_image, (0, 0))
        mouse_x, mouse_y = pg.mouse.get_pos()

        # Draw button 1 and button 2
        draw_button(button1_x, button1_y, button_width, button_height, color_button1, text_button1)
        draw_button(button2_x, button2_y, button_width, button_height, color_button2, text_button2)
        # Change color button if cursor in it
        change_color_button(mouse_x, mouse_y, RED)
        # Process event
        processing_event(mouse_x, mouse_y)
        # Running animation of the bear
        animations()
        # Reset index of list animation
        reset_animation_loop()
        # Execute option command
        execute_command()
        # Update screen
        pg.display.flip()
    pg.quit()


main_loop()
