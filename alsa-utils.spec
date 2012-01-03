# 
# Do NOT Edit the Auto-generated Part!
# Generated by: spectacle version 0.23
# 
# >> macros
%define alsa_version 1.0.24.1
# << macros

Name:       alsa-utils
Summary:    Advanced Linux Sound Architecture (ALSA) utilities
Version:    1.0.24.2
Release:    1
Group:      Applications/Multimedia
License:    GPLv2+
URL:        http://www.alsa-project.org/
Source0:    ftp://ftp.alsa-project.org/pub/utils/alsa-utils-%{version}.tar.bz2
Source1:    alsaunmute
Source2:    alsaunmute.1
Source3:    alsa-info.sh
Source4:    alsa.rules
Source5:    alsactl.conf
Source100:  alsa-utils.yaml
Patch0:     null-pointer-to-avoid-double-free.patch
Requires:   alsa-lib >= %{alsa_version}
BuildRequires:  pkgconfig(alsa) >= %{alsa_version}
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  gettext-devel
Conflicts:   udev < 062


%description
This package contains command line utilities for the Advanced Linux Sound
Architecture (ALSA).




%prep
%setup -q -n %{name}-%{version}

# null-pointer-to-avoid-double-free.patch
%patch0 -p1
# >> setup
# << setup

%build
# >> build pre
# << build pre

%configure --disable-static \
    CFLAGS="$RPM_OPT_FLAGS -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64" \
    --sbindir=/sbin \
    --disable-alsaconf \
    --disable-xmlto

make %{?jobs:-j%jobs}

# >> build post
%{__cp} %{SOURCE1} .

# << build post
%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
#make install DESTDIR=$RPM_BUILD_ROOT

# Install ALSA udev rules
mkdir -p -m 755 $RPM_BUILD_ROOT/lib/udev/rules.d
install -p -m 644 %{SOURCE4} $RPM_BUILD_ROOT/lib/udev/rules.d/90-alsa.rules

# Install support utilities
mkdir -p -m755 $RPM_BUILD_ROOT/bin
install -p -m 755 alsaunmute %{buildroot}/bin/
mkdir -p -m755 $RPM_BUILD_ROOT/%{_mandir}/man1
gzip -9 -c %{SOURCE2} > $RPM_BUILD_ROOT/alsaunmute.1.gz
install -p -m 644 $RPM_BUILD_ROOT/alsaunmute.1.gz %{buildroot}/%{_mandir}/man1
rm $RPM_BUILD_ROOT/alsaunmute.1.gz

# Link alsactl to /usr/sbin
mkdir -p $RPM_BUILD_ROOT/%{_sbindir}
ln -s ../../sbin/alsactl $RPM_BUILD_ROOT/%{_sbindir}/alsactl

# Move /usr/share/alsa/init to /lib/alsa/init
mkdir -p -m 755 %{buildroot}/lib/alsa
mv %{buildroot}%{_datadir}/alsa/init %{buildroot}/lib/alsa

# Link /lib/alsa/init to /usr/share/alsa/init back
ln -s ../../../lib/alsa/init %{buildroot}%{_datadir}/alsa/init


# Create a place for global configuration
mkdir -p -m 755 %{buildroot}/etc/alsa
install -p -m 644 %{SOURCE5} %{buildroot}/etc/alsa
touch %{buildroot}/etc/asound.state

# Install alsa-info.sh script
install -p -m 755 %{SOURCE3} %{buildroot}/usr/bin/alsa-info
ln -s alsa-info %{buildroot}/usr/bin/alsa-info.sh

# << install post
%find_lang %{name}



%post
# >> post
if [ -s /etc/alsa/asound.state -a ! -s /etc/asound.state ] ; then
mv /etc/alsa/asound.state /etc/asound.state
fi
# << post



%files -f %{name}.lang
%defattr(-,root,root,-)
# >> files
%doc COPYING README
%config /lib/udev/rules.d/*
%config /etc/alsa/*
/bin/*
/sbin/*
/lib/alsa/init/*
%{_bindir}/*
%{_sbindir}/*
%{_datadir}/alsa/
%{_datadir}/sounds/
%doc %{_mandir}/man?/*
%dir /etc/alsa/
%dir /lib/alsa/
%dir /lib/alsa/init/
%ghost /etc/asound.state
# << files


