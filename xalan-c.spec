%define	ver	1_2
%define	mainver	1_2
Summary:	XML parser
Summary(pl):	Analizator składniowy XML-a
Name:		xalan-c
Version:	1.2
Release:	1
License:	GPL
Group:		Applications/Publishing/XML
#Source0:	http://xml.apache.org/dist/xerces-c/stable/Xalan-C_%{ver}-linux.tar.gz
Source0:	http://xml.apache.org/dist/xalan-c/Xalan-C_%{ver}-linux.tar.gz
# Source0-md5:	021c981373d7a28a8420c2462dbc4ebb
Patch0:		%{name}-xerces_ver.patch
URL:		http://xml.apache.org/
BuildRequires:	autoconf
BuildRequires:	xerces-c
# Needs "tr".
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
XML parser.

%description -l pl
Analizator składniowy XML-a.

%package devel
Summary:	xalan-c header files
Summary(pl):	Pliki nagłówkowe xalan-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
xalan-c header files.

%description devel -l pl
Pliki nagłówkowe xalan-c.

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
# Binaries provided with sources.
rm -rf c/{bin,lib}/*
# We don't need it, so why waste space?
rm -rf ../xerces-c1_5_1-linux

%build
cd c/src
#chmod 755 configure config.{guess,status,sub}

## Just another shit!!!

export XALANCROOT=`cd ../.. ; pwd`
export XERCESCROOT="%{_includedir}"
#autoconf
#CPPFLAGS="-Iinclude"
#export CPPFLAGS
chmod 755 runConfigure
./runConfigure -plinux -cgcc -xg++ -minmem -nfileonly -tnative
%{__make} XERCES_VER=`rpm -q xerces-c --qf '%%{version}' | tr . _`

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
