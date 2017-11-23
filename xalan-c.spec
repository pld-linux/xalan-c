Summary:	C++ xslt library
Summary(pl.UTF-8):	Biblioteka xslt dla C++
Name:		xalan-c
Version:	1.11.0
Release:	1
License:	Apache v2.0
Group:		Applications/Publishing/XML
Source0:	http://www.apache.org/dist/xalan/xalan-c/sources/xalan_c-1.11-src.tar.gz
# Source0-md5:	9227d3e7ab375da3c643934b33a585b8
Patch1:		%{name}-soname.patch
URL:		https://xalan.apache.org/
BuildRequires:	util-linux
BuildRequires:	xerces-c-devel >= 3.1.1
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
%setup -q -n xalan-c-1.11
%patch1 -p1

sed -i -e 's#debugflag=".*";#debugflag="%{rpmcflags} %{rpmcppflags}";#' c/runConfigure

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

%build
cd c
# create env.sh for easier debug from console
cat << EOF > env.sh
export XALANCROOT=$(pwd)
export XERCESCROOT=%{_prefix}
export ICUROOT=%{_prefix}
EOF

. ./env.sh

./runConfigure \
	-C "--libdir=%{_libdir}" \
	-P %{_prefix} \
	-p linux \
	-c "%{__cc}" \
	-x "%{__cxx}" \
%ifarch %{x8664} aarch64 alpha ppc64 s390x sparc64
	-b 64 \
%else
	-b 32 \
%endif
	-t default \
	-m inmem

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

cd c

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
%doc c/{KEYS,NOTICE,README}
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
