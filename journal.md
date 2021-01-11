# Biodiv project

# ToDO
- [ ] test apply() in detection
- [ ] make detectorV1 work
- [ ] Commit your code
    - [ ] CI should work.
- [ ] Back to website/docker etc.
    - [ ] integration test would be nice.

- [ ] add minimal tests to flask app.
    - screwing around in biodiv should break the flask tests.
- [ ] solve relative imports and such, everything in one package for now.

-- back in docker--
- [ ] Use NGINX to serve static and for server... backend ?
- [ ] use volumes and mount to manage static files.
- [ ] Use detector CLI 
    - [ ] first docker build: review structure with udemy class.
    - [ ] Test it using mount
    - [ ] Make Vs code docker extension specific to your project.
    - [ ] Add test and use docker build on Travis
- [ ] package biodiv or your whole project as a wheel with setup tools. see: https://packaging.python.org/tutorials/packaging-projects/
    - consider using poetry. its just a wrapper that creates a wheel. https://python-poetry.org/docs/basic-usage/

## Up next
- transform your webapp into a labeller.

## mid term
- super simple web app to wrap functions above.
    - 1 container for the app, one for the detection.
- put it on AWS.
- add detection with YOLO instead of biodiv.

## Goal of the project
- [x] Practice testing 
- [x] First foray into CI/CD
- [ ] Tesing flask apps (integration tests)
- [ ] docker
- [ ] multi-container app with docker compose
- [ ] using nginx to serve content, enable logging.
- [ ] combine above on the cloud.
