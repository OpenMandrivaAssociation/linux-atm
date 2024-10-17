%define major 1
%define libname %mklibname atm %{major}
%define devname %mklibname atm -d
%define _disable_lto 1

Summary:	Tools and libraries for ATM networking
Name:		linux-atm
Version:	2.5.2
Release:	17
License:	GPLv2+
Group:		System/Configuration/Networking
Url:		https://linux-atm.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/linux-atm/linux-atm/%{version}/%{name}-%{version}.tar.gz
Patch1:		linux-atm-2.5.0-format_not_a_string_literal_and_no_format_arguments.patch
Patch4:		linux-atm-2.5.0-open-macro.patch
Patch5:		linux-atm-2.5.0-disable-ilmdiag.patch
Patch6:		0001-saaldump-atmdump-Include-linux-sockios.h-for-SIOCGST.patch
BuildRequires:	bison
BuildRequires:	flex-devel

%description
Tools and libraries to support ATM (Asynchronous Transfer Mode)
networking and some types of DSL modems.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}

%description -n	%{libname}
This package contains libraries needed to run programs linked with %{name}.

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	atm-devel = %{version}-%{release}

%description -n	%{devname}
This package contains development files needed to compile programs which
use %{name}.

%prep
%autosetup -p1

sed -i -e 's#$(DESTDIR)/lib/firmware#/$(DESTDIR)/%{_prefix}/lib/firmware#g' src/extra/Makefile.*
sed -i '/#define _LINUX_NETDEVICE_H/d' \
	src/arpd/*.c
%build
%configure \
	--disable-static \
	--enable-shared \
	--enable-cisco \
	--enable-mpoa_1_1 \
	--enable-multipoint

%make_build

%install
%make_install

install -m 0644 src/config/hosts.atm %{buildroot}/etc/

%files
%doc README AUTHORS NEWS THANKS BUGS
%config(noreplace) %{_sysconfdir}/atmsigd.conf
%config(noreplace) %{_sysconfdir}/hosts.atm
%{_bindir}/*
%{_prefix}/lib/firmware/*.bin*
%doc %{_mandir}/man4/*
%doc %{_mandir}/man7/*
%doc %{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/libatm.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so

