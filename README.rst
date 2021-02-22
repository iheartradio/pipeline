========
Pipeline
========

Common utilities used by the Ingestion Pipeline.

-----------------------
Deploying a new version
-----------------------

To manually deploy/test a new version:

* Increment the version in setup.py, make sure CodeArtifact doesn't already have a repo for that version.

* Make sure `dist` directory is empty, then follow instructions [here](https://github.com/iheartradio/content-platform-documentation/blob/master/private_python_modules/README.md#publishing-with-twine)

When a branch is merged to master, a Travis job will build and deploy the version that's in `setup.py`.

**WARNING:**
If you don't delete the version you uploaded for testing, and it conflicts with the final `setup.py` version when the
branch is merged, this will result in a conflict error and the build will fail.

If you redeploy a new version of the same version tag, clear pip cache in dependent repos:
`rm -rf ~/Library/Caches/pip/*`