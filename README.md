# ⏱️ Jarvis Smart Timer System (for Home Assistant)

This project enables **fully voice-controlled smart timers** using [Home Assistant](https://www.home-assistant.io/), [Gemini](https://ai.google.dev/), and [AppDaemon](https://appdaemon.readthedocs.io/en/latest/). It replicates and expands Alexa-style timers with visible countdowns, spoken confirmations, multi-timer support, and mobile notifications.

---

## 🚀 Features

- ✅ Set timers via voice using natural language
- ✅ Multiple timers with independent tracking (Timer 1, Timer 2)
- ✅ Spoken timer confirmations with chimes
- ✅ Countdown display using [Alexa Timers & Alarms Card](https://github.com/Kethlak/card-alexa-alarms-timers)
- ✅ Gemini extracts minutes and optional labels from speech
- ✅ Mobile push notifications when timers end
- ✅ Optional label fallback (e.g., “5 Minute Timer”)
- ✅ Cancel specific timers by voice (e.g., “Cancel the pizza timer”)
- ✅ Resilient to restarts with persistent state

---

## 🧩 Dependencies

Make sure you have the following set up:

### Required Integrations & Tools

| Tool | Purpose |
|------|---------|
| [Home Assistant](https://www.home-assistant.io/) | Core system |
| [AppDaemon Add-on](https://github.com/hassio-addons/addon-appdaemon) | Python script host |
| [Google Generative AI](https://www.home-assistant.io/integrations/google_generative_ai_conversation/) | LLM for voice parsing |
| [Alexa Timers Card](https://github.com/Kethlak/card-alexa-alarms-timers) | Countdown display |
| [chime_tts](https://github.com/nimroddolev/chime_tts) (custom integration) | Optional chime/speech system |

---

## 🛠️ Setup

### 1. 🧠 Voice Timer Request Automation

Located in `JarvisRequest.yaml`. This listens for timer commands like:

- "Set a 10-minute timer"
- "Start a pizza timer for 5 minutes"

It sends your sentence to Gemini, parses it into structured JSON, and writes a `timerObj` to the first available timer slot.

📦 **Helpers used:**
- `input_text.jarvis_timer_data`
- `input_text.jarvis_timer_data_2`

### 2. 🧠 Python: `jarvis_timer.py` (AppDaemon Script)

Watches `input_text.jarvis_timer_data`, calculates remaining time every 10 seconds, and updates `sensor.jarvis_timer` with:

- `triggerTime`, `remainingTime`
- `sorted_active`, `sorted_all` (for Alexa card)
- Human-readable timestamp for visual display

Second script: `jarvis_timer_2.py` watches `jarvis_timer_data_2`.

📁 AppDaemon config location:
```bash
/config/apps/jarvis_timer.py
/config/apps/jarvis_timer_2.py
