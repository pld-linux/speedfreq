# TODO: separate lib from init script (-devel shouldn't add any services)
Summary:	CPU speed management daemon
Summary(pl):	Demon do zarz±dzania prêdko¶ci± procesora
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
BuildRequires:	python-devel >= 1:2.4
PreReq:		rc-scripts
Requires(post):	/sbin/ldconfig
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Speedfreq is a package that manages the CPU performance policy. It is
most likely to be useful to laptop owners. It supports a small number
of useful policies that you can use to trade off system performance
against battery life.

%description -l pl
Speedfreq to pakiet zarz±dzaj±cy polityk± wydajno¶ci procesora. Jest
najczê¶ciej przydatny dla u¿ytkowników laptopów. Obs³uguje niewielk±
liczbê przydatnych polityk pozwalaj±cych po¶wiêciæ wydajno¶æ systemu
dla czasu ¿ycia baterii.

%package devel
Summary:	Development headers for speedfreq
Summary(pl):	Pliki nag³ówkowe dla speedfreq
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The speedfreq-devel package contains the header files necessary for
developing programs which use the speedfreq C library.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe potrzebne do tworzenia programów
u¿ywaj±cych biblioteki C speedfreq.

%package python
Summary:	Python interface to the speedfreq client library
Summary(pl):	Interfejs Pythona do biblioteki klienckiej speedfreq
Group:		Development/Libraries
%pyrequires_eq	python-libs

%description python
The speedfreq-python package contains a Python module that allows you
to perform speedfreq client functions.

%description python -l pl
Ten pakiet zawiera modu³ Pythona pozwalaj±cy wywo³ywaæ funkcje
klienckie speedfreq.

%prep
%setup -q
%patch -p1

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
%attr(755,root,root) %{_libdir}/libspeedfreq.so
%{_includedir}/*.h
%{_mandir}/man3/*

%files python
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/*.so
%{py_sitedir}/*.py
