#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	josepy
Summary:	JOSE protocol implementation
Summary(pl.UTF-8):	Implementacja protokołu JOSE
Name:		python-%{module}
# keep 1.6.x here for python2 support
Version:	1.6.0
Release:	1
Epoch:		1
License:	Apache v2.0
Group:		Development/Languages/Python
Source0:	https://files.pythonhosted.org/packages/source/j/josepy/josepy-%{version}.tar.gz
# Source0-md5:	a1986b642c4381aab9635f1a4ce1a9be
URL:		https://josepy.readthedocs.io/en/latest/
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools >= 1.0
%if %{with tests}
BuildRequires:	python-cryptography >= 0.8
BuildRequires:	python-mock
BuildRequires:	python-pyOpenSSL >= 0.13
BuildRequires:	python-pytest >= 2.8.0
BuildRequires:	python-pytest-cov
BuildRequires:	python-pytest-flake8 >= 0.5
BuildRequires:	python-six >= 1.9.0
%endif
%if %{with doc}
BuildRequires:	python-Sphinx >= 1.0
BuildRequires:	python-cryptography >= 0.8
BuildRequires:	python-pyOpenSSL >= 0.13
BuildRequires:	python-six >= 1.9.0
BuildRequires:	python-sphinx_rtd_theme
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides JOSE protocol implementation.

%description -l pl.UTF-8
Ten pakiet zawiera implementację protokołu JOSE.

%package apidocs
Summary:	API documentation for josepy module
Summary(pl.UTF-8):	Dokumentacja API modułu josepy
Group:		Documentation

%description apidocs
API documentation for josepy module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu josepy.

%prep
%setup -q -n %{module}-%{version}

%build
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="pytest_cov.plugin,pytest_flake8" \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest src
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
%{__make} -C docs html \
	SPHINXBUILD="%{__python} -m sphinx"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/jws{,-2}
# remove tests
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/josepy/{test_util,*_test}.py[co]
%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/josepy/testdata

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst README.rst
%attr(755,root,root) %{_bindir}/jws-2
%{py_sitescriptdir}/josepy
%{py_sitescriptdir}/josepy-%{version}-py*.egg-info

%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,api,man,*.html,*.js}
