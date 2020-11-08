# Biodiv project

# Next up
- this seems to be the culprit: 'biodiv/tests/test_images/but1_lab.jp2'
- fix git prompt in iterminal
- Load everything in docker, might resolve TravisCI issues.

`main.py` *eventually cli.py*
    - [x] find ROIs from provided paths and display result
    - add option to label & save
    - modify so that I am brought back to the program after exiting.
        - must enter `q` to quit.

- Start commiting to GIT and add CI/CD with Travis CI.
    - then everytime you push to master your tests will be run.

- put `main.py` in a docker container to move it around.

## mid term
- super simple web app to wrap functions above.
    - 1 container for the app, one for the detection.
- put it on AWS.
- add detection with YOLO instead of biodiv.

## Goal of the project
- Practice testing
- First foray into CI/CD
*stretch*
- Apply CI/CD with push to lambda.
- docker
- sagemaker to serve output.