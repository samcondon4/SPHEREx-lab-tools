---
layout: post
title:  "Test and Calibration Lab Software Setup"
date:   2021-04-01
categories: [hardware, drivers, stepper-motors, python, software-installation]
---

This section details the setup of the *SPHEREx Test and Calibration Lab Software Suite*. One set of tool(s) has been developed for focus calibration while another has been developed for spectral calibration. Separate setup instructions are provided for each tool set. Before beginning setup, ensure that the following prerequisites have been met:

## Prerequisites
- Windows 10 operating system
- Python 3.8 installed via anaconda: https://www.anaconda.com/products/individual
- Clone the SPHEREx-lab-tools repository to local machine

## Focus Calibration
The focus calibration setup involves the following *software controlled* instruments; each instrument contains its own set of drivers:

- Anaheim Automation DPY50601 stepper motor controller.
- FLIR FLEA3 GigE camera

## Spectral Calibration
Instruments in the spectral calibration setup that are software controlled are given below:

- Oriel Cornerstone 260 monochromator with filter wheel
- NDF filter wheel
- Coherent USB Power Meter

### Driver Installation
#### Oriel Cornerstone 260 monochromator with filter wheel
1. Within the cloned SPHEREx-lab-tools repository, navigate to *./SPHEREx-Calibration-Automation/drivers/Monochromator/MonoUtility5.0.4/*
2. Double click on *setup.exe* to execute the installer for Mono Utility. This is the stock software that Oriel provides to control the Monochromator. While this software will not actually be used, the necessary drivers for USB communication w/ the monochromator are automatically included in this installation.
3. Plug in the power cable to the monochromator and turn the device on. You should audibly hear the device performing its homing operation. Wait until this operation completes before connecting the monochromator to the lab computer.
4. Connect USB cable between monochromator and lab computer and open the newly installed Mono Utility software. We will quickly verify that the drivers were installed properly. Start Mono Utility and match the configuration parameters with our monochromator setup (*model* = Cornerstone 260, *connection* = USB, *# gratings* = 3). Verify that after selecting the green check, the Mono Utility software successfully establishes a communication channel with the monochromator. This verification can be done simply by changing the *Present Wavelength* in the software and ensuring no errors pop up.
