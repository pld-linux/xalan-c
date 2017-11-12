%define	snap	20101114
%define		rel	5
Summary:	C++ xslt library
Summary(pl.UTF-8):	Biblioteka xslt dla C++
Name:		xalan-c
Version:	1.11.0
# snap due to http://article.gmane.org/gmane.text.xml.xalan.c%2B%2B.user/3900
Release:	0.%{snap}.%{rel}
License:	Apache v2.0
Group:		Applications/Publishing/XML
# http://svn.apache.org/repos/asf/xerces/c/trunk/
Source0:	%{name}-%{snap}.tar.bz2
# Source0-md5:	ccf7777cfb2d48652ea2e929de65a907
Patch1:		%{name}-soname.patch
Patch2:		%{name}-include.patch
URL:		http://xml.apache.org/xalan-c/
BuildRequires:	util-linux
BuildRequires:	xerces-c-devel >= 2.7.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache Xalan Project is a collaborative software development project
dedicated to providing robust, full-featured, commercial-quality, and
freely available XSLT support on a wide variety of platforms.

This package contains C++ implementation of Xalan.

%description -l pl.UTF-8
Projekt Apache Xalan to wspólny projekt stworzenia oprogramowania
mającego zapewnic potężną, w pełni funkcjonalną, mającą komercyjną
jakość i jednocześnie wolnodostępną obsługę XSLT na szerokim zakresie
platform.

Ten pakiet zawiera bibliotekę Xalan dla języka C++.

%package devel
Summary:	xalan-c header files
Summary(pl.UTF-8):	Pliki nagłówkowe xalan-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
xalan-c header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe xalan-c.

%package docs
Summary:	Documentation for xalan-c
Summary(pl.UTF-8):	Dokumentacja xlan-c
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description docs
Documentation for xalan-c.

%description docs -l pl.UTF-8
Dokumentacja xalan-c.

%package examples
Summary:	xalan-c examples
Summary(pl.UTF-8):	Przykłady dla xalan-c
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description examples
xalan-c examples.

%description examples -l pl.UTF-8
Przykłady dla xalan-c.

%prep
%setup -q -n %{name}
%patch1 -p2
%patch2 -p2

sed -i -e 's#debugflag=".*";#debugflag="%{rpmcflags} %{rpmcppflags}";#g' runConfigure

find xdocs samples -name CVS | xargs rm -rf

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
# create env.sh for easier debug from console
cat << EOF > env.sh
export XALANCROOT=$(pwd)
export XERCESROOT=%{_prefix}
export ICUROOT=%{_prefix}
EOF

. ./env.sh

./runConfigure \
	-C "--libdir=%{_libdir}" \
	-P %{_prefix} \
	-p linux \
	-c "%{__cc}" \
	-x "%{__cxx}" \
%ifarch %{x8664} alpha ppc64 s390x sparc64
	-b 64 \
%else
	-b 32 \
%endif
	-t default \
	-m inmem

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
. ./env.sh

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a xdocs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc commits.xml KEYS NOTICE
%attr(755,root,root) %{_bindir}/Xalan
%attr(755,root,root) %{_libdir}/libxalan-c.so.*.*
%attr(755,root,root) %{_libdir}/libxalanMsg.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxalan-c.so.111
%attr(755,root,root) %ghost %{_libdir}/libxalanMsg.so.111

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxalan-c.so
%attr(755,root,root) %{_libdir}/libxalanMsg.so
%{_includedir}/xalanc

%files docs
%defattr(644,root,root,755)
%{_docdir}/%{name}-docs-%{version}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
