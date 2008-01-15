%define name		linux-atm
%define major		1
%define libname		lib%{name}
%define fulllibname	%mklibname %{name} %{major}
%define version		2.4.1
%define release		%mkrel 11

Name:		%{name}
Version:	%{version}
Release:	%{release}
Summary:	Tools and libraries for ATM
License:	GPL
Group:		System/Libraries
Url:		http://linux-atm.sourceforge.net/
Source0:	http://prdownloads.sourceforge.net/linux-atm/%{name}-%{version}.tar.bz2
Patch0:		linux-atm-2.4.1-gcc3.4-fix.patch
Patch1:		linux-atm-2.4.1-libtool-fixes.patch
Patch2:		linux-atm-2.4.1-64bit-fixes.patch
Patch3:		linux-atm-2.4.1-gcc4.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	bison
BuildRequires:	flex
%if %{mdkversion} >= 1010
BuildRequires:	automake1.4
%endif

%description
Tools and libraries to support ATM (Asynchronous Transfer Mode)
networking and some types of DSL modems.

%package -n	%{fulllibname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{fulllibname}
This package contains libraries needed to run programs linked with %{name}.

%package -n	%{fulllibname}-devel
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{fulllibname} = %{version}-%{release}
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{fulllibname}-devel
This package contains development files needed to compile programs which
use %{name}.

%prep
%setup -q
%patch0 -p1 -b .gcc3.4
%patch1 -p1 -b .libtool-fixes
%patch2 -p1 -b .64bit-fixes
%patch3 -p1 -b .gcc4
# stick to built-in libtool 1.4
%define __libtoolize /bin/true
autoconf
automake-1.4 --foreign

%build
%configure2_5x --enable-shared
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%post -n %{fulllibname} -p /sbin/ldconfig

%postun -n %{fulllibname} -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog NEWS THANKS BUGS
%doc COPYING COPYING.GPL COPYING.LGPL
%config(noreplace) %{_sysconfdir}/atmsigd.conf
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man4/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files -n %{fulllibname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{fulllibname}-devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la

