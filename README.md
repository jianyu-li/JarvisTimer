# ⏱️ Jarvis Smart Timer System (for Home Assistant)

This project enables **fully voice-controlled smart timers** using [Home Assistant](https://www.home-assistant.io/), [Gemini](https://www.home-assistant.io/integrations/google_generative_ai_conversation/), and [AppDaemon](https://github.com/hassio-addons/addon-appdaemon). It replicates and expands Alexa-style timers with visible countdowns, spoken confirmations, multi-timer support, and mobile notifications.

---

## 🚀 Features

- ✅ Set timers via voice using natural language
- ✅ Multiple timers with independent tracking (Timer 1, Timer 2)
- ✅ Spoken timer confirmations with chimes
- ✅ Countdown display using [Alexa Timers & Alarms Card](https://github.com/Kethlak/card-alexa-alarms-timers) or [Simple Timer Card](https://github.com/eyalgal/simple-timer-card)
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
| [Alexa Timers Card](https://github.com/Kethlak/card-alexa-alarms-timers) or [Simple Timer Card](https://github.com/eyalgal/simple-timer-card) | Countdown display |
| [chime_tts](https://github.com/nimroddolev/chime_tts) | Optional chime/speech system |

> [!WARNING]
> **Important Version Callout:** If using the **Alexa Timers & Alarms Card**, this project currently only works with **version 1.3**. Please ensure you are using [v1.3](https://github.com/Kethlak/card-alexa-alarms-timers/releases/tag/v1.3). Alternatively, the project is fully compatible with the [Simple Timer Card](https://github.com/eyalgal/simple-timer-card).

---

## 🛠️ Setup

### 1. 🧠 Voice Timer Request Automation

Located in `JarvisRequest.yaml`. This listens for timer commands like:

- "Set a 10-minute timer"
- "Start a pizza timer for 5 minutes"

It sends your sentence to Gemini, parses it into structured JSON, and writes a `timerObj` to the first available timer slot.

📦 **Helpers used:**
Be sure to have these helpers created and set maximum length to 5000. 
- `input_text.jarvis_timer_data`
- `input_text.jarvis_timer_data_2`

### OPTIONAL
Appdaemon initializes the sensors a little late after start up so if you have any helpers that reference these sensors they will break on startup. You can pre-initialize the sensors by adding the sensors.yaml code to your config. 

Also, the internal timer on the voice PE sometimes hijacks this automation, I've had better luck turning off "Prefer handling commands locally" in your LLM settings. 

### 2. 🧠 Python: `jarvis_timer.py` (AppDaemon Script)

Watches `input_text.jarvis_timer_data`, calculates remaining time every second, and updates `sensor.jarvis_timer` with:

- `triggerTime`, `remainingTime`
- `sorted_active`, `sorted_all` (for Alexa card)
- Human-readable timestamp for visual display

Second script: `jarvis_timer_2.py` watches `jarvis_timer_data_2`.

### 3. Canceling Timers
Use `CancelSpecificTimer.yaml` (to cancel one of the active timers by name) and `CancelAllTimers.yaml` to cancel all active timers. These basically clear out the data helpers. 

### 4. Timer Done Notification
`TimerEnd.yaml` will send a notification to your homepod and phones when the timer completes. Be sure to update the actions and entities to match your environment.

📁 AppDaemon config location:
```bash
/APPDAEMONPARENTFOLDER/apps/jarvis_timer.py
/APPDAEMONPARENTFOLDER/apps/jarvis_timer_2.py
