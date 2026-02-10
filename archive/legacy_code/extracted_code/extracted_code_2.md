# Interdimensional Radio – Gradio UI Design Document

## Overview
The goal of this UI is to present the **magical** experience of talking to multiple
interdimensional characters while hiding all technical complexity.  
The interface is built with **Gradio**, chosen for its rapid prototyping,
Python‑first API, and ability to run entirely in a web browser without exposing a
terminal.

| Area | Primary Goal |
|------|--------------|
| **Character Library** | Browse characters, preview their voice, and drag them into a scene. |
| **Scene Canvas** | Visually arrange up to four characters; provide a voice‑cloning drop‑zone. |
| **Live Chat** | Show a conversation with speaker highlighting, waveform playback, and word‑level sync. |
| **Settings** | Minimal configuration for LLM, TTS, and audio device. |
| **Overall** | Dark‑mode default, clean modern look, mobile‑responsive, no visible terminal. |

---

## 1. Layout & Navigation