%define		ver	%(echo %{version} | tr . _)
Summary:	C++ xslt library
Summary(pl.UTF-8):	Biblioteka xslt dla C++
Name:		xalan-c
Version:	1.10.0
Release:	8
License:	Apache v2.0
Group:		Applications/Publishing/XML
Source0:	http://www.apache.org/dist/xml/xalan-c/Xalan-C_%{ver}-src.tar.gz
# Source0-md5:	0a3fbb535885531cc544b07a2060bfb1
Patch0:		%{name}-getopt.patch
Patch1:		%{name}-soname.patch
Patch2:		%{name}-include.patch
Patch3:		icu-4.2.patch
URL:		http://xml.apache.org/xalan-c/
BuildRequires:	icu
BuildRequires:	libicu-devel >= 4.2
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

%description devel -l pl.UTF-8
Przykłady dla xalan-c.

%prep
%setup -qc
mv xml-xalan/c/* .
%patch0 -p2
%patch1 -p2
%patch2 -p2
%patch3 -p1

%if "%{_lib}" != "lib"
sed -i -e 's#/lib/icu/pkgdata.inc#/%{_lib}/icu/pkgdata.inc#' \
	src/xalanc/Utils/Makefile.in
%endif

find xdocs samples -name CVS | xargs rm -rf

%build
# create env.sh for easier debug from console
cat << EOF > env.sh
export XALANCROOT=$(pwd)
export XERCESROOT=%{_prefix}
export ICUROOT=%{_prefix}
EOF

. ./env.sh

./runConfigure \
	-P %{_prefix} \
	-p linux \
	-c "%{__cc}" \
	-x "%{__cxx}" \
%ifarch %{x8664} alpha ppc64 s390x sparc64
	-b 64 \
%else
	-b 32 \
%endif
	-t icu \
	-m icu

# force 1 jobserver: tries to link testXSLT before libxalan-c.so symlink is created.
# having XALAN_USE_ICU set on install will copy libicu libs to xalan install
# root, so set it on build only.
%{__make} -j1 \
	XALAN_USE_ICU=true

%install
rm -rf $RPM_BUILD_ROOT
. ./env.sh

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}
install -d $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

cp -a samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a xdocs/* $RPM_BUILD_ROOT%{_docdir}/%{name}-docs-%{version}

%if "%{_lib}" != "lib"
mv $RPM_BUILD_ROOT%{_prefix}/lib/* $RPM_BUILD_ROOT%{_libdir}
%endif

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
%attr(755,root,root) %ghost %{_libdir}/libxalan-c.so.110
%attr(755,root,root) %ghost %{_libdir}/libxalanMsg.so.110

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
