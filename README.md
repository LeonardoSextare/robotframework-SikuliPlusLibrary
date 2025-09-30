# SikuliPlusLibrary

## About the Project

The **SikuliPlusLibrary** is a library for Robot Framework that extends the [SikuliLibrary](https://github.com/rainmanwy/robotframework-sikulilibrary) for GUI test automation through image recognition. It provides additional GUI automation functionalities not covered by the original SikuliLibrary, using only an instance of SikuliLibrary without modifying its code.

## Minimum Viable Product (MVP)

This project is currently in its MVP phase, with a primary focus on the computer vision module (`vision.py`). The goal is to establish a solid foundation for future expansions, implementing essential visual recognition functionalities.

## Objectives Checklist

### Current Objectives (MVP)
- [ ] Implement solid foundation for future expansion
- [ ] Implement computer vision functionalities (vision.py)
  - [ ] Temporary ROI
  - [ ] Temporary Similarity
  - [ ] Highlight on found images
- [ ] Initial functions:
  - [ ] Wait Until Image Appears
  - [ ] Wait One of Multiple Images Appears
  - [ ] Wait Until Multiple Images Appear
- [ ] Implement possibility to choose target screen (multi-monitor)

### Future Plans
- [ ] Improved Error and Exception Handling
- [ ] Mouse module (mouse.py)
- [ ] Keyboard module (keyboard.py)
- [ ] Support for multiple languages (Keywords, Docstrings, Localized error messages)
- [ ] Support for global configuration via:
  - [ ] Environment variables
  - [ ] Configuration file (TOML)
  - [ ] Pyproject.toml
  - [ ] Arguments in the library import in Robot Framework
- [ ] Automated test coverage (unit and integration)
- [ ] Test coverage in Robot Framework environment
- [ ] Complete documentation with libdoc
