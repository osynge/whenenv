# When Env

whenenv is designed to keep the branching involved in build and 
functional test scripts from growing out of control.

You specify a list of environment variables and whenenv will then 
try and reuse existing scrimps to process the request.

If it fails to find suitable scripts you should specify some minium script.

When launching whenenv, always specify the PRODUCT environment variable. The
components of the build are isolated and reusable.




## Background.

Using this "Configuration Matrix" plugin in for Jenkins Builds makes it 
difficult to decouple the matrix settings from the to separate out reusable code
from branching parameters. whenenv addresses this problem, but may well have other uses.

whenenv was designed with the assumption that matrix jobs will be in a regular state of change around axis and thier values.

Managing jenkins builds usually requires a different script for every job, but with whenenv, all of the environment variable branching is coded in pattern matching, leaving you to concentrate on exceptional cases and reuse all your build script fragments.


## How does whenenv work?

1. whenenv reads environment variables, presented from a jenkins matrix job and tries to run jobs to execute a goal.
2. The jobs that make up a goal are executed in order defined by the goals requirements.
3. Goals are specified as jobs with dependencies, that scripts can provide solutions for. Goals can be nested.
4. Goals are achieved when each dependency has been resolved with a Job that provides the dependency.
5. The most specific job will be selected in preference to the least specific job. This binding is as late as possible allowing execution to be overwritten easily.
6. Jobs may execute shell scripts and publish the results to later scripts.
7. Any successful job providing a met dependency will never be run a second time and that requirement is considered handled.

These simple rules allow Jobs to be processed in an order that is defined by the matrix parameters which are presented to whenenv as environment variables.

A simple stack and processed job log is used to prevent jobs being run more than once during goal completion.

## About Jenkins

Jenkins is a very flexible tool for doing automated builds.

Jenkins "Configuration Matrix" plugin make Jenkins a tool for testing ranges of
settings, displaying aggregate test results and easily identifying job failures.

Matrix (range) testing is commonly used for portability testing, comparative
branch testing, and seeing how build parameters effect tests.

whenenv aims is to reduce the maintenance work for writing matrix jobs, and to benefit from code reuse.

Assuming you are running a 3 axis matrix job, with the following axis:

    PRODUCT 
    RELEASE
    OPERATING_SYSTEM

assuming you have a private git repository, that you may want to download.

Add the following script as a build step:

    rm -rf private_repo
    git clone git://git.example.org/whenenv_demo.git private_repo

    whenenv \
        --envvar PRODUCT \
        --envvar RELEASE \
        --envvar OPERATING_SYSTEM \
        --dir-jobs /usr/share/lib/whenenv/jobs/ \
        --dir-jobs /usr/share/whenenv/jobs \
        --dir-jobs private_repo/jobs \
        --dir-scripts /usr/share/lib/whenenv/scripts/ \
        --dir-scripts /usr/share/whenenv/transfer \
        --dir-scripts private_repo/scripts

Note: In this example whenenv will trigger jobs based on 3 environment variables,
and will search 3 directories for jobs, and search for scripts also in 3 directories. This also give a clue as to how to use your version control system to drive job execution.

## A walk through of whenenv on whenenv

Included in this package is an example "whenenv.json"


    # cat jobs/whenenv.json
    {
        "name" : "whenenv",
        "variables" : {
            "require_values" : { "PRODUCT" : "whenenv"},
            "require_keys" : ["RELEASE","OPERATING_SYSTEM"]
        },
        "provides" : ["execution"],
        "depends" :
                    ["whenenv_source",
                    "checkout_source",
                    "unittests",
                    "build_package",
                    "export_package"]
    }

### Format notes:

* name must be unique.
* This job 'provides' "execution" so will be invoked by the command line.
* This job 'depends' on 5 jobs to 'provide' for the dependency.
* This job will only be able to provide "execution" if the "PRODUCT" variable is "whenenv" and it has both "RELEASE" and "OPERATING_SYSTEM" as variables but the value is not fixed.

Since this is the entry point for a execution goal, this is the most common type
of job you will havre to write when extending whenenv to your goal.

whenenv will then try to match each requirement in its order specified.

The only job that "provides" , "whenenv_source" is "whenenv_source.json"


    # cat jobs/whenenv_source.json 
    {
        "name" : "whenenv_source",
        "provides" : ["whenenv_source"],
        "script" : "whenenv_source.sh",
        "variables" : { "provides_keys" : [
            "GIT_SRC",
            "GIT_DEST",
            "GIT_TAG_FILTER"] }
    }

### Format notes:

* Has a script attribute which will need to execute before its finished.
* This script will populate the goals name space with the variables "GIT_SRC",
    "GIT_DEST" and "GIT_TAG_FILTER"

After  "whenenv_source.json" provides "whenenv_source", we will still need to 
process "checkout_source". 

In total 5 files provide "checkout_source" and the most specific will be selected.

    git_checkout_gitbuildpackage.json
    git_checkout_tag.json
    git_checkout_trunk.json
    svn_checkout_master.json
    svn_checkout_tag.json

The "SVN_SRC" variable being required for 2 of them, 1 requires build type 
"gitbuildpackage" so can be excluded.

This leaves "git_checkout_trunk.json" or "git_checkout_tag.json".

The ordinal matrix parameters "RELEASE" can be of 2 values, "development" or
"production". For the following example we show it as "development".


    # cat git_checkout_trunk.json 
    {
        "name" : "git_checkout_trunk",
        "provides" : ["checkout_source"],
        "script" : "git_checkout_development.sh",
        "enviroment" : "chroot",
        "variables" : { "provides_keys" : ["BUILD_SRC"],
            "require_values" : { "RELEASE" : "development" },
            "require_keys" : [ "GIT_SRC" ]
        }
    }

This script sets up a git cache if none exists, and checks out the source with 
reference to the local cache so reducing git download speeds dramatically.

After "git_checkout_trunk" provides "checkout_source" the next dependency is 
"unittests" and the following jobs provide this:

    tests_autotools.json
    tests_python.json
    tests_skip.json

Since the "BUILD_TYPE" variable will have the value "disttools" only 
"tests_python.json" can be selected.

    #cat tests_python.json 
    {
        "name" : "tests_python",
        "provides" : ["unittests"],
        "script" : "nosetests_python.sh",
        "variables" : {
            "require_values" : {
                "BUILD_TYPE" : "disttools" ,
                "TESTS" : "nosetests"},
            "require_keys" : []
        }
    }

The following are all included in the search.


    build_autotools_default.json
    build_autotools_tag_scientific7.json
    build_autotools_tag_scientific.json
    build_gitbuildpackage_default.json
    build_python_branch_debian_development.json
    build_python_branch_debian_production.json
    build_python_branch_scientific7.json
    build_python_branch_scientific.json
    build_python_tag_scientific7.json
    build_python_tag_scientific.json


Due to a series of selection criteria, dependent on the matrix enviroment variables:

    build_python_branch_scientific7.json

is selected and 
