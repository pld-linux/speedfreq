%define py_version 2.4

Summary:	CPU speed management daemon
Name:		speedfreq
Version:	0.7.2
Release:	0.5
License:	GPL
Group:		Applications/System
Source0:	http://www.goop.org/~jeremy/speedfreq/%{name}-%{version}.tar.gz
# Source0-md5:	2d7fd41953f888469831a3fc0b622d42
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
URL:		http://www.goop.org/~jeremy/speedfreq
BuildRequires:	python-devel >= %{py_version}
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
%pyrequires_eq	python-libs

%description python
The speedfreq-python package contains a Python module that allows you
to perform speedfreq client functions.

%prep
%setup -q
%patch -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LIB=%{_libdir} \
	PY_VER=%{py_version}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install  \
	DESTDIR=$RPM_BUILD_ROOT \
	LIB=%{_libdir} \
	PY_VER=%{py_version}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/speedfreqd

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO
%attr(755,root,root) %{_sbindir}/speedfreqd
%attr(755,root,root) %{_bindir}/speedfreq
%attr(755,root,root) %{_libdir}/libspeedfreq.so.*.*.*
%attr(754,root,root) /etc/rc.d/init.d/speedfreqd
%{_mandir}/man[!3]/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*.h
%{_mandir}/man3/*

%files python
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py

%post
/sbin/ldconfig
/sbin/chkconfig --add speedfreqd
if [ -f /var/lock/subsys/speedfreqd ]; then
        /etc/rc.d/init.d/speedfreqd restart >&2
else
        echo "Run \"/etc/rc.d/init.d/speedfreqd start\" to start speedfreqd daemon."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/speedfreqd ]; then
                /etc/rc.d/init.d/speedfreqd stop >&2
        fi
        /sbin/chkconfig --del speedfreqd
fi

%postun -p /sbin/ldconfig
