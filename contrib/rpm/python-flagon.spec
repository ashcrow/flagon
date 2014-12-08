# sitelib for noarch packages, sitearch for others (remove the unneeded one)
%{!?python_sitelib: %global python_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}

%global _pkg_name flagon
%global _short_release 1

Name:           python-flagon
Version:        0.0.3
Release:        %{_short_release}%{?dist}
Summary:        Feature flags for python

License:        MIT
URL:            https://github.com/ashcrow/flagon
Source0:        %{_pkg_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools


%description
Generic feature flags for Python which attempts to be compatible with
Java's Togglz.

%prep
%setup -q -n %{_pkg_name}-%{version}

%build
%{__python2} setup.py build


%install
%{__python2} setup.py install -O1 --skip-build --root=$RPM_BUILD_ROOT

%files
%doc README.md LICENSE AUTHORS example CONTRIBUTING.md
%{python2_sitelib}/*

%changelog
* Mon Dec  8 2014 Steve Milner <stevem@gnulinux.net> - 0.0.3-1
- MongoDB is now supported as a backend.

* Fri Aug 29 2014 Steve Milner <stevem@gnulinux.net> - 0.0.2-1
- Update for upstream release.
* Tue Jun 10 2014 Tim Bielawa <tbielawa@redhat.com> - 0.0.1-1
- First release
