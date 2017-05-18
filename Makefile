########################################################

# Makefile for python-flagon
#
# useful targets (not all implemented yet!):
#   make clean ------------------- Clean up garbage
#   make flake8/coverage -- source code checks
#   make tests ------------------- run all unit tests (export LOG=true for /tmp/ logging)

########################################################

# > VARIABLE = value
#
# Normal setting of a variable - values within it are recursively
# expanded when the variable is USED, not when it's declared.
#
# > VARIABLE := value
#
# Setting of a variable with simple expansion of the values inside -
# values within it are expanded at DECLARATION time.

########################################################

# # This doesn't evaluate until it's called. The -D argument is the
# # directory of the target file ($@), kinda like `dirname`.
# ASCII2MAN = a2x -D $(dir $@) -d manpage -f manpage $<
# MANPAGES := docs/man/man1/re-rest.1

NAME := flagon
PKGNAME := python-flagon
RPMSPECDIR := contrib/rpm
RPMSPEC := $(RPMSPECDIR)/$(PKGNAME).spec
# VERSION file provides one place to update the software version.
VERSION := $(shell cat VERSION)
RPMRELEASE = $(shell awk '/global _short_release/{print $$NF; exit}' $(RPMSPEC).in)


# Build the spec file on the fly. Substitute version numbers from the
# # canonical VERSION file.
$(RPMSPECDIR)/$(PKGNAME).spec: $(RPMSPECDIR)/$(PKGNAME).spec.in
	sed "s/%VERSION%/$(VERSION)/" $< > $@


# Build the distutils setup file on the fly.
setup.py: setup.py.in VERSION $(RPMSPECDIR)/$(PKGNAME).spec.in
	sed -e "s/%VERSION%/$(VERSION)/" -e "s/%RELEASE%/$(RPMRELEASE)/" $< > $@

tag:
	git tag -s -m $(TAG) $(TAG)

test: tests

tests: coverage flake8

coverage:
	@echo "#############################################"
	@echo "# Running Unit + Coverage Tests"
	@echo "#############################################"
	python setup.py nosetests

clean:
	@find . -type f -regex ".*\.py[co]$$" -delete
	@find . -type f \( -name "*~" -or -name "#*" \) -delete
	@rm -fR build cover dist rpm-build MANIFEST htmlcov .coverage flagon.egg-info

flake8:
	@echo "#############################################"
	@echo "# Running flake8 Compliance Tests"
	@echo "#############################################"
	python setup.py flake8

install: clean
	python ./setup.py install

sdist: setup.py clean
	python setup.py sdist

rpmcommon: $(RPMSPECDIR)/$(PKGNAME).spec sdist
	@mkdir -p rpm-build
	@cp dist/$(NAME)-$(VERSION).tar.gz rpm-build/$(NAME)-$(VERSION).tar.gz

srpm: rpmcommon
	@rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir $(RPMSPECDIR)" \
	--define "_sourcedir %{_topdir}" \
	-bs $(RPMSPEC)
	@echo "#############################################"
	@echo "$(PKGNAME) SRPM is built:"
	@find rpm-build -maxdepth 2 -name '$(PKGNAME)*src.rpm' | awk '{print "    " $$1}'
	@echo "#############################################"

rpm: rpmcommon
	@rpmbuild --define "_topdir %(pwd)/rpm-build" \
	--define "_builddir %{_topdir}" \
	--define "_rpmdir %{_topdir}" \
	--define "_srcrpmdir %{_topdir}" \
	--define "_specdir $(RPMSPECDIR)" \
	--define "_sourcedir %{_topdir}" \
	-ba $(RPMSPEC)
	@echo "#############################################"
	@echo "$(PKGNAME) RPMs are built:"
	@find rpm-build -maxdepth 2 -name '$(PKGNAME)*.rpm' | awk '{print "    " $$1}'
	@echo "#############################################"
