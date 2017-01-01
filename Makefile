MKFILE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
CURRENT_DIR := $(notdir $(patsubst %/,%,$(dir $(MKFILE_PATH))))
PROJECT_DIR := $(dir $(MKFILE_PATH))

TMP_SRC_DIR=/tmp/src
WORK_DIR=/mnt/src

PYLINT_PRJ_FLAGS=--persistent=n --good-names=i,j,k,ex,Run,_,fd,ud,ms,ss,mm,hh --extension-pkg-whitelist=re --ignored-modules=re
PYLINT_TESTS_FLAGS=--disable=missing-docstring,no-member,protected-access,no-self-use,redefined-outer-name,too-many-locals

DOCKER_RUN_CMD=docker run -t -i --rm=true --workdir=$(WORK_DIR) -v $(PROJECT_DIR):$(WORK_DIR):ro python:3

COPY_DIR_CMD=mkdir -p $(TMP_SRC_DIR); tar -c --exclude .git --exclude __pycache__ . | tar -x -C $(TMP_SRC_DIR)
CLONE_WORKDIR_CMD=$(COPY_DIR_CMD) ; cd $(TMP_SRC_DIR)

TEST_CMD=$(CLONE_WORKDIR_CMD) && python setup.py test -a "--durations=3"
SETUP_CMD=$(CLONE_WORKDIR_CMD) && python setup.py develop

LINT_FLAKE=flake8 . || true
LINT_PYLINT=pylint srtmerge $(PYLINT_PRJ_FLAGS) --reports=n || true; pylint tests $(PYLINT_PRJ_FLAGS) $(PYLINT_TESTS_FLAGS) --reports=n || true
LINT_CMD=$(SETUP_CMD) && pip install flake8 pylint; $(LINT_FLAKE); $(LINT_PYLINT)

.PHONY: clean-pyc

clean-pyc:
	rm -fr *.egg-info build dist
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

clean: clean-pyc

test:
	$(DOCKER_RUN_CMD) /bin/bash -c "$(TEST_CMD)"

lint:
	$(DOCKER_RUN_CMD) /bin/bash -c "$(LINT_CMD)"