%define major 1
%define libname %mklibname atm %{major}
%define develname %mklibname atm -d

Summary:	Tools and libraries for ATM networking
Name:		linux-atm
Version:	2.5.1
Release:	5
License:	GPLv2+
Group:		System/Configuration/Networking
Url:		http://linux-atm.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/linux-atm/linux-atm/%{version}/%{name}-%{version}.tgz
Patch1:		linux-atm-2.5.0-format_not_a_string_literal_and_no_format_arguments.patch
Patch4:		linux-atm-2.5.0-open-macro.patch
Patch5:		linux-atm-2.5.0-disable-ilmdiag.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	byacc

%description
Tools and libraries to support ATM (Asynchronous Transfer Mode)
networking and some types of DSL modems.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%{mklibname %{name} 1} < 2.5.1

%description -n	%{libname}
This package contains libraries needed to run programs linked with %{name}.

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libatm-devel = %{version}-%{release}
Provides:	atm-devel = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1 -d

%description -n	%{develname}
This package contains development files needed to compile programs which
use %{name}.

%prep

%setup -q
%patch1 -p1
%patch4 -p1
%patch5 -p1

%build
#fix build with new automake
sed -i -e 's,AM_CONFIG_HEADER,AC_CONFIG_HEADERS,g' configure.*
autoreconf -fi
%configure2_5x \
	--enable-shared \
	--enable-cisco \
	--enable-mpoa_1_1 \
	--enable-multipoint

%make -j1

%install
%makeinstall_std

install -m 0644 src/config/hosts.atm %{buildroot}/etc/

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%doc README AUTHORS ChangeLog NEWS THANKS BUGS
%config(noreplace) %{_sysconfdir}/atmsigd.conf
%config(noreplace) %{_sysconfdir}/hosts.atm
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man4/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so


%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-4mdv2011.0
+ Revision: 666080
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 2.5.1-3mdv2011.0
+ Revision: 606410
- rebuild

* Sun Jan 03 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.1-2mdv2010.1
+ Revision: 485930
- disable parallel make as it fails sometimes

* Sun Dec 06 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.1-1mdv2010.1
+ Revision: 474152
- drop patch0, fixed by upstream
- update to new version 2.5.1

* Sat Oct 10 2009 Olivier Blin <oblin@mandriva.com> 2.5.0-8mdv2010.0
+ Revision: 456531
- fix group

* Wed Sep 02 2009 Christophe Fergeau <cfergeau@mandriva.com> 2.5.0-7mdv2010.0
+ Revision: 425980
- rebuild

* Fri Feb 06 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-6mdv2009.1
+ Revision: 338301
- Patch1: fix compiling with -Werror=format-security

* Sat Jul 12 2008 Oden Eriksson <oeriksson@mandriva.com> 2.5.0-5mdv2009.0
+ Revision: 234005
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Jan 31 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-3mdv2008.1
+ Revision: 160947
- realy obsolete older devel library

* Thu Jan 31 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 2.5.0-2mdv2008.1
+ Revision: 160935
- add more provides on devel package
- new version 2.5.0
- new license policy
- new devel library policy (Warning! library is now called libatm)
- drop not needed patches 0,1,2,3
- add two Fedora's patches 4 and 5
- enable support for cisco routers
- enable support for Multi Protocol over ATM (MPOA 1.1)
- spec file clean and fix file list

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild
    - rebuild
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Sun Apr 30 2006 Stefan van der Eijk <stefan@mandrake.org> 2.4.1-9mdk
- %%mkrel
- rebuild for sparc
- add URL to Source0

* Mon Aug 22 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 2.4.1-8mdk
- gcc4 fixes mostly from fedora

* Thu Dec 30 2004 Stefan van der Eijk <stefan@mandrake.org> 2.4.1-7mdk
- BuildRequires: byacc --> bison

* Mon Nov 15 2004 Stefan van der Eijk <stefan@mandrake.org> 2.4.1-6mdk
- BuildRequires

* Wed Oct 06 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 2.4.1-5mdk
- libtool & 64-bit fixes

* Tue Jun 08 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 2.4.1-4mdk
- fix gcc-3.4 build (P0)
- wipe out buildroot at the beginning of %%install, not %%prep

* Fri Aug 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.4.1-3mdk
- rebuild

* Tue Jul 08 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.4.1-2mdk
- rebuild for new rpm devel computation

* Fri Jun 13 2003 Guillaume Rousse <guillomovitch@linux-mandrake.com> 2.4.1-1mdk
- 2.4.1

