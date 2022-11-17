Name:       alsa-utils

%define alsa_version 1.2.8

%global alsacfgdir %{_prefix}/lib/alsa

Summary:    Advanced Linux Sound Architecture (ALSA) utilities
Version:    1.2.8
Release:    1
License:    GPLv2+
URL:        http://www.alsa-project.org/
Source0:    %{name}-%{version}.tar.gz
Source1:    alsaunmute
Source2:    alsaunmute.1
Source4:    alsa.rules
Source5:    alsactl.conf
Requires:   alsa-lib >= %{alsa_version}
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(alsa) >= %{alsa_version}
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  gettext-devel
Conflicts:  udev < 062

%description
This package contains command line utilities for the Advanced Linux Sound
Architecture (ALSA).


%prep
%autosetup -n %{name}-%{version}/%{name}

%build

%reconfigure --disable-static \
    CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" \
    --sbindir=%{_sbindir} \
    --disable-alsaconf \
    --disable-xmlto \
    --with-systemdsystemunitdir=%{_unitdir} \
    --with-udev-rules-dir=%{_udevrulesdir}

%make_build

%{__cp} %{SOURCE1} .

%install
%make_install

# Install ALSA udev rules
install -D -p -m 644 %{SOURCE4} %{buildroot}%{_udevrulesdir}/90-alsa.rules

# Install support utilities
install -D -p -m 755 alsaunmute %{buildroot}%{_bindir}/alsaunmute
gzip -9 -c %{SOURCE2} > %{buildroot}/alsaunmute.1.gz
install -D -p -m 644 %{buildroot}/alsaunmute.1.gz %{buildroot}%{_mandir}/man1
rm %{buildroot}/alsaunmute.1.gz

# Move /usr/share/alsa/init to /usr/lib/alsa/init
mkdir -p -m 755 %{buildroot}%{alsacfgdir}
mv %{buildroot}%{_datadir}/alsa/init %{buildroot}%{alsacfgdir}

# Link /usr/lib/alsa/init to /usr/share/alsa/init back
ln -s ../../lib/init %{buildroot}%{_datadir}/alsa/init

# Create a place for global configuration
install -D -p -m 644 %{SOURCE5} %{buildroot}%{_sysconfdir}/alsa/alsactl.conf
touch %{buildroot}%{_sysconfdir}/asound.state

%find_lang %{name}

%post
if [ -s %{_sysconfdir}/alsa/asound.state -a ! -s %{_sysconfdir}/asound.state ] ; then
mv %{_sysconfdir}/alsa/asound.state %{_sysconfdir}/asound.state
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING README.md
%{_udevrulesdir}/*
%config %{_sysconfdir}/alsa/*
%{alsacfgdir}/init/*
%{_bindir}/*
%{_sbindir}/*
%{_unitdir}/*
%{_datadir}/alsa/
%{_datadir}/sounds/
%{_libdir}/alsa-topology/libalsatplg_module_*
%doc %{_mandir}/man?/*
%dir %{_sysconfdir}/alsa/
%dir %{alsacfgdir}/
%dir %{alsacfgdir}/init/
%ghost %{_sysconfdir}/asound.state
