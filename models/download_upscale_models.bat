
@echo Off
TITLE Download Model Files


:askGFPGAN
ECHO.

set choice=
set /p choice=Press Y key to download the GFPGAN model, press N to skip GFPGAN, or press E to exit [Y/N/E]:     
if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='Y' goto dlGFPGAN
if '%choice%'=='N' goto askRealESRGAN
if '%choice%'=='E' goto toExit
if '%choice%'=='y' goto dlGFPGAN
if '%choice%'=='n' goto askRealESRGAN
if '%choice%'=='e' goto toExit
ECHO "%choice%" is not valid, try again
ECHO.
goto askGFPGAN

:dlGFPGAN
ECHO Downloading GFPGAN model from Github
curl --create-dirs -A "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth" -o %~dp0/GFPGAN/GFPGANv1.4.pth --ssl-no-revoke
curl --create-dirs -A "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/RestoreFormer.pth" -o %~dp0/GFPGAN/RestoreFormer.pth --ssl-no-revoke
goto askRealESRGAN

:askRealESRGAN
ECHO.

set choice=
set /p choice=Press Y key to download the RealESRGAN models, press N to skip RealESRGAN, or press E to exit [Y/N/E]:     
if not '%choice%'=='' set choice=%choice:~0,1%
if '%choice%'=='Y' goto dlRealESRGAN
if '%choice%'=='N' goto toExit
if '%choice%'=='E' goto toExit
if '%choice%'=='y' goto dlRealESRGAN
if '%choice%'=='n' goto toExit
if '%choice%'=='e' goto toExit
if '%choice%'=='e' goto toExit
ECHO "%choice%" is not valid, try again
ECHO.
goto askRealESRGAN


:dlRealESRGAN
ECHO Downloading RealESRGAN models from Github
curl --create-dirs -A "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth" -o %~dp0/RealESRGAN/RealESRGAN_x4plus.pth --ssl-no-revoke
curl --create-dirs -A "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64)" -L "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth" -o %~dp0/RealESRGAN/RealESRGAN_x4plus_anime_6B.pth --ssl-no-revoke
goto toExit


:toExit