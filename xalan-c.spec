Summary:	XML parser
Summary(pl):	Parser XML
Name:		xalan-c
Version:	0.40.0
%define	ver	0_40_0
%define	mainver	0_40_0
%define icuver	1.6
Release:	1
License:	GPL
Group:		Applications/Publishing/XML
Group(de):	Applikationen/Publizieren/XML
Group(pl):	Aplikacje/Publikowanie/XML
Source0:	http://xml.apache.org/dist/xerces-c/stable/Xalan-C_%{ver}-linux.tar.gz
Source1:	http://oss.software.ibm.com/developerworks/opensource/icu/project/download/%{icuver}/icu-%{icuver}.tgz
URL:		http://xml.apache.org
BuildRequires:	autoconf
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description

%description -l pl

%package devel
Summary:	%{name} header files
Summary(pl):	Pliki nagЁСwkowe %{name}
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	Разработка/Библиотеки
Group(uk):	Розробка/Б╕бл╕отеки
Requires:	%{name} = %{version}

%description devel
%{name} header files and documentation.

%description -l pl devel
Pliki nagЁСwkowe i dokumentacja %{name}.

%prep
%setup -q -n xml-xalan/c/src

%build
#chmod 755 configure config.{guess,status,sub}

## Just another shit!!!

export XALANCROOT=`cd ../.. ; pwd`
export XERCESCROOT="%{_includedir}"
autoconf
chmod 755 runConfigure
./runConfigure -plinux -cgcc -xg++ -minmem -nfileonly -tnative
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{_libdir}
install -d $RPM_BUILD_ROOT/%{_includedir}

# Only one file?
cp -a ../lib/* $RPM_BUILD_ROOT%{_libdir}

# I put all stuff from that dir, maybe some can be omitted
cp -a ../include/* $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/*

%files devel
%defattr(644,root,root,755)
%doc ../doc/html ../samples
%{_includedir}/*
##%{_libdir}/*.so
