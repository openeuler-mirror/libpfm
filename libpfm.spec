%define python_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")
%define python_prefix %(python3 -c "import sys; print (sys.prefix)")

Name:           libpfm
Version:        4.10.1
Release:        9
Summary:        A user library help setup performance events for use with the perf_events Linux kernel interface. 
License:        MIT
URL:            http://perfmon2.sourceforge.net/

Source0:        http://sourceforge.net/projects/perfmon2/files/libpfm4/%{name}-%{version}.tar.gz

Patch0001:      0001-libpfm-python3-setup.patch
Patch0002:      0002-libpfm-lib-Makefile.patch
Recommends:	%{name}-help = %{version}-%{release}
BuildRequires:  python3 python3-devel python3-setuptools swig gcc

%description
This is a user library called libpfm4 to help setup performance
events for use with the perf_events Linux kernel interface. 


%package devel
Provides:       %{name}-static = %{version}-%{release}
Obsoletes:      %{name}-static <= %{version}-%{release}
Summary:        Library to provide perf_events in linux
%description    devel
Library package used for development for perf_events interface.

%package -n python3-libpfm
Provides:       %{name}-python = %{version}-%{release}
Obsoletes:      %{name}-python < %{version}-%{release}
Summary:        Python bindings for libpfm

%description -n python3-libpfm
Python bindings for libpfm4 used for perf_events

%package_help

%prep
%autosetup -p1 

%build
%make_build CONFIG_PFMLIB_NOPYTHON=n 

%install
rm -rf $RPM_BUILD_ROOT

make PREFIX=$RPM_BUILD_ROOT%{_prefix} LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
    CONFIG_PFMLIB_NOPYTHON=n PYTHON_PREFIX=$RPM_BUILD_ROOT/%{python_prefix} LDCONFIG=/bin/true install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/lib*.a

%files -n python3-libpfm
%{python3_sitearch}/*

%files help 
%{_mandir}/man3/*


%changelog
* Thu Nov 12 2020 xinghe <xinghe1@huawei.com> - 4.10.1-9
- add help for Recommends

* Tue Aug 18 2020 senlin<xiasenlin1@huawei.com> - 4.10.1-8
- add release for update

* Wed Mar 18 2020 yinzhenling <yinzhenling2@huawei.com> - 4.10.1-7
- add make option

* Sun Dec 1 2019  jiaxiya <jiaxiyajiaxiya@168.com> - 4.10.1-6 
- Package init
