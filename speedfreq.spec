Summary:	CPU speed management daemon
Summary(pl.UTF-8):   Demon do zarządzania prędkością procesora
Name:		speedfreq
Version:	0.7.2
Release:	0.6
License:	GPL
Group:		Applications/System
Source0:	http://www.goop.org/~jeremy/speedfreq/%{name}-%{version}.tar.gz
# Source0-md5:	2d7fd41953f888469831a3fc0b622d42
Source1:	%{name}.init
Patch0:		%{name}-Makefile.patch
URL:		http://www.goop.org/~jeremy/speedfreq
BuildRequires:	python-devel >= 1:2.4
PreReq:		rc-scripts
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Speedfreq is a package that manages the CPU performance policy. It is
most likely to be useful to laptop owners. It supports a small number
of useful policies that you can use to trade off system performance
against battery life.

%description -l pl.UTF-8
Speedfreq to pakiet zarządzający polityką wydajności procesora. Jest
najczęściej przydatny dla użytkowników laptopów. Obsługuje niewielką
liczbę przydatnych polityk pozwalających poświęcić wydajność systemu
dla czasu życia baterii.

%package libs
Summary:	Libraries for %{name}
Summary(pl.UTF-8):   Biblioteki dla %{name}
Group:		Libraries

%description libs
The speedfreq-libs package contains the libraries for %{name} program.

%package devel
Summary:	Development headers for speedfreq
Summary(pl.UTF-8):   Pliki nagłówkowe dla speedfreq
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
The speedfreq-devel package contains the header files necessary for
developing programs which use the speedfreq C library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do tworzenia programów
używających biblioteki C speedfreq.

%package python
Summary:	Python interface to the speedfreq client library
Summary(pl.UTF-8):   Interfejs Pythona do biblioteki klienckiej speedfreq
Group:		Development/Libraries
%pyrequires_eq	python-libs

%description python
The speedfreq-python package contains a Python module that allows you
to perform speedfreq client functions.

%description python -l pl.UTF-8
Ten pakiet zawiera moduł Pythona pozwalający wywoływać funkcje
klienckie speedfreq.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LIB=%{_libdir} \
	PY_VER=%{py_ver}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install  \
	DESTDIR=$RPM_BUILD_ROOT \
	LIB=%{_libdir} \
	PY_VER=%{py_ver}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/speedfreqd

%clean
rm -rf $RPM_BUILD_ROOT

%post
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

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES README TODO
%attr(755,root,root) %{_sbindir}/speedfreqd
%attr(755,root,root) %{_bindir}/speedfreq
%attr(754,root,root) /etc/rc.d/init.d/speedfreqd
%{_mandir}/man[!3]/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libspeedfreq.so.*.*.*

%files devel
%defattr(644,root,root,755)
#%attr(755,root,root) %{_libdir}/libspeedfreq.so
%{_includedir}/*.h
%{_mandir}/man3/*

%files python
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py
