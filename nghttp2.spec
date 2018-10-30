%{?scl:%scl_package nghttp2}
%{!?scl:%global pkg_name %{name}}

Summary: Meta-package that only requires libnghttp2
Name: %{?scl_prefix}nghttp2
Version: 1.7.1
Release: 7%{?dist}
License: MIT
Group: Applications/Internet
URL: https://nghttp2.org/
Source0: https://github.com/tatsuhiro-t/nghttp2/releases/download/v%{version}/nghttp2-%{version}.tar.xz
Patch0: nghttp2-1.7.0-httpd24.patch

BuildRequires: CUnit-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
%{?scl:BuildRequires: %{scl}-runtime}

Requires: %{?scl_prefix}libnghttp2%{?_isa} = %{version}-%{release}

%description
This package installs no files.  It only requires the %{?scl_prefix}libnghttp2 package.


%package -n %{?scl_prefix}libnghttp2
Summary: A library implementing the HTTP/2 protocol
Group: Development/Libraries
%{?scl:Requires: %scl_runtime}

%description -n %{?scl_prefix}libnghttp2
libnghttp2 is a library implementing the Hypertext Transfer Protocol
version 2 (HTTP/2) protocol in C.


%package -n %{?scl_prefix}libnghttp2-devel
Summary: Files needed for building applications with libnghttp2
Group: Development/Libraries
Requires: %{?scl_prefix}libnghttp2%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n %{?scl_prefix}libnghttp2-devel
The libnghttp2-devel package includes libraries and header files needed
for building applications with libnghttp2.


%prep
%setup -q -n %{pkg_name}-%{version}

%patch0 -p1 -b .httpd24

%build
%{?scl:scl enable %{scl} - << \EOF}

%configure                                  \
    --disable-python-bindings               \
    --disable-static                        \
    --without-libxml2                       \
    --without-spdylay                       \
    --disable-app                           \
    --disable-examples

# avoid using rpath
sed -i libtool                              \
    -e 's/^runpath_var=.*/runpath_var=/'    \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/'

make %{?_smp_mflags} V=1
%{?scl:EOF}


%install
%{?scl:scl enable %{scl} - << \EOF}
%make_install

# not needed on Fedora/RHEL
rm -f "$RPM_BUILD_ROOT%{_libdir}/libnghttp2.la"

# will be installed via %%doc
rm -f "$RPM_BUILD_ROOT%{_datadir}/doc/nghttp2/README.rst"

# do not install man pages and helper scripts for tools that are not available
rm -fr "$RPM_BUILD_ROOT%{_datadir}/nghttp2"
rm -fr "$RPM_BUILD_ROOT%{_mandir}/man1"

mv %{buildroot}%{_libdir}/pkgconfig/libnghttp2.pc %{buildroot}%{_libdir}/pkgconfig/%{scl_prefix}libnghttp2.pc
%{?scl:EOF}

%post -n %{?scl_prefix}libnghttp2 -p /sbin/ldconfig

%postun -n %{?scl_prefix}libnghttp2 -p /sbin/ldconfig


%check
%{?scl:scl enable %{scl} - << \EOF}
# test the just built library instead of the system one, without using rpath
export "LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:${LD_LIBRARY_PATH}"
make %{?_smp_mflags} check
%{?scl:EOF}


%files

%files -n %{?scl_prefix}libnghttp2
%{_libdir}/libnghttp2*.so.*
%{!?_licensedir:%global license %%doc}
%license COPYING

%files -n %{?scl_prefix}libnghttp2-devel
%{_includedir}/nghttp2
%{_libdir}/pkgconfig/%{scl_prefix}libnghttp2.pc
%{_libdir}/libnghttp2*.so
%doc README.rst


%changelog
* Thu Sep 13 2018 Luboš Uhliarik <luhliari@redhat.com> - 1.7.1-7
- Resolves: #1540167 - provides without httpd24 pre/in-fix

* Wed May 24 2017 Luboš Uhliarik <luhliari@redhat.com> - 1.7.1-6
- rebuild

* Wed Feb 17 2016 Jan Kaluza <jkaluza@redhat.com> 1.7.1-1
- fix CVE-2016-1544 (out of memory due to unlimited incoming HTTP header)

* Tue Feb 09 2016 Jan Kaluza <jkaluza@redhat.com> 1.7.0-3
- make the package build on RHEL-6 (libnghttp2 only)

* Mon Feb 08 2016 Jan Kaluza <jkaluza@redhat.com> 1.7.0-2
- enable tests

* Mon Jan 25 2016 Kamil Dudka <kdudka@redhat.com> 1.7.0-1
- update to the latest upstream release

* Fri Dec 25 2015 Kamil Dudka <kdudka@redhat.com> 1.6.0-1
- update to the latest upstream release (fixes CVE-2015-8659)

* Thu Nov 26 2015 Kamil Dudka <kdudka@redhat.com> 1.5.0-1
- update to the latest upstream release

* Mon Oct 26 2015 Kamil Dudka <kdudka@redhat.com> 1.4.0-1
- update to the latest upstream release

* Thu Sep 24 2015 Kamil Dudka <kdudka@redhat.com> 1.3.4-1
- update to the latest upstream release

* Wed Sep 23 2015 Kamil Dudka <kdudka@redhat.com> 1.3.3-1
- update to the latest upstream release

* Wed Sep 16 2015 Kamil Dudka <kdudka@redhat.com> 1.3.2-1
- update to the latest upstream release

* Mon Sep 14 2015 Kamil Dudka <kdudka@redhat.com> 1.3.1-1
- update to the latest upstream release

* Mon Aug 31 2015 Kamil Dudka <kdudka@redhat.com> 1.3.0-1
- update to the latest upstream release

* Mon Aug 17 2015 Kamil Dudka <kdudka@redhat.com> 1.2.1-1
- update to the latest upstream release

* Sun Aug 09 2015 Kamil Dudka <kdudka@redhat.com> 1.2.0-1
- update to the latest upstream release

* Wed Jul 15 2015 Kamil Dudka <kdudka@redhat.com> 1.1.1-1
- update to the latest upstream release

* Tue Jun 30 2015 Kamil Dudka <kdudka@redhat.com> 1.0.5-1
- packaged for Fedora (#1237247)
