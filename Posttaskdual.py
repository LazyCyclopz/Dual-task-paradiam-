from psychopy import visual, core, event, gui
import random
import os
import csv

# Set output results on the Desktop for Post-task
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "G13-py")
os.makedirs(desktop_path, exist_ok=True)
result_file = os.path.join(desktop_path, "Post-task_Result.csv")

# Paths to load CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
post_task_file = os.path.join(desktop_path, "Post-task words.csv")

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

# Instructions (no mention of training)
instructions = [
    "ขั้นต่อไปขอให้คุณทำงานตัดสินคำว่าคำที่ขึ้นมา(สิ่งมีชีวิตหรือไม่มีชีวิต) ด้วยวิธีการที่ได้แจ้งไว้ก่อนหน้า"
]
for instruction in instructions:
    text_box = visual.TextBox2(win, text=instruction, font=thai_font, color="white", letterHeight=40, size=(1700, 500), alignment="center")
    text_box.draw()
    win.flip()
    event.waitKeys(keyList=["space"])

# Function to load words from CSV
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

# Load Post-task words
task_living, task_non_living = load_words(post_task_file)

# Define response keys
ldt_keys = {"n": "living", "m": "non-living"}
pm_keys = ["q", "w", "e"]  # PM cues now use Q, W, E
pm_words = ["น้ำเงิน", "แดง", "เขียว"]

# Function to run a trial
def run_trial(word, category):
    if not word or not isinstance(word, str):
        return None
    
    word_stim = visual.TextBox2(win, text=word, font=thai_font, color="white", letterHeight=60, size=(2500, 1000), alignment="center")
    word_stim.draw()
    win.flip()
    
    timer = core.Clock()
    keys = event.waitKeys(maxWait=3.0, keyList=["n", "m", "q", "w", "e"], timeStamped=timer)
    
    response, rt = (keys[0] if keys else (None, None))
    correct = (category == "living" and response == "n") or \
              (category == "non-living" and response == "m") or \
              (category == "PM Cue" and response in pm_keys)
    
    win.flip()
    core.wait(1.0)
    
    return {
        "participant_id": participant_id,
        "word": word,
        "category": category,
        "response": response,
        "reaction_time": rt,
        "correct": correct
    }

# Show instruction before real task
text_box = visual.TextBox2(win, text="ต่อจากนี้จะเป็นการทำงานจริง ขอให้ตั้งใจทำให้ถูกต้องและเร็วที่สุดเท่าที่ทำได้", font=thai_font, color="white", letterHeight=40, size=(1700, 500), alignment="center")
text_box.draw()
win.flip()
event.waitKeys(keyList=["space"])

# Main task trial creation
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

# Run the main experiment trials
results = []
for word, category in final_trials:
    trial_result = run_trial(word, category)
    if trial_result:
        results.append(trial_result)

# Save results to CSV
with open(result_file, "w", newline='', encoding='TIS-620') as file:
    writer = csv.DictWriter(file, fieldnames=[
        "participant_id",
        "word",
        "category",
        "response",
        "reaction_time",
        "correct"
    ])
    writer.writeheader()
    writer.writerows(results)

win.close()
core.quit()
print(f"ผลลัพธ์ถูกบันทึกที่: {result_file}")