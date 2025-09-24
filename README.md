# SikuliPlusLibrary

[![Version](https://img.shields.io/pypi/v/sikulipluslibrary.svg?label=version&style=flat-square)](https://pypi.org/project/sikulipluslibrary/)
[![License](https://img.shields.io/github/license/leonardosextare/sikulipluslibrary.svg?style=flat-square)](LICENSE)

Wrapper for [SikuliLibrary](https://github.com/rainmanwy/robotframework-sikulilibrary) in **Robot Framework**, bringing:
- ✅ Simplified configuration management
- ✅ Enhanced visual feedback (automatic highlight)
- ✅ More keywords and extra parameters for greater flexibility

---

## 📦 Installation

```bash
pip install sikulipluslibrary
```

### 🔗 Dependencies
- [Robot Framework](https://robotframework.org/)
- [robotframework-sikulilibrary](https://github.com/rainmanwy/robotframework-sikulilibrary)  
  - **Requires the Java SDK (JDK)** to be installed and properly configured.

---

## 📖 Documentation
[👉 Access here](url)

---

## 🚀 Usage

Suite example:
```robot
*** Settings ***
Library     SikuliPlusLibrary  similarity=0.85

*** Test Cases ***
Test Vision
    Wait Until Image Appear    ${IMAGES}\\exemple_button.png
    Wait Until Image Appear    ${IMAGES}\\exemple_button_2.png    10    similarity=0.75
    Wait Until Image Appear    ${IMAGES}\\especific_field.png     roi=${IMAGES}\\especific_modal.png
```

---

## ✨ Main Features
- 📌 **New Keywords** → more power for visual recognition
- ⚙️ **Additional parameters** → `similarity` and `roi` directly in the commands
- 🌍 **Global configuration management** via *Library Arguments* and environment variables
- 🎯 **Automatic highlight** → immediate visual feedback on the located elements

---

### 👀 Highlight Example
![example_highlight](https://github.com/user-attachments/assets/85432a06-c576-4168-ad07-b6cdd2b9c4d4)

---

### 🔧 In Development
- Improved handling of **keyword names**, **docstrings**, and **exceptions**
- Support for a **dedicated configuration file** (`sikuliplus.toml`)
