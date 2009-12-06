%define major 1
%define libname %mklibname atm %{major}
%define develname %mklibname atm -d

Summary:	Tools and libraries for ATM networking
Name:		linux-atm
Version:	2.5.1
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Configuration/Networking
Url:		http://linux-atm.sourceforge.net/
Source0:	http://downloads.sourceforge.net/project/linux-atm/linux-atm/%{version}/%{name}-%{version}.tgz
Patch1:		linux-atm-2.5.0-format_not_a_string_literal_and_no_format_arguments.patch
Patch4:		linux-atm-2.5.0-open-macro.patch
Patch5:		linux-atm-2.5.0-disable-ilmdiag.patch
BuildRequires:	bison
BuildRequires:	flex
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Tools and libraries to support ATM (Asynchronous Transfer Mode)
networking and some types of DSL modems.

%package -n %{libname}
Summary:	Libraries for %{name}
Group:		System/Libraries
Provides:	%{name} = %{version}-%{release}
Obsoletes:	%mklibname %{name} 1

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
%configure2_5x \
	--enable-shared \
	--enable-cisco \
	--enable-mpoa_1_1 \
	--enable-multipoint \
	--with-kernel-headers=%{_includedir}

%make

%install
rm -rf %{buildroot}
%makeinstall_std

install -m 0644 src/config/hosts.atm %{buildroot}/etc/

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog NEWS THANKS BUGS
%config(noreplace) %{_sysconfdir}/atmsigd.conf
%config(noreplace) %{_sysconfdir}/hosts.atm
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man4/*
%{_mandir}/man7/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/*.so
%{_libdir}/*.la
