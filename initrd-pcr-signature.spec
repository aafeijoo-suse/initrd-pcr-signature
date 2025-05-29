#
# spec file for package initrd-pcr-signature
#
# Copyright (c) 2025 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           initrd-pcr-signature
Version:        0
Release:        0
Summary:        Import PCR signatures from the initrd
License:        GPL-2.0-or-later
URL:            https://github.com/aafeijoo-suse/initrd-pcr-signature
Source:         %{name}-%{version}.tar.xz
BuildRequires:  pkgconfig
BuildRequires:  rpm-config-SUSE
Requires:       bash
Requires:       coreutils
Requires:       systemd
BuildArch:      noarch

%description
This will make possible the prediction of the initrd (and cmdline)
hashes, as will not require the update of the initrd to introduce the
JSON and PEM files required to unlock the LUKS2 device via
systemd-cryptsetup.

%package dracut
Summary:        dracut module to import PCR signatures
BuildRequires:  pkgconfig(dracut)
Requires:       %{name} = %{version}-%{release}
Requires(post): suse-module-tools-scriptlets
Provides:       dracut-pcr-signature

%description dracut
dracut module to import PCR signatures.

%package mkosi-initrd
Summary:        mkosi-initrd configuration to import PCR signatures
Requires:       %{name} = %{version}-%{release}
Requires:       mkosi-initrd
Requires(post): suse-module-tools-scriptlets

%description mkosi-initrd
mkosi-initrd configuration to import PCR signatures.

%prep
%setup -q

%build

%install
# common
install -D -m 0755 boot-efi-generator.sh %{buildroot}%{_systemdgeneratordir}/boot-efi-generator
install -D -m 0755 initrd-pcr-signature.sh %{buildroot}%{_libexecdir}/initrd-pcr-signature
install -D -m 0644 initrd-pcr-signature.service %{buildroot}%{_unitdir}/initrd-pcr-signature.service

# dracut
install -D -m 0755 module-setup.sh %{buildroot}%{_prefix}/lib/dracut/modules.d/50pcr-signature/module-setup.sh

# mkosi-initrd
install -D -m 0644 mkosi.conf %{buildroot}%{_prefix}/lib/mkosi-initrd/mkosi.conf.d/50-pcr-signature.conf
install -D -m 0644 mkosi.preset %{buildroot}%{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib/systemd/system-preset/50-pcr-signature.preset

%post dracut
%{?regenerate_initrd_post}

%post mkosi-initrd
%{?regenerate_initrd_post}

%posttrans dracut
%{?regenerate_initrd_posttrans}

%posttrans mkosi-initrd
%{?regenerate_initrd_posttrans}

%postun dracut
%{?regenerate_initrd_post}

%postun mkosi-initrd
%{?regenerate_initrd_post}

%files
%license LICENSE
%doc README.md
%dir %{_systemdgeneratordir}
%{_systemdgeneratordir}/boot-efi-generator
%{_libexecdir}/initrd-pcr-signature
%{_unitdir}/initrd-pcr-signature.service

%files dracut
%dir %{_prefix}/lib/dracut
%dir %{_prefix}/lib/dracut/modules.d
%{_prefix}/lib/dracut/modules.d/50pcr-signature

%files mkosi-initrd
%dir %{_prefix}/lib/mkosi-initrd
%dir %{_prefix}/lib/mkosi-initrd/mkosi.conf.d
%{_prefix}/lib/mkosi-initrd/mkosi.conf.d/50-pcr-signature.conf
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra/usr
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib/systemd
%dir %{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib/systemd/system-preset
%{_prefix}/lib/mkosi-initrd/mkosi.extra/usr/lib/systemd/system-preset/50-pcr-signature.preset

%changelog
