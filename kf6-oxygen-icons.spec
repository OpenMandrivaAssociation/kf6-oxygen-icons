%define major 5
%define stable %([ "`echo %{version} |cut -d. -f3`" -ge 80 ] && echo -n un; echo -n stable)
%define git 20230927

Summary:	Oxygen icon theme
Name:		kf6-oxygen-icons
Version:	5.106.0
Release:	%{?git:0.%{git}.}1
License:	GPL
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
%if 0%{?git:1}
Source0:	https://invent.kde.org/frameworks/oxygen-icons5/-/archive/master/oxygen-icons5-master.tar.bz2#/oxygen-icons-%{git}.tar.bz2
%else
Source0:	http://download.kde.org/%{stable}/frameworks/%(echo %{version} |cut -d. -f1-2)/%{name}%{major}-%{version}.tar.xz
%endif
BuildRequires:	cmake
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(Qt6)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Test)

Provides:	kde6-icon-theme
BuildArch:	noarch

%description
Oxygen icon theme. Compliant with FreeDesktop.org naming schema.

%files
%{_iconsdir}/oxygen/
# This is needed as hicolor is the fallback for icons
%{_datadir}/icons/hicolor/*/apps/*

#-----------------------------------------------------------------------------

%prep
%autosetup -p1 -n oxygen-icons5-%{?git:master}%{!?git:%{version}}
%cmake \
	-DBUILD_QCH:BOOL=ON \
	-DBUILD_WITH_QT6:BOOL=ON \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build

# We copy some missing icons from oxygen to hicolor
for size in 16 32 48 64 128; do
    mkdir -p %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/office-address-book.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/krdc.png  %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/akonadi.png  %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/kaffeine.png  %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/semn.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/plasmagik.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/ktip.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/kthesaurus.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/ksniffer.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/korgac.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/knewsticker.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/klipper.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/kjournal.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
    cp %{buildroot}%{_kde5_iconsdir}/oxygen/base/${size}x${size}/apps/kivio.png %{buildroot}/%{_datadir}/icons/hicolor/${size}x${size}/apps
done

# automatic gtk icon cache update on rpm installs/removals
%transfiletriggerin -- %{_datadir}/icons/oxygen
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_datadir}/icons/oxygen &>/dev/null || :
fi

%transfiletriggerpostun -- %{_datadir}/icons/oxygen
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    gtk-update-icon-cache --force %{_datadir}/icons/oxygen &>/dev/null || :
fi
