# This file is necessary so we can run our custom deploy.sh
# script actually at the time of deployment. Calling the script
# in the release: worker does not work as the changes to the
# filesystem are lost when the one-off dyno shuts down.

import os
import subprocess

# Pip builds the setup.py in a separate directory, but we need
# to run the deploy.sh script from the original Heroku BUILD_DIR.
build_dir = os.getenv('BUILD_DIR')
script_fn = os.path.join(build_dir, 'deploy.sh')
print('Running deploy.sh from Heroku build directory ({})'.format(build_dir))
subprocess.call(['bash', script_fn], cwd=build_dir)

# Proxy
from setuptools import setup
setup(name='heroku-deploy')
