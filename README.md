# Dual-Task Paradigm for Prospective Memory Research (Thai language version)
# Overview
This repository contains a Python implementation of a Dual-task paradigm designed to assess Prospective Memory (PM) performance.
The paradigm combines:

Ongoing Task: A semantic decision task (Living vs. Non-living objects)

Prospective Memory Task: Detection of predefined PM cue words that require a different response

This version is specifically developed for Thai-speaking participants, using Thai lexical stimuli and Thai font support via PsychoPy.

โค้ดชุดนี้เป็นการพัฒนา Dual-task paradigm สำหรับการศึกษาความสามารถด้าน Prospective Memory (PM)
โดยผสานงาน 2 ประเภทเข้าด้วยกัน ได้แก่

Ongoing task: งานตัดสินเชิงความหมาย (สิ่งมีชีวิต / สิ่งไม่มีชีวิต)

Prospective Memory task: การตรวจจับคำเป้าหมาย (PM cues) ที่ต้องตอบสนองด้วยปุ่มเฉพาะ

ระบบนี้ถูกออกแบบมาเพื่อใช้กับ กลุ่มประชากรที่ใช้ภาษาไทยเป็นหลัก โดยรองรับคำศัพท์ภาษาไทยและฟอนต์ภาษาไทยผ่าน PsychoPy

---

Objective Use
This paradigm is suitable for research on:

  Event-based prospective memory

  Cognitive load and attentional control

  Dual-task interference

  Thai-language cognitive experiments

เครื่องมือนี้เหมาะสำหรับการวิจัยด้าน:

  Prospective memory แบบ event-based

  ภาระทางปัญญาและความสนใจ

  ผลของ dual-task interference

  การทดลองทางจิตวิทยาในประชากรภาษาไทย

---

# 1. Pre-task (Training + Main Dual Task)

Script: Pretaskdual.py
The pre-task phase consists of:

**Instruction phase (Thai language)
**
Training phase with feedback and enforced correction

Main dual-task phase without corrective feedback

Participants perform a semantic decision task while simultaneously monitoring for PM cue words.

ระยะ Pre-task ประกอบด้วย

การแสดงคำสั่งการทดลอง (ภาษาไทย)

ช่วงฝึกซ้อม (training) พร้อม feedback และบังคับแก้ไขเมื่อกดผิด

ช่วงการทดลองจริงแบบ dual-task (ไม่มี feedback)

ผู้เข้าร่วมต้องทำงานตัดสินคำ (ongoing task) ไปพร้อมกับการเฝ้ารอคำ PM (prospective memory task)

---

# 2. Post-task (PM Retrieval Under Cognitive Load)

Script: Posttaskdual.py

English

The post-task phase evaluates PM performance without training or reminders.
Participants are required to:

Perform the same semantic decision task

Detect PM cues based on previously learned rules

This phase reflects retrospective + prospective components of PM.

ระยะ Post-task ใช้เพื่อประเมินความสามารถด้าน PM โดยไม่มีการฝึกหรือทบทวนกติกา
ผู้เข้าร่วมต้อง:

ทำงาน ongoing task เช่นเดิม

ตรวจจับ PM cues จากกติกาที่เรียนรู้ไปแล้ว

ระยะนี้สะท้อนทั้ง retrospective memory และ prospective component ของ PM

---

# Task Logic (Dual-Task Mechanism)
Words appear one at a time at the center of the screen

Participants must respond within 3 seconds

Two concurrent rules apply:
Task Type	Stimulus	Response
Ongoing Task	Living object	N
Ongoing Task	Non-living object	M
PM Cue	“แดง”	Q
PM Cue	“เขียว”	W
PM Cue	“น้ำเงิน”	E

PM cues are inserted randomly every 8–10 ongoing trials, creating sustained attentional demands.

คำศัพท์จะแสดงทีละคำตรงกลางหน้าจอ

ผู้เข้าร่วมต้องตอบภายใน 3 วินาที

มีเงื่อนไขการตอบสนอง 2 ระบบพร้อมกัน

ประเภทงาน	สิ่งเร้า	ปุ่มตอบ
Ongoing task	สิ่งมีชีวิต	N
Ongoing task	สิ่งไม่มีชีวิต	M
PM cue	“แดง”	Q
PM cue	“เขียว”	W
PM cue	“น้ำเงิน”	E

คำ PM จะถูกแทรกแบบสุ่มทุก 8–10 trial เพื่อเพิ่มภาระด้านความสนใจ (attentional load)

---

# Word Stimuli Files (CSV)
All word lists are stored as CSV files encoded in TIS-620 for Thai compatibility.

File	Description
trainingword.csv	Training words (Living / Non-living)
Pre-task words.csv	Main task words (Pre-task)
Post-task words.csv	Main task words (Post-task)

Each file contains two columns:

Column 1: Living objects

Column 2: Non-living objects

ไฟล์คำศัพท์ทั้งหมดอยู่ในรูปแบบ CSV และเข้ารหัสแบบ TIS-620 เพื่อรองรับภาษาไทย

ไฟล์	รายละเอียด
trainingword.csv	คำสำหรับช่วงฝึก
Pre-task words.csv	คำสำหรับ Pre-task
Post-task words.csv	คำสำหรับ Post-task

แต่ละไฟล์มี 2 คอลัมน์:

คอลัมน์ที่ 1: สิ่งมีชีวิต

คอลัมน์ที่ 2: สิ่งไม่มีชีวิต

---

# Output Data
Results are automatically saved to: Desktop/G13-py/ # the file name is editable
Each CSV output includes:

participant_id

word

category (living / non-living / PM Cue)

response

reaction_time

correctness

ผลการทดลองจะถูกบันทึกอัตโนมัติที่: Desktop/G13-py/ # สามารถเปลี่ยนชื่อไฟล์ได้
โดยข้อมูลที่บันทึกประกอบด้วย:

รหัสผู้เข้าร่วม

คำที่แสดง

ประเภทงาน

ปุ่มที่กด

เวลาในการตอบ

ความถูกต้อง

---


