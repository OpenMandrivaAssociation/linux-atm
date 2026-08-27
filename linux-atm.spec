%define major 1
%define libname %mklibname atm %{major}
%define devname %mklibname atm -d
%define _disable_lto 1
%global optflags %{optflags} -Wno-error -Wno-implicit-function-declaration
%global optflags %{optflags} -Wno-incompatible-function-pointer-types
%global optflags %{optflags} -Wno-incompatible-pointer-types

Summary:	Tools and libraries for ATM networking
Name:		linux-atm
Version:	2.5.2
Release:	18
License:	GPLv2+
Group:		System/Configuration/Networking
Url:		https://linux-atm.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/linux-atm/linux-atm/%{version}/%{name}-%{version}.tar.gz
Patch1:		linux-atm-2.5.0-format_not_a_string_literal_and_no_format_arguments.patch
Patch4:		linux-atm-2.5.0-open-macro.patch
Patch5:		linux-atm-2.5.0-disable-ilmdiag.patch
Patch6:		0001-saaldump-atmdump-Include-linux-sockios.h-for-SIOCGST.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool-base
BuildRequires:	slibtool
BuildRequires:	make
BuildRequires:	bison
BuildRequires:	flex

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

# Kernel 7.2 keeps ATM PVC + PPPoA + BR2684. CLIP/LANE/MPOA, SVC
# signaling, and the old PCI card tools have no in-tree ABI anymore.
# Remaining tree has no flex scanners, so target libfl is not needed.
# Edit Makefile.in too: shipped automake files are older than the
# builder, so %%configure does not regenerate them.
# Automake bakes program lists into am__EXEEXT_*; changing BOOTPGMS
# alone is not enough.
sed -i '/^SUBDIRS = /,/br2684$/c\
SUBDIRS = include lib maint man config br2684' src/Makefile.am src/Makefile.in
sed -i \
	-e 's/^BOOTPGMS =.*/BOOTPGMS = esi/' \
	-e 's/^SYSPGMS =.*/SYSPGMS = atmloop/' \
	-e 's/^USRPGMS =.*/USRPGMS = atmdiag atmdump sonetdiag/' \
	-e 's/^man_MANS = .*/man_MANS = atmdiag.8 atmdump.8 atmloop.8 esi.8/' \
	src/maint/Makefile.am src/maint/Makefile.in
sed -i '/^am__EXEEXT_1 = /,/saaldump/c\
am__EXEEXT_1 = atmdiag$(EXEEXT) atmdump$(EXEEXT) sonetdiag$(EXEEXT)' \
	src/maint/Makefile.in
sed -i \
	-e 's/^am__EXEEXT_2 = .*/am__EXEEXT_2 = esi$(EXEEXT)/' \
	-e '/^am__EXEEXT_3 = /,/hediag/c\
am__EXEEXT_3 = atmloop$(EXEEXT)' \
	src/maint/Makefile.in
touch src/Makefile.in src/maint/Makefile.in

%build
%configure \
	--disable-static \
	--enable-shared

%make_build

%install
%make_install

install -m 0644 src/config/hosts.atm %{buildroot}/etc/

%files
%doc README AUTHORS NEWS THANKS BUGS
%config(noreplace) %{_sysconfdir}/hosts.atm
%{_bindir}/esi
%{_bindir}/atmloop
%{_bindir}/atmdiag
%{_bindir}/atmdump
%{_bindir}/sonetdiag
%{_bindir}/br2684ctl
%doc %{_mandir}/man7/qos.7*
%doc %{_mandir}/man7/sap.7*
%doc %{_mandir}/man8/esi.8*
%doc %{_mandir}/man8/atmloop.8*
%doc %{_mandir}/man8/atmdiag.8*
%doc %{_mandir}/man8/atmdump.8*
%doc %{_mandir}/man8/br2684ctl.8*

%files -n %{libname}
%{_libdir}/libatm.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so

