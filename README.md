# About

1. `Fvsion`, pronounced `Fusion` is a quick bundle of `FastAPI` + `Vite and Vue` + `Stable Diffusion` with async first design.
1. Built on top of [electron-vite-vue-fastapi boilerplate](https://github.com/Hafiidz/electron-vite-vue-fastapi).

# Features & Motivation
1. Independent frontend and backend, choose what you need and as you need.
1. Image generation is sent asynchronously to the fastAPI engine, allowing for automatic queue.
1. Flexible api modules to allow ease of use to add your own or publically shared modules, without interference with UI.
1. Integration with Node for faster prototyping.
1. Versatile UI in Vue & Electron.
1. Cross platform features incoming via Electron and packaged pyInstaller (coming soon).

# Beginner Friendly Installation 
1. Windows Installer/Executable (Coming Soon)
1. Linux and MacOS not yet supported

# Development Installation
1. Make sure you have [git](https://git-scm.com/downloads), [python 3.10.7](https://www.python.org/downloads/) & [virtualenv](https://pypi.org/project/virtualenv/), and [node == 18.9.1](https://nodejs.org/en/) installed.
1. Clone git via `git clone https://github.com/fvsionai/fvsion.git <folder-name>`. Replaced `<folder-name>` with your desired folder name.
1. Navigate to the newly created folder `cd <folder-name>`
1. Download diffusers model as per instruction below: [Link](# Diffusers Model Download)
1. Make sure you are in the root folder and create virtualenv local folders `python -m virtualenv .venv`
1. Activate your virtualenv by using `.venv/scripts/activate`
1. Update pip `python -m pip install --upgrade pip`
1. Install python requirement using `pip install -r py/requirements.txt`
1. Run `python py/main.py` & go to `http://localhost:4242/docs` to confirm server is running. 
1. You can start generating image by directly interacting with the built in SwaggerAPI. Click "CTRL + C" while in terminal to close the server when you are done.
1. For a proper front end, need to install npm requirement using `npm i`
1. Development run via `npm run dev`
1. _(Optional)_ You can run `npm run build` to generate standalone exe files. Do note however it might take a while (~30 minutes on AMD Ryzen 5 1600), especially for the first run.
1. _(Recommended)_ Please send PR for any improvement suggestions. Very much welcomed.

# Diffusers Model Download 
1. There are two options as of today, either download manually by going to huggingface website, or using `git lfs` to handle large files. Note that the whole files total up to >5 GB
1. Additionally, you can use the default download version if you have **8GB VRAM** or more. If you have less VRAM, it is **highly recommended** to download from fp16 tree. Do note that even if you have VRAM >= 8GB, it is also good to have low VRAM model to ensure that you are able to run a lot more prompts in batches. The low VRAM model is just slightly slower than the normal model.
1. Install Git LFS (large file storage) via `git lfs install` command in your favorite cmd/bash.
1. For low VRAM, run the command in cmd/bash `git clone https://huggingface.co/CompVis/stable-diffusion-v1-4 -b fp16 models/stable-diffusion-v1-4-fp16`. There will be prompt asking for your huggingface id and password for the first time.
1. _(Optional)_ If the above fails to work, you can manually download the models, by logging into `https://huggingface.co/login` and navigate to `https://huggingface.co/CompVis/stable-diffusion-v1-4/tree/fp16` . It is important to login first, otherwise you will receive 404 error when navigating to the download page.
1. _(Optional)_ For low VRAM, downloads `stable-diffusion-v1-4` whole folder from `https://huggingface.co/CompVis/stable-diffusion-v1-4/tree/fp16` and copy to `models/stable-diffusion-v1-4-fp16`.

1. For high VRAM, run the command in cmd/bash  `git clone https://huggingface.co/CompVis/stable-diffusion-v1-4 models/stable-diffusion-v1-4`. There will be prompt asking for your huggingface id and password for the first time.
1. _(Optional)_ If the above fails to work, you can manually download the models, by logging into `https://huggingface.co/login` and navigate to `https://huggingface.co/CompVis/stable-diffusion-v1-4/tree/main` . It is important to login first, otherwise you will receive 404 error when navigating to the download page.
1. _(Optional)_ For high VRAM, downloads `stable-diffusion-v1-4` whole folder from `https://huggingface.co/CompVis/stable-diffusion-v1-4/tree/main` and copy to `models/stable-diffusion-v1-4`.
1. Once completed please ensure that you are back in the root directory.

# Known Issues
1. There are edge cases where electron failed to be installed using `npm i`, if so, open `package.json` file, temporaily delete the ` "electron": "2x.x.x", "electron-builder": "2x.x.x", "got": "x.x.x",` lines, save the files and run `npm i` again. Once successful, undo the changes in `package.json` i.e. re-add the deleted line, and re-run `npm i`  
1. There might be undeleted temporary files in `C:\Users\test\AppData\Local\Temp`. Please check if you storage is heavily used. Do note that diffusers libary tend to cache files to speed up operation which also use some amount of data. More details [here](https://huggingface.co/docs/datasets/cache). 
1. UX: Minimal loading indicator when loading generation. 

# Contributors

[Hafiidz](https://github.com/Hafiidz/)



