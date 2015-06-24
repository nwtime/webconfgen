Markers
=======

A marker is a file placed in the OPENSHIFT_REPO_DIR/.openshift/markers/

This file ought to be empty and just be named exact case sensitive spelling.

Updated content can be found at the documentation page.

[Markers User Guide](http://openshift.github.io/documentation/oo_user_guide.html#markers)
[Openshift Documentation](https://developers.openshift.com/en/python-markers.html)

force_clean_build
-----------------

Will cause virtualenv to recreated during builds.

hot_deploy
----------

Will prevent shutdown and startup of the application during builds. Keep in mind
that the memory allocated is still limited, so if you have a memory hogging
application, it would be bad.

enable_public_server_status
---------------------------

Will enable server-status application path to be publicly available.

disable_auto_scaling
--------------------

Will prevent scalable applications from scaling up or down according to application load.
