# 1. Base image
FROM opencvcourses/opencv:440

WORKDIR /src
# Copy current folder in /biodiv inside the container
ENV PYTHONPATH "${PYTHONPATH}:."

COPY . .

RUN pip install -r requirements.txt

RUN mkdir outputs

# Run Bash on starting
CMD ["bash"]
