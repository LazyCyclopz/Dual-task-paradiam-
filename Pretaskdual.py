from psychopy import visual, core, event, gui
import random
import os
import csv

# Set output results on the Desktop
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "G13-py")
os.makedirs(desktop_path, exist_ok=True)
result_file = os.path.join(desktop_path, "Pre-task_Result.csv")

# Paths to load CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
pre_task_file = os.path.join(desktop_path, "Pre-task words.csv")
training_file = os.path.join(desktop_path, "trainingword.csv")

# Define PM words
pm_words = ["แดง", "เขียว", "น้ำเงิน"]

# Participant ID input dialog
dlg = gui.Dlg(title="Experiment ID")
dlg.addField("Participant ID:")
participant_data = dlg.show()
if not dlg.OK:
    core.quit()
participant_id = participant_data[0]

# Create the display window
win = visual.Window(size=(1920, 1080), color="black", units="pix", fullscr=False)
thai_font = "Cordia New"

# Instructions
instructions = [
    "ในการทดลองนี้ คุณจะเห็นชุดคำปรากฏบนหน้าจอคอมพิวเตอร์...",
    "หากคำที่ขึ้นเป็นคำที่มีความหมายถึง สิ่งมีชีวิต ให้กดปุ่ม 'N'ด้วยนิ้วชี้ข้างขวา",
    "แต่หากเป็น สิ่งไม่มีชีวิต ให้กดปุ่ม 'M'ด้วยนิ้วกลางข้างขวา",
    "หากคุณเห็นคำว่า 'แดง' ให้กดปุ่ม 'Q'ด้วยนิ้วนางข้างซ้าย",
    "หากคุณเห็นคำว่า 'เขียว' ให้กดปุ่ม 'W'ด้วยนิ้วกลางข้างซ้าย", 
    "หากคุณเห็นคำว่า 'น้ำเงิน' ให้กดปุ่ม 'E'ด้วยนิ้วชี้ข้างซ้าย",
    "ต่อจากนี้จะเป็นการฝึกซ้อมก่อนเริ่มการทดลองจริง"
]
for instruction in instructions:
    text_box = visual.TextBox2(win, text=instruction, font=thai_font, color="white", letterHeight=40, size=(1700, 500), alignment="center")
    text_box.draw()
    win.flip()
    event.waitKeys(keyList=["space"])

# Function to load words properly
def load_words(file_path):
    living_words = []
    non_living_words = []
    try:
        with open(file_path, newline='', encoding='TIS-620') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                if len(row) >= 2:
                    living_words.append(row[0].strip())
                    non_living_words.append(row[1].strip())
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        core.quit()
    return living_words, non_living_words

# Load words
task_living, task_non_living = load_words(pre_task_file)
training_living, training_non_living = load_words(training_file)

# Define response keys
ldt_keys = {"n": "living", "m": "non-living"}
pm_keys = {"แดง": "q", "เขียว": "w", "น้ำเงิน": "e"}

# Function to run a trial with retry for incorrect response
def run_trial(word, category, enforce_correction=False):
    if not word or not isinstance(word, str):  # Ensure word is valid
        return None
    
    while True:
        word_stim = visual.TextBox2(win, text=word, font=thai_font, color="white", letterHeight=60, size=(2500, 1000), alignment="center")
        word_stim.draw()
        win.flip()
        timer = core.Clock()
        keys = event.waitKeys(maxWait=3.0, keyList=["n", "m", "q", "w", "e"], timeStamped=timer)
        
        response, rt = (keys[0] if keys else (None, None))
        if category == "PM Cue":
            correct = response == pm_keys.get(word, None)
        else:
            correct = (category == "living" and response == "n") or (category == "non-living" and response == "m")
        
        if correct or not enforce_correction:
            break
        
        feedback = visual.TextBox2(win, text="กดผิด! ลองใหม่", font=thai_font, color="red", letterHeight=60, size=(2500, 1000), alignment="center")
        feedback.draw()
        win.flip()
        core.wait(1.0)
    
    win.flip()
    core.wait(1.0)
    return {"participant_id": participant_id, "word": word, "category": category, "response": response, "reaction_time": rt, "correct": correct}

# Training phase
training_samples = random.sample(training_living, 4) + random.sample(training_non_living, 4)
training_pm = random.sample(pm_words, min(2, len(pm_words)))
all_training = [(word, "living") for word in training_samples[:4]] + [(word, "non-living") for word in training_samples[4:]] + [(pm, "PM Cue") for pm in training_pm]
random.shuffle(all_training)
results = []

for word, category in all_training:
    trial_result = run_trial(word, category, enforce_correction=True)
    if trial_result:
        results.append(trial_result)

# Show instruction before real task
text_box = visual.TextBox2(win, text="ต่อจากนี้จะเป็นการทำงานจริงขอให้ตั้งใจทำให้ถูกต้องและเร็วที่สุดเท่าที่ทำได้", font=thai_font, color="white", letterHeight=40, size=(1700, 500), alignment="center")
text_box.draw()
win.flip()
event.waitKeys(keyList=["space"])

# Main task processing
random.shuffle(task_living)
random.shuffle(task_non_living)
ldt_trials = [(word, "living") for word in task_living] + [(word, "non-living") for word in task_non_living]
random.shuffle(ldt_trials)

# Insert PM cues randomly every 8-10 LDT trials
pmt_trials = random.choices(pm_words, k=12)
final_trials = []
ldt_count = 0
while ldt_trials:
    final_trials.append(ldt_trials.pop(0))
    ldt_count += 1
    if ldt_count >= random.randint(8, 10) and pmt_trials:
        final_trials.append((pmt_trials.pop(0), "PM Cue"))
        ldt_count = 0

for word, category in final_trials:
    trial_result = run_trial(word, category, enforce_correction=False)
    if trial_result:
        results.append(trial_result)

# Save results to CSV
with open(result_file, "w", newline="", encoding='TIS-620') as file:
    writer = csv.DictWriter(file, fieldnames=["participant_id", "word", "category", "response", "reaction_time", "correct"])
    writer.writeheader()
    writer.writerows(results)

win.close()
core.quit()
print(f"ผลลัพธ์ถูกบันทึกที่: {result_file}")