"""
Jarvis Timer – memory-cached, no-flicker version 2025-05-01
"""

import appdaemon.plugins.hass.hassapi as hass
import json, time, datetime


class JarvisTimer(hass.Hass):
    # ──────────────────────────────────────────────────────
    def initialize(self):
        self.helper = "input_text.jarvis_timer_data"
        self.sensor = "sensor.jarvis_timer"

        # Cached timer info (None = no active timer)
        self.timer = None  # dict with trigger_ms, id, label, raw

        # Watch the helper (debounced 0.3 s)
        self.listen_state(self._schedule_parse, self.helper)

        # Heartbeat every second
        self.run_every(self._tick,
                       self.datetime() + datetime.timedelta(seconds=1),
                       1)

        # Initial parse
        self._parse_helper()

    # ──────────────────────────────────────────────────────
    def _schedule_parse(self, *_):
        # Parse after the helper write has fully committed
        self.run_in(lambda *_: self._parse_helper(), 0.3)

    # ──────────────────────────────────────────────────────
    def _parse_helper(self):
        txt = (self.get_state(self.helper) or "").strip()
        if not txt or txt in {"unknown", "unavailable"}:
            self.timer = None
            return

        try:
            data = json.loads(txt)

            # Accept [["id", {...}]] as well
            if isinstance(data, list) and data:
                _, data = data[0]

            trigger_ms = int(float(data.get("triggerTime", 0)))
            if trigger_ms <= 0:
                self.log("Timer JSON missing triggerTime", level="WARNING")
                self.timer = None
                return

            self.timer = {
                "trigger_ms": trigger_ms,
                "id":         data.get("id"),
                "label":      data.get("timerLabel", "Timer"),
                "raw":        data,  # full dict for the Alexa card
            }

        except Exception as err:
            self.log(f"JarvisTimer parse error: {err}", level="WARNING")
            self.timer = None

    # ──────────────────────────────────────────────────────
    def _tick(self, *_):
        # No active timer → publish unknown once per second
        if self.timer is None:
            self.set_state(self.sensor, state="unknown", attributes={})
            return

        # How much time is left?
        now_ms    = int(time.time() * 1000)
        remaining = max(self.timer["trigger_ms"] - now_ms, 0)

        # Treat anything under 1 s as finished
        if remaining <= 1000:
            self.set_state(self.sensor, state="unknown", attributes={})
            self.timer = None
            return

        # Format HH:MM:SS
        secs       = remaining // 1000
        mins, secs = divmod(secs, 60)
        hrs,  mins = divmod(mins, 60)
        state      = f"{hrs:02}:{mins:02}:{secs:02}"

        # Build attributes expected by the Alexa Timers card
        full_dict = dict(self.timer["raw"])  # shallow copy
        full_dict["remainingTime"] = remaining
        sorted_json = str(json.dumps([[self.timer["id"], full_dict]]))

        attrs = {
            "friendly_name": "Jarvis next Timer",
            "status": "ON",
            "total_active": 1,
            "total_all": 1,
            "process_timestamp": datetime.datetime.now().isoformat(),
            "sorted_active": sorted_json,
            "sorted_all":    sorted_json,
            **full_dict,
        }

        # Always write (once per second) to keep HA from marking it stale
        self.set_state(self.sensor, state=state, attributes=attrs)