Summary:	C++ xslt library
Summary(pl.UTF-8):	Biblioteka xslt dla C++
Name:		xalan-c
Version:	1.12
Release:	1
License:	Apache v2.0
Group:		Applications/Publishing/XML
Source0:	https://downloads.apache.org/xalan/xalan-c/sources/xalan_c-%{version}.tar.gz
# Source0-md5:	fa4fd34a03ae389b26166c5455b90768
Patch0:		cxx17.patch
URL:		https://xalan.apache.org/
BuildRequires:	cmake >= 3.2
BuildRequires:	doxygen
BuildRequires:	libicu-devel
BuildRequires:	libstdc++-devel >= 6:8
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
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
BuildArch:	noarch

%description examples
xalan-c examples.

%description examples -l pl.UTF-8
Przykłady dla xalan-c.

%prep
%setup -q -n xalan_c-%{version}
%patch -P0 -p1

%build
install -d build
cd build
%cmake ..

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/api

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -pr samples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc KEYS NOTICE README.md readme.html
%attr(755,root,root) %{_bindir}/Xalan
%attr(755,root,root) %{_libdir}/libxalan-c.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxalan-c.so.112
%attr(755,root,root) %{_libdir}/libxalanMsg.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libxalanMsg.so.112

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libxalan-c.so
%attr(755,root,root) %{_libdir}/libxalanMsg.so
%{_includedir}/xalanc
%{_pkgconfigdir}/xalan-c.pc
%{_libdir}/cmake/XalanC

%files docs
%defattr(644,root,root,755)
%doc build/docs/doxygen/api/{*.css,*.html,*.js,*.png,*.svg}

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
