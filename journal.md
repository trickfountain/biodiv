# Biodiv project

# ToDO
- [x] make detection runnable from command line.
    - returns green rectangle and saves it to pic_det.ext
- [ ] change _det images in .png to enable seeing via web browser
- [ ] add -o to send images to host volumes
- [ ] Create super basic website with NGINX that enables browsing pictures.
- [ ] Use detector CLI 
    - [ ] first docker build: review structure with udemy class.
    - [ ] Test it using mount
    - [ ] Make Vs code docker extension specific to your project.
    - [ ] Add test and use docker build on Travis
- [ ] package biodiv or your whole project as a wheel with setup tools. see: https://packaging.python.org/tutorials/packaging-projects/
    - consider using poetry. its just a wrapper that creates a wheel. https://python-poetry.org/docs/basic-usage/

# Up next
- [ ] 2-container process: add either flask app to show labelled or DB to save pic_det.

## mid term
- super simple web app to wrap functions above.
    - 1 container for the app, one for the detection.
- put it on AWS.
- add detection with YOLO instead of biodiv.

## Goal of the project
- [x] Practice testing 
- [x] First foray into CI/CD
- [ ] docker
- [ ] combine above on the cloud.
