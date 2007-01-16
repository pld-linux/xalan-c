%define		_ver	%(echo %{version} | tr . _)
Summary:	XML parser
Summary(pl):	Analizator sk³adniowy XML-a
Name:		xalan-c
Version:	1.10.0
Release:	0.1
License:	Apache License, Version 2.0
Group:		Applications/Publishing/XML
Source0:	http://www.apache.org/dist/xml/xalan-c/Xalan-C_%{_ver}-src.tar.gz
# Source0-md5:	0a3fbb535885531cc544b07a2060bfb1
Patch0:	%{name}-getopt.patch
URL:		http://xalan.apache.org/
BuildRequires:	autoconf
BuildRequires:	util-linux
BuildRequires:	xerces-c >= 2.7.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apache Xalan Project is a collaborative software development project
dedicated to providing robust, full-featured, commercial-quality, and
freely available XSLT support on a wide variety of platforms.

%description -l pl
Analizator sk³adniowy XML-a.

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

%if 1
./runConfigure \
	-p linux \
	-c "%{__cc}" \
	-x "%{__cxx}" \
	-minmem

%{__make}
%endif

# passes CC correctly but broken
%if 0
%ifarch %{x8664}
CXXFLAGS=-DXML_BITSTOBUILD_64
CFLAGS=-DXML_BITSTOBUILD_64
BITSTOBUILD=64
%else
BITSTOBUILD=32
%endif
%configure
%{__make} \
	LIBS="-lpthread" \
	LDFLAGS="%{rpmcflags}" \
	CXXFLAGS="%{rpmcxxflags} $CXXFLAGS" \
	CFLAGS="%{rpmcxxflags} $CFLAGS" \
	CC="%{__cc}" \
	CXX="%{__cxx}" \
	XALAN_LOCALE_SYSTEM=inmem \
	XALAN_LOCALE=en_US \
	BITSTOBUILD=$BITSTOBUILD \
	TRANSCODER= \
%endif

%install
rm -rf $RPM_BUILD_ROOT
cd c/src
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}
install -d $RPM_BUILD_ROOT%{_includedir}

# Only one file?
cp -a ../../lib/* $RPM_BUILD_ROOT%{_libdir}

# I put all stuff from that dir, maybe some can be omitted
cp -a Include/* $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
#%%{_libdir}/*.so

%files docs
%defattr(644,root,root,755)
%doc c/docs c/samples
