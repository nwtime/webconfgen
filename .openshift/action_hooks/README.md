Action Hooks
============

An action hook is a hook which is applied every time something happens to
the repository.

Openshift provides quite a bit of marksers to allow a decent control level
to the cartridge deployment.

Updated content can be found at the documentation page.

[Action Hooks User Guide](http://openshift.github.io/documentation/oo_user_guide.html#action-hooks)
[Openshift Documentation](https://developers.openshift.com/en/managing-action-hooks.html)


Build Action Hooks
==================

During a Git push, applications using the default OpenShift build lifecycle
are given an opportunity to participate in the build/deploy workflow via
another set of action hooks. The workflow and sequence of actions for the
build lifecycle is described in detail in the OpenShift Builds section of
the Cartridge Developers Guide guide.

The build hooks are

pre_build
---------

Runs before build. Useful for running tests and the sort.
pre_build runs before venv is created / re-created, so account for that in your
scripts.

build
-----

Script for building the package. Unless you happen to have some compiled stuff,
this is not as useful for a python developer. (Nothing to build, as it is all scripted)

deploy
------

Handiest script to deploy the python application, this is where we put a lot of
stuff like syncing database migrations and re-generating static files in the
Static Folder to be server efficiently, and the sort.

post_deply
----------

Run whatever you would like to run after deployment is done. Maybe start a few
watchers / daemons to log activity, maybe run a celery daemon?

NOTE: Personally, I feel that celery daemon starter hooks are better off placed
in the Cartridge Control Action Hooks.

Please remember that there are Cartridge Control Action Hooks too! So that you do
not duplicate run scripts.


Cartridge Control Action Hooks
==============================

An openshift cartridge is controlled by a series of action hooks which a cartridge
maker puts in. running

```
	rhc app <action> <name>
```

will allow you to perform the action which the cartridge maker has provided.

In order for the user to have control over these as well, openshift has provided pre and
post hooks into the runtime of these cartridges to allow user actions to be applied on
the application.

For example, on running,

```
	rhc app tidy test
```

the following are run in that order.

pre_tidy (.openshift/action_hooks/pre_tidy)
tidy (provided by the cartridge developer)
post_tidy (.openshift/action_hooks/post_tidy)

In addition, the hooks can be in the form of

```
.openshift/action_hooks/{pre,post}_{action}_{Name}
```

where Name is a name given for easier access.

start
-----

pre_start and post_start can be used to start custom applications like changing the
environment before starting application or maybe starting another application(s)
after the start of the main Django application.

stop
----

pre_stop and post_stop can be used to stop custom applications like stoping another
custom application(s) that you might have started.

reload
------

pre_reload and post_reload can be used to reload custom applications like reloading another
custom application(s) that you might have started.

tidy
----

pre_tidy and post_tidy can be used to tidy custom applications like tidying another
custom application(s) that you might have started.

restart
-------

pre_restart and post_restart can be used to restart custom applications like restarting
another custom application(s) that you might have started.

A good example of the said application would be the celery task queue.
