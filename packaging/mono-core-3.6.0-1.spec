%define ext_man .gz

# Without this, we get: ERROR: No build ID note found in **.dll.so
%define debug_package %{nil}

%define llvm no
%define sgen yes

Name:           mono-core
License:        LGPL v2.1 only
Group:          Development/Languages/Mono
Summary:        A .NET Runtime Environment
Url:            http://www.mono-project.com
Version:        3.6.0
Release:        0
Source0:        mono-%{version}.tar.bz2
BuildRequires:  bison
BuildRequires:  fdupes
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig
BuildRequires:  xorg-x11-libX11-devel
BuildRequires:  zlib-devel
%ifnarch ia64
BuildRequires:  valgrind-devel
%endif
%if %llvm == yes
BuildRequires:  llvm-mono-devel
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Obsoletes:      mono
Obsoletes:      mono-cairo
Obsoletes:      mono-drawing
Obsoletes:      mono-ikvm
Obsoletes:      mono-posix
Obsoletes:      mono-xml-relaxng
Obsoletes:      mono-ziplib
Provides:       mono = %{version}-%{release}
Provides:       mono-cairo
Provides:       mono-drawing
Provides:       mono-ikvm
Provides:       mono-posix
Provides:       mono-xml-relaxng
Provides:       mono-ziplib
# This version of mono has issues with the following versions of apps:
#  (not because of regressions, but because bugfixes in mono uncover bugs in the apps)
Conflicts:      banshee < 1.0
Conflicts:      f-spot < 0.4
Conflicts:      helix-banshee < 1.0
Conflicts:      mono-addins < 0.3.1
Provides:       mono(Commons.Xml.Relaxng) = 1.0.5000.0
Provides:       mono(CustomMarshalers) = 1.0.5000.0
Provides:       mono(I18N) = 1.0.5000.0
Provides:       mono(I18N.West) = 1.0.5000.0
Provides:       mono(ICSharpCode.SharpZipLib) = 0.6.0.0
Provides:       mono(ICSharpCode.SharpZipLib) = 0.84.0.0
Provides:       mono(Mono.Cairo) = 1.0.5000.0
Provides:       mono(Mono.CompilerServices.SymbolWriter) = 1.0.5000.0
Provides:       mono(Mono.Posix) = 1.0.5000.0
Provides:       mono(Mono.Security) = 1.0.5000.0
Provides:       mono(System) = 1.0.5000.0
Provides:       mono(System.Security) = 1.0.5000.0
Provides:       mono(System.Xml) = 1.0.5000.0
Provides:       mono(mscorlib) = 1.0.5000.0

%define _use_internal_dependency_generator 0
%define __find_provides env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-provides && printf "%s\\n" "${filelist[@]}" | prefix=%{buildroot}%{_prefix} %{buildroot}%{_bindir}/mono-find-provides ; } | sort -u'
%define __find_requires env sh -c 'filelist=($(cat)) && { printf "%s\\n" "${filelist[@]}" | /usr/lib/rpm/find-requires && printf "%s\\n" "${filelist[@]}" | prefix=%{buildroot}%{_prefix} %{buildroot}%{_bindir}/mono-find-requires ; } | sort -u'

%description
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

%prep
%setup -q -n mono-%{version}

%build
# These are only needed if there are patches to the runtime
#rm -f libgc/libtool.m4
#autoreconf --force --install
#autoreconf --force --install libgc
export CFLAGS=" $RPM_OPT_FLAGS -fno-strict-aliasing"
# distro specific configure options
%if %llvm == yes
export PATH=/opt/novell/llvm-mono/bin:$PATH
%endif
%configure \
  --with-sgen=%{sgen} \
%if %llvm == yes
  --enable-loadedllvm \
  --disable-system-aot \
%endif
  --with-ikvm=yes \
  --with-moonlight=no
#make # We are not -jN safe! %{?jobs:-j%jobs}
# We are now !
make %{?_smp_mflags}

%install
make install DESTDIR=%buildroot
# remove .la files (they are generally bad news)
rm -f %buildroot%_libdir/*.la
# remove Windows-only stuff
rm -rf %buildroot%_prefix/lib/mono/*/Mono.Security.Win32*
rm -f %buildroot%_libdir/libMonoSupportW.*
# remove .a files for libraries that are really only for us
rm -f %buildroot%_libdir/libMonoPosixHelper.a
rm -f %buildroot%_libdir/libikvm-native.a
rm -f %buildroot%_libdir/libmono-llvm.a
# remove libgc cruft
rm -rf %buildroot%_datadir/libgc-mono
# remove stuff that we don't package
rm -f %buildroot%_bindir/cilc
rm -f %buildroot%_mandir/man1/cilc.1*
rm -f %buildroot%_prefix/lib/mono/*/browsercaps-updater.exe*
rm -f %buildroot%_prefix/lib/mono/*/culevel.exe*
rm -f %buildroot%_prefix/lib/mono/2.0/cilc.exe*
# brp-compress doesn't search _mandir
# so we cheat it
ln -s . %buildroot%_prefix%_prefix
RPM_BUILD_ROOT=%buildroot%_prefix /usr/lib/rpm/brp-compress
rm %buildroot%_prefix%_prefix
%fdupes %buildroot%_prefix
%find_lang mcs

%clean
rm -rf %buildroot

%files -f mcs.lang
%defattr(-, root, root)
%doc AUTHORS COPYING.LIB ChangeLog NEWS README.md
%config %_sysconfdir/mono/2.0/machine.config
%config %_sysconfdir/mono/2.0/settings.map
%config %_sysconfdir/mono/4.0/machine.config
%config %_sysconfdir/mono/4.0/settings.map
%config %_sysconfdir/mono/4.5/machine.config
%config %_sysconfdir/mono/4.5/settings.map
%config %_sysconfdir/mono/config
%dir %_prefix/lib/mono
%dir %_prefix/lib/mono/2.0
%dir %_prefix/lib/mono/3.5
%dir %_prefix/lib/mono/4.0
%dir %_prefix/lib/mono/4.5
%dir %_prefix/lib/mono/compat-2.0
%dir %_prefix/lib/mono/gac
%dir %_sysconfdir/mono
%dir %_sysconfdir/mono/2.0
%dir %_sysconfdir/mono/4.0
%dir %_sysconfdir/mono/4.5
%_bindir/al
%_bindir/al2
%_bindir/certmgr
%_bindir/chktrust
%_bindir/crlupdate
%_bindir/csharp
%_bindir/dmcs
%_bindir/gacutil
%_bindir/gacutil2
%_bindir/gmcs
%_bindir/ikdasm
%_bindir/mcs
%_bindir/mono
%_bindir/mono-configuration-crypto
%if %sgen == yes
%_bindir/mono-sgen
%endif
%_bindir/mono-boehm
%_bindir/mono-test-install
%_bindir/mozroots
%_bindir/peverify
%_bindir/setreg
%_bindir/sn
%_libdir/libMonoPosixHelper.so*
%_libdir/libikvm-native.so
%_mandir/man1/certmgr.1%ext_man
%_mandir/man1/chktrust.1%ext_man
%_mandir/man1/crlupdate.1%ext_man
%_mandir/man1/csharp.1%ext_man
%_mandir/man1/gacutil.1%ext_man
%_mandir/man1/mcs.1%ext_man
%_mandir/man1/mono-configuration-crypto.1%ext_man
%_mandir/man1/mono.1%ext_man
%_mandir/man1/mozroots.1%ext_man
%_mandir/man1/setreg.1%ext_man
%_mandir/man1/sn.1%ext_man
%_mandir/man5/mono-config.5%ext_man
%_prefix/lib/mono/2.0/Commons.Xml.Relaxng.dll
%_prefix/lib/mono/2.0/CustomMarshalers.dll
%_prefix/lib/mono/2.0/I18N.West.dll
%_prefix/lib/mono/2.0/I18N.dll
%_prefix/lib/mono/2.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/2.0/Microsoft.VisualC.dll
%_prefix/lib/mono/2.0/Mono.C5.dll
%_prefix/lib/mono/2.0/Mono.CSharp.dll
%_prefix/lib/mono/2.0/Mono.Cairo.dll
%_prefix/lib/mono/2.0/Mono.CompilerServices.SymbolWriter.dll
%_prefix/lib/mono/2.0/Mono.Management.dll
%_prefix/lib/mono/2.0/Mono.Posix.dll
%_prefix/lib/mono/2.0/Mono.Security.dll
%_prefix/lib/mono/2.0/Mono.Simd.dll
%_prefix/lib/mono/2.0/Mono.Tasklets.dll
%_prefix/lib/mono/2.0/System.Configuration.dll
%_prefix/lib/mono/2.0/System.Core.dll
%_prefix/lib/mono/2.0/System.Drawing.dll
%_prefix/lib/mono/2.0/System.Net.dll
%_prefix/lib/mono/2.0/System.Security.dll
%_prefix/lib/mono/2.0/System.Xml.Linq.dll
%_prefix/lib/mono/2.0/System.Xml.dll
%_prefix/lib/mono/2.0/System.dll
%_prefix/lib/mono/2.0/System.Json.dll
%_prefix/lib/mono/2.0/al.exe*
%_prefix/lib/mono/2.0/cscompmgd.dll
%_prefix/lib/mono/2.0/gacutil.exe*
%_prefix/lib/mono/2.0/mscorlib.dll*
%_prefix/lib/mono/4.0/Commons.Xml.Relaxng.dll
%_prefix/lib/mono/4.0/CustomMarshalers.dll
%_prefix/lib/mono/4.0/I18N.West.dll
%_prefix/lib/mono/4.0/I18N.dll
%_prefix/lib/mono/4.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/4.0/Microsoft.CSharp.dll
%_prefix/lib/mono/4.0/Microsoft.VisualC.dll
%_prefix/lib/mono/4.0/Mono.C5.dll
%_prefix/lib/mono/4.0/Mono.CSharp.dll
%_prefix/lib/mono/4.0/Mono.Cairo.dll
%_prefix/lib/mono/4.0/Mono.CompilerServices.SymbolWriter.dll
%_prefix/lib/mono/4.0/Mono.Management.dll
%_prefix/lib/mono/4.0/Mono.Parallel.dll
%_prefix/lib/mono/4.0/Mono.Posix.dll
%_prefix/lib/mono/4.0/Mono.Security.dll
%_prefix/lib/mono/4.0/Mono.Simd.dll
%_prefix/lib/mono/4.0/Mono.Tasklets.dll
%_prefix/lib/mono/4.0/System.Configuration.dll
%_prefix/lib/mono/4.0/System.Core.dll
%_prefix/lib/mono/4.0/System.Drawing.dll
%_prefix/lib/mono/4.0/System.Dynamic.dll
%_prefix/lib/mono/4.0/System.Json.dll
%_prefix/lib/mono/4.0/System.Json.Microsoft.dll
%_prefix/lib/mono/4.0/System.Net.dll
%_prefix/lib/mono/4.0/System.Numerics.dll
%_prefix/lib/mono/4.0/System.Security.dll
%_prefix/lib/mono/4.0/System.Xml.Linq.dll
%_prefix/lib/mono/4.0/System.Xml.dll
%_prefix/lib/mono/4.0/System.dll
%_prefix/lib/mono/4.5/al.exe*
%_prefix/lib/mono/4.5/certmgr.exe*
%_prefix/lib/mono/4.5/chktrust.exe*
%_prefix/lib/mono/4.5/crlupdate.exe*
%_prefix/lib/mono/4.0/cscompmgd.dll
%_prefix/lib/mono/4.5/csharp.exe*
%_prefix/lib/mono/4.5/gacutil.exe*
%_prefix/lib/mono/4.5/ikdasm.exe*
%_prefix/lib/mono/4.5/mcs.exe*
%_prefix/lib/mono/4.5/mozroots.exe*
%_prefix/lib/mono/4.0/mscorlib.dll*
%_prefix/lib/mono/4.5/setreg.exe*
%_prefix/lib/mono/4.5/sn.exe*
%_prefix/lib/mono/4.5/Commons.Xml.Relaxng.dll
%_prefix/lib/mono/4.5/CustomMarshalers.dll
%_prefix/lib/mono/4.5/I18N.CJK.dll
%_prefix/lib/mono/4.5/I18N.MidEast.dll
%_prefix/lib/mono/4.5/I18N.Other.dll
%_prefix/lib/mono/4.5/I18N.Rare.dll
%_prefix/lib/mono/4.5/I18N.West.dll
%_prefix/lib/mono/4.5/I18N.dll
%_prefix/lib/mono/4.5/IBM.Data.DB2.dll
%_prefix/lib/mono/4.5/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/4.5/Microsoft.CSharp.dll
%_prefix/lib/mono/4.5/Microsoft.VisualC.dll
%_prefix/lib/mono/4.5/Mono.C5.dll
%_prefix/lib/mono/4.5/Mono.CSharp.dll
%_prefix/lib/mono/4.5/Mono.Cairo.dll
%_prefix/lib/mono/4.5/Mono.CompilerServices.SymbolWriter.dll
%_prefix/lib/mono/4.5/Mono.Management.dll
%_prefix/lib/mono/4.5/Mono.Parallel.dll
%_prefix/lib/mono/4.5/Mono.Posix.dll
%_prefix/lib/mono/4.5/Mono.Security.dll
%_prefix/lib/mono/4.5/Mono.Simd.dll
%_prefix/lib/mono/4.5/Mono.Tasklets.dll
%_prefix/lib/mono/4.5/System.Configuration.dll
%_prefix/lib/mono/4.5/System.Core.dll
%_prefix/lib/mono/4.5/System.Drawing.dll
%_prefix/lib/mono/4.5/System.Dynamic.dll
%_prefix/lib/mono/4.5/System.IO.Compression.dll
%_prefix/lib/mono/4.5/System.IO.Compression.FileSystem.dll
%_prefix/lib/mono/4.5/System.Json.dll
%_prefix/lib/mono/4.5/System.Json.Microsoft.dll
%_prefix/lib/mono/4.5/System.Net.dll
%_prefix/lib/mono/4.5/System.Net.Http.dll
%_prefix/lib/mono/4.5/System.Net.Http.WebRequest.dll
%_prefix/lib/mono/4.5/System.Numerics.dll
%_prefix/lib/mono/4.5/System.Security.dll
%_prefix/lib/mono/4.5/System.Threading.Tasks.Dataflow.dll
%_prefix/lib/mono/4.5/System.Xml.Linq.dll
%_prefix/lib/mono/4.5/System.Xml.dll
%_prefix/lib/mono/4.5/System.dll
%_prefix/lib/mono/4.5/cscompmgd.dll
%_prefix/lib/mono/4.5/mscorlib.dll*
%_prefix/lib/mono/4.5/System.Windows.dll
%_prefix/lib/mono/4.5/System.Xml.Serialization.dll
%_prefix/lib/mono/4.5/Facades/*.dll
%_prefix/lib/mono/compat-2.0/ICSharpCode.SharpZipLib.dll
%_prefix/lib/mono/gac/Commons.Xml.Relaxng
%_prefix/lib/mono/gac/CustomMarshalers
%_prefix/lib/mono/gac/I18N
%_prefix/lib/mono/gac/I18N.West
%_prefix/lib/mono/gac/ICSharpCode.SharpZipLib
%_prefix/lib/mono/gac/Microsoft.CSharp
%_prefix/lib/mono/gac/Microsoft.VisualC
%_prefix/lib/mono/gac/Mono.C5
%_prefix/lib/mono/gac/Mono.CSharp
%_prefix/lib/mono/gac/Mono.Cairo
%_prefix/lib/mono/gac/Mono.Cecil
%_prefix/lib/mono/gac/Mono.Cecil.Mdb
%_prefix/lib/mono/gac/Mono.CompilerServices.SymbolWriter
%_prefix/lib/mono/gac/Mono.Management
%_prefix/lib/mono/gac/Mono.Parallel
%_prefix/lib/mono/gac/Mono.Posix
%_prefix/lib/mono/gac/Mono.Security
%_prefix/lib/mono/gac/Mono.Simd
%_prefix/lib/mono/gac/Mono.Tasklets
%_prefix/lib/mono/gac/System
%_prefix/lib/mono/gac/System.Configuration
%_prefix/lib/mono/gac/System.Core
%_prefix/lib/mono/gac/System.Drawing
%_prefix/lib/mono/gac/System.Dynamic
%_prefix/lib/mono/gac/System.IO.Compression
%_prefix/lib/mono/gac/System.IO.Compression.FileSystem
%_prefix/lib/mono/gac/System.Net
%_prefix/lib/mono/gac/System.Net.Http
%_prefix/lib/mono/gac/System.Net.Http.WebRequest
%_prefix/lib/mono/gac/System.Numerics
%_prefix/lib/mono/gac/System.Security
%_prefix/lib/mono/gac/System.Threading.Tasks.Dataflow
%_prefix/lib/mono/gac/System.Xml
%_prefix/lib/mono/gac/System.Xml.Linq
%_prefix/lib/mono/gac/System.Json
%_prefix/lib/mono/gac/System.Json.Microsoft
%_prefix/lib/mono/gac/System.Windows
%_prefix/lib/mono/gac/System.Xml.Serialization
%_prefix/lib/mono/gac/cscompmgd
%_prefix/lib/mono/mono-configuration-crypto

%package -n libmono-2_0-1
License:        LGPL v2.1 only
Summary:	A Library for embedding Mono in your Application
Group:          Development/Libraries/C and C++

%description -n libmono-2_0-1
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

A Library for embedding Mono in your Application.

%files -n libmono-2_0-1
%defattr(-, root, root)
%_libdir/libmono-2.0.so.1*

%post -n libmono-2_0-1 -p /sbin/ldconfig

%postun -n libmono-2_0-1 -p /sbin/ldconfig

%package -n libmono-2_0-devel
License:        LGPL v2.1 only
Summary:	Development files for libmono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n libmono-2_0-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Development files for libmono.

%files -n libmono-2_0-devel
%defattr(-, root, root)
%_bindir/mono-gdb.py
%_includedir/mono-2.0
%_libdir/libmono-2.0.a
%_libdir/libmono-2.0.so
%_libdir/pkgconfig/mono-2.pc

%if %sgen == yes
%package -n libmonosgen-2_0-1
License:        LGPL v2.1 only
Summary:	A Library for embedding Mono in your Application (sgen version)
Group:          Development/Libraries/C and C++

%description -n libmonosgen-2_0-1
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

A Library for embedding Mono in your Application (sgen version).

%files -n libmonosgen-2_0-1
%defattr(-, root, root)
%_libdir/libmonosgen-2.0.so.1*

%post -n libmonosgen-2_0-1 -p /sbin/ldconfig

%postun -n libmonosgen-2_0-1 -p /sbin/ldconfig

%package -n libmonosgen-2_0-devel
License:        LGPL v2.1 only
Summary:	Development files for libmonosgen
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       libmono-2_0-devel

%description -n libmonosgen-2_0-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Development files for libmonosgen.

%files -n libmonosgen-2_0-devel
%defattr(-, root, root)
%_bindir/mono-sgen-gdb.py
%_libdir/libmonosgen-2.0.a
%_libdir/libmonosgen-2.0.so
%_libdir/pkgconfig/monosgen-2.pc
%endif

%package -n libmonoboehm-2_0-1
License:        LGPL v2.1 only
Summary:	A Library for embedding Mono in your Application (boehm version)
Group:          Development/Libraries/C and C++

%description -n libmonoboehm-2_0-1
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

A Library for embedding Mono in your Application (boehm version).

%files -n libmonoboehm-2_0-1
%defattr(-, root, root)
%_libdir/libmonoboehm-2.0.so.1*

%post -n libmonoboehm-2_0-1 -p /sbin/ldconfig

%postun -n libmonoboehm-2_0-1 -p /sbin/ldconfig

%package -n libmonoboehm-2_0-devel
License:        LGPL v2.1 only
Summary:	Development files for libmonosgen
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       libmono-2_0-devel

%description -n libmonoboehm-2_0-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Development files for libmonoboehm.

%files -n libmonoboehm-2_0-devel
%defattr(-, root, root)
%_libdir/libmonoboehm-2.0.a
%_libdir/libmonoboehm-2.0.so

%if %llvm == yes
%package -n libmono-llvm0
License:        LGPL v2.1 only
Summary:	Loadable LLVM libary for mono
Group:          Development/Libraries/C and C++

%description -n libmono-llvm0
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Loadable LLVM libary for mono.

%files -n libmono-llvm0
%defattr(-, root, root)
%_libdir/libmono-llvm.so*

%post -n libmono-llvm0 -p /sbin/ldconfig

%postun -n libmono-llvm0 -p /sbin/ldconfig
%endif

%package -n mono-locale-extras
License:        LGPL v2.1 only
Summary:        Extra locale information
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Provides:       mono(I18N.CJK) = 1.0.5000.0
Provides:       mono(I18N.MidEast) = 1.0.5000.0
Provides:       mono(I18N.Other) = 1.0.5000.0
Provides:       mono(I18N.Rare) = 1.0.5000.0

%description -n mono-locale-extras
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Extra locale information.

%files -n mono-locale-extras
%defattr(-, root, root)
%_prefix/lib/mono/2.0/I18N.CJK.dll
%_prefix/lib/mono/2.0/I18N.MidEast.dll
%_prefix/lib/mono/2.0/I18N.Other.dll
%_prefix/lib/mono/2.0/I18N.Rare.dll
%_prefix/lib/mono/4.0/I18N.CJK.dll
%_prefix/lib/mono/4.0/I18N.MidEast.dll
%_prefix/lib/mono/4.0/I18N.Other.dll
%_prefix/lib/mono/4.0/I18N.Rare.dll
%_prefix/lib/mono/4.5/I18N.CJK.dll
%_prefix/lib/mono/4.5/I18N.MidEast.dll
%_prefix/lib/mono/4.5/I18N.Other.dll
%_prefix/lib/mono/4.5/I18N.Rare.dll
%_prefix/lib/mono/gac/I18N.CJK
%_prefix/lib/mono/gac/I18N.MidEast
%_prefix/lib/mono/gac/I18N.Other
%_prefix/lib/mono/gac/I18N.Rare

%package -n mono-data
License:        LGPL v2.1 only
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-directory
Obsoletes:      mono-ms-enterprise
Obsoletes:      mono-novell-directory
Provides:       mono-directory
Provides:       mono-ms-enterprise
Provides:       mono-novell-directory
Provides:       mono(Mono.Data.Tds) = 1.0.5000.0
Provides:       mono(Novell.Directory.Ldap) = 1.0.5000.0
Provides:       mono(System.Data) = 1.0.5000.0
Provides:       mono(System.DirectoryServices) = 1.0.5000.0
Provides:       mono(System.DirectoryServices.Protocols) = 1.0.5000.0
Provides:       mono(System.EnterpriseServices) = 1.0.5000.0

%description -n mono-data
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.

%files -n mono-data
%defattr(-, root, root)
%_bindir/sqlmetal
%_bindir/sqlsharp
%_mandir/man1/sqlsharp.1%ext_man
%_prefix/lib/mono/2.0/Mono.Data.Tds.dll
%_prefix/lib/mono/2.0/Novell.Directory.Ldap.dll
%_prefix/lib/mono/2.0/System.Data.DataSetExtensions.dll
%_prefix/lib/mono/2.0/System.Data.Linq.dll
%_prefix/lib/mono/2.0/System.Data.dll
%_prefix/lib/mono/2.0/System.DirectoryServices.dll
%_prefix/lib/mono/2.0/System.DirectoryServices.Protocols.dll
%_prefix/lib/mono/2.0/System.EnterpriseServices.dll
%_prefix/lib/mono/2.0/System.Runtime.Serialization.dll
%_prefix/lib/mono/2.0/System.Transactions.dll
%_prefix/lib/mono/4.0/Mono.Data.Tds.dll
%_prefix/lib/mono/4.0/Novell.Directory.Ldap.dll
%_prefix/lib/mono/4.0/System.Data.DataSetExtensions.dll
%_prefix/lib/mono/4.0/System.Data.Linq.dll
%_prefix/lib/mono/4.0/System.Data.dll
%_prefix/lib/mono/4.0/System.DirectoryServices.dll
%_prefix/lib/mono/4.0/System.DirectoryServices.Protocols.dll
%_prefix/lib/mono/4.0/System.EnterpriseServices.dll
%_prefix/lib/mono/4.0/System.Runtime.Serialization.dll
%_prefix/lib/mono/4.0/System.Transactions.dll
%_prefix/lib/mono/4.0/WebMatrix.Data.dll
%_prefix/lib/mono/4.5/Mono.Data.Tds.dll
%_prefix/lib/mono/4.5/Novell.Directory.Ldap.dll
%_prefix/lib/mono/4.5/System.Data.DataSetExtensions.dll
%_prefix/lib/mono/4.5/System.Data.Linq.dll
%_prefix/lib/mono/4.5/System.Data.dll
%_prefix/lib/mono/4.5/System.DirectoryServices.dll
%_prefix/lib/mono/4.5/System.DirectoryServices.Protocols.dll
%_prefix/lib/mono/4.5/System.EnterpriseServices.dll
%_prefix/lib/mono/4.5/System.Runtime.Serialization.dll
%_prefix/lib/mono/4.5/System.Transactions.dll
%_prefix/lib/mono/4.5/WebMatrix.Data.dll
%_prefix/lib/mono/4.5/EntityFramework.dll
%_prefix/lib/mono/4.5/EntityFramework.SqlServer.dll
%_prefix/lib/mono/4.5/sqlmetal.exe*
%_prefix/lib/mono/4.5/sqlsharp.exe*
%_prefix/lib/mono/gac/Mono.Data.Tds
%_prefix/lib/mono/gac/Novell.Directory.Ldap
%_prefix/lib/mono/gac/System.Data
%_prefix/lib/mono/gac/System.Data.DataSetExtensions
%_prefix/lib/mono/gac/System.Data.Linq
%_prefix/lib/mono/gac/System.DirectoryServices
%_prefix/lib/mono/gac/System.DirectoryServices.Protocols
%_prefix/lib/mono/gac/System.EnterpriseServices
%_prefix/lib/mono/gac/System.Runtime.Serialization
%_prefix/lib/mono/gac/System.Transactions
%_prefix/lib/mono/gac/WebMatrix.Data
%_prefix/lib/mono/gac/EntityFramework
%_prefix/lib/mono/gac/EntityFramework.SqlServer

%package -n mono-winforms
License:        LGPL v2.1 only
Summary:        Mono's Windows Forms implementation
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Provides:       mono-window-forms
Obsoletes:      mono-window-forms
Provides:       mono(Accessibility) = 1.0.5000.0
Provides:       mono(System.Design) = 1.0.5000.0
Provides:       mono(System.Drawing) = 1.0.5000.0
Provides:       mono(System.Drawing.Design) = 1.0.5000.0
Provides:       mono(System.Windows.Forms) = 1.0.5000.0

%description -n mono-winforms
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono's Windows Forms implementation.

%files -n mono-winforms
%defattr(-, root, root)
%_prefix/lib/mono/2.0/Accessibility.dll
%_prefix/lib/mono/2.0/Mono.WebBrowser.dll
%_prefix/lib/mono/2.0/System.Design.dll
%_prefix/lib/mono/2.0/System.Drawing.Design.dll
%_prefix/lib/mono/2.0/System.Windows.Forms.dll
%_prefix/lib/mono/4.0/Accessibility.dll
%_prefix/lib/mono/4.0/Mono.WebBrowser.dll
%_prefix/lib/mono/4.0/System.Design.dll
%_prefix/lib/mono/4.0/System.Drawing.Design.dll
%_prefix/lib/mono/4.0/System.Windows.Forms.DataVisualization.dll
%_prefix/lib/mono/4.0/System.Windows.Forms.dll
%_prefix/lib/mono/4.5/Accessibility.dll
%_prefix/lib/mono/4.5/Mono.WebBrowser.dll
%_prefix/lib/mono/4.5/System.Design.dll
%_prefix/lib/mono/4.5/System.Drawing.Design.dll
%_prefix/lib/mono/4.5/System.Windows.Forms.DataVisualization.dll
%_prefix/lib/mono/4.5/System.Windows.Forms.dll
%_prefix/lib/mono/gac/Accessibility
%_prefix/lib/mono/gac/Mono.WebBrowser
%_prefix/lib/mono/gac/System.Design
%_prefix/lib/mono/gac/System.Drawing.Design
%_prefix/lib/mono/gac/System.Windows.Forms
%_prefix/lib/mono/gac/System.Windows.Forms.DataVisualization

%package -n ibm-data-db2
License:        LGPL v2.1 only
Summary:        Database connectivity for DB2
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n ibm-data-db2
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for DB2.

%files -n ibm-data-db2
%defattr(-, root, root)
%_prefix/lib/mono/2.0/IBM.Data.DB2.dll
%_prefix/lib/mono/4.0/IBM.Data.DB2.dll
%_prefix/lib/mono/4.5/IBM.Data.DB2.dll
%_prefix/lib/mono/gac/IBM.Data.DB2

%package -n mono-extras
License:        LGPL v2.1 only
Summary:        Extra packages
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-ms-extras
Provides:       mono-ms-extras
Provides:       mono(Mono.Messaging) = 1.0.5000.0
Provides:       mono(Mono.Messaging.RabbitMQ) = 1.0.5000.0
Provides:       mono(RabbitMQ.Client) = 1.0.5000.0
Provides:       mono(System.Configuration.Install) = 1.0.5000.0
Provides:       mono(System.Management) = 1.0.5000.0
Provides:       mono(System.Messaging) = 1.0.5000.0
Provides:       mono(System.ServiceProcess) = 1.0.5000.0
Provides:       mono(mono-service) = 1.0.5000.0

%description -n mono-extras
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Extra packages.

%files -n mono-extras
%defattr(-, root, root)
%_bindir/mono-service
%_bindir/mono-service2
%_mandir/man1/mono-service.1%ext_man
%_prefix/lib/mono/2.0/Mono.Messaging.RabbitMQ.dll
%_prefix/lib/mono/2.0/Mono.Messaging.dll
%_prefix/lib/mono/2.0/RabbitMQ.Client.Apigen.exe*
%_prefix/lib/mono/2.0/RabbitMQ.Client.dll
%_prefix/lib/mono/2.0/System.Configuration.Install.dll
%_prefix/lib/mono/2.0/System.Management.dll
%_prefix/lib/mono/2.0/System.Messaging.dll
%_prefix/lib/mono/2.0/System.ServiceProcess.dll
%_prefix/lib/mono/2.0/mono-service.exe*
%_prefix/lib/mono/4.0/Mono.Messaging.RabbitMQ.dll
%_prefix/lib/mono/4.0/Mono.Messaging.dll
%_prefix/lib/mono/4.0/RabbitMQ.Client.Apigen.exe*
%_prefix/lib/mono/4.0/RabbitMQ.Client.dll
%_prefix/lib/mono/4.0/System.Configuration.Install.dll
%_prefix/lib/mono/4.0/System.Management.dll
%_prefix/lib/mono/4.0/System.Messaging.dll
%_prefix/lib/mono/4.0/System.Runtime.Caching.dll
%_prefix/lib/mono/4.0/System.ServiceProcess.dll
%_prefix/lib/mono/4.0/System.Xaml.dll
%_prefix/lib/mono/4.5/installutil.exe*
%_prefix/lib/mono/4.5/mono-service.exe*
%_prefix/lib/mono/4.5/Mono.Messaging.RabbitMQ.dll
%_prefix/lib/mono/4.5/Mono.Messaging.dll
%_prefix/lib/mono/4.5/RabbitMQ.Client.Apigen.exe*
%_prefix/lib/mono/4.5/RabbitMQ.Client.dll
%_prefix/lib/mono/4.5/System.Configuration.Install.dll
%_prefix/lib/mono/4.5/System.Management.dll
%_prefix/lib/mono/4.5/System.Messaging.dll
%_prefix/lib/mono/4.5/System.Runtime.Caching.dll
%_prefix/lib/mono/4.5/System.ServiceProcess.dll
%_prefix/lib/mono/4.5/System.Xaml.dll
%_prefix/lib/mono/gac/Mono.Messaging
%_prefix/lib/mono/gac/Mono.Messaging.RabbitMQ
%_prefix/lib/mono/gac/RabbitMQ.Client
%_prefix/lib/mono/gac/System.Configuration.Install
%_prefix/lib/mono/gac/System.Management
%_prefix/lib/mono/gac/System.Messaging
%_prefix/lib/mono/gac/System.Runtime.Caching
%_prefix/lib/mono/gac/System.ServiceProcess
%_prefix/lib/mono/gac/System.Xaml
%_prefix/lib/mono/gac/mono-service

%package -n mono-data-sqlite
License:        LGPL v2.1 only
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release
Provides:       mono(Mono.Data.Sqlite) = 1.0.5000.0

%description -n mono-data-sqlite
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.

%files -n mono-data-sqlite
%defattr(-, root, root)
%_prefix/lib/mono/2.0/Mono.Data.Sqlite.dll
%_prefix/lib/mono/4.0/Mono.Data.Sqlite.dll
%_prefix/lib/mono/4.5/Mono.Data.Sqlite.dll
%_prefix/lib/mono/gac/Mono.Data.Sqlite

%package -n mono-wcf
License:        MIT License (or similar) ; Ms-Pl
Summary:        Mono implementation of WCF, Windows Communication Foundation
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-wcf
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of WCF, Windows Communication Foundation

%files -n mono-wcf
%defattr(-, root, root)
%_bindir/svcutil
%_libdir/pkgconfig/wcf.pc
%_prefix/lib/mono/2.0/System.Data.Services.dll
%_prefix/lib/mono/2.0/System.IdentityModel.Selectors.dll
%_prefix/lib/mono/2.0/System.IdentityModel.dll
%_prefix/lib/mono/2.0/System.ServiceModel.Web.dll
%_prefix/lib/mono/2.0/System.ServiceModel.dll
%_prefix/lib/mono/4.0/System.Data.Services.dll
%_prefix/lib/mono/4.0/System.IdentityModel.Selectors.dll
%_prefix/lib/mono/4.0/System.IdentityModel.dll
%_prefix/lib/mono/4.0/System.Runtime.DurableInstancing.dll
%_prefix/lib/mono/4.0/System.ServiceModel.Activation.dll
%_prefix/lib/mono/4.0/System.ServiceModel.Discovery.dll
%_prefix/lib/mono/4.0/System.ServiceModel.Routing.dll
%_prefix/lib/mono/4.0/System.ServiceModel.Web.dll
%_prefix/lib/mono/4.0/System.ServiceModel.dll
%_prefix/lib/mono/4.5/System.Data.Services.dll
%_prefix/lib/mono/4.5/System.IdentityModel.Selectors.dll
%_prefix/lib/mono/4.5/System.IdentityModel.dll
%_prefix/lib/mono/4.5/System.Runtime.DurableInstancing.dll
%_prefix/lib/mono/4.5/System.ServiceModel.Activation.dll
%_prefix/lib/mono/4.5/System.ServiceModel.Discovery.dll
%_prefix/lib/mono/4.5/System.ServiceModel.Routing.dll
%_prefix/lib/mono/4.5/System.ServiceModel.Web.dll
%_prefix/lib/mono/4.5/System.ServiceModel.dll
%_prefix/lib/mono/4.5/svcutil.exe*
%_prefix/lib/mono/gac/System.Data.Services
%_prefix/lib/mono/gac/System.IdentityModel
%_prefix/lib/mono/gac/System.IdentityModel.Selectors
%_prefix/lib/mono/gac/System.Runtime.DurableInstancing
%_prefix/lib/mono/gac/System.ServiceModel
%_prefix/lib/mono/gac/System.ServiceModel.Activation
%_prefix/lib/mono/gac/System.ServiceModel.Discovery
%_prefix/lib/mono/gac/System.ServiceModel.Routing
%_prefix/lib/mono/gac/System.ServiceModel.Web

%package -n mono-winfxcore
License:        MIT License (or similar) ; Ms-Pl
Summary:        Mono implementation of core WinFX APIs
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-winfxcore
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of core WinFX APIs

%files -n mono-winfxcore
%defattr(-, root, root)
%_prefix/lib/mono/2.0/System.Data.Services.Client.dll*
%_prefix/lib/mono/2.0/WindowsBase.dll*
%_prefix/lib/mono/4.0/System.Data.Services.Client.dll*
%_prefix/lib/mono/4.0/WindowsBase.dll*
%_prefix/lib/mono/4.5/System.Data.Services.Client.dll*
%_prefix/lib/mono/4.5/WindowsBase.dll*
%_prefix/lib/mono/gac/System.Data.Services.Client
%_prefix/lib/mono/gac/WindowsBase

%package -n mono-web
License:        MIT License (or similar) ; Ms-Pl
Summary:        Mono implementation of ASP.NET, Remoting and Web Services
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Obsoletes:      mono-remoting
Obsoletes:      mono-web-forms
Obsoletes:      mono-web-services
Provides:       mono-remoting
Provides:       mono-web-forms
Provides:       mono-web-services
Provides:       mono(Mono.Http) = 1.0.5000.0
Provides:       mono(System.Runtime.Remoting) = 1.0.5000.0
Provides:       mono(System.Runtime.Serialization.Formatters.Soap) = 1.0.5000.0
Provides:       mono(System.Web) = 1.0.5000.0
Provides:       mono(System.Web.Services) = 1.0.5000.0

%description -n mono-web
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of ASP.NET, Remoting and Web Services.

%files -n mono-web
%defattr(-, root, root)
%config %_sysconfdir/mono/2.0/Browsers
%config %_sysconfdir/mono/2.0/DefaultWsdlHelpGenerator.aspx
%config %_sysconfdir/mono/2.0/web.config
%config %_sysconfdir/mono/4.0/Browsers
%config %_sysconfdir/mono/4.0/DefaultWsdlHelpGenerator.aspx
%config %_sysconfdir/mono/4.0/web.config
%config %_sysconfdir/mono/4.5/Browsers
%config %_sysconfdir/mono/4.5/DefaultWsdlHelpGenerator.aspx
%config %_sysconfdir/mono/4.5/web.config
%config %_sysconfdir/mono/browscap.ini
%config %_sysconfdir/mono/mconfig/config.xml
%dir %_sysconfdir/mono/mconfig
%_bindir/disco
%_bindir/mconfig
%_bindir/soapsuds
%_bindir/wsdl
%_bindir/wsdl2
%_bindir/xsd
%_libdir/pkgconfig/aspnetwebstack.pc
%_mandir/man1/disco.1%ext_man
%_mandir/man1/mconfig.1%ext_man
%_mandir/man1/soapsuds.1%ext_man
%_mandir/man1/wsdl.1%ext_man
%_mandir/man1/xsd.1%ext_man
%_prefix/lib/mono/2.0/Mono.Http.dll
%_prefix/lib/mono/2.0/System.ComponentModel.DataAnnotations.dll
%_prefix/lib/mono/2.0/System.Runtime.Remoting.dll
%_prefix/lib/mono/2.0/System.Runtime.Serialization.Formatters.Soap.dll
%_prefix/lib/mono/2.0/System.Web.Abstractions.dll
%_prefix/lib/mono/2.0/System.Web.Routing.dll
%_prefix/lib/mono/2.0/System.Web.Services.dll
%_prefix/lib/mono/2.0/System.Web.dll
%_prefix/lib/mono/2.0/wsdl.exe*
%_prefix/lib/mono/2.0/xsd.exe*
%_prefix/lib/mono/4.0/Microsoft.Web.Infrastructure.dll
%_prefix/lib/mono/4.0/Mono.Http.dll
%_prefix/lib/mono/4.0/System.ComponentModel.Composition.dll
%_prefix/lib/mono/4.0/System.ComponentModel.DataAnnotations.dll
%_prefix/lib/mono/4.0/System.Runtime.Remoting.dll
%_prefix/lib/mono/4.0/System.Runtime.Serialization.Formatters.Soap.dll
%_prefix/lib/mono/4.0/System.Web.Abstractions.dll
%_prefix/lib/mono/4.0/System.Web.ApplicationServices.dll
%_prefix/lib/mono/4.0/System.Web.Routing.dll
%_prefix/lib/mono/4.0/System.Web.Services.dll
%_prefix/lib/mono/4.0/System.Web.dll
%_prefix/lib/mono/4.5/Mono.Http.dll
%_prefix/lib/mono/4.5/System.ComponentModel.Composition.dll
%_prefix/lib/mono/4.5/System.ComponentModel.DataAnnotations.dll
%_prefix/lib/mono/4.5/System.Net.Http.Formatting.dll
%_prefix/lib/mono/4.5/System.Runtime.Remoting.dll
%_prefix/lib/mono/4.5/System.Runtime.Serialization.Formatters.Soap.dll
%_prefix/lib/mono/4.5/System.Web.Abstractions.dll
%_prefix/lib/mono/4.5/System.Web.ApplicationServices.dll
%_prefix/lib/mono/4.5/System.Web.Http.dll
%_prefix/lib/mono/4.5/System.Web.Http.SelfHost.dll
%_prefix/lib/mono/4.5/System.Web.Http.WebHost.dll
%_prefix/lib/mono/4.5/System.Web.Routing.dll
%_prefix/lib/mono/4.5/System.Web.Razor.dll
%_prefix/lib/mono/4.5/System.Web.Services.dll
%_prefix/lib/mono/4.5/System.Web.WebPages.Deployment.dll
%_prefix/lib/mono/4.5/System.Web.WebPages.Razor.dll
%_prefix/lib/mono/4.5/System.Web.WebPages.dll
%_prefix/lib/mono/4.5/System.Web.dll
%_prefix/lib/mono/4.5/disco.exe*
%_prefix/lib/mono/4.5/mconfig.exe*
%_prefix/lib/mono/4.5/soapsuds.exe*
%_prefix/lib/mono/4.5/wsdl.exe*
%_prefix/lib/mono/4.5/xsd.exe*
%_prefix/lib/mono/4.5/Microsoft.Web.Infrastructure.dll
%_prefix/lib/mono/gac/Microsoft.Web.Infrastructure
%_prefix/lib/mono/gac/Mono.Http
%_prefix/lib/mono/gac/System.ComponentModel.Composition
%_prefix/lib/mono/gac/System.ComponentModel.DataAnnotations
%_prefix/lib/mono/gac/System.Net.Http.Formatting
%_prefix/lib/mono/gac/System.Runtime.Remoting
%_prefix/lib/mono/gac/System.Runtime.Serialization.Formatters.Soap
%_prefix/lib/mono/gac/System.Web
%_prefix/lib/mono/gac/System.Web.Abstractions
%_prefix/lib/mono/gac/System.Web.ApplicationServices
%_prefix/lib/mono/gac/System.Web.Http
%_prefix/lib/mono/gac/System.Web.Http.SelfHost
%_prefix/lib/mono/gac/System.Web.Http.WebHost
%_prefix/lib/mono/gac/System.Web.Routing
%_prefix/lib/mono/gac/System.Web.Razor
%_prefix/lib/mono/gac/System.Web.Services
%_prefix/lib/mono/gac/System.Web.WebPages.Deployment
%_prefix/lib/mono/gac/System.Web.WebPages.Razor
%_prefix/lib/mono/gac/System.Web.WebPages

%package -n mono-mvc
License:        MIT License (or similar) ; Ms-Pl
Summary:        Mono implementation of ASP.NET MVC
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-mvc
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Mono implementation of ASP.NET MVC.

%files -n mono-mvc
%defattr(-, root, root)
%_libdir/pkgconfig/system.web.extensions.design_1.0.pc
%_libdir/pkgconfig/system.web.extensions_1.0.pc
%_libdir/pkgconfig/system.web.mvc.pc
%_libdir/pkgconfig/system.web.mvc2.pc
%_libdir/pkgconfig/system.web.mvc3.pc
%_prefix/lib/mono/2.0/System.Web.DynamicData.dll
%_prefix/lib/mono/2.0/System.Web.Extensions.Design.dll
%_prefix/lib/mono/2.0/System.Web.Extensions.dll
%_prefix/lib/mono/2.0/System.Web.Mvc.dll
%_prefix/lib/mono/4.0/System.Web.DynamicData.dll
%_prefix/lib/mono/4.0/System.Web.Extensions.Design.dll
%_prefix/lib/mono/4.0/System.Web.Extensions.dll
%_prefix/lib/mono/4.5/System.Web.DynamicData.dll
%_prefix/lib/mono/4.5/System.Web.Extensions.Design.dll
%_prefix/lib/mono/4.5/System.Web.Extensions.dll
%_prefix/lib/mono/4.5/System.Web.Mvc.dll
%_prefix/lib/mono/compat-2.0/System.Web.Extensions.Design.dll
%_prefix/lib/mono/compat-2.0/System.Web.Extensions.dll
%_prefix/lib/mono/compat-2.0/System.Web.Mvc.dll
%_prefix/lib/mono/gac/System.Web.DynamicData
%_prefix/lib/mono/gac/System.Web.Extensions
%_prefix/lib/mono/gac/System.Web.Extensions.Design
%_prefix/lib/mono/gac/System.Web.Mvc

%package -n mono-data-oracle
License:        LGPL v2.1 only
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release
Provides:       mono(System.Data.OracleClient) = 1.0.5000.0

%description -n mono-data-oracle
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.

%files -n mono-data-oracle
%defattr(-, root, root)
%_prefix/lib/mono/2.0/System.Data.OracleClient.dll
%_prefix/lib/mono/4.0/System.Data.OracleClient.dll
%_prefix/lib/mono/4.5/System.Data.OracleClient.dll
%_prefix/lib/mono/gac/System.Data.OracleClient

%package -n mono-data-postgresql
License:        LGPL v2.1 only
Summary:        Database connectivity for Mono
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-data == %version-%release
Provides:       mono(Npgsql) = 1.0.5000.0

%description -n mono-data-postgresql
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Database connectivity for Mono.

%files -n mono-data-postgresql
%defattr(-, root, root)
%_prefix/lib/mono/2.0/Npgsql.dll
%_prefix/lib/mono/4.0/Npgsql.dll
%_prefix/lib/mono/4.5/Npgsql.dll
%_prefix/lib/mono/gac/Npgsql

%package -n mono-rx-core
License:        MIT License (or similar) ; Apache License 2.0
Summary:        Reactive Extensions for Mono core libraries
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Provides:       mono(System.Reactive.Interfaces) = 1.0.5000.0

%description -n mono-rx-core
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Reactive Extensions for Mono, core packages, which don't depend on
desktop-specific features.

%files -n mono-rx-core
%defattr(-, root, root)
%_libdir/pkgconfig/reactive.pc
%_prefix/lib/mono/4.5/System.Reactive.Core.dll
%_prefix/lib/mono/4.5/System.Reactive.Debugger.dll
%_prefix/lib/mono/4.5/System.Reactive.Experimental.dll
%_prefix/lib/mono/4.5/System.Reactive.Interfaces.dll
%_prefix/lib/mono/4.5/System.Reactive.Linq.dll
%_prefix/lib/mono/4.5/System.Reactive.Observable.Aliases.dll
%_prefix/lib/mono/4.5/System.Reactive.PlatformServices.dll
%_prefix/lib/mono/4.5/System.Reactive.Providers.dll
%_prefix/lib/mono/4.5/System.Reactive.Runtime.Remoting.dll
%_prefix/lib/mono/gac/System.Reactive.Core
%_prefix/lib/mono/gac/System.Reactive.Debugger
%_prefix/lib/mono/gac/System.Reactive.Experimental
%_prefix/lib/mono/gac/System.Reactive.Interfaces
%_prefix/lib/mono/gac/System.Reactive.Linq
%_prefix/lib/mono/gac/System.Reactive.Observable.Aliases
%_prefix/lib/mono/gac/System.Reactive.PlatformServices
%_prefix/lib/mono/gac/System.Reactive.Providers
%_prefix/lib/mono/gac/System.Reactive.Runtime.Remoting

%package -n mono-rx-desktop
License:        MIT License (or similar) ; Apache License 2.0
Summary:        Reactive Extensions for Mono desktop-specific libraries
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       mono-rx-core == %version-%release
Provides:       mono(System.Reactive.Interfaces) = 1.0.5000.0

%description -n mono-rx-desktop
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Reactive Extensions for Mono, desktop-specific packages (winforms,
windows threading).

%files -n mono-rx-desktop
%defattr(-, root, root)
%_prefix/lib/mono/4.5/System.Reactive.Windows.Forms.dll
%_prefix/lib/mono/4.5/System.Reactive.Windows.Threading.dll
%_prefix/lib/mono/gac/System.Reactive.Windows.Forms
%_prefix/lib/mono/gac/System.Reactive.Windows.Threading

%package -n mono-nunit
License:        LGPL v2.1 only
Summary:        NUnit Testing Framework
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release

%description -n mono-nunit
NUnit is a unit-testing framework for all .Net languages.  Initially
ported from JUnit, the current release, version 2.2,  is the fourth
major release of this  Unit based unit testing tool for Microsoft .NET.
It is written entirely in C# and  has been completely redesigned to
take advantage of many .NET language		 features, for example
custom attributes and other reflection related capabilities. NUnit
brings xUnit to all .NET languages.

%files -n mono-nunit
%defattr(-, root, root)
%_libdir/pkgconfig/mono-nunit.pc
%_prefix/bin/nunit-console
%_prefix/bin/nunit-console2
%_prefix/bin/nunit-console4
%_prefix/lib/mono/2.0/nunit-console-runner.dll
%_prefix/lib/mono/2.0/nunit-console.exe*
%_prefix/lib/mono/2.0/nunit.core.dll
%_prefix/lib/mono/2.0/nunit.core.extensions.dll
%_prefix/lib/mono/2.0/nunit.core.interfaces.dll
%_prefix/lib/mono/2.0/nunit.framework.dll
%_prefix/lib/mono/2.0/nunit.framework.extensions.dll
%_prefix/lib/mono/2.0/nunit.mocks.dll
%_prefix/lib/mono/2.0/nunit.util.dll
%_prefix/lib/mono/4.5/nunit-console-runner.dll
%_prefix/lib/mono/4.5/nunit-console.exe*
%_prefix/lib/mono/4.5/nunit.core.dll
%_prefix/lib/mono/4.5/nunit.core.extensions.dll
%_prefix/lib/mono/4.5/nunit.core.interfaces.dll
%_prefix/lib/mono/4.5/nunit.framework.dll
%_prefix/lib/mono/4.5/nunit.framework.extensions.dll
%_prefix/lib/mono/4.5/nunit.mocks.dll
%_prefix/lib/mono/4.5/nunit.util.dll
%_prefix/lib/mono/gac/nunit-console-runner
%_prefix/lib/mono/gac/nunit.core
%_prefix/lib/mono/gac/nunit.core.extensions
%_prefix/lib/mono/gac/nunit.core.interfaces
%_prefix/lib/mono/gac/nunit.framework
%_prefix/lib/mono/gac/nunit.framework.extensions
%_prefix/lib/mono/gac/nunit.mocks
%_prefix/lib/mono/gac/nunit.util

%package -n mono-devel
License:        LGPL v2.1 only
Summary:        Mono development tools
Group:          Development/Languages/Mono
Requires:       mono-core == %version-%release
Requires:       libgdiplus0
Requires:       pkgconfig
Provides:       mono-xbuild
# Required because they are referenced by .pc files
Requires:       mono-data == %version-%release
Requires:       mono-data-oracle == %version-%release
Requires:       mono-extras == %version-%release
Requires:       mono-web == %version-%release
Requires:       mono-winforms == %version-%release
# We build natively on ppc64 now
%ifarch ppc64
Provides:       mono-biarchcompat
Obsoletes:      mono-biarchcompat
%endif
Provides:       mono(PEAPI) = 1.0.5000.0
Provides:       mono(resgen) = 1.0.5000.0

%description -n mono-devel
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. This package contains compilers and
other tools needed to develop .NET applications.

Mono development tools.

%post -n mono-devel -p /sbin/ldconfig

%postun -n mono-devel -p /sbin/ldconfig

%files -n mono-devel
%defattr(-, root, root)
%_bindir/caspol
%_bindir/ccrewrite
%_bindir/cccheck
%_bindir/cert2spc
%_bindir/dtd2rng
%_bindir/dtd2xsd
%_bindir/genxs
%_bindir/httpcfg
%_bindir/ilasm
%_bindir/installvst
%_bindir/lc
%_bindir/macpack
%_bindir/makecert
%_bindir/mkbundle
%_bindir/mono-api-info
%_bindir/mono-cil-strip
%_bindir/mono-find-provides
%_bindir/mono-find-requires
%_bindir/mono-heapviz
%_bindir/mono-shlib-cop
%_bindir/mono-xmltool
%_bindir/monodis
%_bindir/monograph
%_bindir/monolinker
%_bindir/monop
%_bindir/monop2
%_bindir/mprof-report
%_bindir/pdb2mdb
%_bindir/pedump
%_bindir/permview
%_bindir/prj2make
%_bindir/resgen
%_bindir/resgen2
%_bindir/secutil
%_bindir/sgen
%_bindir/signcode
%_bindir/xbuild
%_bindir/mdbrebase
%dir %_datadir/mono-2.0
%dir %_datadir/mono-2.0/mono
%dir %_datadir/mono-2.0/mono/cil
%_datadir/mono-2.0/mono/cil/cil-opcodes.xml
%_libdir/libmono-profiler-*.*
%_libdir/pkgconfig/cecil.pc
%_libdir/pkgconfig/dotnet.pc
%_libdir/pkgconfig/dotnet35.pc
%_libdir/pkgconfig/mono-cairo.pc
%_libdir/pkgconfig/mono-lineeditor.pc
%_libdir/pkgconfig/mono-options.pc
%_libdir/pkgconfig/mono.pc
%_libdir/pkgconfig/xbuild12.pc
%_mandir/man1/al.1%ext_man
%_mandir/man1/ccrewrite.1%ext_man
%_mandir/man1/cccheck.1%ext_man
%_mandir/man1/cert2spc.1%ext_man
%_mandir/man1/dtd2xsd.1%ext_man
%_mandir/man1/genxs.1%ext_man
%_mandir/man1/httpcfg.1%ext_man
%_mandir/man1/ilasm.1%ext_man
%_mandir/man1/lc.1%ext_man
%_mandir/man1/macpack.1%ext_man
%_mandir/man1/makecert.1%ext_man
%_mandir/man1/mkbundle.1%ext_man
%_mandir/man1/mono-api-info.1%ext_man
%_mandir/man1/mono-cil-strip.1%ext_man
%_mandir/man1/mono-shlib-cop.1%ext_man
%_mandir/man1/mono-xmltool.1%ext_man
%_mandir/man1/monodis.1%ext_man
%_mandir/man1/monolinker.1%ext_man
%_mandir/man1/monop.1%ext_man
%_mandir/man1/mprof-report.1%ext_man
%_mandir/man1/pdb2mdb.1%ext_man
%_mandir/man1/permview.1%ext_man
%_mandir/man1/prj2make.1%ext_man
%_mandir/man1/resgen.1%ext_man
%_mandir/man1/secutil.1%ext_man
%_mandir/man1/sgen.1%ext_man
%_mandir/man1/signcode.1%ext_man
%_mandir/man1/xbuild.1%ext_man
%_prefix/lib/mono-source-libs
%_prefix/lib/mono/2.0/MSBuild
%_prefix/lib/mono/2.0/Microsoft.Build.Engine.dll
%_prefix/lib/mono/2.0/Microsoft.Build.Framework.dll
%_prefix/lib/mono/2.0/Microsoft.Build.Tasks.dll
%_prefix/lib/mono/2.0/Microsoft.Build.Utilities.dll
%_prefix/lib/mono/2.0/Microsoft.Build.xsd
%_prefix/lib/mono/2.0/Microsoft.CSharp.targets
%_prefix/lib/mono/2.0/Microsoft.Common.targets
%_prefix/lib/mono/2.0/Microsoft.Common.tasks
%_prefix/lib/mono/2.0/Microsoft.VisualBasic.targets
%_prefix/lib/mono/2.0/Mono.Debugger.Soft.dll
%_prefix/lib/mono/2.0/Mono.XBuild.Tasks.dll
%_prefix/lib/mono/2.0/PEAPI.dll
%_prefix/lib/mono/2.0/genxs.exe*
%_prefix/lib/mono/2.0/ilasm.exe*
%_prefix/lib/mono/2.0/mkbundle.exe*
%_prefix/lib/mono/2.0/monolinker.*
%_prefix/lib/mono/2.0/monop.exe*
%_prefix/lib/mono/2.0/resgen.exe*
%_prefix/lib/mono/2.0/xbuild.exe*
%_prefix/lib/mono/2.0/xbuild.rsp
%_prefix/lib/mono/3.5/MSBuild
%_prefix/lib/mono/3.5/Microsoft.Build.Engine.dll
%_prefix/lib/mono/3.5/Microsoft.Build.Framework.dll
%_prefix/lib/mono/3.5/Microsoft.Build.Tasks.v3.5.dll
%_prefix/lib/mono/3.5/Microsoft.Build.Utilities.v3.5.dll
%_prefix/lib/mono/3.5/Microsoft.Build.xsd
%_prefix/lib/mono/3.5/Microsoft.CSharp.targets
%_prefix/lib/mono/3.5/Microsoft.Common.targets
%_prefix/lib/mono/3.5/Microsoft.Common.tasks
%_prefix/lib/mono/3.5/Microsoft.VisualBasic.targets
%_prefix/lib/mono/3.5/Mono.XBuild.Tasks.dll
%_prefix/lib/mono/3.5/xbuild.exe*
%_prefix/lib/mono/3.5/xbuild.rsp
%_prefix/lib/mono/4.0/Microsoft.Build.dll
%_prefix/lib/mono/4.0/Microsoft.Build.Engine.dll
%_prefix/lib/mono/4.0/Microsoft.Build.Framework.dll
%_prefix/lib/mono/4.0/Microsoft.Build.Tasks.v4.0.dll
%_prefix/lib/mono/4.0/Microsoft.Build.Utilities.v4.0.dll
%_prefix/lib/mono/4.0/Mono.Debugger.Soft.dll
%_prefix/lib/mono/4.0/Mono.XBuild.Tasks.dll
%_prefix/lib/mono/4.0/PEAPI.dll
%_prefix/lib/mono/4.5/MSBuild
%_prefix/lib/mono/4.5/Microsoft.Build.dll
%_prefix/lib/mono/4.5/Microsoft.Build.Engine.dll
%_prefix/lib/mono/4.5/Microsoft.Build.Framework.dll
%_prefix/lib/mono/4.5/Microsoft.Build.Tasks.v4.0.dll
%_prefix/lib/mono/4.5/Microsoft.Build.Utilities.v4.0.dll
%_prefix/lib/mono/4.5/Microsoft.Build.xsd
%_prefix/lib/mono/4.5/Microsoft.CSharp.targets
%_prefix/lib/mono/4.5/Microsoft.Common.targets
%_prefix/lib/mono/4.5/Microsoft.Common.tasks
%_prefix/lib/mono/4.5/Microsoft.VisualBasic.targets
%_prefix/lib/mono/4.5/Mono.Debugger.Soft.dll
%_prefix/lib/mono/4.5/Mono.CodeContracts.dll
%_prefix/lib/mono/4.5/Mono.XBuild.Tasks.dll
%_prefix/lib/mono/4.5/PEAPI.dll
%_prefix/lib/mono/4.5/caspol.exe*
%_prefix/lib/mono/4.5/cccheck.exe*
%_prefix/lib/mono/4.5/ccrewrite.exe*
%_prefix/lib/mono/4.5/cert2spc.exe*
%_prefix/lib/mono/4.5/dtd2rng.exe*
%_prefix/lib/mono/4.5/dtd2xsd.exe*
%_prefix/lib/mono/4.5/genxs.exe*
%_prefix/lib/mono/4.5/httpcfg.exe*
%_prefix/lib/mono/4.5/ictool.exe*
%_prefix/lib/mono/4.5/ilasm.exe*
%_prefix/lib/mono/4.5/installvst.exe*
%_prefix/lib/mono/4.5/lc.exe*
%_prefix/lib/mono/4.5/macpack.exe*
%_prefix/lib/mono/4.5/makecert.exe*
%_prefix/lib/mono/4.5/mkbundle.exe*
%_prefix/lib/mono/4.5/mono-api-info.exe*
%_prefix/lib/mono/4.5/mono-cil-strip.exe*
%_prefix/lib/mono/4.5/mono-shlib-cop.exe*
%_prefix/lib/mono/4.5/mono-xmltool.exe*
%_prefix/lib/mono/4.5/monolinker.*
%_prefix/lib/mono/4.5/monop.exe*
%_prefix/lib/mono/4.5/pdb2mdb.exe*
%_prefix/lib/mono/4.5/permview.exe*
%_prefix/lib/mono/4.5/resgen.exe*
%_prefix/lib/mono/4.5/secutil.exe*
%_prefix/lib/mono/4.5/sgen.exe*
%_prefix/lib/mono/4.5/signcode.exe*
%_prefix/lib/mono/4.5/xbuild.exe*
%_prefix/lib/mono/4.5/xbuild.rsp
%_prefix/lib/mono/4.5/mdbrebase.exe*
%_prefix/lib/mono/gac/Microsoft.Build
%_prefix/lib/mono/gac/Microsoft.Build.Engine
%_prefix/lib/mono/gac/Microsoft.Build.Framework
%_prefix/lib/mono/gac/Microsoft.Build.Tasks
%_prefix/lib/mono/gac/Microsoft.Build.Tasks.v3.5
%_prefix/lib/mono/gac/Microsoft.Build.Tasks.v4.0
%_prefix/lib/mono/gac/Microsoft.Build.Tasks.v12.0
%_prefix/lib/mono/gac/Microsoft.Build.Utilities
%_prefix/lib/mono/gac/Microsoft.Build.Utilities.v3.5
%_prefix/lib/mono/gac/Microsoft.Build.Utilities.v4.0
%_prefix/lib/mono/gac/Microsoft.Build.Utilities.v12.0
%_prefix/lib/mono/gac/Mono.CodeContracts
%_prefix/lib/mono/gac/Mono.Debugger.Soft
%_prefix/lib/mono/gac/Mono.XBuild.Tasks
%_prefix/lib/mono/gac/PEAPI
%_prefix/lib/mono/xbuild
%_prefix/lib/mono/xbuild-frameworks

%package -n monodoc-core
License:        LGPL v2.1 only
Summary:        Monodoc - Documentation tools for C# code
Group:          Development/Tools/Other
Requires:       mono-core == %version-%release
Obsoletes:      monodoc
Provides:       monodoc
# Added to uncompress and compare documentation used by build-compare
Requires:       unzip

%description -n monodoc-core
Monodoc-core contains documentation tools for C#.

%files -n monodoc-core
%defattr(-, root, root)
%_bindir/mdassembler
%_bindir/mdoc
%_bindir/mdoc-assemble
%_bindir/mdoc-export-html
%_bindir/mdoc-export-msxdoc
%_bindir/mdoc-update
%_bindir/mdoc-validate
%_bindir/mdvalidater
%_bindir/mod
%_bindir/monodocer
%_bindir/monodocs2html
%_bindir/monodocs2slashdoc
%_libdir/pkgconfig/monodoc.pc
%_mandir/man1/mdassembler.1%ext_man
%_mandir/man1/mdoc-assemble.1%ext_man
%_mandir/man1/mdoc-export-html.1%ext_man
%_mandir/man1/mdoc-export-msxdoc.1%ext_man
%_mandir/man1/mdoc-update.1%ext_man
%_mandir/man1/mdoc-validate.1%ext_man
%_mandir/man1/mdoc.1%ext_man
%_mandir/man1/mdvalidater.1%ext_man
%_mandir/man1/monodocer.1%ext_man
%_mandir/man1/monodocs2html.1%ext_man
%_mandir/man5/mdoc.5%ext_man
%_prefix/lib/mono/4.5/mdoc.exe*
%_prefix/lib/mono/4.5/mod.exe*
%_prefix/lib/mono/4.0/monodoc.dll*
%_prefix/lib/mono/gac/monodoc
%_prefix/lib/mono/monodoc
%_prefix/lib/monodoc

%package -n mono-complete
License:        LGPL v2.1 only
Summary:        Install everything built from the mono source tree
Group:          Development/Languages/Mono
Requires:       mono-core = %version-%release
Requires:       ibm-data-db2 = %version-%release
Requires:       libmono-2_0-1 = %version-%release
Requires:       libmono-2_0-devel = %version-%release
%if %llvm == yes
Requires:       libmono-llvm0 = %version-%release
%endif
%if %sgen == yes
Requires:       libmonosgen-2_0-1 = %version-%release
Requires:       libmonosgen-2_0-devel = %version-%release
%endif
Requires:       mono-data = %version-%release
Requires:       mono-data-oracle = %version-%release
Requires:       mono-data-postgresql = %version-%release
Requires:       mono-data-sqlite = %version-%release
Requires:       mono-devel = %version-%release
Requires:       mono-extras = %version-%release
Requires:       mono-locale-extras = %version-%release
Requires:       mono-nunit = %version-%release
Requires:       mono-wcf = %version-%release
Requires:       mono-web = %version-%release
Requires:       mono-winforms = %version-%release
Requires:       mono-winfxcore = %version-%release
Requires:       monodoc-core = %version-%release

%description -n mono-complete
The Mono Project is an open development initiative that is working to
develop an open source, Unix version of the .NET development platform.
Its objective is to enable Unix developers to build and deploy
cross-platform .NET applications. The project will implement various
technologies that have been submitted to the ECMA for standardization.

Install everything built from the mono source tree.  Note that this does
not install anything from outside the mono source (XSP, mono-basic, etc.).

%files -n mono-complete
%defattr(-, root, root)
%dir %_prefix/lib/mono/compat-2.0

%changelog
