# About

1. `Fvsion`, pronounced `Fusion` is a quick bundle of `FastAPI` + `Vite and Vue` + `Stable Diffusion` with async first design.
1. Built on top of [electron-vite-vue-fastapi boilerplate](https://github.com/Hafiidz/electron-vite-vue-fastapi).

![image](https://user-images.githubusercontent.com/3688500/195201878-45f72826-f784-41c7-b152-95da9f736724.png)

<!-- ![image](https://user-images.githubusercontent.com/3688500/195201501-6d08280a-7be0-4f89-9d52-54f95e7eb6b5.png) -->

# Features & Motivation

1. Independent frontend and backend, choose what you need and as you need.
1. Image generation is sent asynchronously to the fastAPI engine, allowing for automatic queue.
1. Flexible api modules to allow ease of use to add your own or publically shared modules, without interference with UI.
1. Integration with Node for faster prototyping.
1. Versatile UI in Vue & Electron.
1. Cross platform features incoming via Electron and packaged pyInstaller (coming soon).

# Beginner Friendly Installation for Windows

0. First, if you have some programming background, it is highly recommended to follow [development installation](https://github.com/fvsionai/fvsion/wiki/2.-Installation#development-installation), to get the latest version and full NodeJS and Python capabilities. However, if you are new, and just wanted to get standalone AI image generation started, please follow the next step.
1. Download Windows Installer/Executable [https://github.com/fvsionai/fvsion/releases](https://github.com/fvsionai/fvsion/releases).
2. Make sure you have all 3 binary zip files (fvsion.zip.z001/2/3) in the same folder. You can unzip them via winzip or 7zip (https://www.7-zip.org/download.html)
   ![image](https://user-images.githubusercontent.com/3688500/195199551-6d589fb9-4e90-4e91-a62e-422caa50f84e.png)
3. Your unzip folders should look as follows:

   ![image](https://user-images.githubusercontent.com/3688500/195200461-af38918b-d682-4110-a39e-58416c718d55.png)

4. Download the difusers models as per instruction [below](https://github.com/fvsionai/fvsion/wiki/2.-Installation/_edit#diffusers-model-download).
5. Download the upscaler models by clicking on `models/download_upscaler_model.bat`.
6. Run the UI and python engine by double clicking `start_app.cmd`.
7. You are ready to generate your image.

# Other OS

1. Linux is currently supported via development installation as per instruction [here](https://github.com/fvsionai/fvsion/wiki/2.-Installation#development-installation). Need help to create a docker image.
1. MacOS not yet supported

# Help Needed

1. Appreciate a Pull Request for setting up docker for both NPM and python, still learning about this to do myself but appreciate a more experienced hand to do this part.

# Contributors

[Hafiidz](https://github.com/Hafiidz/)
