#
%define		_ver	%(echo %{version} | tr . _)
Summary:	XML parser
Summary(pl):	Analizator sk³adniowy XML-a
Name:		xalan-c
Version:	1.10.0
Release:	0.2
License:	Apache License, Version 2.0
Group:		Applications/Publishing/XML
Source0:	http://www.apache.org/dist/xml/xalan-c/Xalan-C_%{_ver}-src.tar.gz
# Source0-md5:	0a3fbb535885531cc544b07a2060bfb1
Patch0:		%{name}-getopt.patch
URL:		http://xalan.apache.org/
BuildRequires:	icu
BuildRequires:	libicu-devel
BuildRequires:	util-linux
BuildRequires:	xerces-c-devel >= 2.7.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache Xalan Project is a collaborative software development project
dedicated to providing robust, full-featured, commercial-quality, and
freely available XSLT support on a wide variety of platforms.

%description -l pl
Projekt Apache Xalan to wspólny projekt stworzenia oprogramowania
maj±cego zapewnic potê¿n±, w pe³ni funkcjonaln±, maj±c± komercyjn±
jako¶æ i jednocze¶nie wolnodostêpn± obs³ugê XSLT na szerokim zakresie
platform.

%package devel
Summary:	xalan-c header files
Summary(pl):	Pliki nag³ówkowe xalan-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
xalan-c header files.

%description devel -l pl
Pliki nag³ówkowe xalan-c.

%package docs
Summary:	Documentation for xalan-c
Summary(pl):	Dokumentacja xlan-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description docs
Documentation for xalan-c.

%description docs -l pl
Dokumentacja xalan-c.

%prep
%setup -q -n xml-xalan
%patch0 -p1

%build
cd c
export XALANCROOT=$(pwd)
export XERCESROOT=/usr
export ICUROOT=/usr
export XALAN_USE_ICU=true

./runConfigure \
	-P /usr \
	-p linux \
	-c "%{__cc}" \
	-x "%{__cxx}" \
%ifarch %{x8664}
	-b 64 \
%else
	-b 32 \
%endif
	-t icu \
	-m icu

# tries to link testXSLT before libxalan-c.so symlink is created
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
cd c
export XALANCROOT=$(pwd)
export XERCESROOT=/usr
export ICUROOT=/usr

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/Xalan
%attr(755,root,root) %{_libdir}/libxalan*

%files devel
%defattr(644,root,root,755)
%{_includedir}/xalanc

%files docs
%defattr(644,root,root,755)
%doc c/xdocs c/samples
