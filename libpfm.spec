%bcond_without python
%if %{with python}
%define python_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%define python_prefix %(python3 -c "import sys; print (sys.prefix)")
%{?filter_setup:
%filter_provides_in %{python3_sitearch}/perfmon/.*\.so$
%filter_setup
}
%endif

Name:           libpfm
Version:        4.10.1
Release:        6
Summary:        A user library help setup performance events for use with the perf_events Linux kernel interface. 
License:        MIT
URL:            http://perfmon2.sourceforge.net/

Source0:        http://sourceforge.net/projects/perfmon2/files/libpfm4/%{name}-%{version}.tar.gz

# PATCH-FIX、python version 
Patch2:         0001-libpfm-python3-setup.patch

BuildRequires:  gcc
%if %{with python}
BuildRequires:  python3 python3-devel python3-setuptools swig
%endif

%description
This is a user library called libpfm4 to help setup performance
events for use with the perf_events Linux kernel interface. 

%package devel
Summary:        Development library to encode performance events for perf_events based tools
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development library and header files to create performance monitoring
applications for the perf_events interface.

%package_help

%if %{with python}
%package -n python3-libpfm
%{?python_provide:%python_provide python3-libpfm}
# Remove before F30
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
Summary: Python bindings for libpfm and perf_event_open system call
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python3-libpfm
Python bindings for libpfm4 and perf_event_open system call.
%endif

%prep
%setup -q
%patch2 -p1 -b .python3

%build
%if %{with python}
%global python_config CONFIG_PFMLIB_NOPYTHON=n
%else
%global python_config CONFIG_PFMLIB_NOPYTHON=y
%endif
make %{python_config} %{?_smp_mflags} \
     OPTIM="%{optflags}" LDFLAGS="%{build_ldflags}"


%install
rm -rf $RPM_BUILD_ROOT

%if %{with python}
%global python_config CONFIG_PFMLIB_NOPYTHON=n PYTHON_PREFIX=$RPM_BUILD_ROOT/%{python_prefix}
%else
%global python_config CONFIG_PFMLIB_NOPYTHON=y
%endif

make \
    PREFIX=$RPM_BUILD_ROOT%{_prefix} \
    LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
    %{python_config} \
    LDCONFIG=/bin/true \
    install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.a

%if %{with python}
%files -n python3-libpfm
%{python3_sitearch}/*
%endif

%files help 
%{_mandir}/man3/*


%changelog

* Sat Nov 30 2019  openEuler Buildteam <buildteam@openeuler.org> - 4.10.1-6 
- Package init
