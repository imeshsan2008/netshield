# 🛡️ NetShield – Adobe Internet Access Manager

**NetShield** is a lightweight desktop application that allows you to block or allow internet access for Adobe software like Photoshop, Illustrator, and InDesign using Windows Firewall rules. It's built with Python and `ttkbootstrap`, featuring a modern UI and real-time status display.

---

## 🎯 Features

- ✅ Auto-detects Adobe app installations from both `Program Files` and `Program Files (x86)`
- 🔒 Blocks or unblocks **inbound and outbound** internet access
- 🧠 Displays **Blocked / Allowed** status for each app
- 🔁 Manual "Refresh Status" button
- 🎨 Stylish GUI using `ttkbootstrap` (Tkinter-based theme system)
- 💡 No background services – fully user-controlled

---

## 📷 Screenshot

![NetShield Screenshot](https://github.com/imeshsan2008/netshield/blob/main/Ui.png?raw=true)

<br>
📸 Modern UI with real-time firewall status

---

## 📦 Requirements

- **Operating System**: Windows 10 or 11
- **Python**: Version 3.8 or higher
- **Permissions**: Must be run as Administrator (required to modify firewall rules)

---

## 🧪 Install Dependencies

Make sure Python is installed. Then open Command Prompt or PowerShell and run:

```bash
pip install ttkbootstrap

