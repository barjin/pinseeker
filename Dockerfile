# First, specify the base Docker image. You can read more about
# the available images at https://sdk.apify.com/docs/guides/docker-images
# You can also use any other image from Docker Hub.
FROM apify/actor-node-playwright-firefox:16

USER root

RUN apt-get update
RUN apt-get install -y --no-install-recommends python3 python3-pip build-essential

USER myuser
WORKDIR /home/myuser

RUN  pip3 install setuptools
RUN  pip3 install --upgrade setuptools pip
RUN  pip3 install matplotlib opencv-python numpy tqdm

# Second, copy just package.json and package-lock.json since it should be
# the only file that affects "npm install" in the next step, to speed up the build
COPY package*.json ./
COPY --chown=myuser:myuser .npmrc /home/myuser/


# Install NPM packages, skip optional and development dependencies to
# keep the image small. Avoid logging too much and print the dependency
# tree for debugging
RUN npm --quiet set progress=false \
    && npm install --only=prod --no-optional \
    && echo "Installed NPM packages:" \
    && (npm list --only=prod --no-optional --all || true) \
    && echo "Node.js version:" \
    && node --version \
    && echo "NPM version:" \
    && npm --version

# Next, copy the remaining files and directories with the source code.
# Since we do this after NPM install, the quick build will be really fast
# for most source file changes.
COPY . ./

# Optionally, specify how to launch the source code of your actor.
# By default, Apify's base Docker images define the CMD instruction
# that runs the Node.js source code using the command specified
# in the "scripts.start" section of the package.json file.
# In short, the instruction looks something like this:
#
# CMD npm start
