%define py_version 2.4

Summary:	CPU speed management daemon
Name:		speedfreq
Version:	0.7.2
Release:	0.1
License:	GPL
Group:		Applications/System
Source0:	http://www.goop.org/~jeremy/speedfreq/%{name}-%{version}.tar.gz
# Source0-md5:	2d7fd41953f888469831a3fc0b622d42
URL:		http://www.goop.org/~jeremy/speedfreq
BuildRequires:	python-devel >= %{py_version}
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Speedfreq is a package that manages the CPU performance policy. It is
most likely to be useful to laptop owners. It supports a small number
of useful policies that you can use to trade off system performance
against battery life.

%package devel
Summary:	Development headers and libraries for speedfreq
Group:		Development/Libraries

%description devel
The speedfreq-devel package contains the header and object files
necessary for developing programs which use the speedfreq C library.

%package python
Summary:	Python interface to the speedfreq client library
Group:		Development/Libraries
Requires:	python >= %{py_version}

%description python
The speedfreq-python package contains a Python module that allows you
to perform speedfreq client functions.

%prep
%setup -q
sed -n '/chown/!p' -i Makefile
sed -n '/^INST_OPTS/!p' -i Makefile

%build
%{__make} VERSION=%{version} \
	PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
	INITD=$RPM_BUILD_ROOT/%{_initrddir} \
	MAN=$RPM_BUILD_ROOT/%{_mandir} \
	PY_VER=%{py_version}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	VERSION=%{version} \
	PREFIX=$RPM_BUILD_ROOT/%{_prefix} \
	INITD=$RPM_BUILD_ROOT/%{_initrddir} \
	MAN=$RPM_BUILD_ROOT/%{_mandir} \
	PY_VER=%{py_version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO
%attr(755,root,root) %{_sbindir}/speedfreqd
%attr(755,root,root) %{_bindir}/speedfreq
%attr(755,root,root) %{_prefix}/lib/libspeedfreq.so.*
%attr(754,root,root) /etc/rc.d/init.d/speedfreqd
%{_mandir}/man[!3]/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_mandir}/man3/*

%files python
%defattr(644,root,root,755)
%{_prefix}/lib/python%{py_version}/site-packages/*

%post
/sbin/ldconfig
/sbin/chkconfig --add speedfreqd

%preun
/etc/rc.d/init.d/speedfreqd stop
/sbin/chkconfig --del speedfreqd

%postun -p /sbin/ldconfig
